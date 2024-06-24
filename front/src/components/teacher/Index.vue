<template>
  <div>
    <Navbar />
    <div class="teacher-home-page">
      <div class="greeting-container">
        <h1 class="animated-greeting">{{ nickname }}, 您好！</h1>
        <p v-if="isMorning">早上好，希望您度过美好的一天！</p>
        <p v-else-if="isAfternoon">下午好，继续保持良好的状态！</p>
        <p v-else>晚上好，注意休息！</p>
      </div>
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
      nickname: 'TeacherNickname', // 假设教师昵称为固定值
    };
  },
  computed: {
    isMorning() {
      const hour = new Date().getHours();
      return hour < 12;
    },
    isAfternoon() {
      const hour = new Date().getHours();
      return hour >= 12 && hour < 18;
    }
  }
};
</script>

<style>
/* 使用莫兰迪色系和一些科技元素的改动 */
.teacher-home-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #d3d0cb 0%, #afbdc4 100%);
  text-align: center;
  animation: gradientShift 5s infinite;
}

.greeting-container {
  background-color: rgba(245, 244, 240, 0.95);
  padding: 50px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  animation: fadeIn 2s ease-in-out;
  border: 1px solid #bcc1c7;
  position: relative;
  overflow: hidden;
}

.animated-greeting {
  font-size: 2.5rem;
  color: #53565a;
  text-shadow: 0 0 8px rgba(83, 86, 90, 0.3);
  animation: slideIn 1.5s ease-out, textGlow 2s infinite alternate;
}

.greeting-container::before, .greeting-container::after {
  content: '';
  position: absolute;
  height: 3px;
  background: linear-gradient(90deg, rgba(68,138,202,1) 0%, rgba(128,182,234,1) 100%);
  animation: animateLine 3s linear infinite;
  border-radius: 1.5px;
}

.greeting-container::before {
  top: 0;
  left: -100%;
  right: -100%;
}

.greeting-container::after {
  bottom: 0;
  left: -100%;
  right: -100%;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes textGlow {
  from {
    text-shadow: 0 0 8px rgba(83, 86, 90, 0.3);
  }
  to {
    text-shadow: 0 0 24px rgba(83, 86, 90, 0.7);
  }
}

@keyframes animateLine {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

@keyframes gradientShift {
  0%, 100% {
    background: linear-gradient(135deg, #d3d0cb 0%, #afbdc4 100%);
  }
  50% {
    background: linear-gradient(135deg, #afbdc4 0%, #d3d0cb 100%);
  }
}
</style>