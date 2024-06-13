<template>
  <div id="app">
    <h1>MYWW OJ 数据库版</h1>
    <router-view/>
  </div>
</template>

<style>
#app {
  font-family: 'Unifont', 'Source Code Pro', sans-serif;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 20px;
}
#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
