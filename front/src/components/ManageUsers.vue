<template>
<div> 
  <Navbar />
   <div class="manage-users-container">
    <h1>用户管理</h1>

    <!-- 搜索框 -->
    <div class="search-container">
      <input v-model="searchId" placeholder="通过ID搜索">
    </div>

    <!-- 用户列表 -->
    <table class="users-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>用户名</th>
          <th>角色</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user) in filteredUsers" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.role }}</td>
          <td>
            <!-- 根据角色显示不同按钮 -->
            <button @click="toggleUserRole(user.id, user.role)">
              {{ parseInt(user.role) === 0 ? '设为教师' : '设为学生' }}
            </button>
            <!-- 编辑密码按钮 -->
            <button @click="deleteUser(user.id)">删除用户</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div></div>

</template>

<script>
import axios from 'axios';
import Navbar from '@/components/Navbar.vue';

export default {
  components: {
    Navbar
  },
  name: 'ManageUsers',
  data() {
    return {
      users: [],
      searchId: '',
    };
  },
  computed: {
    filteredUsers() {
      if (this.searchId === '') {
        return this.users;
      } else {
        return this.users.filter(user => user.id.toString() === this.searchId);
      }
    }
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    fetchUsers() {
      axios.get('/api/manageusers')
        .then(response => {
          this.users = response.data;
        })
        .catch(error => {
          alert('获取用户列表失败:', error);
        });
    },
    toggleUserRole(user_id, currentRole) {
      const userId = parseInt(user_id);
      const newRole = parseInt(currentRole) === 0 ? 1 : 0;
      axios.put(`/api/manageusers`,{id: userId, role: newRole})
        .then(
          alert('切换用户角色成功'),
          window.location.reload()
        )
        .catch(error => {
          alert('切换用户角色失败:', error);
        });
    },
    deleteUser(user_id) {
      const userId = parseInt(user_id);
      axios.post(`/api/manageusers`,{id: userId})
        .then(
          alert('删除用户成功'),
          window.location.reload()
        )
        .catch(error => {
          alert('删除用户失败:', error);
        });
    }

  }
};
</script>

<style scoped>
.manage-users-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

h1 {
  text-align: center;
  font-size: 24px;
}

.search-container {
  text-align: center;
  margin-bottom: 20px;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
}

.users-table th, .users-table td {
  border: 1px solid #ccc;
  padding: 8px;
}

button {
  padding: 5px 10px;
  margin-left: 5px;
  cursor: pointer;
}
</style>
