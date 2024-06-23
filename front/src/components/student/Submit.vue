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
import axios from 'axios';
export default {
  name: 'Submit',
  components: {
    Navbar,
    SubmissionRecord
  },
  data() {
    return {
      submissions: [],
    };
  },
  methods: {
    fetchAll() {
      axios.get('/api/submitlist', {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          fetchall: true
        }
      })
        .then(response => {
          this.submissions = response.data.data.sort((a, b) => new Date(b.submit_time) - new Date(a.submit_time));
        })
        .catch(error => {
          alert(`失败: ${error.response.data.message}`);
        });
    },
    fetchMine() {
      axios.get('/api/submitlist', {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          fetchall: false,
          student_id: localStorage.getItem('userID')
        }
      })
        .then(response => {
          this.submissions = response.data.data.sort((a, b) => new Date(b.submit_time) - new Date(a.submit_time));
        })
        .catch(error => {
          alert(`失败: ${error.response.data.message}`);
        });
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