<template>
    <div class="manage-users-container">
      <h1>Manage Users</h1>
  
      <!-- 搜索框 -->
      <div class="search-container">
        <input v-model="searchId" placeholder="Search by ID">
        <button @click="searchUser">Search</button>
      </div>
  
      <!-- 用户列表 -->
      <table class="users-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Password</th>
            <th>Role</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(user, index) in filteredUsers" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.password }}</td>
            <td>{{ user.role }}</td>
            <td>
              <button @click="setAsTeacher(user.id)" v-if="user.role !== 'teacher'">Set as Teacher</button>
              <button @click="editPassword(index)">Edit Password</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ManageUsers',
    data() {
      return {
        users: [
          { id: 1, username: 'user1', password: 'password1', role: 'student' },
          { id: 2, username: 'user2', password: 'password2', role: 'student' },
          { id: 3, username: 'user3', password: 'password3', role: 'teacher' },
          { id: 4, username: 'user4', password: 'password4', role: 'student' }
        ],
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
    methods: {
      searchUser() {
        // Implement search functionality here
        // For now, just log the search ID
        console.log('Search ID:', this.searchId);
      },
      setAsTeacher(userId) {
        const index = this.users.findIndex(user => user.id === userId);
        if (index !== -1) {
          this.users[index].role = 'teacher';
          // Move the user to the top of the list
          const teacherUser = this.users.splice(index, 1)[0];
          this.users.unshift(teacherUser);
        }
      },
      editPassword(index) {
        const newPassword = prompt('Enter new password:');
        if (newPassword !== null && newPassword !== '') {
          this.users[index].password = newPassword;
          alert('Password updated successfully!');
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
  