<template>
  <div :class="theme">
    <Navbar />
    <div class="article-detail-page">
      <div class="controls">
        <label for="theme-selector">选择主题颜色:</label>
        <select id="theme-selector" v-model="selectedTheme" @change="updateTheme">
          <option value="default">默认</option>
          <option value="black">黑色</option>
          <option value="white">白色</option>
          <option value="morandi">莫兰迪色</option>
          <option value="blue-black">蓝黑色系</option>
        </select>
      </div>
      <div class="article-container shadow">
        <h1 class="article-title">{{ article.title }}</h1>
        <div class="article-metadata">
          <span class="author">作者ID: {{ article.user_id }}</span>
          <span class="publish-time">发布时间: {{ formatDate(article.publish_time) }}</span>
        </div>
        <div class="article-content" v-html="parsedContent"></div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';
import axios from 'axios';
import marked from 'marked';

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
      },
      selectedTheme: 'default' // 默认主题
    };
  },
  mounted() {
    this.fetchArticleDetails();
  },
  methods: {
    fetchArticleDetails() {
      const articleId = this.$route.params.id;
      axios.get('/api/community', {
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
    },
    updateTheme() {
      this.theme = this.selectedTheme;
    }
  },
  computed: {
    theme() {
      return {
        default: 'theme-default',
        black: 'theme-black',
        white: 'theme-white',
        morandi: 'theme-morandi',
        'blue-black': 'theme-blue-black'
      }[this.selectedTheme];
    },
    parsedContent() {
      return marked(this.article.content);
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

body {
  font-family: 'Roboto', sans-serif;
}

.theme-default {
  background-color: #f7f7f7;
}

.theme-black {
  background-color: #000;
  color: #fff;
}

.theme-white {
  background-color: #fff;
  color: #000;
}

.theme-morandi {
  background-color: #d8c8c8;
  color: #383838;
}

.theme-blue-black {
  background-color: #1e1e2e;
  color: #b0c4de;
}

.article-detail-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  min-height: 100vh;
}

.controls {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
  align-items: center;
}

#theme-selector {
  padding: 5px;
  border-radius: 3px;
  border: 1px solid #ccc;
}

.article-container {
  width: 70%;
  max-width: 1200px;
  background-color: #fff;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.theme-black .article-container {
  background-color: #333;
  color: #fff;
}

.theme-white .article-container {
  background-color: #f9f9f9;
  color: #333;
}

.theme-morandi .article-container {
  background-color: #f2ede3;
  color: #383838;
}

.theme-blue-black .article-container {
  background-color: #26263a;
  color: #b0c4de;
}

.article-container:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.article-title {
  margin-bottom: 20px;
  color: inherit;
  font-size: 2.4rem;
  text-align: center;
  word-break: break-word; /* 关键词很长时可以换行 */
  line-height: 1.2; /* 行高设置，让换行时有足够空间 */
}

.article-metadata {
  display: flex;
  justify-content: space-between;
  font-size: 1rem;
  color: inherit;
  margin-bottom: 20px;
}

.author, .publish-time {
  display: inline-block;
  background-color: #e9ecef;
  padding: 5px 10px;
  border-radius: 5px;
}

.theme-black .author, .theme-black .publish-time,
.theme-blue-black .author, .theme-blue-black .publish-time {
  background-color: #444;
  color: #b0c4de;
}

.article-content {
  font-size: 1.1rem;
  line-height: 1.8;
  color: inherit;
  text-align: justify;
}

.article-content p {
  margin-bottom: 20px;
}

/* Markdown 内容的样式 */
.article-content h1,
.article-content h2,
.article-content h3,
.article-content h4,
.article-content h5,
.article-content h6 {
  margin-top: 20px;
  margin-bottom: 10px;
  font-weight: 500;
}

.article-content ul,
.article-content ol {
  margin-left: 20px;
}

.article-content blockquote {
  margin: 20px 0;
  padding: 10px 20px;
  background-color: #f5f5f5;
  border-left: 5px solid #ddd;
}

.article-content code {
  background-color: #f5f5f5;
  padding: 2px 4px;
  border-radius: 3px;
}

.article-content pre {
  background-color: #f5f5f5;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
}
</style>
