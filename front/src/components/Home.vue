<template>
  <div id="app">
    <div class="background">
      <img src="@/assets/bk1.png" alt="Background">
    </div>
    <div class="overlay">
      <header>
        <img src="@/assets/logo.png" alt="Logo" class="logo">
        <div class="title">MYWW OJ 判题系统</div>
        <div class="buttons">
          <button @click="toggleForm('login')" class="btn">登录</button>
          <button @click="toggleForm('register')" class="btn">注册</button>
        </div>
      </header>
      <main>
        <h1>MYWW OJ</h1>
        <p class="typewriter">{{ typewriterText }}</p>
      </main>
    </div>
    <transition name="slide-fade">
      <div class="login-register" v-if="showForm">
        <form @submit.prevent="handleSubmit" class="form">
          <button type="button" class="back-btn" @click="showForm = false">&larr;</button>
          <h2>{{ isLogin ? '用户登录' : '用户注册' }}</h2>
          <input type="text" v-model="id" placeholder="id" required>
          <div v-if="!isLogin">
            <input type="text" v-model="username" placeholder="用户名" required>
          </div>
          <input type="password" v-model="password" placeholder="密码" required>
          <button type="submit" class="submit-btn">{{ isLogin ? '登录' : '注册' }}</button>
          <div class="switch-form">
            <button type="button" @click="toggleForm(isLogin ? 'register' : 'login')" class="switch-btn">
              {{ isLogin ? '没有账号？注册一个' : '已有账号？登录' }}
            </button>
          </div>
        </form>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      showForm: false,
      isLogin: true,
      id: '',
      username: '',
      password: '',
      typewriterText: '',
      fullText: '做最酷的OJ平台！',
      isTyping: true,
    };
  },
  methods: {
    typeWriterEffect() {
      let i = 0;
      const speed = 50;
      const typing = () => {
        if (i < this.fullText.length && this.isTyping) {
          this.typewriterText += this.fullText.charAt(i);
          i++;
          setTimeout(typing, speed);
        } else if (i >= this.fullText.length) {
          setTimeout(() => {
            this.isTyping = false;
            this.typewriterText = '';
            i = 0;
            this.isTyping = true;
            typing();
          }, 3000);
        }
      };
      typing();
    },
    toggleForm(formType) {
      this.isLogin = formType === 'login';
      this.showForm = true;
    },
    async handleSubmit() {
      if (this.isLogin) {
        try {
          const response = await axios.post('/api/login', {
            id: parseInt(this.id),
            password: this.password,
          });
          const userID = this.id;
          const userName = response.data.username;
          const userRole = response.data.role;
          const sessionToken = response.data.session; // 获取session token

          // 将session token存储在本地存储中
          localStorage.setItem('session', sessionToken); 
          // 设置用户角色
          localStorage.setItem('userRole', userRole);
          // 设置用户ID
          localStorage.setItem('userID', userID);
          // 设置用户名
          localStorage.setItem('userName', userName);

          if (userRole === 0) {
            alert(`登录成功！id: ${this.id}\n欢迎来做作业或打比赛！`)
            this.$router.push('/index');
          } else if (userRole === 1) {
            alert(`登录成功！id: ${this.id}\n老师您辛苦了！`)
            this.$router.push('/index');
          } else if (userRole === 2) {
            alert(`登录成功！id: ${this.id}\n管理员，您好！`)
            this.$router.push('/admin');
          } else {
            alert('用户身份无效，重新注册！');
          }
        } catch (error) {
          alert('登录失败：' + error.response.data.message);
        }
      } else {
        try {
          const response = await axios.post('/api/register', {
            id: parseInt(this.id),
            username: this.username,
            password: this.password,
          });
          alert(response.data.message);
          this.$router.push('/');
        } catch (error) {
          if (error.response && error.response.data && error.response.data.message) {
            alert(`注册失败：` + error.response.data.message);
          } else {
            alert('注册失败！');
          }
        }
      }
    }
  },
  mounted() {
    this.typeWriterEffect();
  }
};
</script>

<style scoped>
#app {
  font-family: 'Noto Sans', 'Microsoft YaHei UI', 'Source Code Pro', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.background img {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: blur(0px);
  z-index: -1;
}

.overlay {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

header {
  position: fixed;
  top: 0;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: rgba(255, 255, 255, 0.8);
}

.logo {
  height: 40px;
}

.title {
  flex-grow: 1;
  text-align: center;
  font-size: 24px;
  font-weight: bold;
}

.buttons {
  display: flex;
  gap: 20px; /* 调整按钮之间的间距 */
}

.btn {
  padding: 15px 20px; /* 增加按钮的内边距 */
  border: none;
  border-radius: 10px;
  background-color: #2b8cd1;
  color: white;
  cursor: pointer;
  font-size: 18px; /* 增加字体大小 */
}

main {
  margin-top: 100px; /* 确保内容不会与 header 重叠 */
}

main h1 {
  font-size: 48px;
  margin-bottom: 20px;
  color: white; /* 改变字体颜色 */
}

main p {
  font-size: 24px;
  color: white; /* 改变字体颜色 */
}

.typewriter {
  display: inline-block; /* 确保元素是行内块级元素 */
  overflow: hidden;
  border-right: .15em solid orange;
  white-space: nowrap;
  margin: 0 auto;
  letter-spacing: .15em;
  animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite;
  font-size: 24px; /* 调整字体大小 */
  line-height: 1.5; /* 增加行高 */
}

.subtitle {
  font-size: 20px;
  line-height: 1.5;
  color: white;
  margin-top: 20px;
}

@keyframes typing {
  from { width: 0 }
  to { width: 100% }
}

@keyframes blink-caret {
  from, to { border-color: transparent }
  50% { border-color: orange; }
}

.login-register {
  position: fixed;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2; /* 确保在主文字层之上 */
}

.form {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 300px;
  position: relative;
}

.form h2 {
  margin-bottom: 20px;
}

.form input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.form .form-buttons {
  display: flex;
  gap: 10px;
}

.form .submit-btn {
  padding: 10px;
  width: 100%;
  border: none;
  border-radius: 5px;
  background-color: #2b8cd1;
  color: white;
  cursor: pointer;
}

.form .submit-btn:hover {
  background-color: #1a6ca7;
}

.form .switch-form {
  margin-top: 10px;
}

.form .switch-btn {
  padding: 10px;
  width: 100%;
  border: none;
  border-radius: 5px;
  background-color: #6c757d;
  color: white;
  cursor: pointer;
}

.form .switch-btn:hover {
  background-color: #5a6268;
}

.form .back-btn {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: #2b8cd1;
  color: white;
  border: none;
  border-radius: 80%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.slide-fade-enter-active, .slide-fade-leave-active {
  transition: all 0.5s ease;
}

.slide-fade-enter, .slide-fade-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

.logout-button {
  background-color: #ff4d4d;
  color: #fff;
  border: none;
  padding: 10px 20px;
  margin: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: transform 0.2s, background-color 0.2s;
}

.logout-button:hover {
  transform: translateY(-2px);
  background-color: #ff1a1a;
}
</style>
