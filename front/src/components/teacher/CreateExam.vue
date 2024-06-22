<template>
  <div>
    <!-- <Navbar /> -->
    <div class="create-exam-container">
      <h1>Create Exam</h1>
      <p>创建竞赛</p>
      
      <!-- 输入考试信息 -->
      <div class="form-group">
        <label>Exam Name:</label>
        <input v-model="examName" placeholder="Exam Name" @input="updateExamName">
      </div>
      <!-- <div class="form-group">
        <label>Start Time:</label>
        <input type="datetime-local" v-model="startTime" @input="updateExamTime('start')">
      </div>
      <div class="form-group">
        <label>End Time:</label>
        <input type="datetime-local" v-model="endTime" @input="updateExamTime('end')">
      </div> -->
      
      <!-- 学生添加 -->
      <div class="form-group">
        <label>Add Student by ID:</label>
        <input v-model="studentId" placeholder="Student ID">
        <button @click="addStudent">Add Student</button>
      </div>
      
      <!-- 题目添加 -->
      <div v-for="(question, index) in questions" :key="index" class="form-group">
        <label>Question {{ index + 1 }}:</label>
        <input v-model="question.number" placeholder="Question Number">
        <input v-model.number="question.score" type="number" placeholder="Score">
        <button @click="removeQuestion(index)">Remove</button>
      </div>
      <button @click="addQuestion">Add Question</button>
      
      <!-- 表格展示题目 -->
      <table v-if="questions.length > 0" class="exam-table">
        <thead>
          <tr>
            <th>Question Number</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(question, index) in questions" :key="index">
            <td>{{ question.number }}</td>
            <td>{{ question.score }}</td>
          </tr>
        </tbody>
      </table>
      
      <!-- 右侧显示总题目数量和总分值 -->
      <div class="totals">
        Total Questions: {{ totalQuestions }}
        Total Score: {{ totalScore }}
      </div>
      
      <!-- 完成创建按钮 -->
      <button @click="submitExam">Finish Creating</button>
    </div>
  </div>
</template>

<script>
// import Navbar from '@/components/teacher/Navbar.vue';
import { mapState, mapActions } from 'vuex';

export default {
  // components: {
  //   Navbar
  // },
  data() {
    return {
      examName: '',
      // startTime: '',
      // endTime: '',
      studentId: '',
      questions: [{ number: '', score: '' }]
    };
  },
  computed: {
    ...mapState({
      // students: state => state.newExam.students,
      totalQuestions: state => state.newExam.questions.length,
      totalScore: state => state.newExam.questions.reduce((acc, cur) => acc + cur.score, 0)
    })
  },
  methods: {
    ...mapActions(['addStudent', 'addQuestion', 'removeQuestion', 'submitExam']),
    updateExamName() {
      this.$store.commit('SET_EXAM_NAME', this.examName);
    },
    // updateExamTime(type) {
    //   const time = type === 'start' ? this.startTime : this.endTime;
    //   this.$store.commit('SET_EXAM_TIME', { startTime: this.startTime, endTime: this.endTime });
    // },
    addStudent() {
      if (this.studentId) {
        this.$store.dispatch('addStudent', { id: this.studentId });
        this.studentId = '';
      }
    },
    addQuestion() {
      this.questions.push({ number: '', score: '' });
    },
    removeQuestion(index) {
      this.$store.dispatch('removeQuestion', index);
    },
    submitExam() {
      if (this.questions.length > 0 && this.examName) {
        this.$store.dispatch('submitExam');
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

.form-group {
  margin-bottom: 10px;
}

.exam-table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
}

.exam-table th, .exam-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

.totals {
  margin-top: 20px;
  font-weight: bold;
}
</style>
