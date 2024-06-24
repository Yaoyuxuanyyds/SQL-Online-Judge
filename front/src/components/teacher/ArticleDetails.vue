<template>
  <div>
    <Navbar />
    <div class="article-detail-page">
      <div class="controls">
        <label for="font-size">字体大小:</label>
        <select id="font-size" @change="updateFontSize" v-model="selectedFontSize">
          <option value="0.8rem">小</option>
          <option value="1.2rem">中</option>
          <option value="1.5rem">大</option>
        </select>
        <button @click="toggleUnderline" :class="{ active: isUnderline }">下划线</button>
        <button @click="toggleHighlight" :class="{ active: isHighlight }">高亮</button>
      </div>
      <div class="article-container shadow" :style="{ fontSize: selectedFontSize }" ref="articleContent">
        <h1>{{ article.title }}</h1>
        <div class="article-metadata">
          <span class="author">作者ID: {{ article.user_id }}</span>
          <span class="publish-time">发布时间: {{ formatDate(article.publish_time) }}</span>
        </div>
        <div class="article-content">
          <p v-html="formattedContent"></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/student/Navbar.vue';
import axios from 'axios';

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
      selectedFontSize: '1.1rem',
      isUnderline: false,
      isHighlight: false
    };
  },
  mounted() {
    this.fetchArticleDetails();
  },
  computed: {
    formattedContent() {
      let content = this.article.content;
      if (this.isUnderline) {
        content = `<u>${content}</u>`;
      }
      if (this.isHighlight) {
        content = `<mark>${content}</mark>`;
      }
      return content;
    }
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
    updateFontSize() {
      this.$refs.articleContent.style.fontSize = this.selectedFontSize;
    },
    toggleUnderline() {
      this.isUnderline = !this.isUnderline;
    },
    toggleHighlight() {
      this.isHighlight = !this.isHighlight;
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
  background-color: #f7f7f7; /* 背景颜色 */
  min-height: 100vh; /* 保证页面至少占满整个视窗高度 */
}
.controls {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
  align-items: center;
}
#font-size {
  padding: 5px;
  border-radius: 3px;
  border: 1px solid #ccc;
}
button {
  padding: 5px 10px;
  border: none;
  border-radius: 3px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}
button.active {
  background-color: #0056b3;
}
button:hover {
  background-color: #0056b3;
}
.article-container {
  width: 50%; /* 占屏幕宽度的60% */
  background-color: #fff; /* 白色背景 */
  padding: 40px; /* 内部边距 */
  border-radius: 10px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1); /* 阴影效果 */
  margin-top: 20px; /* 顶部间距 */
  transition: transform 0.2s, box-shadow 0.2s; /* 动效 */
}
.article-container:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* 悬停效果 */
}
h1 {
  margin-bottom: 20px; /* 标题底部间距 */
  color: #333; /* 标题颜色 */
  font-size: 2rem; /* 标题字体大小 */
}
.article-metadata {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 20px;
}
.author, .publish-time {
  display: inline-block;
  background-color: #e9ecef; /* 标签背景色 */
  padding: 5px 10px;
  border-radius: 5px;
}
.article-content {
  font-size: 1.1rem;
  line-height: 1.8; /* 行间距 */
  text-align: justify; /* 对齐方式 */
  color: #444; /* 内容颜色 */
  margin-bottom: 20px; /* 内容底部间距 */
}
</style>
