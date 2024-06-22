<template>
    <div>
      <h2>题目详情</h2>
      <p>题目ID: {{ question.id }}</p>
      <h3>{{ question.title }}</h3>
      <p>描述: {{ question.description }}</p>
      <p>难度: {{ question.difficulty }}</p>
      <!-- 临时答题界面 -->
      <div class="answer-area">
        <p>这里是答题界面（临时）</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        question: {},
      };
    },
    methods: {
      fetchQuestion() {
        const questionId = this.$route.params.id;
        fetch(`/api/question/${questionId}`)
          .then(response => response.json())
          .then(data => {
            this.question = data;
          });
      },
    },
    mounted() {
      this.fetchQuestion();
    },
  };
  </script>
  
  <style>
  .answer-area {
    border: 1px solid #ccc;
    padding: 16px;
    margin-top: 16px;
  }
  </style>
  