<template>
  <div>
    <Navbar />
    <div class="create-exam-container">
      <div class="exam-time">
        <h2>设置考试时间</h2>
        <div class="form-group">
          <label>开始时间:</label>
          <input type="datetime-local" v-model="startTime">
        </div>
        <div class="form-group">
          <label>截止时间:</label>
          <input type="datetime-local" v-model="endTime">
        </div>
      </div>

      <div class="add-question">
        <h2>添加题目</h2>
        <div class="form-group">
          <label>题目ID:</label>
          <input v-model="questionId" placeholder="题目ID">
          <label>分值:</label>
          <input v-model.number="questionScore" type="number" placeholder="分值">
          <button @click="addQuestion">添加题目</button>
        </div>
        <table v-if="questions.length > 0" class="exam-table">
          <thead>
            <tr>
              <th>题目ID</th>
              <th>分值</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(question, index) in questions" :key="index">
              <td>{{ question.id }}</td>
              <td>{{ question.score }}</td>
              <td><button @click="removeQuestion(index)">删除</button></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="add-student">
        <h2>添加学生</h2>
        <div class="form-group">
          <label>学生ID:</label>
          <input v-model="studentId" placeholder="学生ID">
          <button @click="addStudent">添加学生</button>
        </div>
        <table v-if="students.length > 0" class="student-table">
          <thead>
            <tr>
              <th>学生ID</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(student, index) in students" :key="index">
              <td>{{ student.id }}</td>
              <td><button @click="removeStudent(index)">删除</button></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="submit-section">
        <button @click="submitExam">完成创建</button>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/teacher/Navbar.vue';

export default {
  components: {
    Navbar
  },
  name: 'CreateExam',
  data() {
    return {
      startTime: '',
      endTime: '',
      questionId: '',
      questionScore: '',
      studentId: '',
      questions: [],
      students: []
    };
  },
  methods: {
    addQuestion() {
      if (this.questionId && this.questionScore) {
        this.questions.push({ id: this.questionId, score: this.questionScore });
        this.questionId = '';
        this.questionScore = '';
      }
    },
    removeQuestion(index) {
      this.questions.splice(index, 1);
    },
    addStudent() {
      if (this.studentId) {
        this.students.push({ id: this.studentId });
        this.studentId = '';
      }
    },
    removeStudent(index) {
      this.students.splice(index, 1);
    },
    submitExam() {
      if (this.questions.length > 0 && this.startTime && this.endTime) {
        // Handle exam submission logic here (could be an API call or further action)
        alert('考试创建成功！');
      } else {
        alert('请填写完整的考试信息！');
      }
    }
  }
};
</script>

<style scoped>
.create-exam-container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.exam-time, .add-question, .add-student, .submit-section {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 10px;
}

.exam-table, .student-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.exam-table th, .exam-table td, .student-table th, .student-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

.submit-section button {
  display: block;
  margin: auto;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
