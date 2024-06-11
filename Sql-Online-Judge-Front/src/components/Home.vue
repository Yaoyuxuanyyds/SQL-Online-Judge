<template>
  <div id="app">
    <header>
      <img src="@/assets/logo.png">
    </header>
    <main>
      <h1>用户登录</h1>
      <form @submit.prevent="login">
        <div>
          <label for="id">ID：</label>
          <input type="text" v-model="id" required>
        </div>
        <div>
          <label for="password">密码：</label>
          <input type="password" v-model="password" required>
        </div>
        <button type="submit">登录</button>
      </form>
      <p>
        还没有账号？快去<router-link to="/register">注册</router-link>吧！
      </p>
    </main>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Home',
  data() {
    return {
      id: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('/api/login', {
          id: this.id,
          password: this.password
        });
        const userRole = response.data.role;
        if (userRole === 0) {
          this.$router.push('/student');
        } else if (userRole === 1) {
          this.$router.push('/teacher');
        } else if (userRole === 2) {
          this.$router.push('/admin');
        } else {
          alert('Invalid user role');
        }
      } catch (error) {
        alert('Login failed: ' + error.response.data.message);
      }
    }
  }
};
</script>

<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

header {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  background-color: #f5f5f5;
}

img {
  height: 40px;
}

main {
  padding: 20px;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

form div {
  margin-bottom: 10px;
}

label {
  margin-right: 10px;
}

input {
  padding: 5px;
  font-size: 16px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
}

p {
  margin-top: 20px;
}
</style>
