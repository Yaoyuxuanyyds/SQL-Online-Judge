<template>
  <div>
    <Navbar />
    <div class="create-exam-container">
      <h1 class="header-title">创建新考试</h1>

      <!-- 考试名称和时间部分 -->
      <div class="section-container">
        <!-- <div class="form-group">
          <label>考试名称:</label>
          <input v-model="examName" placeholder="请输入考试名称" class="large-input" />
        </div> -->
        <div class="form-group-horizontal">
          <div class="form-group">
            <label>开始时间:</label>
            <input type="datetime-local" v-model="startTime" class="large-input" />
          </div>
          <div class="form-group">
            <label>截止时间:</label>
            <input type="datetime-local" v-model="endTime" class="large-input" />
          </div>
        </div>
      </div>

      <!-- 添加题目部分 -->
      <div class="section-container">
        <div class="form-group form-group--center">
          <button @click="toggleAddQuestion" class="create-button">
            {{ showAddQuestion ? "取消添加题目" : "添加题目" }}
          </button>
        </div>
        <div v-if="showAddQuestion">
          <div class="form-group">
            <label>题目ID:</label>
            <input v-model="questionId" placeholder="题目ID" class="large-input" />
          </div>
          <div class="form-group">
            <label>分值:</label>
            <input v-model.number="questionScore" type="number" placeholder="分值" class="large-input" />
          </div>
          <div class="form-group form-group--center">
            <button @click="addQuestion" class="create-button">确认添加题目</button>
          </div>
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
              <td><button @click="removeQuestion(index)" class="remove-button">删除</button></td>
            </tr>
          </tbody>
        </table>
        <div class="totals" v-if="questions.length > 0">
          总题目数量: {{ questions.length }}
          总分值: {{ totalScore }}
        </div>
      </div>

      <!-- 添加学生部分 -->
      <div class="section-container">
        <div class="form-group form-group--center">
          <button @click="toggleAddStudent" class="create-button">
            {{ showAddStudent ? "取消添加学生" : "添加学生" }}
          </button>
        </div>
        <div v-if="showAddStudent">
          <div class="form-group">
            <label>学生ID:</label>
            <input v-model="studentId" placeholder="学生ID" class="large-input" />
          </div>
          <div class="form-group form-group--center">
            <button @click="addStudent" class="create-button">确认添加学生</button>
          </div>
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
              <td><button @click="removeStudent(index)" class="remove-button">删除</button></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 提交部分 -->
      <div class="section-container submit-section">
        <button @click="submitExam" class="create-button">完成创建</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '@/components/teacher/Navbar.vue';

export default {
  components: {
    Navbar
  },
  name: 'CreateExam',
  data() {
    return {
      // examName: '',
      startTime: '',
      endTime: '',
      questionId: '',
      questionScore: '',
      studentId: '',
      questions: [],
      students: [],
      showAddQuestion: false,
      showAddStudent: false
    };
  },
  computed: {
    totalScore() {
      return this.questions.reduce((total, question) => total + parseInt(question.score), 0);
    }
  },
  methods: {
    toggleAddQuestion() {
      this.showAddQuestion = !this.showAddQuestion;
    },
    toggleAddStudent() {
      this.showAddStudent = !this.showAddStudent;
    },
    addQuestion() {
      if (this.questionId && this.questionScore) {
        this.questions.push({ id: this.questionId, score: this.questionScore });
        this.questionId = '';
        this.questionScore = '';
        this.showAddQuestion = false;
      }
    },
    removeQuestion(index) {
      this.questions.splice(index, 1);
    },
    addStudent() {
      if (this.studentId) {
        this.students.push({ id: this.studentId });
        this.studentId = '';
        this.showAddStudent = false;
      }
    },
    removeStudent(index) {
      this.students.splice(index, 1);
    },
    async submitExam() {
      if (this.startTime && this.endTime) {
        try {
          // 提交考试基本信息
          const examResponse = await axios.post('/api/contest', {
            teacher_id: localStorage.getItem('userID'),
            start_time: this.startTime,
            end_time: this.endTime,
          },
          { headers: { 'session': localStorage.getItem('session'), 'Content-Type': 'application/json' } });

          if (examResponse.status === 201) {
            const examId = examResponse.data.id;

            // 提交考试-题目关联信息
            for (const question of this.questions) {
              await axios.post('/api/contest-question', {
                exam_id: examId,
                question_id: question.id,
                score: question.score
              },
              { headers: { 'session': localStorage.getItem('session'), 'Content-Type': 'application/json' } });
            }

            // 提交考试-学生关联信息
            for (const student of this.students) {
              await axios.post('/api/contest-student', {
                exam_id: examId,
                student_id: student.id,
              },
              { headers: { 'session': localStorage.getItem('session'), 'Content-Type': 'application/json' } });
            }

            alert('考试创建成功！');
          } else {
            alert('创建考试时出错，请重试。');
          }
        } catch (error) {
          console.error('Error creating exam:', error);
          alert('创建考试时出错，请重试。');
        }
      } else {
        alert('请填写完整的考试信息！');
      }
    }
  }
};


</script>

<style scoped>
/* 主容器样式 */
.create-exam-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 30px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 部分容器样式 */
.section-container {
  margin-bottom: 20px;
  background-color: #ffffff;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
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

/* 标题样式 */
.header-title {
  text-align: center;
  margin-bottom: 30px;
  font-size: 2rem;
  color: #007bff;
  font-weight: bold;
}

/* 水平布局 */
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

/* 按钮样式 */
.create-button,
.remove-button,
.submit-button {
  padding: 10px 20px;
  background-color: #007BFF;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 16px;
  transition: background-color 0.3s, transform 0.2s;
  margin: 5px; /* 保持间距 */
}

.create-button:hover,
.remove-button:hover,
.submit-button:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
}

.create-button:active,
.remove-button:active,
.submit-button:active {
  transform: translateY(0);
  background-color: #003f80;
  transition: background-color 0.1s, transform 0.1s;
}

/* 表格样式 */
.exam-table,
.student-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}

.exam-table th,
.exam-table td,
.student-table th,
.student-table td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: left;
  font-size: 16px;
}

.exam-table th,
.student-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.totals {
  margin-top: 10px;
  font-weight: bold;
  color: #333;
}

/* 提交按钮的区域 */
.submit-section {
  text-align: center;
  margin-top: 30px;
}
</style>