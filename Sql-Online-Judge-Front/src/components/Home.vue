<template>
  <div>
    <Header />
    <div class="login-container">
      <h2>Login</h2>
      <el-form :model="loginForm" :rules="rules" ref="loginForm" label-width="100px">
        <el-form-item label="Role" prop="role">
          <el-select v-model="loginForm.role" placeholder="Select Role">
            <el-option label="Student" value="0"></el-option>
            <el-option label="Teacher" value="1"></el-option>
            <el-option label="Admin" value="2"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="ID" prop="id">
          <el-input v-model="loginForm.id"></el-input>
        </el-form-item>
        <el-form-item label="Password" prop="password">
          <el-input type="password" v-model="loginForm.password"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin">Login</el-button>
          <el-button type="text" @click="handleRegister">Register</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import Header from './Header.vue';

export default {
  name: "Home",
  components: {
    Header
  },
  data() {
    const validateRole = (rule, value, callback) => {
      if (value === '') {
        return callback(new Error('Role is required'));
      }
      callback();
    };

    const validateId = (rule, value, callback) => {
      if (value === '') {
        return callback(new Error('ID is required'));
      }
      callback();
    };

    const validatePassword = (rule, value, callback) => {
      if (value === '') {
        return callback(new Error('Password is required'));
      }
      callback();
    };

    return {
      loginForm: {
        role: '',
        id: '',
        password: ''
      },
      rules: {
        role: [{ validator: validateRole, trigger: 'change' }],
        id: [{ validator: validateId, trigger: 'blur' }],
        password: [{ validator: validatePassword, trigger: 'blur' }]
      }
    };
  },
  methods: {
    ...mapActions(['login']),
    handleLogin() {
      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          const loginData = {
            id: this.loginForm.id,
            password: this.loginForm.password,
            usertype: this.loginForm.role === 0 ? 'student' : (this.loginForm.role === 1 ? 'teacher' : 'admin')
          };
          this.login(loginData).then(() => {
            this.$message.success('Login successful');
            if (loginData.usertype === 'admin') {
              this.$router.push('/admin');
            } else if (loginData.usertype === 'student') {
              this.$router.push('/student');
            } else if (loginData.usertype === 'teacher') {
              this.$router.push('/teacher');
            }
          }).catch((err) => {
            this.$message.error(`Login failed: ${err.response.data.message}`);
          });
        } else {
          this.$message.error('Please fill in the form correctly');
          return false;
        }
      });
    },
    handleRegister() {
      this.$router.push('/register');
    }
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}
</style>
