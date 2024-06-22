<template>
  <div>
    <Navbar />
    <div class="question-list">
      <div v-for="question in paginatedQuestions" :key="question.id" class="question-card" @click="goToQuestion(question.id)">
        <h3>{{ question.title }}</h3>
        <p>ID: {{ question.id }}</p>
        <p>难度: {{ question.difficulty }}</p>
      </div>
    </div>
    <div class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
      <span>第 {{ currentPage }} 页</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/student/Navbar.vue';
export default {
  name: 'QuestionList',
  components: {
    Navbar,
  },
  data() {
    return {
      questions: [],
      currentPage: 1,
      pageSize: 10,
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.questions.length / this.pageSize);
    },
    paginatedQuestions() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.questions.slice(start, end);
    },
  },
  methods: {
    fetchQuestions() {
      fetch('/api/questions')
        .then(response => response.json())
        .then(data => {
          this.questions = data.data;
        });
    },
    goToQuestion(questionId) {
      this.$router.push({ name: 'QuestionDetail', params: { id: questionId } });
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage -= 1;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage += 1;
      }
    },
  },
  mounted() {
    this.fetchQuestions();
  },
};
</script>

<style>
.question-list {
  display: flex;
  flex-direction: column;
}
.question-card {
  border: 1px solid #ccc;
  padding: 16px;
  margin: 8px 0;
  cursor: pointer;
}
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 16px;
}
</style>
