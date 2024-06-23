<template>
  <div>
    <Navbar />
    <div class="import-questions-container">
      <h1>Import Questions</h1>
      <p>导入题目</p>

      <!-- 输入新题目信息 --><div class="form-group">
      <label>题目标题:</label>
      <input v-model="newQuestion.title" class="large-input" placeholder="题目标题">
    </div>
    <div class="form-group">
      <label>建表语句:</label>
      <input v-model="newQuestion.create_code" class="large-input code-input" placeholder="建表语句">
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
      <input type="checkbox" v-model="newQuestion.is_public">
    </div>

      <!-- 完成创建按钮 -->
      <button @click="createQuestion">完成创建</button>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/teacher/Navbar.vue';

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
      const questoinId = 
      axios.post(`/api/questions/<int:question_id>`, { 
        ...this.newQuestion,
        headers: {
          'session': localStorage.getItem('session')
        }
       })
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
          alert(`提交成功: ${response.data.message}`);
        })
        .catch(error => {
          alert(`提交失败: ${error.response.data.message}`);
        }); 
      
    }
  }
};
</script>

<style scoped>
.import-questions-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.form-group {
  margin-bottom: 15px;
}

.large-input {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
}

.large-textarea {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  height: 150px;
}

button {
  padding: 10px 20px;
  background-color: #007BFF;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
}

button:hover {
  background-color: #0056b3;
}

/* 等宽字体和代码框样式 */
.code-input {
  font-family: 'Source Code Pro', 'Unifont', 'Courier New', Courier, monospace;
  background-color: #f5f5f5;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 4px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* 使大文本区域具有相同样式 */
textarea.code-input {
  min-height: 100px;
  resize: vertical; /* 允许用户垂直调整大小 */
}

</style>
