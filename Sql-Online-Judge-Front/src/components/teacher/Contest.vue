<template>
  <div>
    <!-- 页面导航 -->
    <navbar></navbar>

    <!-- 比赛列表部分 -->
    <div class="contest-list">
      <h1>Available Contests</h1>
      <ul>
        <li v-for="contest in contests" :key="contest.id">
          <h2>{{ contest.name }} ({{ contest.category }}) - [ID: {{ contest.id }}]</h2>
          <button @click="enterContest(contest)" :disabled="!contest.hasAccess">
            Enter
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/student/Navbar.vue';

export default {
  components: {
    Navbar
  },
  data() {
    return {
      contests: []
    };
  },
  created() {
    this.fetchContests();
  },
  methods: {
    fetchContests() {
      // 假设有一个 API 来获取比赛列表和访问权限
      // 这里的数据应该从后端获取，以下是示例数据
      this.contests = [
        { id: 1, name: 'Mathematics Olympiad', category: 'Mathematics', hasAccess: true },
        { id: 2, name: 'Physics Contest', category: 'Physics', hasAccess: false },
        { id: 3, name: 'Chemistry Challenge', category: 'Chemical', hasAccess: true }
      ];
    },
    enterContest(contest) {
      if (contest.hasAccess) {
        // 例如，可以用路由导航到比赛详情页
        this.$router.push(`/contests/${contest.id}`);
      } else {
        alert("You do not have access to enter this contest.");
      }
    }
  }
}
</script>

<style scoped>
ul {
  list-style: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
}

button {
  margin-top: 5px;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
