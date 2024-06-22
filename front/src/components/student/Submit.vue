<template>

  <div>
    <Navbar />
    <h1>Submissions</h1>
    <button @click="fetchAll">All Submissions</button>
    <button @click="fetchMine">My Submissions</button>
    <div v-for="item in submissions" :key="item.id">
      <SubmissionRecord :record="item"/>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/student/Navbar.vue';
import SubmissionRecord from './SubmissionRecord.vue';
// 
export default {
  name: 'Submit',
  components: {
    Navbar,
    SubmissionRecord
  },
  data() {
    return {
      submissions: [],
      // 默认或测试数据，实际中应当通过API获取
    };
  },
  methods: {
    fetchAll() {
      // 模拟API调用
      this.submissions = [
        { id: 1, submissionTime: '2024-06-22T12:00:00.000Z', problemId: 101, submissionContent: 'SELECT * FROM users;', result: 'Accepted' },
        { id: 2, submissionTime: '2024-06-21T14:20:00.000Z', problemId: 102, submissionContent: 'SELECT name FROM users WHERE id = 1;', result: 'Wrong Answer' }
      ].sort((a, b) => new Date(b.submissionTime) - new Date(a.submissionTime));
    },
    fetchMine() {
      // 模拟
      this.submissions = [
        { id: 3, submissionTime: '2024-06-20T09:34:00.000Z', problemId: 103, submissionContent: 'SELECT * FROM orders WHERE order_id = 10;', result: 'Accepted' }
      ].sort((a, b) => new Date(b.submissionotionTime) - new Date(a.submissionTime));
    }
  }
};
</script>

<style scoped>
h1 {
  color: #2c3e50;
}
button {
  margin: 10px;
  padding: 5px 15px;
}
</style>