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
            <button @click="deleteContest(contest.id)">删除</button>
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
      axios.get('/api/contests', {
        headers: {
          'session': localStorage.getItem('session')
        }
        , data: { 
            user_id: localStorage.getItem('userId')
          }
        })
        .then(response => {
          this.contests = response.data.data;
        })
        .catch(error => {
          console.error("There was an error fetching the contests!", error);
        });
    },
    deleteContest(contestId) {
      axios.delete(`/api/contest?contest_id=${contestId}`)
        .then(response => {
          this.fetchContests();
        })
        .catch(error => {
          console.error("There was an error deleting the contest!", error);
        });
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
</style>
