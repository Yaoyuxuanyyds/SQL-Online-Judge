<template>
  <div>
    <Navbar />
    <!-- 用户信息部分 -->
    <div class="user-info">
      <h1>欢迎来到主页，{{ nickname }}</h1>
      <p>{{ nickname }}, 你已经完成{{ totalQuestions }}道题啦！</p>
      <p v-if="correctRate < 30">万事开头难，再接再厉！</p>
      <p v-else-if="correctRate >= 31 && correctRate <= 60">还不错哦，继续加油！</p>
      <p v-else-if="correctRate >= 61 && correctRate <= 85">真棒！</p>
      <p v-else-if="correctRate >= 86 && correctRate <= 100">永远的神！</p>
      <table>
        <tr>
          <td>昵称：</td>
          <td>{{ nickname }}</td>
        </tr>
        <tr>
          <td>个性签名：</td>
          <td>{{ signature }}</td>
        </tr>
      </table>
    </div>

    <!-- 提交记录部分 -->
    <div class="commit-history">
      <h2>提交记录：</h2>
      <table>
        <thead>
          <tr>
            <th>提交信息</th>
            <th>时间戳</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="commit in commitHistory" :key="commit.id">
            <td>{{ commit.message }}</td>
            <td>{{ commit.timestamp }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/teacher/Navbar.vue';

export default {
  components: {
    Navbar
  },
  data() {
    return {
      nickname: 'YourNickname',
      signature: 'YourSignature',
      commitHistory: [
        { id: 1, message: 'Initial commit', timestamp: '2024-06-20' },
        { id: 2, message: 'Added Home.vue component', timestamp: '2024-06-21' },
        { id: 3, message: 'Updated Navbar.vue styling', timestamp: '2024-06-22' }
      ],
      totalQuestions: 100, // 总题目数量，这里假设为固定值
      correctRate: 60 // 初始的正确率，这里假设为固定值
    };
  }
};
</script>

<style>
.user-info {
  margin: 20px;
  padding: 20px;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
}

.commit-history {
  margin: 20px;
  padding: 20px;
  background-color: #f0f0f0;
  border: 1px solid #ccc;
}

.commit-history table {
  width: 100%;
  border-collapse: collapse;
}

.commit-history th, .commit-history td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

.commit-history th {
  background-color: #f2f2f2;
}
</style>

