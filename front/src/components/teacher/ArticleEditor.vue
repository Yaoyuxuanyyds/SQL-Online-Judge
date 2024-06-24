<template>
  <div>
      <Navbar />
      <div class="publish-article-page">
    <h1>发布新文章</h1>
    <form @submit.prevent="publishArticle">
      <div class="form-group">
        <label for="title">标题:</label>
        <input type="text" id="title" v-model="article.title" class="form-control">
      </div>
      <div class="form-group">
        <label for="content">内容:</label>
        <textarea id="content" v-model="article.content" class="form-control" rows="8"></textarea>
      </div>
      <div class="form-group">
        <label for="question_id">问题ID (可选):</label>
        <input type="number" id="question_id" v-model="article.question_id" class="form-control">
      </div>
      <button type="submit" class="btn btn-primary">发布文章</button>
    </form>
      </div>
  </div>
</template>

<script>
import Navbar from '@/components/teacher/Navbar.vue';
import axios from 'axios';
import moment from 'moment-timezone';
export default {
  name: 'PublishArticle',
  components: {
    Navbar
  },
  data() {
    return {
      article: {  // Define article as an object containing all fields
        title: '',
        content: '',
        question_id: null,
        is_notice: false
      }
    };
  },
  methods: {
    publishArticle() {
      // Construct the payload to include user_id and times
      
      const payload = {
        ...this.article,
        user_id: localStorage.getItem('userID'), // Fetch the user ID from local storage
        publish_time: new Date().toISOString(), // Set publish time to current time
        last_modify_time: new Date().toISOString() // Set last modify time to current time
      };

      // Make the axios post request
      axios.post('/api/community', payload, {
            headers: {
            'session': localStorage.getItem('session')
          }
        })
        .then(() => {
          alert('文章已发布');
          this.$router.push('/student/community'); // Redirect to community page or wherever appropriate
        })
        .catch(error => {
          alert('发布失败: ' + error.response.data.message);
        });
    }
  }
}
</script>


<style scoped>
.publish-article-page {
  display: flex;
flex-direction: column;
max-width: 1400px;
margin: 40px auto;
padding: 20px;
background-color: #f8f9fa;
border-radius: 10px;
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 1.1rem;
  color: #495057;
  margin-bottom: 5px;
}

.form-control {
  display: block;
  width: 100%;
  padding: 0.75rem 1.25rem;
  font-size: 1rem;
  line-height: 5;
  color: #495057;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid #ced4da;
  border-radius: 0.3rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:focus {
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.btn-primary {
  color: #fff;
  background-color: #007bff;
  border-color: #007bff;
  font-size: 1.1rem;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.15s ease;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #004085;
}

textarea.form-control {
  height: auto;
  min-height: 120px;
}
</style>

