<template>
    <nav class="navbar">
      <router-link :to="{ path: '/student' }" :class="{ active: isActive('/student') }">Home</router-link>
      <router-link :to="{ path: '/student/question' }" :class="{ active: isActive('/student/Question') }">Questions</router-link>
      <router-link :to="{ path: '/student/submit' }" :class="{ active: isActive('/student/Submit') }">Submit</router-link>
      <router-link :to="{ path: '/student/contest' }" :class="{ active: isActive('/student/Contest') }">Contest</router-link>
      <router-link :to="{ path: '/community' }" :class="{ active: isActive('/student/Community') }">Community</router-link>
    </nav>
  </template>
  
  <script>
  export default {
    name: 'Navbar',
    methods: {
      isActive(path) {
        return this.$route.path === path;
      }
    }
  };
  </script>
  
  <style scoped>
  .navbar {
    display: flex;
    justify-content: space-around;
    background-color: #f5f5f5;
    padding: 10px;
  }
  
  .navbar a {
    text-decoration: none;
    color: #333;
    padding: 10px;
    border-radius: 5px;
  }
  
  .navbar a.active {
    background-color: #333;
    color: #fff;
  }
  </style>
  