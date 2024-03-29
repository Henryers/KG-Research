const express = require('express')
const router = express.Router()
// 导入处理函数
const { getMenu } = require('../router_handler/menu')
// 请求地址：http://127.0.0.1:9000/my/menus (其中 /my 是在 app.js 中添加的访问前缀)
router.get('/menu', getMenu)

module.exports = router
