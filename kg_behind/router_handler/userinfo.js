// 1. 导入数据库操作模块：
const db = require('../db/index')
// 导入处理密码的模块
const bcrypt = require('bcryptjs')

// 获取用户基本信息的处理函数
exports.getUserInfo = (req, res) => {
  // 定义 SQL 语句
  const sql = 'select id, username, nickname, email, user_pic from kg_users where id=?'
  // 执行 SQL 语句，查询用户的数据
  // 注意：req 对象上的 user 属性，是 Token 解析成功，express-jwt 中间件帮我们挂载上去的
  // get没传数据怎么有req和token? 别忘了请求/my/要传headers,里面就有req: token！
  console.log(req.auth)
  db.query(sql, req.auth.id, (err, results) => {
    // 执行 SQL 语句失败
    if (err) return res.cc(err)
    // 执行 SQL 语句成功，但是查询到的数据条数不等于 1
    if (results.length !== 1) return res.cc('获取用户信息失败！')
    // 用户信息获取成功
    res.send({
      status: 0,
      message: '获取用户信息成功！',
      data: results[0]
    })
  })
  // res.send('ok')
}

// 更新用户基本信息的处理函数
exports.updateUserInfo = (req, res) => {
  const sql = 'update kg_users set ? where id=?'
  // ------------------- 下面一堆注释别看了，本来req.body好好的，非要改成req.auth多此一举... -----------------------
  console.log(req)
  // console.log(req.auth)
  db.query(sql, [req.body, req.body.id], (err, results) => {
    // 执行 SQL 语句失败
    if (err) {
      console.log(err)
      return res.cc(err)
    }
    // 执行 SQL 语句成功，但影响行数不为 1
    if (results.affectedRows !== 1) return res.cc('修改用户基本信息失败！')
    // 修改用户信息成功(不完善，只要有合法token就能修改任何存在id的人的信息)
    console.log('------------------------------成功了！------------------------------------')
    console.log(req.body)
    return res.cc('修改用户基本信息成功！', 0)
  })
}

// 更新用户头像的处理函数
exports.updateAvatar = (req, res) => {
  const sql = 'update kg_users set user_pic=? where id=?'
  // console.log(req.auth.id)
  db.query(sql, [req.body.avatar, req.auth.id], (err, results) => {
    // 执行 SQL 语句失败
    if (err) return res.cc(err)
    // 执行 SQL 语句成功，但是影响行数不等于 1
    if (results.affectedRows !== 1) return res.cc('更新头像失败！')
    // 更新用户头像成功
    return res.cc('更新头像成功！', 0)
  })
}

// 重置密码的处理函数
exports.updatePassword = (req, res) => {
  // 定义根据 id 查询用户数据的 SQL 语句
  const sql = 'select * from kg_users where id=?'
  console.log(req)
  console.log(req.auth)
  // 执行 SQL 语句查询用户是否存在
  db.query(sql, req.auth.id, (err, results) => {
    console.log('results')
    console.log(results)
    // 执行 SQL 语句失败
    if (err) return res.cc(err)
    // 检查指定 id 的用户是否存在
    if (results.length !== 1) return res.cc('用户不存在！')
    // 判断提交的旧密码是否正确
    const compareResult = bcrypt.compareSync(req.body.old_pwd, results[0].password)
    if (!compareResult) return res.cc('原密码错误！')
    // 定义更新用户密码的 SQL 语句
    const sql = 'update kg_users set password=? where id=?'
    // 对新密码进行 bcrypt 加密处理
    const newPwd = bcrypt.hashSync(req.body.new_pwd, 10)
    // 执行 SQL 语句，根据 id 更新用户的密码
    db.query(sql, [newPwd, req.auth.id], (err, results) => {
      // SQL 语句执行失败
      if (err) return res.cc(err)
      // SQL 语句执行成功，但是影响行数不等于 1
      if (results.affectedRows !== 1) return res.cc('更新密码失败！')
      // 更新密码成功
      res.cc('更新密码成功！', 0)
    })
  })
}
