<template>
    <div>
      <h1>Questions List</h1>
      <ul>
        <li v-for="question in questions" :key="question.id">
          {{ question.title }}
          <button @click="editQuestion(question.id)">Edit</button>
          <button @click="deleteQuestion(question.id)">Delete</button>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: 'QuestionsList',
    data() {
      return {
        questions: []
      };
    },
    methods: {
      fetchQuestions() {
        // Assuming an API call to fetch questions
        this.questions = [{ id: 1, title: 'What is Vue.js?' }]; // Example data
      },
      editQuestion(id) {
        // Route to edit page
        this.$router.push(`/questions/edit/${id}`);
      },
      deleteQuestion(id) {
        // API call to delete the question
        alert('Delete function triggered');
      }
    },
    mounted() {
      this.fetchQuestions();
    }
  }
  </script>
  
  <style scoped>
  /* Add your CSS styling here */
  </style>