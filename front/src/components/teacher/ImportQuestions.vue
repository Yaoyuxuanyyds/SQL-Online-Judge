<template>
  <div>
    <Navbar />
    <div class="import-questions-container">
      <h1>Import Questions</h1>
      <p>导入题目</p>

      <!-- 输入新题目信息 -->
      <div class="form-group">
        <label>题目ID:</label>
        <input v-model="newQuestion.id" class="large-input" placeholder="题目ID">
      </div>
      <div class="form-group">
        <label>题目标题:</label>
        <input v-model="newQuestion.title" class="large-input" placeholder="题目标题">
      </div>
      <div class="form-group">
        <label>创建者代码:</label>
        <input v-model="newQuestion.creator_code" class="large-input" placeholder="创建者代码">
      </div>
      <div class="form-group">
        <label>题目描述:</label>
        <textarea v-model="newQuestion.description" class="large-textarea" placeholder="题目描述"></textarea>
      </div>
      <div class="form-group">
        <label>输出:</label>
        <input v-model="newQuestion.output" class="large-input" placeholder="输出">
      </div>
      <div class="form-group">
        <label>难度:</label>
        <select v-model="newQuestion.difficulty" class="large-input">
          <option value="1">1 - 最简单</option>
          <option value="2">2 - 简单</option>
          <option value="3">3 - 一般</option>
          <option value="4">4 - 中等</option>
          <option value="5">5 - 困难</option>
        </select>
      </div>
      <div class="form-group">
        <label>答案示例:</label>
        <textarea v-model="newQuestion.answer_example" class="large-textarea" placeholder="答案示例"></textarea>
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
        id: '',
        title: '',
        creator_code: '',
        description: '',
        output: '',
        difficulty: '1', // 默认难度为最简单
        answer_example: '',
        is_public: false
      }
    };
  },
  methods: {
    createQuestion() {
      // 假设这里需要将新题目数据传递到 Questions 页面
      this.$emit('new-question', this.newQuestion);
      // 或者通过 Vuex 的 actions 将数据提交到 store，然后在 Questions 页面获取
      // this.$store.dispatch('addQuestion', this.newQuestion);

      // 清空输入框
      this.newQuestion = {
        id: '',
        title: '',
        creator_code: '',
        description: '',
        output: '',
        difficulty: '1', // 重置难度为最简单
        answer_example: '',
        is_public: false
      };

      alert('题目已创建并加入到 Questions 页面中！');
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

</style>
