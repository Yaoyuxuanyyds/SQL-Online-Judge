<template>
  <div>
    <Navbar />
    <div class="container">
    <h1>题目列表</h1>
    <div class="search-bar">
      <el-input
        placeholder="搜索标题..."
        v-model="searchQuery"
        class="search-input"
      />
      <el-button
        type="primary"
        @click="handleSearch"
        class="search-button">搜索</el-button>
    </div>
    <el-table
      :data="filteredQuestions.slice((currentPage-1) * pageSize, currentPage * pageSize)"
      style="width: 100%" 
      border
      stripe>
      <el-table-column prop="id" label="ID" width="180"/>
      <el-table-column prop="title" label="标题"/>
      <el-table-column prop="difficulty" label="难度" width="120"/>
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button @click="enterQuestion(scope.row.id)" type="success" size="small">进入</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      @current-change="handlePageChange"
      :current-page="currentPage"
      :page-size="pageSize"
      :page-sizes="[5, 10, 20, 30]"
      layout="total, sizes, prev, pager, next, jumper"
      :total="filteredQuestions.length">
    </el-pagination>
  </div>
  </div>
  
</template>

<script>
import Navbar from '@/components/student/Navbar.vue';
import axios from 'axios';

export default {
  name: 'QuestionList',
  components: {
    Navbar
  },
  data() {
    return {
      questions: [],
      currentPage: 1,
      pageSize: 20,
      searchQuery: ''
    }
  },
  mounted() {
    this.fetchQuestions();
  },
  computed: {
    filteredQuestions() {
      return this.questions.filter(question => 
        question.title.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
    fetchQuestions() {
      axios.get(`/api/questionlist`, {
        headers: {
          'session': localStorage.getItem('session')
        }
      })
      .then(response => {
        this.questions = response.data.data;
      })
      .catch(error => {
        alert("Error fetching questions:", error);
      });
    },
    enterQuestion(id) {
      this.$router.push({ name: 'answer-question', params: { id: id } });
    },
    handlePageChange(newPage) {
      this.currentPage = newPage;
    },
    handleSearch() {
      // Placeholder for potentially updating list or analytics
    }
  }
}
</script>

<style scoped>
.container {
  padding: 20px;
}
.search-bar {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}
.search-input {
  flex: 1;
}
.search-button {
  margin-left: 10px; /* Spacing between input and button */
}
</style>