<template>
  <div>
    <Navbar />
    <div class="community-page">
      <div class="page-header">
        <h1>社群分享</h1>
      </div>
      <div class="controls">
        <input type="text" v-model="searchKeyword" class="form-control search-field" placeholder="搜索文章...">
        <button type="button" @click="goToEditor" class="btn btn-create">
          创建新文章
        </button>
      </div>
      <div class="article-list">
        <div v-for="article in filteredArticles" :key="article.id" class="article-item" @click="goToArticle(article.id)">
          <div class="article-header">
            <h2 class="article-title">{{ article.title }}</h2>
            <div class="article-info">
              <span class="article-user-id"><i class="fas fa-user"></i> 作者: {{ article.user_id }}</span>
              <span class="article-question-id"><i class="fas fa-question-circle"></i> 问题ID: {{ article.question_id }}</span>
            </div>
          </div>
          <hr class="article-divider">
          <div class="article-content">
            <p>{{ articleExcerpt(article.content) }}</p>
            <span class="article-time"><i class="fas fa-clock"></i> {{ formatDate(article.publish_time) }}</span>
          </div>
        </div>
        <div v-if="filteredArticles.length === 0" class="no-results">
          没有找到匹配的文章。
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';
import axios from 'axios';

export default {
  name: 'Community',
  components: {
    Navbar
  },
  data() {
    return {
      articles: [],
      searchKeyword: '' // 添加搜索关键词属性
    };
  },
  created() {
    this.fetchArticles();
  },
  computed: {
    filteredArticles() {
      if (!this.searchKeyword.trim()) {
        return this.articles; // 如果搜索关键词为空，则返回所有文章
      }
      const keyword = this.searchKeyword.trim().toLowerCase();
      return this.articles.filter(article =>
        article.title.toLowerCase().includes(keyword) // 根据文章标题进行关键词匹配
      );
    }
  },
  methods: {
    fetchArticles() {
      axios.get('/api/communitylist', {
        headers: {
          'session': localStorage.getItem('session')
        }
      })
        .then(response => {
          this.articles = response.data;
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
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

body {
  font-family: 'Roboto', sans-serif;
}

.community-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
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
  margin-bottom: 30px;
}

.search-field {
  width: 100%;
  max-width: 600px;
  padding: 15px;
  font-size: 1.1rem;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
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
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  width: 100%;
  max-width: 1400px;
}

.article-item {
  border: 1px solid #dee2e6;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.article-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.article-header {
  margin-bottom: 15px;
  text-align: center;
}

.article-title {
  font-size: 1.5rem;
  color: #007bff;
  font-weight: bold;
  margin-bottom: 10px;
}

.article-info {
  display: flex;
  justify-content: center; /* Center-align the info within the container */
  gap: 20px;
  font-size: 1.1rem;
  color: #666;
}

.article-divider {
  border: 0;
  border-top: 1px solid #eee;
  margin: 15px 0;
}

.article-content p {
  margin: 0 0 15px;
  color: #333;
  line-height: 1.6;
}

.article-time {
  font-size: 0.85rem;
  color: #999;
  text-align: right;
}
</style>
