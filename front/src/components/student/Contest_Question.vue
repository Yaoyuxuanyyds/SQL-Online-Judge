<template>
  <div class="container">
    <h1 class="exam-title">{{ examName }}</h1>
    <div class="exam-info">
      <p>开始时间: {{ examStartTime | formatDate }}</p>
      <p>截止时间: {{ examEndTime | formatDate }}</p>
    </div>

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
      :total="filteredQuestions.length"
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
      contestQuestions: [],
      currentPage: 1,
      pageSize: 20,
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
  },
  methods: {
    fetchExamInfo() {
      const contestId = this.$route.params.id;
      axios.get(`/api/contest`, {
        headers: {
          'session': localStorage.getItem('session')
        },
         params: { contest_id: contestId } })
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
      axios.get(`/api/contest-question`,{params: { contest_id: contestId }})
        .then(response => {
          this.contestQuestions = response.data.questionIds;
          this.fetchQuestions();
        })
        .catch(error => {
          alert("获取竞赛题目列表失败: " + error.response.data.message);
        });
    },
    fetchQuestions() {
      axios.get(`/api/questionlist`,
        { headers: { 'session': localStorage.getItem('session') },}
      )
        .then(response => {
          this.questions = response.data.map(question => ({
            ...question,
            accuracy: 0 // 假设不需要显示准确率，设置为默认值
          }));
        })
        .catch(error => {
          alert("获取题目列表失败: " + error.response.data.message);
        });
    },
    enterQuestion(id) {
      this.$router.push({ name: 'answer-question', params: { id: id } });
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
    getColor(difficulty) {
      switch (difficulty) {
        case 1: return 'green';
        case 2: return 'blue';
        case 3: return 'orange';
        case 4: return 'purple';
        case 5: return 'red';
        default: return 'black';
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
