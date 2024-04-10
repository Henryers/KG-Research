// 导入 express
const express = require('express')
// 创建服务器的实例对象
const app = express()
const joi = require('joi')

// 导入并配置 cors 中间件
const cors = require('cors')
app.use(cors())

// 使用 express.json() 中间件来解析 JSON 请求体
// (没写这句只能解析表单，不能解析content-type: application/json的请求体!!!)
app.use(express.json({ limit: '5mb' }))
// 配置解析表单数据的中间件，注意：这个中间件，只能解析 application/x-www-form-urlencoded 格式的表单数据
app.use(express.urlencoded({ extended: false }))
// 配置静态资源目录
app.use(express.static('resource'))

// 一定要在路由之前，封装 res.cc 函数(失败时调用)
app.use((req, res, next) => {
  // status 默认值为 1，表示失败的情况
  // err 的值，可能是一个错误对象，也可能是一个错误的描述字符串
  res.cc = function (err, status = 1) { // 默认失败时调用，所以status不传时默认为1，表示失败的状态
    res.send({
      status,
      // 判断 err 是 错误对象 还是 字符串
      message: err instanceof Error ? err.message : err
    })
  }
  next()
})

// 一定要在路由之前配置解析 Token 的中间件
const expressJWT = require('express-jwt')
const config = require('./config')
// 使用 .unless({ path: [/^\/api\//] }) 指定/api开头的接口不需要进行 Token 的身份认证
app.use(
  expressJWT.expressjwt({ secret: config.jwtSecretKey, algorithms: ['HS256'] }).unless({
    path: [/^\/api/]
  })
)

// “路由”部分: 向外暴露http://127.0.0.1:9000这个端口下的，以/api和/my开头的多个路由接口
// 注意：以 /my 开头的接口，都是有权限的接口，需要进行 Token 身份认证
// 导入并注册用户路由模块
const userRouter = require('./router/user')
app.use('/api', userRouter)
// 导入并使用用户信息路由模块
const userinfoRouter = require('./router/userinfo')
app.use('/my', userinfoRouter)
// 附加自己写的图表数据和菜单栏的接口
const graphRouter = require('./router/graph')
app.use('/api', graphRouter)
const menuRouter = require('./router/menu')
app.use('/my', menuRouter)

// 定义错误级别的中间件
app.use((err, req, res, next) => {
  // 验证失败导致的错误
  if (err instanceof joi.ValidationError) return res.cc(err)
  // 身份认证失败后的错误
  if (err.name === 'UnauthorizedError') return res.cc('身份认证失败！')
  // 未知的错误
  res.cc(err)
})

// 启动服务器
app.listen(9000, '0.0.0.0', () => {
  console.log('api server running at http://127.0.0.1:9000')
})
