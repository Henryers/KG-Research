import request from '@/utils/request' // 引入自定义的axios函数

// 节点json
export const getGraph1API = () => { // 其实直接(obj)更简洁，但是语义不明确
  // 原地是一个Promise对象(内部包含了一个原生ajax请求)
  // return 这个Promise对象，到逻辑页面，到那边对Promise对象提取结果
  return request({
    url: '/api/graph_nodes',
    method: 'get' // 默认get可以不写，post就一定要写
    // axios传参：params,data
    // params的对象参数名和值，axios源码会把参数和值，拼接在url?后面给后台(query查询字符串)
    // data的对象参数名和值，axios源码会把参数和值，拼接在请求体里(body参数)
  })
}
// 关系数组
export const getGraph2API = () => { // 其实直接(obj)更简洁，但是语义不明确
  // 原地是一个Promise对象(内部包含了一个原生ajax请求)
  // return 这个Promise对象，到逻辑页面，到那边对Promise对象提取结果
  return request({
    url: '/api/graph_rels',
    method: 'get' // 默认get可以不写，post就一定要写
    // axios传参：params,data
    // params的对象参数名和值，axios源码会把参数和值，拼接在url?后面给后台(query查询字符串)
    // data的对象参数名和值，axios源码会把参数和值，拼接在请求体里(body参数)
  })
}

export const registerAPI = ({ username, password, repassword }) => { // 其实直接(obj)更简洁，但是语义不明确
  return request({
    url: '/api/reg',
    method: 'post',
    data: {
      username,
      password,
      repassword
    }
  })
}

/**
 * 登录接口（这是JSDoc注释）
 * @param {*} param0 {username: 用户名, password: 密码}
 * @returns Promise对象
 */
export const loginAPI = ({ username, password }) => {
  return request({
    url: '/api/login',
    method: 'post',
    data: {
      username,
      password
    }
  })
}

/**
 * 获取-侧边栏菜单数据
 * @returns Promise对象
 */
export const getMenuListAPI = () => {
  return request({
    url: '/my/menu'
  })
}

/**
 * 获取用户信息
 * @returns Promise对象
 */
export const getUserInfoAPI = () => {
  return request({
    url: '/my/userinfo'
    // method不写默认就是'get'方式请求
    // 传参给后台: params(查询字符串query), data(请求体body), headers(请求头)
    // headers不写，统一在 request.js 里的自定义 myAxios 进行配置
  })
}

/**
 * 更新基本资料
 */
export const updateUserInfoAPI = ({ id, username, nickname, email, user_pic }) => {
  return request({
    url: '/my/userinfo',
    method: 'PUT',
    data: {
      id,
      username,
      nickname,
      email,
      user_pic
    }
  })
}

/**
 * 更新头像
 */
export const updateAvatarAPI = (avatar) => {
  return request({
    url: '/my/updateavatar',
    method: 'PATCH',
    data: {
      avatar
    }
  })
}

/**
 * 更新-用户密码
 * @param {*} param0 { old_pwd: 旧密码, new_pwd: 新密码, re_pwd: 新密码确认 }
 * @returns Promise对象
 */
export const updatePwdAPI = ({ old_pwd, new_pwd, re_pwd }) => {
  return request({
    url: '/my/updatepwd',
    method: 'PATCH',
    data: {
      old_pwd,
      new_pwd,
      re_pwd
    }
  })
}
