<template>
  <div>
    <Navbar />
      <div>
        <button @click="handlePageChange(currentPage - 1)" :disabled="currentPage <= 1">上一页</button>
        <span>Page {{ currentPage }}</span>
        <button @click="handlePageChange(currentPage + 1)" :disabled="currentPage >= totalPages">下一页</button>
      </div>
    <div class="question-list">
      <ul>
        <li v-for="question in paginatedQuestions" :key="question.id">
          <h2>{{ question.title }}</h2>
          <p>{{ question.description }}</p>
          <span>Difficulty: {{ question.difficulty }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '@/components/student/Navbar.vue';

export default {
  name: 'QuestionList',
  components: {
    Navbar
  },
  data() {
    return {
      questions: [],
      currentPage: 1,
      pageSize: 10,
      totalPages: 1
    };
  },
  computed: {
    paginatedQuestions() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.questions.slice(start, end);
    }
  },
  created() {
    this.fetchQuestions();
  },
  methods: {
    fetchQuestions() {
      axios.get('/question')
        .then(response => {
          this.questions = response.data.data;
          this.totalPages = Math.ceil(this.questions.length / this.pageSize);
        })
        .catch(error => {
          console.error("There was an error fetching the questions:", error);
        });
    },
    handlePageChange(page) {
      if (page < 1 || page > this.totalPages) return;
      this.currentPage = page;
    }
  }
}
</script>

<style>
/* Add your styles here */
.question-list ul {
  list-style-type: none;
  padding: 0;
}
.question-list li {
  margin-bottom: 20px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 10px;
}
nav div {
  margin-bottom: 20px;
}
</style>
