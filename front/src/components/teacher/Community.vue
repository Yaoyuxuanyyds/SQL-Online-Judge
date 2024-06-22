<template>
  <div>

    <meta charset="UTF-8">
    <title>Community</title>
    <!-- Bootstrap for styling -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <div class="container mt-5">
      <Navbar />

      <h2>社群分享</h2>
      <div class="mb-3">
        <button type="button" @click="goToEditor" class="btn btn-primary mb-3">
          写新文章
        </button>
        <input type="text" class="form-control mb-2" id="search-field" placeholder="搜索文章...">
        <div class="btn-group">
          <button class="btn btn-outline-secondary" @click="filterArticles('all')">所有文章</button>
          <button class="btn btn-outline-secondary" @click="filterArticles('mine')">我的文章</button>
        </div>
        <select class="form-select w-auto" @change="changeEntries($event)">
          <option value="5">显示 5 条</option>
          <option value="10" selected>显示 10 条</option>
          <option value="20">显示 20 条</option>
        </select>
      </div>
      <ul class="list-group">
        <li class="list-group-item" v-for="article in articles" :key="article.id">
          #{{ article.id }} - <strong>{{ article.author }}</strong> 分享于 {{ article.date }}
          <a :href="article.url" target="_blank">{{ article.title }}</a>
          <span class="float-end">
            <button class="btn btn-outline-primary" @click="likeArticle(article.id)">点赞 {{ article.likes }}</button>
            浏览量：{{ article.views }}
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/teacher/Navbar.vue';
export default {
  name: 'Community',
  components: {
    Navbar
  },
  data() {
    return {
      articles: []  // 这个应根据实际数据结构初始化
    };
  },
  methods: {
    likeArticle(articleId) {
      // 实际情况下应发送一个axios或fetch请求去后端处理点赞
    },
    filterArticles(filter) {
      // 实际情况下应与后端交互，过滤数据
    },
    changeEntries(event) {
      // Change display entries, actual implementation needed with backend support
    },
    goToEditor() {
      window.location = 'editor.html';
    }
  }
};
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
