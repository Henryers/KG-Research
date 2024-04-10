// 1. 导入数据库操作模块：
const db = require('../db/index')
// 2. 导入 bcryptjs 模块进行密码的加密
const bcrypt = require('bcryptjs')
// 用这个包来生成 Token 字符串
const jwt = require('jsonwebtoken')
// 导入配置文件
const config = require('../config')

/**
* 在这里定义和用户相关的路由处理函数，供 /router/user.js 模块进行调用
*/
// 注册用户的处理函数
exports.regUser = (req, res) => {
  // 接收表单数据？？？？？？？？？？？？？？？？？？？？？你™最好是表单！！！找了半天发现前端vue项目中，这是json！！！！
  const userinfo = req.body
  console.log(userinfo)
  // 判断数据是否合法
  if (!userinfo.username || !userinfo.password) {
    // return res.send({ status: 1, message: '用户名或密码不能为空！' })
    return res.cc('用户名或密码不能为空！')
  }
  // 数据规格合法了，进行下一步的流程：检查用户名是否重复
  const sql = 'select * from kg_users where username=?'
  db.query(sql, [userinfo.username], function (err, results) {
    // 执行 SQL 语句失败
    if (err) {
      // return res.send({ status: 1, message: err.message })
      return res.cc(err)
    }
    // 用户名被占用
    if (results.length > 0) {
      // return res.send({ status: 1, message: '用户名被占用，请更换其他用户名！' })
      return res.cc('用户名被占用，请更换其他用户名！')
    }
    // TODO: 用户名可用，继续后续流程...
    // 对用户的密码,进行 bcrype 加密，返回值是加密之后的密码字符串
    userinfo.password = bcrypt.hashSync(userinfo.password, 10) // (明文密码, 随机长度)、
    // 定义插入新用户的 SQL 语句
    const sql = 'insert into kg_users set ?'
    // 调用 db.query() 执行 SQL 语句
    db.query(sql, { username: userinfo.username, password: userinfo.password }, (err, results) => {
      // 执行 SQL 语句失败
      // if (err) return res.send({ status: 1, message: err.message })
      if (err) return res.cc(err)
      // SQL 语句执行成功，但影响行数不为 1
      if (results.affectedRows !== 1) {
        // return res.send({ status: 1, message: '注册用户失败，请稍后再试！' })
        return res.cc('注册用户失败，请稍后再试！')
      }
      // 注册成功
      res.send({ status: 0, message: '注册成功！' })
    })
  })
}

// 登录的处理函数
exports.login = (req, res) => {
  const userinfo = req.body
  // 定义 SQL 语句
  const sql = 'select * from kg_users where username=?'
  // 执行 SQL 语句查询用户的数据
  db.query(sql, userinfo.username, (err, results) => {
    // 执行 SQL 语句失败
    if (err) return res.cc(err)
    // 执行 SQL 语句成功，但是查询到数据条数不等于 1
    if (results.length !== 1) return res.cc('查无此人！试试注册下哦，亲？')
    // TODO：判断用户输入的登录密码是否和数据库中的密码一致
    // 使用 bcrypt.compareSync(明文密码, hash 加密密码) 方法比对密码是否正确
    const compareResult = bcrypt.compareSync(userinfo.password, results[0].password)
    // 如果对比的结果等于 false，则证明用户输入的密码错误
    if (!compareResult) return res.cc('密码错误！')
    // 在服务器端生成 JWT 的 Token 字符串，其中要剔除 password 和 user_pic 字段后再保存到客户端，防止黑客盗取敏感信息
    // 先用展开运算符，将用户对象results[0]展开后，再将password和user_pic字段覆盖成空字符串
    const user = { ...results[0], password: '', user_pic: '' }
    // 对用户的信息进行加密，生成 Token 字符串
    const tokenStr = jwt.sign(user, config.jwtSecretKey, { expiresIn: config.expiresIn }) // token有效期为10小时
    // 将生成的 Token 字符串响应给客户端
    res.send({
      status: 0,
      message: '登录成功！',
      // 为了方便客户端使用 Token，在服务器端直接拼接上 'Bearer ' 的前缀(注意空格不能丢！)
      token: 'Bearer ' + tokenStr
    })
  })
  // res.send('login OK')
}
