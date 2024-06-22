<template>
  <div>
    <Navbar />
    <h1>Submit Page</h1>
    <p>This is the Submit page. Test your navigation here.</p>
  </div>
</template>

<script>
import Navbar from '@/components/student/Navbar.vue';

export default {
  name: 'Submit',
  components: {
    Navbar
  }
};
</script>

<style scoped>
h1 {
  color: #2c3e50;
}
</style>
