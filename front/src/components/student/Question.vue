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
          size="medium"
          clearable
        />
        <span class="search-tip">输入标题关键词进行搜索</span>
        <el-select
          v-model="filterType"
          placeholder="按难度筛选"
          size="medium"
          class="filter-select"
          @change="filterQuestions"
        >
          <el-option label="全部" value="all" />
          <el-option label="简单" value="1" />
          <el-option label="中等" value="2" />
          <el-option label="困难" value="3" />
          <el-option label="挑战" value="4" />
          <el-option label="地狱" value="5" />
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
            <span :class="getDifficultyClass(scope.row.difficulty)">{{ getDifficultyLabel(scope.row.difficulty) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="completed" label="是否完成" width="120" align="center">
          <template slot-scope="scope">
            <span :class="scope.row.completed ? 'completed-true' : 'completed-false'">{{ scope.row.completed ? '已完成' : '未完成' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="accuracy" label="准确率" width="120" align="center">
          <template slot-scope="scope">
            {{ scope.row.accuracy }}%
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
      filterType: 'all', // 默认显示全部
      randomMode: false,
      randomQuestionId: null,
      userId: localStorage.getItem('userId'), // Assuming userId is stored in localStorage
    }
  },
  mounted() {
    this.fetchQuestions();
  },
  computed: {
    filteredQuestions() {
      if (this.randomMode) {
        return this.questions.filter(question => question.id === this.randomQuestionId);
      }
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
        },
        params: {
          userId: this.userId
        }
      })
      .then(response => {
        // 假设后端返回的数据结构包含了 accuracy 和 completed 字段
        this.questions = response.data.map(question => ({
          ...question
        }));
      })
      .catch(error => {
        alert("获取题目列表失败:", error);
      });
    },
    filterQuestion(question) {
      const matchesSearch = question.title.toLowerCase().includes(this.searchQuery.toLowerCase());
      if (this.filterType === 'all') {
        return matchesSearch;
      } else {
        return question.difficulty == this.filterType && matchesSearch;
      }
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
      const randomIndex = Math.floor(Math.random() * this.questions.length);
      this.randomQuestionId = this.questions[randomIndex].id;
      this.randomMode = true;
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
    getDifficultyClass(difficulty) {
      return {
        'difficulty-easy': difficulty === 1,
        'difficulty-medium': difficulty === 2,
        'difficulty-hard': difficulty === 3,
        'difficulty-challenge': difficulty === 4,
        'difficulty-hell': difficulty === 5,
      };
    }
  }
}
</script>

<style scoped>
.container {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  font-size: 24px;
  color: #333;
  margin: 0;
  padding: 20px 0;
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

.search-tip {
  margin-left: 10px;
  color: #666;
}

.filter-select {
  width: 150px;
  margin-left: 20px;
}

.random-button {
  margin-left: 20px;
}

.el-table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

th, td {
  padding: 12px 15px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
  color: #333;
  font-weight: bold;
  text-align: center;
}

td {
  text-align: center;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
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

button:hover {
  background-color: #0056b3;
}

.difficulty-easy {
  background-color: green;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.difficulty-medium {
  background-color: blue;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.difficulty-hard {
  background-color: orange;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.difficulty-challenge {
  background-color: purple;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.difficulty-hell {
  background-color: red;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.completed-true {
  background-color: green;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.completed-false {
  background-color: red;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}
</style>
