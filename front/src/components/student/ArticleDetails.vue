<template>
    <div>
        <Navbar />
<div class="article-detail-page">
<div class="article-container">
  <h1>{{ article.title }}</h1>
  <div class="article-metadata">
    <span>作者ID: {{ article.user_id }}</span>
    <span>发布时间: {{ formatDate(article.publish_time) }}</span>
  </div>
  <div class="article-content">
    <p>{{ article.content }}</p>
  </div></div></div></div>
  </template>

<script>
import axios from 'axios';
import Navbar from '@/components/student/Navbar.vue';

export default {
  name: 'ArticleDetail',
  components: {
    Navbar
  },
  data() {
    return {
      article: {
        id: null,
        title: '',
        content: '',
        user_id: '',
        publish_time: ''
      }
    };
  },
  mounted() {
    this.fetchArticleDetails();
  },
  methods: {
    fetchArticleDetails() {
      const articleId = this.$route.params.id;
      axios.get('/api/community/operate', {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          article_id: parseInt(articleId)
        }
      })
      .then(response => {
        this.article = response.data;
      })
      .catch(error => {
          alert(`失败: ${error.response.data.message}`);
        });
    },
    formatDate(date) {
      return new Date(date).toLocaleString();
    }
  }
}
</script>

<style scoped>
.article-detail-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}
.article-container {
  max-width: 800px;
  width: 100%;
}
.article-metadata {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 10px;
}
.article-content {
  font-size: 1.1rem;
  line-height: 1.6;
  text-align: justify;
}
h1 {
  margin-bottom: 10px;
}
</style>

