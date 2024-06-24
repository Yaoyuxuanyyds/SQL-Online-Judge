<template>
  <nav class="navbar">
    <!-- 添加 logo -->
    <div class="logo">
      <img src="@/assets/logo.png" alt="Logo">
    </div>

    <router-link :to="{ path: '/index' }" :class="{ active: isActive('/index') }">主页</router-link>
    <router-link :to="{ path: '/import' }" :class="{ active: isActive('/import') }">创建题目</router-link>
    <router-link :to="{ path: '/create' }" :class="{ active: isActive('/create') }">创建比赛</router-link>
    <router-link :to="{ path: '/question' }" :class="{ active: isActive('/question') }">题目列表</router-link>
    <router-link :to="{ path: '/contest' }" :class="{ active: isActive('/contest') }">比赛列表</router-link>
    <router-link :to="{ path: '/submit' }" :class="{ active: isActive('/submit') }">提交记录</router-link>
    <router-link :to="{ path: '/community' }" :class="{ active: isActive('/community') }">社群动态</router-link>
    <!-- 添加 logout 按钮 -->
    <button class="logout-button" @click="logout">Logout</button>
  </nav>
</template>


<script>
import axios from 'axios';

export default {
  name: 'Navbar',
  data() {
    return {
      nickname: ''  // 初始化用户昵称
    };
  },
  mounted() {
    // 在组件挂载时获取用户昵称
    // userName 有问题
    this.nickname = localStorage.getItem('userName') || 'Guest';
  },
  methods: {
    isActive(path) {
      return this.$route.path === path;
    },
    logout() {
      const sessionToken = localStorage.getItem('session');
      axios.delete('/api/login', {
        headers: {
          'session': sessionToken,
          'Content-Type': 'application/json'
        },
        data: {
        }
      })
      .then(response => {
        alert(response.data.message); // 显示成功消息
        localStorage.removeItem('session'); // 清除本地存储中的 session
        this.$router.push('/'); // 回到主页
      })
      .catch(error => {
        alert('退出登录失败: ' + error.response.data.message);
      });
    }
  }
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-around;
  align-items: center; /* 确保项目在垂直方向上居中对齐 */
  background-color: #f5f5f5;
  padding: 10px;
}

.logo img {
  height: 40px;
}

.navbar a {
  text-decoration: none;
  color: #333;
  padding: 10px;
  border-radius: 5px;
}

.navbar a.active {
  background-color: #333;
  color: #fff;
}

.logout-button {
  background-color: #ff4d4f;
  color: #fff;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
}

.logout-button:hover {
  background-color: #ff7875;
}
</style>
