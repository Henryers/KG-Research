const express = require('express')
const router = express.Router()
// 导入处理函数
const { getGraphNodes, getGraphRels } = require('../router_handler/graph')
// 请求地址：http://127.0.0.1:9000/api/graph_nodes (其中 /api 是在 app.js 中添加的访问前缀)
// 请求地址：http://127.0.0.1:9000/api/graph_rels (其中 /api 是在 app.js 中添加的访问前缀)
router.get('/graph_nodes', getGraphNodes)
router.get('/graph_rels', getGraphRels)

module.exports = router
