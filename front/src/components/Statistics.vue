<template>
    <div>
      <Navbar />
      <div class="container">
        <h1 class="title">学生成绩</h1>
        <button @click="goBack" class="back-button">返回</button>
        <table class="el-table">
          <thead>
            <tr>
              <th>学生ID</th>
              <th>分数</th>
              <th>排名</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in studentScores" :key="student.id">
              <td>{{ student.id }}</td>
              <td>{{ student.score }}</td>
              <td>{{ student.rank }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import Navbar from '@/components/Navbar.vue';
  
  export default {
    name: 'ContestScores',
    components: {
      Navbar
    },
    data() {
      return {
        studentScores: []
      };
    },
    created() {
      this.fetchStudentScores();
    },
    methods: {
      fetchStudentScores() {
        const contestId = this.$route.params.id;
        axios.get(`/api/contest-scores`, {
          headers: {
            'session': localStorage.getItem('session')
          },
          params: {
            contest_id: contestId
          }
        })
        .then(response => {
          this.studentScores = response.data;
        })
        .catch(error => {
          alert("获取学生成绩时发生错误！", error);
        });
      },
      goBack() {
        this.$router.push({ name: 'contest' });
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
  
  .back-button {
    display: block;
    margin: 0 auto 20px;
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .back-button:hover {
    background-color: #0056b3;
  }
  
  .el-table {
    width: 100%;
    border-collapse: collapse;
    background-color: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }
  
  th, td {
    padding: 12px 15px;
    text-align: left;
  }
  
  th {
    background-color: #f2f2f2;
    color: #333;
    font-weight: bold;
    text-align: center;
  }
  
  td {
    text-align: center;
  }
  
  tr:nth-child(even) {
    background-color: #f9f9f9;
  }
  </style>
  