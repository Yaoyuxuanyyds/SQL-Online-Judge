<template>
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
          <el-table-column prop="status" label="提交结果" align="center"></el-table-column>
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
          <span class="tag">通过题数: {{ passCount }}</span>
          <span class="tag">通过率: {{ correctRate }}%</span>
          <span class="tag">发表文章数: {{ articlesCount }}</span>
        </div>
      </div>
      <div class="card chart">
        <h2>提交结果</h2>
        <PieChart :chart-data="chartData" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '@/components/student/Navbar.vue';
import { Pie } from 'vue-chartjs';

export default {
  components: {
    Navbar,
    PieChart: {
      extends: Pie,
      props: ['chartData'],
      mounted() {
        this.renderChart(this.chartData, {
          responsive: true,
          maintainAspectRatio: false
        });
      }
    }
  },
  data() {
    return {
      name: localStorage.getItem('name'),
      role: localStorage.getItem('role'),
      roleMap: { '0': '学生', '1': '老师', '2': '管理员' },
      totalQuestions: 0,
      numberAnswered: 0,
      passCount: 0,
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
  methods: {
    fetchInfo() {
      const session = localStorage.getItem('session');
      const userId = localStorage.getItem('userID');
      axios.get('/api/questionlist', { headers: { session }, params: { student_id: userId } })
        .then(response => {
          this.totalQuestions = response.data.length;
        })
        .catch(error => {
          alert("获取题目列表失败: " + error);
        });

      axios.get('/api/submitlist', { headers: { session }, params: { fetchall: false, user_id: userId } })
        .then(response => {
          this.submissions = response.data.sort((a, b) => b.id - a.id);
          this.updateChartData(response.data);
        })
        .catch(error => {
          alert("获取提交列表失败: " + error);
        });

      axios.get('/api/answeredquestions', { headers: { session }, params: { student_id: userId } })
        .then(response => {
          this.numberAnswered = response.data.length;
        })
        .catch(error => {
          alert("获取做过的题目数失败: " + error);
        });

      axios.get('/api/passcount', { headers: { session }, params: { student_id: userId } })
        .then(response => {
          this.passCount = response.data.passCount;
          this.correctRate = ((this.passCount / this.totalQuestions) * 100).toFixed(2);
        })
        .catch(error => {
          alert("获取通过的题目数失败: " + error);
        });

      axios.get('/api/articlescount', { headers: { session }, params: { user_id: userId } })
        .then(response => {
          this.articlesCount = response.data.length;
        })
        .catch(error => {
          alert("获取发表文章数失败: " + error);
        });
    },
    updateTime() {
      this.currentTime = new Date().toLocaleString();
    },
    getDailyQuote() {
      const randomIndex = Math.floor(Math.random() * this.quotes.length);
      this.quote = this.quotes[randomIndex];
    },
    updateChartData(data) {
      const resultCounts = {
        'Accepted': 0,
        'Wrong Answer': 0,
        'Runtime Error': 0,
        'Time Limit Exceeded': 0,
        'Memory Limit Exceeded': 0
      };
      data.forEach(submission => {
        switch (submission.status) {
          case 0:
            resultCounts['Accepted']++;
            break;
          case 2:
            resultCounts['Wrong Answer']++;
            break;
          case 1:
            resultCounts['Runtime Error']++;
            break;
          case 3:
            resultCounts['Time Limit Exceeded']++;
            break;
          case 4:
            resultCounts['Memory Limit Exceeded']++;
            break;
        }
      });
      this.chartData.datasets[0].data = [
        resultCounts['Accepted'],
        resultCounts['Wrong Answer'],
        resultCounts['Runtime Error'],
        resultCounts['Time Limit Exceeded'],
        resultCounts['Memory Limit Exceeded']
      ];
    }
  }
};
</script>

<style scoped>
.home-container {
  display: flex;
  justify-content: space-between;
  padding: 20px;
}
.left-column, .right-column {
  width: 48%;
}
.card {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  padding: 20px;
}
.user-info {
  text-align: center;
}
.highlight {
  color: #4A90E2;
  font-weight: bold;
}
.tag {
  display: inline-block;
  background-color: #e8eaf6;
  padding: 5px 10px;
  margin: 5px;
  border-radius: 5px;
}
.daily-quote, .current-time {
  margin-top: 10px;
  font-size: 1.1em;
}
</style>