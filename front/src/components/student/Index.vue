<template>
  <div>
    <Navbar />
    <!-- 用户信息部分 -->
    <div class="user-info">
      <h1>欢迎来到主页，<span class="highlight">{{ nickname }}</span></h1>
      <p><span class="highlight">{{ nickname }}</span>, 你已经完成{{ totalQuestions }}道题啦！</p>
      <div :class="{ 'encouragement': true, 'alert': correctRate < 30 }" v-if="correctRate < 30">
        <span class="special-quote">山重水复疑无路，柳暗花明又一村！</span>
      </div>
      <div v-else-if="correctRate >= 31 && correctRate <= 60" :class="{ 'encouragement': true, 'notice': true }">
        <p>破釜沉舟，百二秦关终属楚！</p>
      </div>
      <div v-else-if="correctRate >= 61 && correctRate <= 85" :class="{ 'encouragement': true, 'progress': true }">
        <p>天生我材必有用，千金散尽还复来！</p>
      </div>
      <div v-else-if="correctRate >= 86 && correctRate <= 100" :class="{ 'encouragement': true, 'success': true }">
        <p>博观而约取，厚积而薄发！</p>
      </div>
      <table>
        <tr>
          <td>昵称：</td>
          <td><span class="highlight">{{ nickname }}</span></td>
        </tr>
        <tr>
          <td>个性签名：</td>
          <td><span class="highlight">{{ signature }}</span></td>
        </tr>
      </table>
      <!-- 显示统计数据为标签 -->
      <div class="stat" v-if="numberAnswered && totalQuestions">
        <span class="tag">做题数 / 总题数: {{ numberAnswered }} / {{ totalQuestions }}</span>
        <span class="tag">正确率: {{ correctRate }}%</span>
      </div>
    </div>
    <!-- 统计信息部分 —— 饼图 -->
    <PieChart :chart-data="chartData" />
  </div>
</template>

<script>
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
      nickname: 'YourNickname',
      signature: 'YourSignature',
      totalQuestions: 100,
      numberAnswered: 80, // 做过的题目总数
      correctRate: 75, // 正确率百分比
      chartData: {
        labels: ['Accepted', 'Wrong Answer', 'Complete Error'],
        datasets: [{
          label: 'Statistics',
          backgroundColor: ['#83b799', '#e7cfc9', '#c1beb0'], // 莫兰迪色
          data: [60, 15, 5] // 示例数据，实际应根据后端数据调整
        }]
      }
    };
  }
};
</script>

<style scoped>
.user-info {
  text-align: center; /* 居中文本 */
  margin: 20px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease-in-out;
}

.user-info:hover {
  transform: scale(1.02);
}

.highlight, .tag {
  color: #4A90E2; /* Royal blue for better visibility */
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  text-shadow: 1px 1px 1px #aaa; /* Slight shadow for depth */
}

.tag {
  display: inline-block;
  background-color: #e8eaf6; /* 莫兰迪灰色背景 */
  padding: 5px 10px;
  margin: 5px;
  border-radius: 5px;
  font-size: 0.9em;
}

.encouragement p {
  font-size: 1.1em;
}

.special-quote {
  font-size: 1.2em;
  font-family: 'Courier New', Courier, monospace;
}

.alert { background: linear-gradient(to right, #fcebeb, #ffcdd2); color: #b71c1c; }
.notice { background: linear-gradient to right, #fff3e0, #ffe0b2); color: #e65100; }
.progress { background: linear-gradient to right, #e1f5fe, #81d4fa); color: #01579b; }
.success { background: linear-gradient to right, #e8f5e9, #c8e6c9); color: #2e7d32; }
</style>