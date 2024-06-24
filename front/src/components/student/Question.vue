<template>
  <div>
    <Navbar />
    <div class="container">
      <h1>题目列表</h1>
      <div class="search-bar">
        <div class="search-input-group">
          <el-input
            placeholder="搜索标题..."
            v-model="searchQuery"
            class="search-input"
            size="medium"
          />
          <el-button
            type="primary"
            @click="handleSearch"
            class="search-button"
          >
            搜索
          </el-button>
        </div>
        <el-select
          v-model="filterType"
          placeholder="状态"
          size="medium"
          class="filter-select"
        >
          <el-option label="全部" value="all" />
          <el-option label="已完成" value="completed" />
          <el-option label="未完成" value="uncompleted" />
        </el-select>
        <el-button
          type="primary"
          @click="randomQuestion"
          class="random-button"
        >
          随机一题
        </el-button>
      </div>
      <el-table
        :data="filteredQuestions.slice((currentPage - 1) * pageSize, currentPage * pageSize)"
        style="width: 100%"
        border
        stripe
      >
        <el-table-column prop="id" label="ID" width="100" align="center" />
        <el-table-column prop="title" label="标题" align="center" />
        <el-table-column prop="difficulty" label="难度" width="120" align="center">
          <template slot-scope="scope">
            <span :style="{ color: getColor(scope.row.difficulty) }">{{ getDifficultyLabel(scope.row.difficulty) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" align="center">
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
        :total="filteredQuestions.length"
      />
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
      searchQuery: '',
      filterType: 'all' // 默认显示全部
    }
  },
  mounted() {
    this.fetchQuestions();
  },
  computed: {
    filteredQuestions() {
      return this.questions.filter(question => 
        this.filterQuestion(question)
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
    filterQuestion(question) {
      if (this.filterType === 'all') {
        return question.title.toLowerCase().includes(this.searchQuery.toLowerCase());
      } else if (this.filterType === 'completed') {
        return question.completed && question.title.toLowerCase().includes(this.searchQuery.toLowerCase());
      } else if (this.filterType === 'uncompleted') {
        return !question.completed && question.title.toLowerCase().includes(this.searchQuery.toLowerCase());
      }
      return true; // 默认情况
    },
    enterQuestion(id) {
      this.$router.push({ name: 'answer-question', params: { id: id } });
    },
    handlePageChange(newPage) {
      this.currentPage = newPage;
    },
    handleSearch() {
      // Placeholder for potentially updating list or analytics
    },
    randomQuestion() {
      // Placeholder for random question functionality
      alert("随机一题功能尚未实现！");
    },
    getDifficultyLabel(difficulty) {
      switch (difficulty) {
        case 1: return '简单';
        case 2: return '中等';
        case 3: return '困难';
        case 4: return '挑战';
        case 5: return '地狱';
        default: return '未知';
      }
    },
    getColor(difficulty) {
      switch (difficulty) {
        case 1: return 'green';
        case 2: return 'blue';
        case 3: return 'orange';
        case 4: return 'purple';
        case 5: return 'red';
        default: return 'black';
      }
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
  justify-content: center;
  margin-bottom: 20px;
}
.search-input-group {
  display: flex;
  align-items: center;
}
.search-input {
  max-width: 300px;
  margin-right: 10px;
}
.search-button {
  margin-left: 10px;
}
.filter-select {
  width: 120px;
  margin-left: 10px;
}
.random-button {
  margin-left: 10px;
}
</style>
