<template>
  <div class="manage-users-container">
    <h1>用户管理</h1>

    <!-- 搜索框 -->
    <div class="search-container">
      <input v-model="searchId" placeholder="通过ID搜索">
      <button @click="searchUser">搜索</button>
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
        <tr v-for="(user, index) in filteredUsers" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.role }}</td>
          <td>
            <!-- 根据角色显示不同按钮 -->
            <button @click="toggleUserRole(user.id, user.role, user.password)">
              {{ user.role === AUTH_STUDENT ? '设为教师' : '设为学生' }}
            </button>
            <!-- 编辑密码按钮 -->
            <button @click="editPassword(index)">编辑密码</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ManageUsers',
  data() {
    return {
      users: [],
      searchId: '',
      newPassword: ''
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
          console.error('获取用户列表失败:', error);
        });
    },
    searchUser() {
      console.log('搜索 ID:', this.searchId);
      // 可以在这里添加向后端发送搜索请求的逻辑
      // TODO
    },
    toggleUserRole(user_id, currentRole, password) {
      const userId = ParseInt(user_id);
      const newPassword = password
      const newRole = ParseInt(currentRole) === AUTH_STUDENT ? AUTH_TEACHER : AUTH_STUDENT;
      axios.put(`/api/manageusers`,{id: userId, password: newPassword, role: newRole })
        .then(response => {
          console.log(response.data.message);
          const userIndex = this.users.findIndex(u => u.id === userId);
          if (userIndex !== -1) {
            this.users[userIndex].role = newRole;
          }
        })
        .catch(error => {
          console.error('切换用户角色失败:', error);
        });
    },
    editPassword(index) {
      const userId = this.users[index].id;
      const role = this.users[index].role;
      console.log('编辑密码:', userId, role);
      const newPassword = prompt('输入新密码:');
      if (newPassword !== null && newPassword !== '') {
        // 发送更新密码的请求
        axios.put(`/api/manageusers`,{id: userId}, { password: newPassword }, { role: role })
          .then(response => {
            alert('密码更新成功!');
          })
          .catch(error => {
            console.error('密码更新失败:', error);
          });
      }
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
