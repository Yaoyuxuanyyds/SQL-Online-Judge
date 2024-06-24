<template>
  <nav class="el-navbar">
    <!-- Logo 和 Hello, 用户昵称 -->
    <div class="logo">
      <img src="..\..\assets\logo.png" alt="Logo">
      <span class="hello-user">Hello, {{ nickname }}</span>
    </div>

    <router-link :to="{ path: '/student' }" :class="{ active: isActive('/student') }">Home</router-link>
    <router-link :to="{ path: '/student/question' }" :class="{ active: isActive('/student/question') }">Questions</router-link>
    <router-link :to="{ path: '/student/contest' }" :class="{ active: isActive('/student/contest') }">Contest</router-link>
    <router-link :to="{ path: '/student/submit' }" :class="{ active: isActive('/student/submit') }">Submit</router-link>
    <router-link :to="{ path: '/student/community' }" :class="{ active: isActive('/student/community') }">Community</router-link>
    
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
    this.nickname = localStorage.getItem('nickname') || 'Guest';
  },
  methods: {
    isActive(path) {
      return this.$route.path === path;
    },
    logout() {
      const sessionToken = localStorage.getItem('sessionToken');
      axios.delete('/api/login', {session: sessionToken})
      .then(() => {
        alert('成功退出登录');
        localStorage.removeItem('sessionToken'); // 清除本地存储中的 sessionToken
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
.el-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f5f5f5;
  padding: 10px;
}

.logo {
  display: flex;
  align-items: center;
}

.logo img {
  height: 40px;
  margin-right: 10px;
}

.hello-user {
  font-size: 16px;
  font-weight: bold;
}

.el-navbar a {
  text-decoration: none;
  color: #333;
  padding: 10px;
  border-radius: 5px;
}

.el-navbar a.active {
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
