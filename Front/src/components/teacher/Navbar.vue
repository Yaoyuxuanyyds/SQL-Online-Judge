<template>
    <nav class="navbar">
      <router-link :to="{ path: '/teacher' }" :class="{ active: isActive('/teacher') }">Home</router-link>
      <router-link :to="{ path: '/teacher/question_create' }" :class="{ active: isActive('/teacher/question_create') }">Create Questions</router-link>
      <router-link :to="{ path: '/teacher/contest_create' }" :class="{ active: isActive('/teacher/contest_create') }">Create Contest</router-link>
      <router-link :to="{ path: '/teacher/question' }" :class="{ active: isActive('/teacher/question') }">Questions</router-link>
      <router-link :to="{ path: '/teacher/contest' }" :class="{ active: isActive('/teacher/contest') }">Contest</router-link>
      <router-link :to="{ path: '/teacher/submit' }" :class="{ active: isActive('/teacher/submit') }">Submit</router-link>
      <router-link :to="{ path: '/community' }" :class="{ active: isActive('/teacher/community') }">Community</router-link>
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
  