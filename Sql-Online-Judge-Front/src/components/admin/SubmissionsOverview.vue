<template>
    <div>
      <h1>Submissions Overview</h1>
      <ul>
        <li v-for="submission in submissions" :key="submission.id">
          {{ submission.author }}: {{ submission.score }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SubmissionsOverview',
    data() {
      return {
        submissions: []
      };
    },
    methods: {
      fetchSubmissions() {
        // Assuming an API call to fetch submissions
        this.submissions = [{ id: 1, author: 'John Doe', score: 95 }]; // Example data
      }
    },
    mounted() {
      this.fetchSubmissions();
    }
  }
  </script>
  
  <style scoped>
  /* Add your CSS styling here */
  </style>