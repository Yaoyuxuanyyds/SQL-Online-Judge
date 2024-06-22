<template>
  <div>
    <Navbar />
    <h1>Contest Page</h1>
    <p>This is the Contest page. Test your navigation here.</p>
  </div>
</template>

<script>
import Navbar from '@/components/student/Navbar.vue';

export default {
  name: 'Contest',
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
