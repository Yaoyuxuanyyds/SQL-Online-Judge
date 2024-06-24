<template>
  <div>
    <Navbar />
    <div class="container">
      <el-menu class="side-menu" @select="handleSelect">
        <el-menu-item index="1">所有记录</el-menu-item>
        <el-menu-item index="2">我的记录</el-menu-item>
      </el-menu>
      <div class="content">
        <h1>提交记录</h1>
        <!-- 表格展示提交记录 -->
        <table>
          <thead>
            <tr>
              <th>提交ID</th>
              <th>题目ID</th>
              <th v-if="!hideStudentID">学生ID</th>
              <th>结果</th>
              <th>提交时间</th>
              <th v-if="showExtraColumn">提交记录</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in submissions" :key="record.submissionId">
              <td>{{ record.id }}</td>
              <td>{{ record.question_id }}</td>
              <td v-if="!hideStudentID">{{ record.student_id }}</td>
              <td>{{ judgeResult(record.pass_rate) }}</td>
              <td>{{ record.submit_time | formatDate }}</td>
              <td v-if="showExtraColumn">{{ record.submit_sql }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/student/Navbar.vue';
import axios from 'axios';

export default {
  name: 'Submissions',
  components: {
    Navbar
  },
  data() {
    return {
      submissions: [],
      showExtraColumn: false,
      hideStudentID: false, // 控制隐藏学生ID列
    };
  },
  methods: {
    handleSelect(index) {
      this.showExtraColumn = (index === '2');
      this.hideStudentID = (index === '2'); // 当选择我的记录时隐藏学生ID列
      if (index === '1') {
        this.fetchAll();
      } else if (index === '2') {
        this.fetchMine();
      }
    },
    fetchAll() {
      axios.get('/api/submitlist', {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          fetchall: true
        }
      })
        .then(response => {
          this.submissions = response.data.data.sort((a, b) => new Date(b.submit_time) - new Date(a.submit_time));
        })
        .catch(error => {
          alert(`失败: ${error.response.data.message}`);
        });
    },
    fetchMine() {
      axios.get('/api/submitlist', {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          fetchall: false,
          user_id: localStorage.getItem('userID')
        }
      })
        .then(response => {
          this.submissions = response.data.data.sort((a, b) => new Date(b.submit_time) - new Date(a.submit_time));
        })
        .catch(error => {
          alert(`失败: ${error.response.data.message}`);
        });
    },
    judgeResult(passRate) {
      const mapping = {
        '-1': 'PENDING',
        '0': 'ACCEPTED',
        '1': 'RUNERROR',
        '2': 'WRONGANSWER',
        '3': 'TIMELIMIT_EXCEED',
        '4': 'MEMLIMIT_EXCEED',
      };
      return mapping[passRate] || 'UNKNOWN';
    }
  },
  filters: {
    formatDate(value) {
      return new Date(value).toLocaleString();
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
}
.side-menu {
  width: 200px;
  height: 100vh;
  border-right: 1px solid #ebeef5;
}
.content {
  flex: 1;
  padding: 20px;
}
h1 {
  text-align: center;
  color: #2c3e50;
}
table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed; /* 同样宽度的列 */
}
th, td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: center; /* 居中显示所有的列 */
}
th {
  background-color: #f4f4f4;
}
</style>
