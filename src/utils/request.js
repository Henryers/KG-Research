import axios from 'axios'
import store from '@/store'
import router from '@/router'
import { Message } from 'element-ui'

export const baseURL = 'http://127.0.0.1:9000'
// 创建一个自定的axios方法(比原axios多了个基地址)
// axios函数请求的url地址前面会被拼接基地址, 然后axios请求baseURL+url后台完整地址
const myAxios = axios.create({
  baseURL: baseURL
})
// 1.定义"请求"拦截器(前端给后端服务器的请求)
// api里每次调用request方法，都会触发一次请求拦截器
myAxios.interceptors.request.use(function (config) {
  // config配置对象（要请求后台的参数都在这个对象上）
  console.log('------请求拦截器-------')
  // 在发起时要统一携带请求头Authorization和token值
  // 判断，登录和注册页面，vuex里无token，而且登录接口和注册接口也不需要携带token（其他页面需要——）
  if (store.state.token) {
    // 为请求头挂载 Authorization 字段
    config.headers.Authorization = store.state.token
  }
  return config
}, function (error) {
  // 请求发起前的代码，如果有异常报错，会直接进入这里(类似catch)
  // 返回一个拒绝状态的promise对象(axios留着原地的promise对象状态就为失败，结果为error变量值)
  // 口诀：return 非Promise对象值，会作为成功的结果，返回给下一个Promise对象（axios留在原地）
  // Promise.reject()原地留下一个新的Promise对象(状态为失败)
  return Promise.reject(error)
})

// 2.定义"响应"拦截器(后端服务器给前端的响应)
myAxios.interceptors.response.use(function (response) {
  // 响应http状态码为 2xx,3xx 时触发成功的回调，形参中的 response 是“成功的结果”
  console.log('------响应拦截器-------')
  console.log(response)
  // 如果返回的data里有状态码status并且不是0，说明输入密码错误/查无此人
  // 不过此部分代码在const res = await API()之后的部分进行处理，此处把response返回就行
  return response
}, function (error) {
  // 响应状态码是 4xx,5xx 时触发失败的回调，形参中的 error 是“失败的结果”
  console.dir(error)
  console.log('-------------')
  console.log(error)
  if (error.response.status === 401) {
    // 无效的 token (过期，伪造或者被修改)
    // token没用了，把 Vuex 中的一切重置为空，并跳转到登录页面(相当于没token的状态)
    store.commit('updateToken', '')
    store.commit('updateUserInfo', {})
    router.push('/login') // js无法获取this.$router，所以要引入router来跳转
    Message.error('用户身份已过期~~')
  }
  // 响应状态码不是 2xx 时触发失败的回调，形参中的 error 是“失败的结果”
  return Promise.reject(error)
})

// 导出自定义axios
export default myAxios
