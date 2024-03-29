import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: () => import('@/views/layout'),
    redirect: '/home',
    // layout组件的子路由（即显示在侧边栏右边的主屏幕部分），默认让home显示在该部分作为首页展示
    children: [
      {
        path: '/home',
        component: () => import('@/views/home')
      },
      {
        path: '/chart1',
        component: () => import('@/views/zotero_kg/chart')
      },
      {
        path: '/graph1',
        component: () => import('@/views/zotero_kg/graph')
      },
      {
        path: '/search1',
        component: () => import('@/views/zotero_kg/search')
      },
      {
        path: '/chart2',
        component: () => import('@/views/medical_kg/chart')
      },
      {
        path: '/graph2',
        component: () => import('@/views/medical_kg/graph')
      },
      {
        path: '/search2',
        component: () => import('@/views/medical_kg/search')
      },
      {
        path: '/ai2',
        component: () => import('@/views/medical_kg/ai')
      },
      {
        path: '/diy',
        component: () => import('@/views/diy')
      },
      {
        path: '/manage',
        component: () => import('@/views/knowledge/manage')
      },
      {
        path: '/memory',
        component: () => import('@/views/knowledge/memory')
      },
      {
        path: '/info',
        component: () => import('@/views/user/userInfo')
      },
      {
        path: '/avatar',
        component: () => import('@/views/user/userAvatar')
      },
      {
        path: '/pwd',
        component: () => import('@/views/user/userPwd')
      }
    ]
  },
  {
    path: '/reg',
    component: () => import('@/views/register')
  },
  {
    path: '/login',
    component: () => import('@/views/login')
  }
]

const router = new VueRouter({
  routes
})

const whiteList = ['/login', '/reg'] // 白名单，无需登录可以访问的路由地址

// 全局前置路由守卫： 路由跳转时，先获取用户信息，再跳转
// 浏览器第一次打开页面，会触发一次全局前置路由守卫函数
// next如果强行跳转，会再次触发全局前置路由守卫函数
router.beforeEach((to, from, next) => {
  const token = store.state.token
  if (token) { // 登录了
    if (!store.state.userInfo.username) {
      // 如果现在本地有token但没有username(刚刚重新登录时)，才去获取用户信息
      // 没token会401无授权错误，有username说明你已经登录且有用户信息了，跳转不用再请求
      store.dispatch('getUserInfoActions')
    }
    next() // 放行
  } else { // 没登录
    if (whiteList.includes(to.path)) {
      // 未登录，但是要去的路由地址可以访问，则放行（路由全局前置守卫不会再次触发，而是匹配路由表，让组件挂载）
      next() // 正常放行
    } else {
      next('/login') // 强制跳转到登录页，需要走全局前置守卫
    }
  }
})

export default router
