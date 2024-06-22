<template>
  <div>
    <Navbar />
    <div>
      <!-- 临时内容 -->
      <h1>欢迎来到主页</h1>
      <p>这里展示一些个人信息。</p>
    </div>
  </div>
</template>

<script>
import Navbar from './Navbar.vue';

export default {
  components: {
    Navbar
  }
}
</script>

<style>
/* 添加任何 Home.vue 特定的样式 */
</style>
