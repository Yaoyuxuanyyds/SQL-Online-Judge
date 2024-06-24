<template>
  <div>
    <Navbar />
    <div class="create-question-container">
      <h1 class="header-title">{{ examName }}</h1>
      <div class="section-container">
        <div class="exam-info">
          <p class="exam-info-item">开始时间: <span class="blue-text">{{ examStartTime | formatDate }}</span></p>
          <p class="exam-info-item">截止时间: <span class="blue-text">{{ examEndTime | formatDate }}</span></p>
          <p v-if="userRole == 0" class="exam-info-item">当前总分: <span class="blue-text">{{ totalScore }}</span></p>
        </div>
      </div>
      <div class="section-container">
        <el-table
          :data="filteredQuestions.slice((currentPage - 1) * pageSize, currentPage * pageSize)"
          style="width: 100%"
          border
          stripe
        >
          <el-table-column prop="id" label="ID" width="100" align="center" />
          <el-table-column prop="title" label="标题" align="center" />
          <el-table-column prop="difficulty" label="难度" width="120" align="center">
            <template slot-scope="scope">
              <span :class="getDifficultyClass(scope.row.difficulty)">{{ getDifficultyLabel(scope.row.difficulty) }}</span>
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
          :total="filteredQuestions.length"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '@/components/Navbar.vue';

export default {
  name: 'QuestionList',
  components: {
    Navbar,
  },
  data() {
    return {
      examName: '',
      examStartTime: '',
      examEndTime: '',
      questions: [],
      contestQuestions: [],
      currentPage: 1,
      pageSize: 20,
      userRole: parseInt(localStorage.getItem('userRole')), // Ensure userRole is parsed as integer
      totalScore: 0,
    };
  },
  computed: {
    filteredQuestions() {
      return this.questions.filter(question => this.contestQuestions.includes(question.id));
    }
  },
  mounted() {
    this.fetchExamInfo();
    this.fetchContestQuestions();
    if (this.userRole == 0) {
      this.fetchTotalScore();
    }
  },
  methods: {
    fetchExamInfo() {
      const contestId = this.$route.params.id;
      axios.get(`/api/contest`, {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: { contest_id: contestId }
      })
      .then(response => {
        this.examName = response.data.name;
        this.examStartTime = response.data.start_time;
        this.examEndTime = response.data.end_time;
      })
      .catch(error => {
        alert('获取考试信息失败: ' + error.response.data.message);
      });
    },
    fetchContestQuestions() {
      const contestId = this.$route.params.id;
      axios.get(`/api/contest-question`, { params: { contest_id: contestId }})
      .then(response => {
        this.contestQuestions = response.data.questionIds;
        this.fetchQuestions();
        if (this.contestQuestions.length === 0) {
          alert("该竞赛没有题目");
          this.$router.push({ name: 'contest-list' });
        }
      })
      .catch(error => {
        alert("获取竞赛题目列表失败: " + error.response.data.message);
      });
    },
    fetchQuestions() {
      axios.get(`/api/questionlist`, {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          student_id: localStorage.getItem('userID')
        }
      })
      .then(response => {
        this.questions = response.data.map(question => ({
          ...question,
          accuracy: 0 // Assuming accuracy is not needed
        }));
      })
      .catch(error => {
        alert("获取题目列表失败: " + error.response.data.message);
      });
    },
    fetchTotalScore() {
      const examId = this.$route.params.id;
      const studentId = localStorage.getItem('userID');
      axios.get(`/api/getscore`, {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          exam_id: examId,
          student_id: studentId
        }
      })
      .then(response => {
        this.totalScore = response.data.score;
      })
      .catch(error => {
        alert("获取总分失败: " + error.response.data.message);
      });
    },
    enterQuestion(id) {
      this.$router.push({ name: 'answer-question-contest', params: { questionId: id, examId: this.$route.params.id }});
    },
    handlePageChange(newPage) {
      this.currentPage = newPage;
    },
    getDifficultyLabel(difficulty) {
      switch (difficulty) {
        case 1: return '简单';
        case 2: return '中等';
        case 3: return '困难';
        case 4: return '挑战';
        case 5: return '地狱';
        default: return '未知';
      }
    },
    getDifficultyClass(difficulty) {
      switch (difficulty) {
        case 1: return 'difficulty-easy';
        case 2: return 'difficulty-medium';
        case 3: return 'difficulty-hard';
        case 4: return 'difficulty-challenge';
        case 5: return 'difficulty-hell';
        default: return '';
      }
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
.create-question-container {
  max-width: 1000px;
  margin: 40px auto;
  padding: 30px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.section-container {
  margin-bottom: 20px;
  background-color: #ffffff;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.header-title {
  text-align: center;
  margin-bottom: 30px;
  font-size: 2rem;
  color: #007bff;
  font-weight: bold;
}

.exam-info {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.exam-info-item {
  margin: 0 10px;
  font-weight: bold;
}

.blue-text {
  color: #007bff;
  font-weight: bold;
}

.el-table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.th {
  background-color: #f2f2f2;
  color: #333;
  font-weight: bold;
  text-align: center;
  font-family: 'Arial', sans-serif;
  font-size: 16px;
}

.td {
  text-align: center;
  font-family: 'Arial', sans-serif;
  font-size: 14px;
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

.difficulty-easy {
  background-color: green;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.difficulty-medium {
  background-color: blue;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.difficulty-hard {
  background-color: orange;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.difficulty-challenge {
  background-color: purple;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.difficulty-hell {
  background-color: red;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}
</style>
