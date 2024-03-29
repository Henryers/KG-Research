<template>
  <!-- 注册页面的整体盒子 -->
  <div class="background">
    <!-- 注册的盒子 -->
    <div class="reg-box">
      <!-- 标题“后台管理系统(图片)”的盒子 -->
      <div class="title-box">注 册</div>
      <!-- 注册的表单区域 -->
      <!-- el-form 自带校验能力，所以直接自定义规则就行(不用什么自定义监听之类的) -->
      <el-form ref="form" :model="form" label-width="0px" :rules="rulesOBbj">
        <el-form-item prop="username">
          <el-input placeholder="请输入用户名" v-model="form.username"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input type="password" placeholder="请输入密码" v-model="form.password"></el-input>
        </el-form-item>
        <el-form-item prop="repassword">
          <el-input type="password" placeholder="请再次确认密码" v-model="form.repassword"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="btn-reg" @click="registerFn">注册</el-button>
          <el-link class="router" type="info" @click="$router.push('/login')">去登录</el-link>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
// 经验
// 前端绑定数据对象属性名，可以直接跟要调用的功能接口的参数名一致
// 好处是：我们可以吧前端对象（带着同名的属性和前端的值）发给后台
// 比如 axios
// data: {username: this.form.username,
//        password: this.form.password
// }
// -->
// data: this.form   (直接简写，因为属性和值的名字对应)

// 导出是命名导出，所以这里导入要加{}
import { registerAPI } from '@/api'
export default {
  name: 'my-register',
  data () {
    // 自定义校验规则: 两次密码是否一致
    // 注意：必须在data函数里定义此箭头函数，才能确保this.from能使用，从而获取到password的值
    const samePwd = (rule, value, callback) => {
      if (value !== this.form.password) {
        // 如果验证失败，则调用 回调函数时，指定一个 Error 对象。
        callback(new Error('两次输入的密码不一致!'))
      } else {
        // 如果验证成功，则直接调用 callback 回调函数即可。
        callback()
      }
    }
    return {
      form: { // 表单的数据对象
        username: '', // 用户名
        password: '', // 密码
        repassword: '' // 确认密码
      },
      rulesOBbj: { // 表单的规则检验对象
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          {
            pattern: /^[a-zA-Z0-9]{1,10}$/,
            message: '用户名必须是1-10的大小写字母数字',
            trigger: 'blur'
          }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          {
            pattern: /^\S{6,15}$/,
            message: '密码必须是6-15的非空字符',
            trigger: 'blur'
          }
        ],
        repassword: [
          { required: true, message: '请再次输入密码', trigger: 'blur' },
          { pattern: /^\S{6,15}$/, message: '密码必须是6-15的非空字符', trigger: 'blur' },
          { validator: samePwd, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    // 注册：点击事件
    registerFn () {
      // JS兜底校验
      this.$refs.form.validate(async valid => {
        if (valid) {
          // 通过校验，拿到绑定的数据
          console.log(this.form)
          // 1.调用注册接口，通过接口的return request，拿到promise对象
          const { data: res } = await registerAPI(this.form)
          console.log(res)
          console.log('注册失败????byd有病是吧！！！')
          // 2.注册失败，提示用户
          // elementUI还在Vue的原型链上添加了弹窗提示，$message属性
          if (res.status !== 0) {
            console.log('登录失败????byd有病是吧！！！')
            return this.$message.error('6,res都没这个属性...')
          }
          // 3.注册成功，提示用户
          this.$message.success(res.message)
          // 4.路由跳转到登录页面
          this.$router.push('/login')
        } else {
          return false // 阻止默认提交行为（表单下面红色提示）
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

.reg-box {
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
    height: 60px;
    line-height: 60px;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
  }

  .btn-reg {
    width: 100%; // 可以让其占满一行，不用考虑怎么变成块级然后独占一行之类的...
  }
  .router{
    text-align: left;
  }
}
</style>
