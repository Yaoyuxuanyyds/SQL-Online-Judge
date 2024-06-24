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
            <span v-if="scope.row.difficulty === 'easy'" style="color: green;">简单</span>
            <span v-else-if="scope.row.difficulty === 'medium'" style="color: orange;">中等</span>
            <span v-else-if="scope.row.difficulty === 'hard'" style="color: red;">困难</span>
          </template>
        </el-table-column>
        <el-table-column prop="accuracy" label="准确率" width="120" align="center">
          <template slot-scope="scope">
            {{ scope.row.accuracy }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" align="center">
          <template #default="scope">
            <el-button @click="enterQuestion(scope.row.id)" type="success" size="small">进入</el-button>
            <el-tag style="margin-left: 10px;">进入答题</el-tag>
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
import Navbar from '@/components/teacher/Navbar.vue';
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
