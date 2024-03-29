const express = require('express')
const router = express.Router()
// 导入用户信息的处理函数模块
const userinfo_handler = require('../router_handler/userinfo')

// 1. 导入验证表单数据的中间件
const expressJoi = require('@escook/express-joi')
// 2. 导入需要的验证规则对象
const { update_userinfo_schema, update_avatar_schema, update_password_schema } = require('../schema/user')

// 获取用户的基本信息(get 在headers里传token就行)
router.get('/userinfo', userinfo_handler.getUserInfo)
// 更新用户的基本信息(post 在body里传id, nickname, email)
// 所以需要先对这些数据进行验证，因此才要在userinfo_handler之前先写中间件验证合法性
router.put('/userinfo', expressJoi(update_userinfo_schema), userinfo_handler.updateUserInfo)
// 更新用户头像的路由
router.patch('/updateavatar', expressJoi(update_avatar_schema), userinfo_handler.updateAvatar)
// 重置密码的路由
router.patch('/updatepwd', expressJoi(update_password_schema), userinfo_handler.updatePassword)

module.exports = router
