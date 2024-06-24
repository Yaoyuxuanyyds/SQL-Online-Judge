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
        
        <!-- 搜索框和按钮 -->
        <div class="search-bar">
          <input type="text" class="form-control search-field" v-model="searchQuery" placeholder="搜索题目ID...">
        </div>
        
        <!-- 表格展示提交记录 -->
        <table>
          <thead>
            <tr>
              <th>提交ID</th>
              <th>提交时间</th>
              <th>题目ID</th>
              <th v-if="!hideStudentID">学生ID</th>
              <th>结果</th>
              <th>通过率</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in filteredSubmissions" :key="record.submissionId">
              <td>{{ record.id }}</td>
              <td>{{ record.submit_time | formatDate }}</td>
              <td>{{ record.question_id }}</td>
              <td v-if="!hideStudentID">{{ record.student_id }}</td>
              <td>{{ judgeResult(record.status) }}</td>
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
      searchQuery: '', // 搜索条件：题目ID
    };
  },
  computed: {
    filteredSubmissions() {
      if (!this.searchQuery.trim()) {
        return this.submissions;
      } else {
        const query = this.searchQuery.trim().toLowerCase();
        return this.submissions.filter(submission =>
          submission.question_id.toString().toLowerCase().includes(query)
        );
      }
    }
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
    judgeResult(status) {
      const mapping = {
        '-1': 'Pending',
        '0': 'Accepted',
        '1': 'Runtime error',
        '2': "Wrong answer",
        '3': "Time limit exceeded",
        '4': "Memery limit exceeded",
      };
      return mapping[status];
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
.search-bar {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
.search-field {
  flex: 1;
  padding: 8px;
  font-size: 1rem;
  margin-right: 10px; /* 调整搜索框和按钮之间的间距 */
  max-width: 200px; /* 设置搜索框的最大宽度 */
}
.btn-search {
  padding: 8px 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.btn-search:hover {
  background-color: #0056b3;
}
</style>