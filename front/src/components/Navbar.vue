<template>
  <nav class="navbar">
    <!-- 添加 logo -->
    <div class="logo">
      <img src="@/assets/logo.png" alt="Logo">
    </div>

    <!-- 根据用户角色动态显示链接 -->
    <div class="links-container">
      <router-link
        v-if="canAccessHomePage"
        :to="{ path: '/index' }"
        :class="['nav-link', isActive('/index'), { 'activated': isCurrentPath('/index') }]"
        @click="handleClick('/index')"
      >主页</router-link>
      <router-link
        v-if="canAccessCreateQuestion"
        :to="{ path: '/import' }"
        :class="['nav-link', isActive('/import'), { 'activated': isCurrentPath('/import') }]"
        @click="handleClick('/import')"
      >创建题目</router-link>
      <router-link
        v-if="canAccessCreateContest"
        :to="{ path: '/create' }"
        :class="['nav-link', isActive('/create'), { 'activated': isCurrentPath('/create') }]"
        @click="handleClick('/create')"
      >创建比赛</router-link>
      <router-link
        v-if="canAccessQuestionList"
        :to="{ path: '/question' }"
        :class="['nav-link', isActive('/question'), { 'activated': isCurrentPath('/question') }]"
        @click="handleClick('/question')"
      >题目列表</router-link>
      <router-link
        v-if="canAccessContestList"
        :to="{ path: '/contest' }"
        :class="['nav-link', isActive('/contest'), { 'activated': isCurrentPath('/contest') }]"
        @click="handleClick('/contest')"
      >比赛列表</router-link>
      <router-link
        v-if="canAccessSubmitRecords"
        :to="{ path: '/submit' }"
        :class="['nav-link', isActive('/submit'), { 'activated': isCurrentPath('/submit') }]"
        @click="handleClick('/submit')"
      >提交记录</router-link>
      <router-link
        v-if="canAccessCommunity"
        :to="{ path: '/community' }"
        :class="['nav-link', isActive('/community'), { 'activated': isCurrentPath('/community') }]"
        @click="handleClick('/community')"
      >社群动态</router-link>
      <router-link
        v-if="canAccessUserManagement"
        :to="{ path: '/admin' }"
        :class="['nav-link', isActive('/admin'), { 'activated': isCurrentPath('/admin') }]"
        @click="handleClick('/admin')"
      >用户管理</router-link>
    </div>

    <button class="logout-button" @click="logout">退出登录</button>
  </nav>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Navbar',
  data() {
    return {
      nickname: '', // 初始化用户昵称
      userRole: parseInt(localStorage.getItem('userRole')) || 0, // 从本地存储中获取用户角色，默认为 0 (student)
      currentPath: ''
    };
  },
  computed: {
    canAccessHomePage() {
      return this.userRole === 0 || this.userRole === 1 || this.userRole === 2;
    },
    canAccessCreateQuestion() {
      return this.userRole === 1 || this.userRole === 2;
    },
    canAccessCreateContest() {
      return this.userRole === 1 || this.userRole === 2;
    },
    canAccessQuestionList() {
      return this.userRole === 0 || this.userRole === 1 || this.userRole === 2;
    },
    canAccessContestList() {
      return this.userRole === 0 || this.userRole === 1 || this.userRole === 2;
    },
    canAccessSubmitRecords() {
      return this.userRole === 0 || this.userRole === 1 || this.userRole === 2;
    },
    canAccessCommunity() {
      return this.userRole === 0 || this.userRole === 1 || this.userRole === 2;
    },
    canAccessUserManagement() {
      return this.userRole === 2;
    }
  },
  methods: {
    isActive(path) {
      return this.$route.path === path ? 'active' : '';
    },
    isCurrentPath(path) {
      return this.currentPath === path;
    },
    handleClick(path) {
      this.currentPath = path;
    },
    logout() {
      const sessionToken = localStorage.getItem('session');
      axios.delete('/api/login', {
        headers: {
          'session': sessionToken,
          'Content-Type': 'application/json'
        },
        data: {}
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
  },
  mounted() {
    // 在组件挂载时获取用户昵称
    this.nickname = localStorage.getItem('userName') || 'Guest';
    this.currentPath = this.$route.path;
  }
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  padding: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo img {
  height: 40px;
  margin: 10px 20px;
}

.links-container {
  display: flex;
  flex: 1;
}

.nav-link {
  flex: 1;
  text-align: center;
  text-decoration: none;
  color: #000;
  padding: 15px 0;
  transition: all 0.3s ease;
  font-size: 16px;
  background-color: #fff;
  border: none;
  border-bottom: 2px solid transparent;
}

.nav-link:hover {
  background-color: #f0f0f0;
}

.nav-link.active {
  background-color: #000;
  color: #fff;
  border-bottom: 2px solid #000;
}

.nav-link.activated {
  transform: scale(1.05);
  background-color: #666;
  color: #fff;
  font-size: 18px;
  box-shadow: 0 4px 8px rgba(102, 102, 102, 0.5);
}

.logout-button {
  background-color: #ff4d4d;
  color: #fff;
  border: none;
  padding: 10px 20px;
  margin: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: transform 0.2s, background-color 0.2s;
}

.logout-button:hover {
  transform: translateY(-2px);
  background-color: #ff1a1a;
}

</style>