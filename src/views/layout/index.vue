<template>
  <el-container class="main-container">
    <el-header>
      <!-- header 左侧的 logo -->
      <img src="../../assets/images/logo.png" alt="" />
      <!-- header 右侧的菜单 -->
      <div class="showtime"></div>
      <el-menu class="el-menu-top" mode="horizontal" background-color="#42C0F8" text-color="#fff"
        active-text-color="#409EFF">
        <el-menu-item index="1" @click="quitFn"><i class="el-icon-switch-button"></i>退出</el-menu-item>
      </el-menu>
    </el-header>
    <el-container>
      <el-aside width="200px">
        <!-- 用户信息区域 -->
        <div class="user-box">
          <img :src="user_pic" alt="" v-if="user_pic" />
          <img src="../../assets/images/logo.png" alt="" v-else />
          <!-- 有昵称显示昵称，没昵称显示用户名，啥都没有不显示(不过这是未登录的情况，也进不来这个页面...) -->
          <span>欢迎 {{ nickname || username }}</span>
        </div>
        <!-- 导航菜单区域 -->
        <el-menu default-active="/home" class="el-menu-vertical-demo" background-color="#42C0F8" text-color="#fff"
          active-text-color="#ffd04b" unique-opened router>
          <!-- 加了router模式，就会在激活导航时以index作为path进行路径跳转（nb!不用自己写路由了!） -->
          <!-- 根据不同情况选择menu-item/submenu进行遍历，所以外层套template遍历，里面组件做判断看是否该次遍历到自己 -->
          <template v-for="item in menuList">
            <el-menu-item v-if="!item.children" :index="item.path" :key="item.path">
              <i :class="item.icon"></i>
              <span slot="title">{{ item.title }}</span>
            </el-menu-item>
            <el-submenu v-else :index="item.path" :key="item.path">
              <!-- 有子菜单的侧边栏项 -->
              <template slot="title">
                <i :class="item.icon"></i>
                <span>{{ item.title }}</span>
              </template>
              <!-- 该项下的子菜单 -->
              <el-menu-item v-for="obj in item.children" :index="obj.path" :key="obj.path">
                <i :class="obj.icon"></i>
                <span>{{ obj.title }}</span>
              </el-menu-item>
            </el-submenu>
          </template>
        </el-menu>
      </el-aside>
      <el-container>
        <el-main>
          <router-view></router-view>
        </el-main>
        <el-footer>2024.3.29 -- 持续维护更新中...</el-footer>
      </el-container>
    </el-container>
  </el-container>
</template>

<script>
import { mapGetters } from 'vuex'
import { getMenuListAPI } from '@/api'
export default {
  name: 'my-layout',
  // 只有data/computed里面的变量才能在template里面直接使用
  data () {
    return {
      // 菜单列表数据，template模板里只能用data/computed里面的变量
      menuList: [] // 侧边栏数据
    }
  },
  created () { // created尽量不要用async/await
    // 获取菜单列表数据
    this.getMenuList()
  },
  computed: {
    ...mapGetters(['username', 'nickname', 'user_pic'])
  },
  mounted () {
    // 显示时间
    const date = new Date() // 获取当前时间
    this.$el.querySelector('.showtime').innerHTML = date.toLocaleString() // 将当前时间显示在页面上

    setInterval(() => {
      const date = new Date()
      this.$el.querySelector('.showtime').innerHTML = date.toLocaleString()
    }, 1000)
  },
  // 退出登录->点击事件
  methods: {
    quitFn () {
      // 为了让用户体验更好，来个确认提示框
      this.$confirm('走了, 爱是会消失的吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 清除 vuex，把原有token和userInfo分别用空字符串、空对象覆盖掉
        this.$store.commit('updateToken', '')
        this.$store.commit('updateUserInfo', {})
        // 强制跳转到登录页面
        this.$router.push('/login')
      }).catch(() => {
        // 取消选择
        this.$message({
          type: 'info',
          message: '已取消退出'
        })
      })
    },
    handleOpen (key, keyPath) {
      console.log(key, keyPath)
    },
    handleClose (key, keyPath) {
      console.log(key, keyPath)
    },
    async getMenuList () {
      const { data: res } = await getMenuListAPI()
      // 失败只有一种可能：token过期，已经有 "已过期" 提示信息 并且 跳转到登录页面，不用再加提示信息了
      // if (res.status !== 0) return this.$message.error('获取菜单列表失败！')
      // 获取菜单列表成功
      this.menuList = res.data
    }
  }
}
</script>

<style lang="less" scoped>
.el-submenu /deep/ .el-icon-arrow-down {
  color: #fff;
}

[class^="el-icon-"] {
  color: blue;
}

.main-container {
  height: 100%;

  .el-header {
    background-color: #00B0F0
  }

  .el-aside {
    background-color: #42C0F8;

    .el-menu-vertical-demo {
      border-right: none;
    }
  }

  .el-header {
    padding: 0;
    display: flex;
    justify-content: space-between;

    img {
      width: 200px;
    }

    .showtime {
      position: absolute;
      top: 20px;
      right: 120px;
      color: aliceblue;
      font-size: 16px;
      font-weight: normal;
    }

    .el-icon-switch-button {
      color: #fff;
    }
  }

  .el-main {
    overflow-y: scroll;
    height: 0;
    background-color: #f2f2f2;
  }

  .el-footer {
    background-color: #eee;
    font-size: 12px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
}

.user-box {
  height: 70px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-top: 1px solid #00B0F0;
  border-bottom: 1px solid #00B0F0;
  user-select: none;

  img {
    width: 35px;
    height: 35px;
    border-radius: 50%;
    background-color: #fff;
    margin-right: 15px;
    object-fit: cover;
  }

  span {
    color: white;
    font-size: 12px;
  }
}</style>
