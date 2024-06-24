<template>
  <div>
    <Navbar />
    <div class="container">
      <el-menu :default-active="'1'" class="side-menu" @select="handleSelect">
        <el-menu-item index="1">所有记录</el-menu-item>
        <el-menu-item index="2">我的记录</el-menu-item>
      </el-menu>
      <div class="content">
        <h1 class="header-title">提交记录</h1>
        
        <!-- 搜索框和按钮 -->
        <div class="search-bar">
          <el-input
            type="text"
            class="search-field"
            v-model="searchQuery"
            placeholder="搜索题目ID..."
            clearable
          ></el-input>
        </div>
        
        <!-- 表格展示提交记录 -->
        <el-table :data="filteredSubmissions" style="width: 100%;" border stripe>
          <el-table-column prop="id" label="提交ID" width="100" align="center"></el-table-column>
          <el-table-column prop="submit_time" label="提交时间" width="200" align="center">
            <template slot-scope="scope">
              {{ scope.row.submit_time | formatDate }}
            </template>
          </el-table-column>
          <el-table-column prop="question_id" label="题目ID" width="100" align="center"></el-table-column>
          <el-table-column v-if="currentTab === '1'" prop="student_id" label="学生ID" width="100" align="center"></el-table-column>
          <el-table-column v-if="currentTab === '2'" prop="submit_sql" label="提交代码" width="120" align="center">
            <template slot-scope="scope">
              <el-button @click="showCode(scope.row.submit_sql)" type="success" size="small">点击查看</el-button>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="结果" width="200" align="center">
            <template slot-scope="scope">
              <span :style="{ color: getStatusColor(scope.row.status) }">{{ judgeResult(scope.row.status) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="pass_rate" label="通过率" width="100" align="center"></el-table-column>
        </el-table>
        
        <!-- 弹窗 -->
        <el-dialog :visible.sync="dialogVisible" width="60%" :before-close="handleClose">
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
import Navbar from '@/components/Navbar.vue';
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
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.side-menu {
  width: 200px;
  height: calc(100vh - 40px);
  border-right: 1px solid #ebeef5;
  border-radius: 10px 0 0 10px;
}

.content {
  flex: 1;
  padding: 20px;
  margin-left: 20px;
  border-radius: 0 10px 10px 0;
  background-color: white;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  min-width: 800px; /* 确保内容区最小宽度 */
}

.header-title {
  text-align: center;
  color: #007bff;
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
}

.search-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
  transition: all 0.3s ease;
}

.search-field {
  width: 300px;
  max-width: 100%;
  padding: 10px;
  font-size: 1rem;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.el-table {
  width: 100%; /* 确保表格占据内容区的全部宽度 */
  border-collapse: collapse;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  table-layout: auto; /* 允许自动调整列宽度 */
}

.el-table th,
.el-table td {
  padding: 12px 15px;
  text-align: center;
  white-space: nowrap; /* 防止内容换行，确保列宽自动调整 */
}

.el-table th {
  background-color: #f4f4f4;
  font-weight: bold;
}

.view-code-btn {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.view-code-btn:hover {
  background-color: #218838;
}

.code-display {
  font-family: 'Source Code Pro', 'Consolas', 'Unifont', monospace;
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 5px;
  white-space: pre-wrap;
  overflow-x: auto;
  text-align: left;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.dialog-footer {
  text-align: right;
}

.el-dialog {
  border-radius: 10px;
}

.el-button {
  transition: all 0.3s ease;
}

.el-button:hover {
  transform: translateY(-2px);
}

.el-button:active {
  transform: translateY(0);
}

.el-button--primary {
  background-color: #007bff;
  border-color: #007bff;
  color: white;
}

.el-button--primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

.el-button--success {
  background-color: #28a745;
  border-color: #28a745;
  color: white;
}

.el-button--success:hover {
  background-color: #218838;
  border-color: #218838;
}
</style>