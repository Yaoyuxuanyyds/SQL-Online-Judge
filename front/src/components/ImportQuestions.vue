<template>
  <div>
    <Navbar />
    <div class="create-question-container">
      <h1 class="header-title">创建题目</h1>
      <div class="section-container">
        <h2>题目信息</h2>
        <div class="form-group">
          <label>题目标题:</label>
          <input v-model="newQuestion.title" placeholder="题目标题" class="large-input" />
        </div>
        <div class="form-group">
          <label>建表语句:</label>
          <textarea v-model="newQuestion.create_code" placeholder="建表语句" class="large-textarea"></textarea>
        </div>
        <div class="form-group">
          <label>题目描述:</label>
          <textarea v-model="newQuestion.description" placeholder="题目描述" class="large-textarea"></textarea>
        </div>
        <div class="form-group-horizontal">
          <div class="form-group">
            <label>输入示例:</label>
            <textarea v-model="newQuestion.input_example" placeholder="输入示例" class="large-textarea"></textarea>
          </div>
          <div class="form-group">
            <label>输出示例:</label>
            <textarea v-model="newQuestion.output_example" placeholder="输出示例" class="large-textarea"></textarea>
          </div>
        </div>
        <div class="form-group-horizontal">
          <div class="form-group">
            <label>难度:</label>
            <el-select v-model="newQuestion.difficulty" placeholder="选择难度" class="large-input">
              <el-option label="1 - 简单" value="1" />
              <el-option label="2 - 中等" value="2" />
              <el-option label="3 - 困难" value="3" />
              <el-option label="4 - 挑战" value="4" />
              <el-option label="5 - 地狱" value="5" />
            </el-select>
          </div>
          <div class="form-group">
            <label>公开题目:</label>
            <el-checkbox v-model="newQuestion.is_public" class="large-input">公开题目</el-checkbox>
          </div>
        </div>
        <div class="form-group">
          <label>答案示例:</label>
          <textarea v-model="newQuestion.answer_example" placeholder="答案示例" class="large-textarea"></textarea>
        </div>
      </div>

      <div class="section-container">
        <h2>添加测试点</h2>
        <div class="form-group">
          <label>测试表:</label>
          <textarea v-model="newQuestion.tablename" placeholder="测试表" class="large-textarea"></textarea>
        </div>
        <div v-for="(testCase, index) in testCases" :key="index" class="test-case">
          <div class="form-group-horizontal">
            <div class="form-group">
              <label>输入数据:</label>
              <textarea v-model="testCase.input_sql" placeholder="输入数据" class="large-textarea"></textarea>
            </div>
            <div class="form-group">
              <label>输出数据:</label>
              <textarea v-model="testCase.output" placeholder="输出数据" class="large-textarea"></textarea>
            </div>
          </div>
          <div class="form-group form-group--center">
            <button @click="removeTestCase(index)" class="remove-button">删除测试点</button>
          </div>
        </div>
        <div class="form-group form-group--center">
          <button @click="addTestCase" class="create-button">添加测试点</button>
        </div>
      </div>

      <div class="section-container submit-section">
        <button @click="createQuestionWithTestCases" class="submit-button">创建题目</button>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
import Navbar from '@/components/Navbar.vue';

export default {
  name: 'ImportQuestion',
  components: {
    Navbar
  },
  data() {
    return {
      newQuestion: {
        title: '',
        create_code: '',
        description: '',
        input_example: '',
        output_example: '',
        difficulty: '1',
        answer_example: '',
        is_public: true,
        tablename: ''
      },
      testCases: [
        { input_sql: '', output: '' }
      ]
    };
  },
  methods: {
    addTestCase() {
      this.testCases.push({ input_sql: '', output: '' });
    },
    removeTestCase(index) {
      this.testCases.splice(index, 1);
    },
    createQuestionWithTestCases() {
      axios.post(`/api/question`, { ...this.newQuestion },
        { headers: { 'session': localStorage.getItem('session'), 'Content-Type': 'application/json' } })
        .then(response => {
          const questionId = response.data.question_id;
          const testCases = this.testCases.map(testCase => ({
            ...testCase,
            tablename: this.newQuestion.tablename,
            question_id: questionId
          }));
          return axios.post(`/api/testcase`, { test_cases: testCases, question_id: questionId },
            { headers: { 'session': localStorage.getItem('session'), 'Content-Type': 'application/json' } });
        })
        .then(response => {
          // 清空输入框
          this.newQuestion = {
            title: '',
            create_code: '',
            description: '',
            input_example: '',
            output_example: '',
            difficulty: '1',
            answer_example: '',
            is_public: true
          };
          this.testCases = [{ input_sql: '', output: '' }];
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
.create-question-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 30px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.section-container {
  margin-bottom: 20px;
  background-color: #ffffff;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.large-input,
.large-textarea,
select.large-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
  font-size: 16px;
}

.large-textarea {
  height: 120px;
  resize: vertical;
}

.header-title {
  text-align: center;
  margin-bottom: 30px;
  font-size: 2rem;
  color: #007bff;
  font-weight: bold;
}

.form-group-horizontal {
  display: flex;
  justify-content: space-between;
}

.form-group-horizontal .form-group {
  flex: 1;
}

.form-group-horizontal .form-group + .form-group {
  margin-left: 20px;
}

.form-group--center {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.remove-button {
  padding: 10px 20px;
  background-color: #ff2b14;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 16px;
  transition: background-color 0.3s, transform 0.2s;
  margin: 5px;
}

.create-button {
  padding: 10px 20px;
  background-color: #01910d;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 16px;
  transition: background-color 0.3s, transform 0.2s;
  margin: 5px;
}

.submit-button {
  padding: 10px 20px;
  background-color: #1257e1;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 16px;
  transition: background-color 0.3s, transform 0.2s;
  margin: 5px;
}

.create-button:hover {
  background-color: #006823;
  transform: translateY(-2px);
}

.remove-button:hover {
  background-color: #983000;
  transform: translateY(-2px);
}

.submit-button:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
}

.create-button:active {
  transform: translateY(0);
  background-color: #025d00;
  transition: background-color 0.1s, transform 0.1s;
}

.remove-button:active {
  transform: translateY(0);
  background-color: #800000;
  transition: background-color 0.1s, transform 0.1s;
}

.submit-button:active {
  transform: translateY(0);
  background-color: #003f80;
  transition: background-color 0.1s, transform 0.1s;
}

.submit-section {
  text-align: center;
  margin-top: 30px;
}
</style>