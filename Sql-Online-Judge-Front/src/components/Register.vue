<template>
  <div id="app">
    <header>
      <img src="@/assets/logo.png">
    </header>
    <main>
      <h1>用户注册</h1>
      <form @submit.prevent="register">
        <div>
          <label for="id">ID：</label>
          <input type="text" v-model="id" required>
        </div>
        <div>
          <label for="username">用户名：</label>
          <input type="text" v-model="username" required>
        </div>
        <div>
          <label for="password">密码：</label>
          <input type="password" v-model="password" required>
        </div>
        <button type="submit">注册</button>
      </form>
    </main>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Register',
  data() {
    return {
      id: '',
      username: '',
      password: ''
    };
  },
  methods: {
    async register() {
      await axios.post('/api/register', {
          id: this.id,
          username: this.username,
          password: this.password,
      });
      //console.log(response.data);
      this.$router.push('/home');
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
