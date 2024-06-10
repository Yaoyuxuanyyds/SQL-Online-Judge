<template>
  <div>
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal">
      <el-menu-item index="1" @click="handleSelect('/home')">Home</el-menu-item>
      <el-menu-item v-if="usertype === 'admin'" index="2" @click="handleSelect('/admin')">Admin</el-menu-item>
      <el-menu-item v-if="usertype === 'teacher'" index="3" @click="handleSelect('/teacher')">Teacher</el-menu-item>
      <el-menu-item v-if="usertype === 'student'" index="4" @click="handleSelect('/student')">Student</el-menu-item>
      <el-menu-item v-if="usertype === ''" index="5" @click="handleSelect('/login')">Login</el-menu-item>
      <el-menu-item v-if="usertype === ''" index="6" @click="handleSelect('/register')">Register</el-menu-item>
      <el-menu-item v-if="usertype !== ''" index="7" @click="logout">Logout</el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: "Header",
  data() {
    return {
      activeIndex: '1',
      usertype: this.$store.getters.Usertype
    };
  },
  methods: {
    handleSelect(path) {
      this.$router.push(path);
    },
    logout() {
      this.$store.dispatch('logout');
      this.$router.push('/home');
    }
  }
}
</script>
