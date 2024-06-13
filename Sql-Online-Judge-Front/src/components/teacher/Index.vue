<template>
    <div id="app">
      <header>
        <img src="@/assets/logo.png">
        <nav>
          <router-link to="/">Home</router-link>
          <router-link to="/question">Questions</router-link>
          <router-link to="/statistics">Statistics</router-link>
          <router-link to="/submit">Submit</router-link>
          <!-- 新增的导航栏选项 -->
          <router-link to="/teacher/import">Import Questions</router-link>
          <router-link to="/teacher/create-exam">Create Exam</router-link>
        </nav>
      </header>
      <router-view/>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Index',
    data() {
      return {
        //
      };
    },
    methods: {
      //
    }
  };
  </script>
  
  <style scoped>
  nav {
    display: flex;
    justify-content: space-around;
  }
  
  nav a {
    text-decoration: none;
    color: #333;
  }
  
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    background-color: #f5f5f5;
  }
  
  img {
    height: 40px;
  }
  
  #app {
    font-family: 'Unifont', 'Source Code Pro', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
  </style>
  