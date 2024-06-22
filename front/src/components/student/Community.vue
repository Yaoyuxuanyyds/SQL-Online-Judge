<template>
  <div>
  
    <Navbar />
    <h2>社群分享</h2>
      <div class="mb-3">
        <button type="button" @click="goToEditor" class="btn btn-primary mb-3">
          写新文章
        </button>
        <input type="text" class="form-control mb-2" id="search-field" placeholder="搜索文章...">
      </div>

    <ul v-if="articles.length > 0">
      <li v-for="article in articles" :key="article.id">
        文章ID: {{ article.id }} - 用户ID: {{ article.user_id }} - 问题ID: {{ article.question_id }}
        <br>
        发布时间: {{ article.publish_time }} - 是否通知: {{ article.is_notice ? '是' : '否' }}
      </li>
    </ul>
    <p v-else>当前没有文章。</p>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '@/components/student/Navbar.vue';

export default {
  name: 'Community',
  components: {
    Navbar
  },
  data() {
    return {
      articles: []
    }
  },
  created() {
    this.fetchArticles();
  },
  methods: {
    fetchArticles() {
      axios.get('/api/community', {
        headers: {
          'session': localStorage.getItem('session')
        }
      })  
        .then(response => {
          this.articles = response.data.data;
        })
        .catch(error => {
          console.error('获取文章列表失败:', error);
        });
    }
  }
}
</script>

<style scoped>
.container {
  padding: 20px;
}
.list-group-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 1px solid #e1e1e1;
  background-color: #f9f9f9;
  margin-bottom: 10px;
}
.list-group-item a {
  color: #007bff; /* Bootstrap primary color */
}
.list-group-item:hover {
  background-color: #eef9f9;
}
.btn-primary {
  background-color: #007bff; /* Ensure consistency with Bootstrap colors */
}
h2 {
  text-align: center;
  color: #333;
}
</style>
