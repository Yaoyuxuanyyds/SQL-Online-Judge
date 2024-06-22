<template>
  <div>
    <h1>题目列表</h1>
    <ul>
      <li v-for="question in questions" :key="question.id">
        {{ question.title }} - 难度: {{ question.difficulty }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      questions: []
    }
  },
  mounted() {
    this.fetchQuestions();
  },
  methods: {
    fetchQuestions() {
      axios.get('/api/questionlist')  // 确保这是正确的API URL
        .then(response => {
          this.questions = response.data.data;  // 确保与后端返回的格式匹配
        })
        .catch(error => {
          console.error("There was an error fetching the questions:", error);
        });
    }
  }
}
</script>
