<template>
    <div>
      <Navbar />
      <div class="container">
  <div class="question-container">
    <div class="card">
      <h1>{{ question.title }}</h1>
      <p><strong>难度:</strong> {{ getDifficultyLabel(question.difficulty) }}</p>
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
      <h2>输入示例:</h2>
      <p>{{ question.input_example }}</p>
    </div>
    <div class="card">
      <h2>输出示例:</h2>
      <p>{{ question.output_example }}</p>
    </div>
  
    <textarea v-model="userAnswer" placeholder="在这里输入你的答案..." class="answer-textbox"></textarea>
    <button @click="submitAnswer" class="submit-btn">提交答案</button>
  </div>
  </div>
    </div>
  
  </template>
  
  <script>
  import axios from 'axios';
  import Navbar from '@/components/Navbar.vue';
  
  export default {
    components: {
      Navbar
    },
    data() {
      return {
        question: {
          title: '',
          create_code: '',
          description: '',
          input_example: '',
          output_example: '',
          difficulty: 1, // 默认难度为1
          answer_example: '',
          is_public: true // 默认为公开题目
        },
        userAnswer: '',
        userid: localStorage.getItem('userID'),
        pass_rate: ''
      };
    },
    mounted() {
      this.fetchQuestion();
    },
    methods: {
      fetchQuestion() {
        const QuestionId = this.$route.params.id;
        // 发送请求获取题目信息
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
          alert(`获取题目信息失败: ${error.response.data.message}`);
        });
      },
      submitAnswer() {
        // 获取当前的最高pass_rate
        const QuestionId = this.$route.params.id;
        const examId = this.$route.params.examId;
        const userId = localStorage.getItem('userID');
        // 发送请求获取当前最高pass_rate
        axios.get(`/api/submit`, {
          headers: {
            'session': localStorage.getItem('session'),
          },
          params: {
            question_id: QuestionId,
            exam_id: examId,
            student_id: userId
          }
        })
        .then(response => {
          this.pass_rate = response.data.pass_rate;
        })
        .catch(error => {
          alert(`获取当前最高pass_rate失败: ${error.response.data.message}`);
        });
        // 记录提交
        axios.post(`/api/submit`, { 
          student_id: localStorage.getItem('userID'),
          exam_id: this.$route.params.examId,
          submit_sql: this.userAnswer,
          submit_time: new Date().toISOString(),
          question_id: this.$route.params.questionId,
        }, {
          headers: {
            'session': localStorage.getItem('session'),
            'Content-Type': 'application/json'
          }
        })
        // 判题
        .then(response => {
          const submit_id = response.data.submit_id;
          return axios.post('/api/judge', {
            submit_sql: this.userAnswer,
            question_id: this.$route.params.questionId,
            create_code: this.question.create_code,
            submit_id: submit_id
          }, {
            headers: {
              'session': localStorage.getItem('session'),
              'Content-Type': 'application/json'
            }
          });
        })
        .then(response => {
          alert(`判题结果: ${JSON.stringify(response.data.result)}`)
          // 进一步调用api更新得分
          const examId = this.$route.params.examId;
          const questionId = this.$route.params.questionId;
          const userId = localStorage.getItem('userID');
          const pass_rate = response.data.result.pass_rate;
          if (pass_rate > this.pass_rate) {
            // 更新得分
            return axios.post('/api/update_score', {
              exam_id: examId,
              question_id: questionId,
              user_id: userId,
              old_rate: this.pass_rate,
              new_rate: pass_rate
            }, {
              headers: {
                'session': localStorage.getItem('session'),
                'Content-Type': 'application/json'
              }});
          }
        })
        .then(response => {
          alert(`得分更新成功: ${response.data.message}`);
        })
        .catch(error => {
          alert(`更新得分失败: ${error.response.data.message}`);
        })
        .catch(error => {
          alert(`提交答案失败: ${error.response.data}`);
        });
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
  