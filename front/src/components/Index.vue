<template>
  <div>
    <Navbar />
  <div class="home-container">
    <div class="left-column">
      <div class="card user-info">
        <h1>欢迎来到主页，<span class="highlight">{{ name }}</span></h1>
        <p><span class="highlight">{{ name }}</span>, 你已经完成{{ totalQuestions }}道题啦！</p>
        <div v-if="quote" class="daily-quote">每日一言：{{ quote }}</div>
        <div class="current-time">当前时间：{{ currentTime }}</div>
        <table>
          <tr>
            <td>昵称：</td>
            <td><span class="highlight">{{ name }}</span></td>
          </tr>
          <tr>
            <td>身份：</td>
            <td><span class="highlight">{{ roleMap[role] }}</span></td>
          </tr>
        </table>
      </div>
      <div class="card submissions">
        <h2>最近提交</h2>
        <el-table :data="submissions" style="width: 100%">
          <el-table-column prop="id" label="提交ID" width="100" align="center"></el-table-column>
          <el-table-column prop="question_id" label="题目ID" align="center"></el-table-column>
          <el-table-column prop="status" label="提交结果" align="center">
            <template slot-scope="scope">
              <span :style="{ color: getStatusColor(scope.row.status) }">{{ judgeResult(scope.row.status) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="pass_rate" label="通过率" align="center"></el-table-column>
          <el-table-column prop="submit_time" label="时间" align="center"></el-table-column>
        </el-table>
      </div>
    </div>
    <div class="right-column">
      <div class="card statistics">
        <h2>做题统计</h2>
        <div class="stat">
          <span class="tag">题目总数: {{ totalQuestions }}</span>
          <span class="tag">做过题数: {{ numberAnswered }}</span>
          <span class="tag">通过题数: {{ pass_count }}</span>
          <span class="tag">通过率: {{ correctRate }}%</span>
          <span class="tag">发表文章数: {{ articlesCount }}</span>
        </div>
      </div>
      <div class="card chart">
        <h2>提交结果</h2>
        <PieChart ref="pieChart" :chart-data="chartData" />
      </div>
    </div>
  </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '@/components/Navbar.vue';
import { Pie } from 'vue-chartjs';

export default {
  components: {
    Navbar,
    PieChart: {
      extends: Pie,
      props: ['chartData'],
      mounted() {
      }
    }
  },
  data() {
    return {
      name: localStorage.getItem('userName'),
      role: localStorage.getItem('userRole'),
      roleMap: { '0': '学生', '1': '老师', '2': '管理员' },
      totalQuestions: 0,
      numberAnswered: 0,
      pass_count: 0,
      correctRate: 0,
      articlesCount: 0,
      currentTime: new Date().toLocaleString(),
      quote: '',
      submissions: [],
      chartData: {
        labels: ['Accepted', 'Wrong Answer', 'Runtime Error', 'Time Limit Exceeded', 'Memory Limit Exceeded'],
        datasets: [{
          label: 'Statistics',
          backgroundColor: ['#83b799', '#e7cfc9', '#c1beb0', '#f5b7b1', '#aed6f1'],
          data: [0, 0, 0, 0, 0]
        }]
      },
      quotes: [
        "程序员的世界里没有Bug，只有无限可能的Feature！",
        "代码如诗，写出来要让人赏心悦目。",
        "一天不写代码，手就会发痒。",
        "没有什么问题是重启解决不了的，如果有，那就再重启一次。",
        "代码是程序员与世界沟通的桥梁。"
      ]
    };
  },
  mounted() {
    this.fetchInfo();
    this.updateTime();
    this.getDailyQuote();
    setInterval(this.updateTime, 1000); // 每秒更新时间
  },
  watch: {
    chartData: {
      deep: true,
      handler() {
        this.$refs.pieChart.renderChart(this.chartData, {
        responsive: true,
        maintainAspectRatio: false
      });
      }
    }
  },
  methods: {
    fetchInfo() {
      axios.get('/api/questionlist', {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          student_id: localStorage.getItem('userID')
        }
      })
      .then(response => {
        this.totalQuestions = response.data.length;
      })
      .catch(error => {
        alert("获取题目列表失败: " + error);
      });

      axios.get('/api/submitlist', {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          fetchall: false,
          user_id: localStorage.getItem('userID')
        }
      })
      .then(response => {
        this.submissions = response.data.sort((a, b) => b.id - a.id);
      })
      .catch(error => {
        alert("获取提交列表失败: " + error);
      });

      // 获取做过的题目数
      axios.get('/api/answeredquestions', {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          student_id: localStorage.getItem('userID')
        }
      })
      .then(response => {
        this.numberAnswered = response.data.length;
      })
      .catch(error => {
        alert("获取做过的题目数失败: " + error);
      });

      // 获取发表文章数
      axios.get('/api/communitylist', {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          user_id: localStorage.getItem('userID')
        }
      })
      .then(response => {
        this.articlesCount = response.data.length;
      })
      .catch(error => {
        alert("获取发表文章数失败: " + error);
      });
      // 获取提交结果统计数据
      axios.get('/api/statuscount', {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          student_id: localStorage.getItem('userID')
        }
      })
      .then(response => {
        const { pass_count, status_count } = response.data;
        this.pass_count = pass_count;
        this.chartData.datasets[0].data = status_count;
        if (this.totalQuestions === 0) this.correctRate = 0.0
        else this.correctRate = (this.pass_count / this.totalQuestions * 100.0).toFixed(2);
      })
      .catch(error => {
        alert("获取提交结果统计数据失败: " + error);
      });
    },
    updateTime() {
      this.currentTime = new Date().toLocaleString();
    },
    getDailyQuote() {
      const randomIndex = Math.floor(Math.random() * this.quotes.length);
      this.quote = this.quotes[randomIndex];
    },
    getStatusColor(status) {
      const colorMapping = {
        0: 'green',
        1: 'red',
        2: 'orange',
        3: 'purple',
        4: 'blue'
      };
      return colorMapping[status] || 'black';
    },
    judgeResult(status) {
      const mapping = {
        0: 'Accepted',
        1: 'Runtime Error',
        2: 'Wrong Answer',
        3: 'Time Limit Exceeded',
        4: 'Memory Limit Exceeded'
      };
      return mapping[status] || 'Unknown';
    }
  }
};
</script>

<style scoped>
.home-container {
  display: flex;
  justify-content: space-between;
}
.left-column {
  width: 70%;
}
.right-column {
  width: 25%;
}
.card {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}
.highlight {
  color: #4A90E2;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  text-shadow: 1px 1px 1px #aaa;
}
.daily-quote {
  font-size: 1.2em;
  margin-top: 10px;
}
.current-time {
  margin-top: 10px;
}
.stat {
  display: flex;
  flex-wrap: wrap;
}
.tag {
  background-color: #e8eaf6;
  color: #4A90E2;
  padding: 5px 10px;
  margin: 5px;
  border-radius: 5px;
  font-size: 0.9em;
}
</style>
