<template>
  <div>
    <Navbar />
    <div class="container">
      <h1 class="title">考试列表</h1>
      <div class="filter-container">
        <el-select v-model="filterStatus" placeholder="筛选考试状态" @change="filterContests">
          <el-option label="全部" value="all"></el-option>
          <el-option label="未开始" value="not_started"></el-option>
          <el-option label="进行中" value="ongoing"></el-option>
          <el-option label="已结束" value="ended"></el-option>
        </el-select>
      </div>
      <table class="el-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>教师ID</th>
            <th>开始时间</th>
            <th>结束时间</th>
            <th>状态</th>
            <th>操作</th>
            <th v-if="userRole !== 0">查看答题</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="contest in filteredContests" :key="contest.id">
            <td>{{ contest.id }}</td>
            <td>{{ contest.teacher_id }}</td>
            <td>{{ formatTime(contest.start_time) }}</td>
            <td>{{ formatTime(contest.end_time) }}</td>
            <td>
              <span :class="getStatusClass(contest.status)">{{ getStatusText(contest.status) }}</span>
            </td>
            <td>
              <button @click="goToContestQuestions(contest.id)">开始考试</button>
            </td>
            <td v-if="userRole !== 0">
              <button @click="viewScores(contest.id)">查看答题</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '@/components/Navbar.vue';

export default {
  name: 'Contest',
  components: {
    Navbar
  },
  data() {
    return {
      contests: [],
      filteredContests: [],
      filterStatus: '',
      userRole: parseInt(localStorage.getItem('userRole')),
    };
  },
  created() {
    this.fetchContests();
  },
  methods: {
    fetchContests() {
      const userId = localStorage.getItem('userID');
      const userRole = localStorage.getItem('userRole');
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
        this.contests = response.data.map(contest => {
          return {
            ...contest,
            status: this.getContestStatus(contest.start_time, contest.end_time)
          };
        });
        this.filteredContests = this.contests;
      })
      .catch(error => {
        alert("获取考试列表时发生错误！", error);
      });
    },
    getContestStatus(startTime, endTime) {
      const now = new Date();
      const start = new Date(startTime);
      const end = new Date(endTime);

      if (now < start) {
        return 'not_started';
      } else if (now > end) {
        return 'ended';
      } else {
        return 'ongoing';
      }
    },
    formatTime(time) {
      const date = new Date(time);
      const year = date.getFullYear();
      const month = ('0' + (date.getMonth() + 1)).slice(-2);
      const day = ('0' + date.getDate()).slice(-2);
      const hours = ('0' + date.getHours()).slice(-2);
      const minutes = ('0' + date.getMinutes()).slice(-2);

      return `${year}-${month}-${day} ${hours}:${minutes}`;
    },
    filterContests() {
      if (this.filterStatus && this.filterStatus !== 'all') {
        this.filteredContests = this.contests.filter(contest => contest.status === this.filterStatus);
      } else {
        this.filteredContests = this.contests;
      }
    },
    goToContestQuestions(contestId) {
      this.$router.push({ name: 'contest-question', params: { id: contestId } });
    },
    viewScores(contestId) {
      this.$router.push({ name: 'contest-statistics', params: { id: contestId } });
    },
    getStatusText(status) {
      switch (status) {
        case 'not_started':
          return '未开始';
        case 'ongoing':
          return '进行中';
        case 'ended':
          return '已结束';
        default:
          return '';
      }
    },
    getStatusClass(status) {
      return {
        'status-not-started': status === 'not_started',
        'status-ongoing': status === 'ongoing',
        'status-ended': status === 'ended'
      };
    }
  }
};
</script>

<style scoped>
.container {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  font-size: 24px;
  color: #333;
  margin: 0;
  padding: 20px 0;
}

.filter-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.el-select {
  width: 200px;
}

.el-table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

th, td {
  padding: 12px 15px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
  color: #333;
  font-weight: bold;
  text-align: center;
}

td {
  text-align: center;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
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

.status-not-started {
  background-color: #f0ad4e;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.status-ongoing {
  background-color: #5cb85c;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.status-ended {
  background-color: #d9534f;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}
</style>
