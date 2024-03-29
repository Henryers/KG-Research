const menu = {
  0: {
    path: '/home',
    title: '首页',
    icon: 'el-icon-s-home',
    children: null
  },
  1: {
    path: '2',
    title: 'zotero知识图谱',
    icon: 'el-icon-s-order',
    children: {
      0: {
        path: '/chart1',
        title: '数据图表',
        icon: 'el-icon-s-data',
        children: null
      },
      1: {
        path: '/graph1',
        title: '图谱大屏',
        icon: 'el-icon-picture',
        children: null
      },
      2: {
        path: '/search1',
        title: '知识检索',
        icon: 'el-icon-search',
        children: null
      }
    }
  },
  2: {
    path: '3',
    title: '医疗知识图谱',
    icon: 'el-icon-first-aid-kit',
    children: {
      0: {
        path: '/chart2',
        title: '数据图表',
        icon: 'el-icon-s-data',
        children: null
      },
      1: {
        path: '/graph2',
        title: '图谱大屏',
        icon: 'el-icon-picture',
        children: null
      },
      2: {
        path: '/search2',
        title: '知识检索',
        icon: 'el-icon-search',
        children: null
      },
      3: {
        path: '/ai2',
        title: '智能问答',
        icon: 'el-icon-question',
        children: null
      }
    }
  },
  3: {
    path: '/diy',
    title: '自制图谱',
    icon: 'el-icon-s-opportunity',
    children: null
  },
  4: {
    path: '/manage',
    title: '知识管理',
    icon: 'el-icon-s-management',
    children: null
  },
  5: {
    path: '/memory',
    title: '知识记忆',
    icon: 'el-icon-s-claim',
    children: null
  },
  6: {
    path: '7',
    title: '个人中心',
    icon: 'el-icon-user-solid',
    children: {
      0: {
        path: '/info',
        title: '基本信息',
        icon: 'el-icon-share',
        children: null
      },
      1: {
        path: '/avatar',
        title: '更换头像',
        icon: 'el-icon-upload',
        children: null
      },
      2: {
        path: '/pwd',
        title: '修改密码',
        icon: 'el-icon-s-tools',
        children: null
      }
    }
  }
}

exports.getMenu = (req, res) => {
  res.send({
    status: 0,
    data: menu,
    message: '获取左侧菜单成功！'
  })
}
