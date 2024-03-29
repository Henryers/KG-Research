import Vue from 'vue'
import Vuex from 'vuex'
// vuex 默认保存在内存中，无法做到持久化存储(刷新页面就丢失)
// 用下面的插件就能做到持久化存储
import createPersistedState from 'vuex-persistedstate'
import { getUserInfoAPI } from '@/api'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // 用来存储登录成功之后，得到的token
    token: '',
    userInfo: {} // 定义用户信息对象(id, username, nickname, email, user_pic)
  },
  // getters相当于计算属性，用来计算state里面的数据，并用 getters.xxx 接受计算返回的结果
  // this.$store.state.userInfo.username => this.$store.getters.username，相当于将userInfo设为全局状态
  getters: {
    username: state => state.userInfo.username, // 用户名
    nickname: state => state.userInfo.nickname, // 用户昵称
    user_pic: state => state.userInfo.user_pic // 用户头像
  },
  // dispatch('getUserInfoActions')是vc组件来调用，不是store里面的部分
  // 上面解释：dispatch调用actions里的getUserInfoActions方法
  // 由原理图可知：actions和后台服务器API打交道，进行数据的请求、判断处理等等
  actions: {
    // 请求用户信息
    // store是mini版的store，官方文档叫context，表示存有当前上下文的东西
    // 里面有commit、dispatch、getters等等但是其他的配置项属性等比较少
    async getUserInfoActions (store) {
      // 1. 调用接口获取用户信息
      const res = await getUserInfoAPI()
      console.log(res)
      // 2. 把用户信息保存到vuex中
      store.commit('updateUserInfo', res.data.data)
      // updateUserInfo这个函数名传给mutation，所以mutation里面要有这个函数的定义
    }
  },
  // 由原理图可知：mutations和state打交道，进行数据的更新
  mutations: {
    // 更新保存token
    updateToken (state, newToken) {
      state.token = newToken
    },
    // 更新用户的信息
    updateUserInfo (state, newUserInfo) {
      state.userInfo = newUserInfo
    }
  },
  modules: {
  },
  // 配置为 vuex 的插件
  plugins: [createPersistedState()]
})
