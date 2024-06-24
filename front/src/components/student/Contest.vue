<template>
  <div>
    <Navbar />
    <h1>考试列表</h1>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>教师ID</th>
          <th>开始时间</th>
          <th>结束时间</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="contest in contests" :key="contest.id">
          <td>{{ contest.id }}</td>
          <td>{{ contest.teacher_id }}</td>
          <td>{{ contest.start_time }}</td>
          <td>{{ contest.end_time }}</td>
          <td>
            <button @click="goToContestQuestions(contest.id)">开始考试</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '@/components/student/Navbar.vue';

export default {
  name: 'Contest',
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
      const userId = localStorage.getItem('userID');
      const userRole = localStorage.getItem('userRole');
      // 发送请求获取考试列表
      axios.get('/api/contestlist', {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          user_id: userId,
          user_role: userRole
        }
        })
        .then(response => {
          this.contests = response.data;
        })
        .catch(error => {
          alert("There was an error fetching the contests!", error);
        });
    },    
    goToContestQuestions(contestId) {
      // 导航到考试题目页面
      this.$router.push({ name: 'contest-question', params: { id: contestId } });
    }
  }
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

button {
  padding: 5px 10px;
  border: none;
  border-radius: 3px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}
button:hover {
  background-color: #0056b3;
}
</style>
