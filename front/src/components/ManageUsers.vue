<template>
  <div>
    <Navbar />
    <div class="manage-users-container">
      <h1>用户管理</h1>

      <!-- 搜索框 -->
      <div class="search-container">
        <input v-model="searchId" placeholder="通过ID搜索" class="search-input">
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
            <td>{{ user.role !== 0 ? '教师' : '学生' }}</td>
            <td>
              <!-- 根据角色显示不同按钮 -->
              <button @click="toggleUserRole(user.id, user.role)" :class="user.role === 0 ? 'teacher-button' : 'student-button'">
                {{ user.role !== 0 ? '设为学生' : '设为教师' }}
              </button>
              <!-- 删除用户按钮 -->
              <button @click="deleteUser(user.id)" class="delete-button">删除用户</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
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
      const newRole = currentRole === 0 ? 1 : 0;
      axios.put(`/api/manageusers`, { id: userId, role: newRole })
        .then(() => {
          alert('切换用户角色成功');
          this.fetchUsers(); // 更新操作后重新获取用户列表
        })
        .catch(error => {
          alert('切换用户角色失败:', error);
        });
    },
    deleteUser(user_id) {
      const userId = parseInt(user_id);
      axios.delete(`/api/manageusers`, {
        headers: {
          'session': localStorage.getItem('session'),
          'Content-Type': 'application/json'
        },
        params: {
          user_id: userId
        },
        data: {}})
        .then(() => {
          alert('删除用户成功');
          this.fetchUsers(); // 删除用户后重新获取用户列表
        })
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
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加容器阴影效果 */
}

h1 {
  text-align: center;
  font-size: 2rem;
  color: #007bff;
  font-weight: bold;
  margin-bottom: 20px;
}

.search-container {
  text-align: center;
  margin-bottom: 20px;
}

.search-input {
  padding: 8px;
  width: 300px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 添加表格阴影效果 */
}

.users-table th, .users-table td {
  border: 1px solid #ccc;
  padding: 12px;
}

.teacher-button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 5px 10px;
  margin-right: 5px;
  cursor: pointer;
}

.student-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 5px 10px;
  margin-right: 5px;
  cursor: pointer;
}

.delete-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}

button:hover {
  opacity: 0.8;
}
</style>
