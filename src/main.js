import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './assets/global.less'
import './elementUI/index.js' // 注册elementUI组件

Vue.config.productionTip = false

new Vue({
  router,
  store, // 声明全局的store对象，所有组件都可以通过this.$store来访问
  render: h => h(App)
}).$mount('#app')
