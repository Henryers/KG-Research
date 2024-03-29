<template>
  <div class="background">
    <el-form label-width="0px" class="login-box" :model="form" :rules="rules" ref="loginRef">
      <div class="title-box">登 录</div>
      <el-form-item prop="username">
        <el-input v-model="form.username" placeholder="请输入账号"></el-input>
      </el-form-item>
      <el-form-item  prop="password">
        <el-input type="password" v-model="form.password" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item class="my-el-form-item">
        <el-button type="primary" class="btn-login" @click="loginFn">登录</el-button>
        <el-link type="info" @click="$router.push('/reg')">去注册</el-link>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { loginAPI } from '@/api'
import { mapMutations } from 'vuex'
export default {
  name: 'my-login',
  data () {
    return {
      form: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { pattern: /^[a-zA-Z0-9]{1,10}$/, message: '用户名必须是1-10的字母数字', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { pattern: /^\S{6,15}$/, message: '密码必须是6-15的非空字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    // 把函数映射过来，这里就可以this来调用updateToken这个函数
    ...mapMutations(['updateToken']),
    // 相当于以下代码
    // updateToken(){
    //  this.$store.commit('updateToken')
    // }
    // 注意：这是精髓部分！由于没有传参，因此可以不要dispatch，直接通过vc组件去commit!
    // 登录->点击事件
    loginFn () {
      // JS兜底校验(防止用户没输入或输入不合法，之后才去数据库看看是否信息匹配)
      this.$refs.loginRef.validate(async valid => {
        if (valid) {
          // 1.调用注册接口，通过接口的return request，拿到promise对象
          const { data: res } = await loginAPI(this.form) // 只拿到对象中data属性的部分(解构赋值)
          console.log(res)
          // 2.登录失败，提示用户
          // elementUI还在Vue的原型链上添加了弹窗提示，$message属性
          if (res.status !== 0) {
            console.log('啊？？？')
            return this.$message.error(res.message)
          }
          // 3.登录成功，提示用户
          this.$message.success(res.message)
          // 4.提交给mutations把token字符串保存到vuex中
          this.updateToken(res.token)
          // 5.跳转到首页
          this.$router.push('/')
        } else {
          return false
        }
      })
    }
  }
}
</script>

<style lang="less" scoped>
.background {
  /* css自制动态背景 */
  margin: 0;
  min-height: 100vh;
  background-color: #d5f2f9;
  background-image:
    radial-gradient(closest-side, rgba(33, 240, 234, 1), rgba(18, 235, 228, 0)),
    radial-gradient(closest-side, rgba(14, 179, 244, 1), rgba(18, 235, 228, 0)),
    radial-gradient(closest-side, rgba(103, 185, 243, 1), rgba(18, 235, 228, 0)),
    radial-gradient(closest-side, rgba(126, 251, 232, 1), rgba(18, 235, 228, 0)),
    radial-gradient(closest-side, rgba(61, 211, 248, 1), rgba(18, 235, 228, 0));
  background-size:
    130vmax 130vmax,
    100vmax 100vmax,
    80vmax 80vmax,
    160vmax 60vmax,
    90vmax 140vmax;
  background-position:
    -80vmax -80vmax,
    60vmax 30vmax,
    30vmax -10vmax,
    20vmax 70vmax,
    -30vmax 10vmax;
  background-repeat: no-repeat;
  animation: move-forever 20s linear infinite;
}

.background::after {
  content: '';
  display: block;
  position: fixed;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

/* 设置0% 25% 50% 75% 100% 五个部分的关键帧，通过自定义好css的关键帧规则，实现平滑过渡效果 */
@keyframes move-forever {

  0%,
  100% {
    background-size:
      130vmax 130vmax,
      100vmax 100vmax,
      80vmax 80vmax,
      160vmax 60vmax,
      90vmax 140vmax;
    background-position:
      -80vmax -80vmax,
      60vmax 30vmax,
      30vmax -10vmax,
      20vmax 70vmax,
      -30vmax 10vmax;
  }

  25%,
  75% {
    background-size:
      130vmax 90vmax,
      70vmax 100vmax,
      100vmax 90vmax,
      120vmax 60vmax,
      90vmax 110vmax;
    background-position:
      -30vmax -50vmax,
      60vmax 50vmax,
      50vmax 10vmax,
      20vmax 70vmax,
      -20vmax 0vmax;
  }

  50% {
    background-size:
      130vmax 130vmax,
      60vmax 100vmax,
      80vmax 80vmax,
      160vmax 70vmax,
      60vmax 140vmax;
    background-position:
      30vmax -30vmax,
      60vmax 30vmax,
      70vmax -10vmax,
      20vmax 170vmax,
      0vmax -20vmax;
  }
}

.login-box {
  z-index: 10;
  width: 400px;
  height: 340px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  padding: 0 30px;
  box-sizing: border-box;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: #afebf0 0 0 100px;

  .title-box {
    height: 100px;
    line-height: 100px;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
  }

  // .my-el-form-item {
  //   width: 300px;
  //   margin-right: 0px;
  // }

  .btn-login {
    width: 100%;
  }
}
</style>
