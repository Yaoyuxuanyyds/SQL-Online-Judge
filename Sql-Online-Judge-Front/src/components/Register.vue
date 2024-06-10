<template>
  <div>
    <Header />
    <div class="register-container">
      <h2>Register</h2>
      <el-form ref="registerForm" :model="registerForm" :rules="rules" label-width="100px">
        <el-form-item label="ID" prop="id">
          <el-input v-model="registerForm.id"></el-input>
        </el-form-item>
        <el-form-item label="Username" prop="username">
          <el-input v-model="registerForm.username"></el-input>
        </el-form-item>
        <el-form-item label="Password" prop="password">
          <el-input type="password" v-model="registerForm.password"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleRegister">Register</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import Header from './Header.vue';

export default {
  name: "Register",
  components: {
    Header
  },
  data() {
    const validateId = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('ID is required'));
      }
      callback();
    };

    const validateUsername = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('Username is required'));
      }
      callback();
    };

    const validatePassword = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('Password is required'));
      }
      callback();
    };

    return {
      registerForm: {
        id: '',
        username: '',
        password: ''
      },
      rules: {
        id: [{ validator: validateId, trigger: 'blur' }],
        username: [{ validator: validateUsername, trigger: 'blur' }],
        password: [{ validator: validatePassword, trigger: 'blur' }]
      }
    };
  },
  methods: {
    ...mapActions(['register']),
    handleRegister() {
      this.$refs.registerForm.validate((valid) => {
        if (valid) {
          const registerData = {
            id: this.registerForm.id,
            username: this.registerForm.username,
            password: this.registerForm.password
          };
          this.register(registerData).then(() => {
            this.$message.success('Registration successful');
            this.$router.push('/home');
          }).catch((err) => {
            this.$message.error(`Registration failed: ${err.response.data.message}`);
          });
        } else {
          this.$message.error('Please fill in the form correctly');
          return false;
        }
      });
    }
  }
}
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}
</style>
