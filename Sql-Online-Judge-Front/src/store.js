import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    usertype: '',
    token: '',
    username: ''
  },
  getters: {
    Usertype: state => state.usertype,
    Token: state => state.token,
    Username: state => state.username
  },
  mutations: {
    setUsertype(state, usertype) {
      if (['', 'student', 'admin', 'teacher'].includes(usertype))
        state.usertype = usertype
    },
    setToken(state, token) {
      state.token = token
    },
    setUsername(state, username) {
      state.username = username
    }
  },
  actions: {
    login(context, data) {
      return new Promise((resolve, reject) => {
        const userType = data['usertype'];
        const loginData = {
          id: data['id'],
          password: data['password']
        };

        let url = '/session/';
        if (userType === 'admin') {
          url += 'admin';
        } else if (userType === 'student') {
          url += 'student';
        } else if (userType === 'teacher') {
          url += 'teacher';
        } else {
          reject('用户身份无效，重新注册！');
          return;
        }

        return axios.post(url, loginData).then((response) => {
          context.commit('setToken', response.data['session']);
          context.commit('setUsertype', userType);
          context.commit('setUsername', response.data['name']);
          resolve();
        }).catch((response) => {
          reject(response);
        });
      });
    },
    register(context, data) {
      return new Promise((resolve, reject) => {
        return axios.post('/register', data)
          .then((response) => {
            resolve(response.data);
          }).catch((response) => {
            reject(response);
          });
      });
    },
    logout(ctx) {
      ctx.commit('setUsertype', '');
      ctx.commit('setToken', '');
    }
  }
})
