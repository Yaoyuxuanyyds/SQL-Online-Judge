<template>
  <div>
    <Navbar />
    <div class="container">
      <el-menu :default-active="'1'" class="side-menu" @select="handleSelect">
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
              <th v-if="currentTab === '1'">学生ID</th>
              <th v-if="currentTab === '2'">提交代码</th>
              <th>结果</th>
              <th>通过率</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in filteredSubmissions" :key="record.id">
              <td>{{ record.id }}</td>
              <td>{{ record.submit_time | formatDate }}</td>
              <td>{{ record.question_id }}</td>
              <td v-if="currentTab === '1'">{{ record.student_id }}</td>
              <td v-if="currentTab === '2'">
                <button @click="showCode(record.submit_sql)" class="view-code-btn">点击查看</button>
              </td>
              <td :style="{ color: getStatusColor(record.status) }">{{ judgeResult(record.status) }}</td>
              <td>{{ record.pass_rate }}</td>
              
            </tr>
          </tbody>
        </table>
        
        <!-- 弹窗 -->
        <el-dialog :visible.sync="dialogVisible" width="60%">
          <template slot="title">
            <span>提交代码</span>
          </template>
          <pre ref="code" class="code-display">{{ codeToShow }}</pre>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">关闭</el-button>
          </div>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/teacher/Navbar.vue';
import axios from 'axios'; 

export default {
  name: 'Submissions',
  components: {
    Navbar
  },
  data() {
    return {
      submissions: [],
      searchQuery: '', // 搜索条件：题目ID
      dialogVisible: false,
      codeToShow: '',
      currentTab: '1', // 默认选中第一个标签
    };
  },
  mounted() {
    this.handleSelect('1');
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
      this.currentTab = index; // 更新当前选中的索引
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
          this.submissions = response.data.sort((a, b) => b.id - a.id);
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
          this.submissions = response.data.sort((a, b) => b.id - a.id);
        })
        .catch(error => {
          alert(`失败: ${error.response.data.message}`);
        });
    },
    judgeResult(status) {
      const mapping = [
        'Pending',
        'Accepted',
        'Runtime error',
        "Wrong answer",
        "Time limit exceeded",
        "Memery limit exceeded",
      ];
      return mapping[status + 1];
    },
    getStatusColor(status) {
      const colorMapping = [
        'grey',
        'green',
        'red',
        'orange',
        'purple',
        'blue',
    ];
      return colorMapping[status + 1] || 'black';
    },
    showCode(submitSql) {
      this.codeToShow = submitSql;
      this.dialogVisible = true;
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

.view-code-btn {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
}

.view-code-btn:hover {
  background-color: #218838;
}

.code-display {
  font-family: 'Source Code Pro', 'Consolas', 'Unifont', monospace;
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 5px;
  white-space: pre-wrap; /* 自动换行 */
  overflow-x: auto; /* 横向滚动条 */
  text-align: left; /* 左对齐 */
}

.hljs-ln-numbers {
  text-align: right;
  padding-right: 10px;
  border-right: 1px solid #ccc;
  user-select: none;
}

.hljs-ln-code {
  padding-left: 10px;
}
</style>
