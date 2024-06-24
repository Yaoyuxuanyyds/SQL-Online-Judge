<template>
  <div>
    <Navbar />
    <div class="container">
      <div class="main-content">
        <div class="card">
          <h1 class="header-title">{{ question.title }}</h1>
          <div class="card-content">
            <div class="section">
              <h2>题目介绍</h2>
              <p>{{ question.description }}</p>
            </div>
            <div class="section half-section-container">
              <div class="half-section">
                <h3>示例输入</h3>
                <pre class="code">{{ question.input_example }}</pre>
              </div>
              <div class="half-section">
                <h3>示例输出</h3>
                <pre class="code">{{ question.output_example }}</pre>
              </div>
            </div>
            <div class="section">
              <h3>建表语句</h3>
              <pre class="code">{{ question.create_code }}</pre>
            </div>
            <div v-if="userRole > 0" class="section">
              <h3>参考答案</h3>
              <pre class="code">{{ question.answer_example }}</pre>
            </div>
            <div class="section">
              <h3>做题区域</h3>
              <el-input
                type="textarea"
                v-model="userAnswer"
                placeholder="在这里编写你的SQL代码..."
                class="answer-input"
              ></el-input>
              <el-button
                type="success"
                @click="submitAnswer"
                class="submit-button"
              >
                提交代码
              </el-button>
            </div>
          </div>
        </div>
      </div>
      <div class="sidebar">
        <div class="card">
          <div class="card-content">
            <h1 class="header-title">题目信息</h1>
            <div>
              <p><strong>题目ID：</strong>{{ question.id }}</p>
            <p><strong>题目难度：</strong>{{ getDifficultyLabel(question.difficulty) }}</p>
            <p><strong>已完成？</strong> {{ question.completed ? '是' : '否' }}</p>
            <p><strong>通过率：</strong> {{ question.accuracy }}%</p>
            <p><strong>完成率：</strong> {{ question.completion_rate }}%</p>
            <p><strong>提交数：</strong> {{ question.submission_count }}</p>
            </div>
          </div>
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
        title: '',
        create_code: '',
        description: '',
        input_example: '',
        output_example: '',
        difficulty: 1, // 默认难度为1
        answer_example: '',
        is_public: true, // 默认为公开题目,
        completed: false,
        accuracy: null,
        completion_rate: null,
        submission_count: null
      },
      userAnswer: '',
      userid: localStorage.getItem('userID'),
      userRole: localStorage.getItem('userRole'), // 获取用户角色
      submitResult: null, // 用于存储提交结果
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
          question_id: QuestionId,
          student_id: this.userid
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
        student_id: localStorage.getItem('userID'),
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
        this.submitResult = response.data.result;
        alert(`判题结果: ${JSON.stringify(this.submitResult)}`);
      })
      .catch(error => {
        alert(`提交答案失败: ${error.response.data.message}`);
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
  flex-wrap: wrap;
  padding: 20px;
  background-color: #f9f9f9;
  gap: 20px;
}

.main-content {
  flex: 3;
  min-width: 60%;
}

.sidebar {
  flex: 1;
  min-width: 20%;
}

.card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.header-title {
  font-size: 24px;
  font-weight: bold;
  color: #007bff;
  text-align: center;
  margin-bottom: 20px;
}

.card-content {
  padding: 20px;
}

.section {
  margin-bottom: 20px;
}

.half-section-container {
  display: flex;
  justify-content: space-between;
}

.half-section {
  width: 48%;
}

h2, h3 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

p {
  font-size: 16px;
  color: #666;
  line-height: 1.5;
}

.code {
  background: #f5f5f5;
  border-radius: 5px;
  padding: 10px;
  font-family: 'Source Code Pro', monospace;
  white-space: pre-wrap;
  word-wrap: break-word;
  overflow-x: auto;
}

.answer-input {
  width: 100%;
  min-height: 100%;
  font-family: 'Source Code Pro', monospace;
  border-radius: 5px;
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 20px;
}

.submit-button {
  background-color: #28a745;
  border: none;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #218838;
}

.card-content p {
  margin: 10px 0;
}
</style>
