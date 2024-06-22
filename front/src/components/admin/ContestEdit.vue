<template>
    <div>
      <h1>Edit Contest</h1>
      <form @submit.prevent="saveContest">
        <label for="name">Contest Name:</label>
        <input type="text" id="name" v-model="contest.name" />
  
        <label for="description">Description:</label>
        <textarea id="description" v-model="contest.description"></textarea>
  
        <button type="submit">Submit</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ContestEdit',
    data() {
      return {
        contest: {
          name: '',
          description: ''
        }
      };
    },
    methods: {
      saveContest() {
        // API call to save the contest
        alert(`Saving: ${this.contest.name}`);
      }
    }
  }
  </script>
  
  <style scoped>
  /* Add your CSS styling here */
  </style>