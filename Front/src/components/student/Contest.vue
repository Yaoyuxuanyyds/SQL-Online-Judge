<template>
  <div class="contest-container">
    <Navbar />

    <div class="container">
      <h1>Available Contests</h1>
      <div class="contest-list">
        <table class="contest-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Category</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="contest in contests" :key="contest.id">
              <td>
                <!-- 使用路由链接跳转到题目列表页面 -->
                <router-link :to="{ name: 'question_contest', params: { id: contest.id }}">{{ contest.name }}</router-link>
              </td>
              <td>{{ contest.category }}</td>
              <td>{{ contest.completed ? '已完成' : '未完成' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 右侧栏位显示竞赛的剩余时间和得分情况 -->
      <div class="contest-info">
        <h2>Contest Information</h2>
        <p v-if="selectedContest">Remaining Time: {{ selectedContest.remainingTime }}</p>
        <p v-if="selectedContest">Score: {{ selectedContest.score }}</p>
      </div>
    </div>

    <!-- 当没有选择比赛时显示的内容 -->
    <div v-if="!selectedContest">
      <p>No contest selected.</p>
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
      contests: [],
      selectedContest: null
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
        { 
          id: 1, 
          name: 'Mathematics Olympiad', 
          category: 'Mathematics', 
          hasAccess: true, 
          completed: false,
          remainingTime: '2 hours',
          score: '80%',
          problems: [
            { id: 101, title: 'Equation Solving', keywords: ['algebra'], difficulty: 'Medium' },
            { id: 102, title: 'Geometry Problem', keywords: ['geometry'], difficulty: 'Hard' }
          ]
        },
        { 
          id: 2, 
          name: 'Physics Contest', 
          category: 'Physics', 
          hasAccess: false, 
          completed: true,
          remainingTime: '1 hour',
          score: '90%',
          problems: []
        },
        { 
          id: 3, 
          name: 'Chemistry Challenge', 
          category: 'Chemical', 
          hasAccess: true, 
          completed: false,
          remainingTime: '3 hours',
          score: '75%',
          problems: []
        }
      ];
    }
  }
};
</script>

<style scoped>
.contest-container {
  display: flex;
  flex-direction: column;
}

.container {
  padding: 20px;
  flex: 1; /* 让内容区域占满剩余空间 */
}

.contest-list {
  margin-top: 20px;
}

.contest-table {
  width: 100%;
  border-collapse: collapse;
}

.contest-table th, .contest-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: center;
}

.contest-info {
  margin-top: 20px;
  padding: 10px;
  border: 1px solid #ccc;
}

.contest-info h2 {
  margin-bottom: 10px;
}

div {
  /* 确保占位组件的高度不会过小 */
  min-height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
