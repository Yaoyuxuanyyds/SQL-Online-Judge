<template>
  <div>
    <Navbar />
    <div class="container">
      <div class="main-content">
        <h1 class="header-title">{{ question.title }}</h1>
        
        <div class="card">
          <h2 class="card-title">题目介绍</h2>
          <p>{{ question.description }}</p>
        </div>

        <div class="card-row">
          <div class="card half-card">
            <h2 class="card-title">示例输入</h2>
            <pre class="code-block">{{ question.input_example }}</pre>
          </div>
          <div class="card half-card">
            <h2 class="card-title">示例输出</h2>
            <pre class="code-block">{{ question.output_example }}</pre>
          </div>
        </div>

        <div class="card">
          <h2 class="card-title">建表语句</h2>
          <pre class="code-block">{{ question.create_code }}</pre>
        </div>

        <div v-if="parseInt(this.role) > 0" class="card">
          <h2 class="card-title">参考答案</h2>
          <pre class="code-block">{{ question.answer_example }}</pre>
        </div>

        <div class="card">
          <h2 class="card-title">做题区域</h2>
          <el-input type="textarea" v-model="userAnswer" class="answer-input" rows="10" placeholder="在这里编写你的答案"></el-input>
          <el-button type="success" class="submit-button" @click="submitAnswer">提交代码</el-button>
        </div>
      </div>

      <div class="sidebar">
        <div class="card">
          <h2 class="card-title">题目信息</h2>
          <p><strong>题目ID：</strong>{{ question.id }}</p>
          <p><strong>题目难度：</strong>{{ getDifficultyLabel(question.difficulty) }}</p>
          <p><strong>已通过：</strong>{{ question.completed ? '是' : '否' }}</p>
          <p><strong>通过率：</strong>{{ question.accuracy }}%</p>
          <p><strong>完成率：</strong>{{ question.completion_rate }}%</p>
          <p><strong>提交数：</strong>{{ question.submit_count }}</p>
        </div>
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
        id: '',
        title: '',
        create_code: '',
        description: '',
        input_example: '',
        output_example: '',
        difficulty: 1, // 默认难度为1
        answer_example: '',
        is_public: true, // 默认为公开题目
        completed: false,
        accuracy: 0,
        completion_rate: 0,
        submit_count: 0,
        role: localStorage.getItem('userRole'),
      },
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
        alert(`获取题目信息失败: ${error.response.data.message}`);
      });
    },
    submitAnswer() {
      axios.post(`/api/submit`, { 
        student_id: this.userid,
        exam_id: null,
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
        const submit_id = response.data.submit_id;
        return axios.post('/api/judge', {
          submit_sql: this.userAnswer,
          question_id: this.$route.params.id,
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
        alert(`判题结果: ${JSON.stringify(response.data.result)}`);
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
  display: flex;
  padding: 20px;
  background-color: #f9f9f9;
  gap: 20px;
}

.main-content {
  flex: 3;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.header-title {
  text-align: center;
  color: #007bff;
  font-size: 2rem;
  font-weight: bold;
}

.card {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.card-row {
  display: flex;
  gap: 20px;
}

.half-card {
  flex: 1;
}

.code-block {
  font-family: 'Source Code Pro', 'Consolas', monospace;
  background-color: #f5f5f5;
  padding: 10px;
  border-radius: 5px;
  white-space: pre-wrap;
  overflow-x: auto;
}

.answer-input {
  width: 100%;
  font-family: 'Source Code Pro', 'Consolas', monospace;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.submit-button {
  display: block;
  margin: 20px auto 0;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #218838;
}
</style>
