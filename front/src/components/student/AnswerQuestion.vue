<template>
  <div class="container">
    <Navbar />
    <div class="question-container">
      <div class="card">
        <h1>{{ question.title }}</h1>
        <p><strong>难度:</strong> {{ question.difficulty }}</p>
      </div>
      <div class="card">
        <h2>题目描述:</h2>
        
        <p>{{ question.description }}</p>
      </div>
      <div class="card">
        <h2>建表语句:</h2>
        <p>{{ question.create_code }}</p>
      </div>
      <div class="card">
        <h2>参考答案示例:</h2>
        <p>{{ question.answer_example }}</p>
      </div>
      <textarea v-model="userAnswer" placeholder="在这里输入你的答案..." class="answer-textbox"></textarea>
      <button @click="submitAnswer" class="submit-btn">提交答案</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '@/components/student/Navbar.vue';

export default {
  components: {
    Navbar
  },
  data() {
    return {
      question: {},
      userAnswer: '',
      userid: localStorage.getItem('userID')
    };
  },
  mounted() {
    this.fetchQuestion();
  },
  methods: {
    fetchQuestion() {
      const QuestionId = this.$route.params.id;
      axios.get(`/api/question`, {
        headers: {
          'session': localStorage.getItem('session'),
        },
        params: {
          question_id: QuestionId
        }
      })
      .then(response => {
        this.question = response.data;
      })
      .catch(error => {
          alert(`失败: ${error.response.data.message}`);
        }); 
    },
    submitAnswer() {
      // Submit第一步：在submit表中添加一条记录
      axios.post(`/api/submit`, { 
        student_id: localStorage.getItem('userID'),
        exam_id: -1,
        submit_sql: this.userAnswer,
        submit_time: new Date().toISOString(),
        question_id: this.$route.params.id,
      }, {
        headers: {
          'session': localStorage.getItem('session'),
          'Content-Type': 'application/json'
        }
      })
        .then(response => {
          alert(`成功: ${response.data.message}`);
        })
        .catch(error => {
          alert(`失败: ${error.response.data.message}`);
        }); 
    }
  }
};
</script>

<style scoped>
.container {
  padding: 20px;
  margin: auto;
  width: 80%;
}
.question-container {
  margin: auto;
}
.card {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.answer-textbox {
  width: 100%;
  height: 200px;
  margin-top: 20px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  box-shadow: inset 0 1px 2px rgba(0,0,0,0.1);
}
.submit-btn {
  display: block;
  width: 100%;
  padding: 10px;
  margin-top: 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}
.submit-btn:hover {
  background-color: #45a049;
}
</style>
