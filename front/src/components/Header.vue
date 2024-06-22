<template>
  <div>
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal">
      <el-menu-item index="1" @click="handleSelect('/')">主页</el-menu-item>
      <el-menu-item v-if="usertype === 'admin'" index="2" @click="handleSelect('/admin')">系统管理</el-menu-item>
      <el-menu-item v-if="usertype === 'teacher'" index="3" @click="handleSelect('/teacher')">教师</el-menu-item>
      <el-menu-item v-if="usertype === 'student'" index="4" @click="handleSelect('/student')">学生</el-menu-item>
      <el-menu-item v-if="usertype === ''" index="5" @click="handleSelect('/login')">登录</el-menu-item>
      <el-menu-item v-if="usertype === ''" index="6" @click="handleSelect('/register')">注册</el-menu-item>
      <el-menu-item v-if="usertype !== ''" index="7" @click="logout">退出登录</el-menu-item>
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
      this.$router.push('/');
    }
  }
}
</script>
