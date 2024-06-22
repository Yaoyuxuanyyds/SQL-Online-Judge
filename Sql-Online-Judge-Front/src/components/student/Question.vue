<template>
  <div class="container">
    <div class="nav">
    <Navbar />
  </div>
    <h1>题目列表</h1>
    <div class="header">
      <span class="header-item">ID</span>
      <span class="header-item">标题</span>
      <span class="header-item">难度</span>
      <span class="header-item">操作</span>
    </div>
    <ul class="question-list">
      <li v-for="question in questions" :key="question.id" class="question-item">
        <span class="question-id">{{ question.id }}</span>
        <span class="question-title">{{ question.title }}</span>
        <span class="question-difficulty">{{ question.difficulty }}</span>
        <span class="question-action">
          <button @click="enterQuestion(question.id)">进入</button>
        </span>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'
import Navbar from '@/components/student/Navbar.vue';

export default {
  name: 'QuestionList',
  components: {
    Navbar
  },
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
      axios.get(`/api/questionlist`, {
        headers: {
          'session': "f834cfc29a496d93ff627f9220287e0bfffcbc9a"
        }
      })
        .then(response => {
          this.questions = response.data.data;
        })
        .catch(error => {
          console.error("There was an error fetching the questions:", error);
        });
    },
    enterQuestion(id) {
      // 在这里加入进入题目详细页的逻辑
      this.$router.push(`/question/${id}`);
    }
  }
}
</script>

<style scoped>
.container {
  padding: 20px;
}
.header, .question-item {
  display: flex;
  align-items: center;
  padding: 10px;
  margin-bottom: 5px;
  border: 1px solid #e1e1e1;
  background-color: #f9f9f9;
}
.header-item, .question-id, .question-title, .question-difficulty, .question-action {
  flex: 1;
  text-align: center;
}
.question-id {
  flex: 0.2;
}
.question-title {
  flex: 1.5;
}
.question-difficulty {
  flex: 0.3;
}
.question-action {
  flex: 0.5;
}
button {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  outline: none;
}
button:hover {
  background-color: #45a049;
}
.question-item:hover {
  background-color: #eef9f9;
}
h1 {
  color: #333;
  text-align: center;
}
.question-list {
  list-style-type: none;
  padding: 0;
}
</style>
