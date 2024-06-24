<template>
    <div class="container">
      <h1 class="exam-title">{{ examName }}</h1>
      <div class="exam-info">
        <p>开始时间: {{ examStartTime | formatDate }}</p>
        <p>截止时间: {{ examEndTime | formatDate }}</p>
      </div>
  
      <el-table
        :data="questions.slice((currentPage - 1) * pageSize, currentPage * pageSize)"
        style="width: 100%"
        border
        stripe
      >
        <el-table-column prop="id" label="ID" width="100" align="center" />
        <el-table-column prop="title" label="标题" align="center" />
        <el-table-column prop="difficulty" label="难度" width="120" align="center">
          <template slot-scope="scope">
            <span :style="{ color: getColor(scope.row.difficulty) }">{{ getDifficultyLabel(scope.row.difficulty) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" align="center">
          <template #default="scope">
            <el-button @click="enterQuestion(scope.row.id)" type="success" size="small">进入</el-button>
          </template>
        </el-table-column>
      </el-table>
  
      <el-pagination
        @current-change="handlePageChange"
        :current-page="currentPage"
        :page-size="pageSize"
        :page-sizes="[5, 10, 20, 30]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="questions.length"
      />
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'QuestionList',
    data() {
      return {
        examName: '',
        examStartTime: '',
        examEndTime: '',
        questions: [],
        currentPage: 1,
        pageSize: 20,
      };
    },
    mounted() {
      this.fetchExamInfo();
      this.fetchQuestions();
    },
    methods: {
      fetchExamInfo() {
        // 示例：从后端获取考试信息
        axios.get('/api/contest')
          .then(response => {
            this.examName = response.data.name;
            this.examStartTime = response.data.startTime;
            this.examEndTime = response.data.endTime;
          })
          .catch(error => {
            console.error('获取考试信息失败:' + error.response.data.message);
          });
      },
      fetchQuestions() {
        // 示例：从后端获取题目列表数据
        axios.get(`/api/questionlist`, {
          headers: {
            'session': localStorage.getItem('session')
          }
        })
        .then(response => {
          // 假设后端返回的数据结构包含了题目的基本信息
          this.questions = response.data.map(question => ({
            ...question,
            accuracy: 0 // 假设不需要显示准确率，设置为默认值
          }));
        })
        .catch(error => {
          console.error("获取题目列表失败:" + error.response.data.message);
        });
      },
      filterQuestion(question) {
        // 省略题目过滤逻辑，根据需要进行实现
      },
      enterQuestion(id) {
        this.$router.push({ name: 'answer-question', params: { id: id } });
      },
      handlePageChange(newPage) {
        this.currentPage = newPage;
      },
      getDifficultyLabel(difficulty) {
        // 省略难度标签显示逻辑，根据需要进行实现
      },
      getColor(difficulty) {
        // 省略难度颜色显示逻辑，根据需要进行实现
      }
    },
    filters: {
      formatDate(date) {
        if (!date) return '';
        const d = new Date(date);
        return d.toLocaleString();
      }
    }
  };
  </script>
  
  <style scoped>
  .container {
    padding: 20px;
    text-align: center;
  }
  .exam-title {
    font-size: 24px;
    margin-bottom: 10px;
  }
  .exam-info {
    margin-bottom: 20px;
  }
  </style>
  