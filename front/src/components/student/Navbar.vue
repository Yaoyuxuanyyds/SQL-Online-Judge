<template>
  <nav class="navbar">
    <router-link :to="{ path: '/student' }" :class="{ active: isActive('/student') }">Home</router-link>
    <router-link :to="{ path: '/student/question' }" :class="{ active: isActive('/student/question') }">Questions</router-link>
    <router-link :to="{ path: '/student/contest' }" :class="{ active: isActive('/student/contest') }">Contest</router-link>
    <router-link :to="{ path: '/student/submit' }" :class="{ active: isActive('/student/submit') }">Submit</router-link>
    <router-link :to="{ path: '/student/community' }" :class="{ active: isActive('/student/community') }">Community</router-link>

    <!-- 比赛信息显示区域 -->
    <div v-if="contestInfo" class="contest-info">
      <p>Remaining Time: {{ contestInfo.remainingTime }}</p>
      <p>Score: {{ contestInfo.score }}</p>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  props: {
    contestInfo: {
      type: Object,
      default: null
    }
  },
  methods: {
    isActive(path) {
      return this.$route.path === path;
    }
  }
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-around;
  background-color: #f5f5f5;
  padding: 10px;
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

.contest-info {
  margin-left: auto; /* 将比赛信息区域靠右对齐 */
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.contest-info p {
  margin: 0;
  font-size: 14px;
}
</style>
