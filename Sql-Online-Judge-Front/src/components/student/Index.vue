<template>
  <div id="app">
    <header>
      <img src="@/assets/logo.png">
      <nav>
        <router-link to="/">Home</router-link>
        <router-link to="/student/question">Questions</router-link>
        <router-link to="/student/submit">Submit</router-link>
        <router-link to="/student/statistics">Statistics</router-link>
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
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
