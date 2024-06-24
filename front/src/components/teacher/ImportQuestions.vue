<template>
  <div>
    <Navbar />
    <div class="import-questions-container">
      <h1>创建新题目</h1>

      <div class="form-group">
        <label>题目标题:</label>
        <input v-model="newQuestion.title" class="large-input" placeholder="题目标题" />
      </div>
      <div class="form-group">
        <label>建表语句:</label>
        <input v-model="newQuestion.create_code" class="large-input code-input" placeholder="建表语句" />
      </div>
      <div class="form-group">
        <label>题目描述:</label>
        <textarea v-model="newQuestion.description" class="large-textarea code-input" placeholder="题目描述"></textarea>
      </div>
      <div class="form-group">
        <label>示例输入:</label>
        <textarea v-model="newQuestion.input_example" class="large-textarea code-input" placeholder="输入"></textarea>
      </div>
      <div class="form-group">
        <label>示例输出:</label>
        <textarea v-model="newQuestion.output_example" class="large-textarea code-input" placeholder="输出"></textarea>
      </div>
      <div class="form-group">
        <label>难度:</label>
        <select v-model="newQuestion.difficulty" class="large-input">
          <option value="1">1 - 简单</option>
          <option value="2">2 - 中等</option>
          <option value="3">3 - 困难</option>
          <option value="4">4 - 挑战</option>
          <option value="5">5 - 地狱</option>
        </select>
      </div>
      <div class="form-group">
        <label>答案示例:</label>
        <textarea v-model="newQuestion.answer_example" class="large-textarea code-input" placeholder="答案示例"></textarea>
      </div>
      <div class="form-group">
        <label>是否公开:</label>
        <input type="checkbox" v-model="newQuestion.is_public" />
      </div>

      <button class="create-button" @click="createQuestion">完成创建</button>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/teacher/Navbar.vue';
import axios from 'axios';

export default {
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
      }
    };
  },
  methods: {
    createQuestion() {
      axios.post(`/api/question`, { ...this.newQuestion },
        { headers: { 'session': localStorage.getItem('session'), 'Content-Type': 'application/json' } })
        .then(response => {
          // 清空输入框
          this.newQuestion = {
            title: '',
            create_code: '',
            description: '',
            input_example: '',
            output_example: '',
            difficulty: '1', // 重置难度为最简单
            answer_example: '',
            is_public: true
          };
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
/* 主容器样式 */
.import-questions-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 30px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 表单组件样式 */
.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

/* 输入框和文本区域样式 */
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
  resize: vertical; /* 允许用户垂直调整大小 */
}

/* 按钮样式 */
.create-button {
  padding: 15px 25px;
  background-color: #007BFF;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 16px;
  transition: background-color 0.3s, transform 0.2s;
}

.create-button:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
}

/* 按钮点击效果 */
.create-button:active {
  transform: translateY(0);
  background-color: #003f80;
  transition: background-color 0.1s, transform 0.1s;
}

/* 等宽字体和代码框样式 */
.code-input {
  font-family: 'Source Code Pro', 'Courier New', Courier, monospace;
  background-color: #f5f5f5;
  border: 1px solid #ccc;
  border-radius: 4px;
}

</style>