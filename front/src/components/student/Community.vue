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

    <ul class="article-list">
      <li v-for="article in articles" :key="article.id" class="article-item">
        <span class="article-id">{{ article.id }}</span>
        <span class="article-title">{{ article.user_id }}</span>
        <span class="article-content">{{ article.question_id }}</span>
        <span class="article-time">{{ formatDate(article.publish_time) }}</span>
        <span class="article-notice">{{ article.is_notice ? '是' : '否' }}</span>
      </li>
    </ul>
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
    };
  },
  created() {
    this.fetchArticles();
  },
  methods: {
    fetchArticles() {
      axios.get('/api/communitylist', {
        headers: {
          'session': localStorage.getItem('session')
        }
      })
        .then(response => {
          this.articles = response.data.data;
          // console.log(response.data.data);
        })
        .catch(error => {
          // console.error('Error fetching articles:', error);
          this.$emit('error', error);
        });
    },
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    }
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
}
.article-list {
  list-style: none;
  padding: 0;
}
.article-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 1px solid #e1e1e1;
  background-color: #f9f9f9;
  margin-bottom: 10px;
  padding: 10px;
}
.article-item:hover {
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
