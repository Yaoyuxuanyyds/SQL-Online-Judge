<template>
    <div>
      <h1>Forum Management</h1>
      <div v-for="post in posts" :key="post.id">
        <h3>{{ post.title }}</h3>
        <p>{{ post.content }}</p>
        <button @click="deletePost(post.id)">Delete Post</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ForumManagement',
    data() {
      return {
        posts: []
      };
    },
    methods: {
      fetchPosts() {
        // Placeholder for API call to fetch posts
        this.posts = [{ id: 1, title: 'How to learn Vue?', content: 'Content of the post' }]; // Example data
      },
      deletePost(id) {
        // Placeholder for API call to delete a post
        alert('Delete function triggered');
      }
    },
    mounted() {
      this.fetchPosts();
    }
  }
  </script>
  
  <style scoped>
  /* Add your CSS styling here */
  </style>