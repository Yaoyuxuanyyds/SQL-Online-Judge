<template>
  <div>
    <Navbar />
    <div class="community-page">
<div class="page-header">
  <h1>社群分享</h1>
</div>
<div class="controls">
  <input type="text" class="form-control search-field" placeholder="搜索文章...">
  <button type="button" @click="goToEditor" class="btn btn-create">
    创建新文章
  </button>
</div>
<div class="article-list">
  <div v-for="article in articles" :key="article.id" class="article-item shadow" @click="goToArticle(article.id)">
    <div class="article-header">
      <span class="article-id">{{ article.id }}</span>
      <span class="article-title">{{ article.title }}</span>
      <div class="article-info">
        <span class="article-user-id">作者ID: {{ article.user_id }}</span>
        <span class="article-question-id">问题ID: {{ article.question_id }}</span>
      </div>
    </div>
    <div class="article-content">
      <p>{{ articleExcerpt(article.content) }}</p>
      <span class="article-time">{{ formatDate(article.publish_time) }}</span>
    </div>
  </div>
</div>
</div>
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
        })
        .catch(error => {
          alert(`失败: ${error.response.data.message}`);
        });
    },
    formatDate(date) {
      return new Date(date).toLocaleString();
    },
    articleExcerpt(content) {
      return content.length > 100 ? content.substring(0, 100) + '...' : content;
    },
    goToEditor() {
      this.$router.push({ name: 'article-editor' });
    },
    goToArticle(articleId) {
    this.$router.push({ name: 'article-details', params: { id: articleId } });
  }
    
  }
}
</script>

<style scoped>
.community-page {
  display: flex;
  flex-direction: column;
}
.page-header {
  margin-bottom: 20px;
}
h1 {
  color: #333;
  font-weight: bold;
  margin-bottom: 20px;
}
.controls {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}
.search-field {
  width: 100%;
  max-width: 600px;
  padding: 10px;
  font-size: 1.1rem;
  margin-bottom: 15px;
}
.btn-create {
  padding: 10px 20px;
  font-size: 1.1rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.btn-create:hover {
  background-color: #218838;
}
.article-list {
  display: flex;
  flex-direction: column;
}
.article-item {
  border: 1px solid #dee2e6;
  margin-bottom: 10px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}
.article-item:hover {
  transform: translateY(-5px);
}
.article-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.article-id, .article-question-id {
  background-color: #007bff;
  color: #fff;
  padding: 8px 16px;
  border-radius: 50%;
  text-align: center;
}
.article-title {
  font-size: 1.5rem;
  margin: 0 15px;
  flex-grow: 1;
}
.article-info {
  display: flex;
  align-items: center;
}
.article-user-id, .article-question-id {
  margin-left: 10px;
}
.article-content p {
  margin: 10px 0 5px;
}
.article-time {
  font-size: 0.85rem;
  color: #666;
}
</style>
