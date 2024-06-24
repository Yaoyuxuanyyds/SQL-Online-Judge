<template>
  <div>
    <Navbar />
    <div class="container">
      <h1 class="title">创建题目</h1>
      <div class="card">
        <h2>题目信息</h2>
        <input v-model="newQuestion.title" placeholder="题目标题" class="input-title" />
        <textarea v-model="newQuestion.create_code" placeholder="建表语句" class="textarea-code"></textarea>
        <textarea v-model="newQuestion.description" placeholder="题目描述" class="textarea-description"></textarea>
        <div class="examples">
          <textarea v-model="newQuestion.input_example" placeholder="输入示例" class="textarea-example"></textarea>
          <textarea v-model="newQuestion.output_example" placeholder="输出示例" class="textarea-example"></textarea>
        </div>
        <div class="difficulty-public">
          <el-select v-model="newQuestion.difficulty" placeholder="选择难度" class="select-difficulty">
            <el-option label="1 - 简单" value="1" />
            <el-option label="2 - 中等" value="2" />
            <el-option label="3 - 困难" value="3" />
            <el-option label="4 - 挑战" value="4" />
            <el-option label="5 - 地狱" value="5" />
          </el-select>
          <el-checkbox v-model="newQuestion.is_public">公开题目</el-checkbox>
        </div>
        <textarea v-model="newQuestion.answer_example" placeholder="答案示例" class="textarea-answer"></textarea>
      </div>

      <div class="card">
        <h2>添加测试点</h2>
        <div v-for="(testCase, index) in testCases" :key="index" class="test-case">
          <textarea v-model="testCase.input_sql" placeholder="输入数据" class="textarea-example"></textarea>
          <textarea v-model="testCase.output" placeholder="输出数据" class="textarea-example"></textarea>
          <el-button @click="removeTestCase(index)" type="danger" size="small" class="remove-btn">删除测试点</el-button>
        </div>
        <el-button @click="addTestCase" type="primary" size="small" class="add-btn">添加测试点</el-button>
      </div>

      <el-button @click="createQuestionWithTestCases" type="primary" size="large" class="submit-btn">创建题目</el-button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Navbar from '@/components/teacher/Navbar.vue';
export default {
  name: 'importQUestion',
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
        is_public: true
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
          const questionId = response.data.id;
          const testCases = this.testCases.map(testCase => ({
            ...testCase,
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
.container {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  font-size: 24px;
  color: #333;
  margin: 0;
  padding: 20px 0;
}

.card {
  padding: 20px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  background-color: white;
}

.card h2 {
  margin-bottom: 15px;
  font-size: 20px;
}

.input-title {
  width: 100%;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.textarea-code,
.textarea-description,
.textarea-example,
.textarea-answer {
  width: 100%;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-family: 'Courier New', Courier, monospace;
}

.examples {
  display: flex;
  justify-content: space-between;
}

.examples .textarea-example {
  width: 48%;
}

.difficulty-public {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.select-difficulty {
  width: 48%;
}

.remove-btn {
  margin-top: 10px;
}

.add-btn {
  display: block;
  margin: 20px 0;
}

.submit-btn {
  display: block;
  margin: 20px auto;
  width: 100%;
}
</style>
调整后的Vue脚本
javascript
复制代码
<script>
export default {
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
        is_public: true
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
          const questionId = response.data.id;
          const testCases = this.testCases.map(testCase => ({
            ...testCase,
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