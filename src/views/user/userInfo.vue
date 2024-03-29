<template>
  <el-card class="box-card">
    <div slot="header" class="clearfix">
      <span>基本资料</span>
    </div>
    <!-- 表单 -->
    <!-- ref相当于为整个表单打上一个id值，可以获取这个dom元素/vc对象 -->
    <el-form
      :model="userForm"
      :rules="userFormRules"
      ref="userFormRef"
      label-width="100px"
    >
      <el-form-item label="登录名称" prop="username">
        <el-input v-model="userForm.username" disabled></el-input>
      </el-form-item>
      <el-form-item label="用户昵称" prop="nickname">
        <el-input
          v-model="userForm.nickname"
          minlength="1"
          maxlength="10"
        ></el-input>
      </el-form-item>
      <el-form-item label="用户邮箱" prop="email">
        <el-input v-model="userForm.email"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitFn">提交修改</el-button>
        <el-button @click="resetFn">重置</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script>
import { updateUserInfoAPI } from '@/api'
export default {
  name: 'UserInfo',
  data () {
    return {
      userForm: {
        username: this.$store.state.userInfo.username, // 默认值用登录后获取到的用户名
        nickname: '',
        email: ''
      },
      // 表单的验证规则对象
      userFormRules: {
        nickname: [
          { required: true, message: '请输入用户昵称', trigger: 'blur' },
          { pattern: /^\S{1,10}$/, message: '昵称必须是1-10位的非空字符串', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入用户邮箱', trigger: 'blur' },
          { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    // 提交修改的点击事件
    submitFn () {
      // 验证表单的合法性
      this.$refs.userFormRef.validate(async valid => {
        if (valid) {
          // 验证成功
          console.log(this.userForm)
          // 根据接口文档指示, 需要携带id(必须)
          this.userForm.id = this.$store.state.userInfo.id // 组件vue内有this，不用import store了
          // 调用更新用户基本信息接口, 把用户在页面输入的新内容传给后台保存
          const { data: res } = await updateUserInfoAPI(this.userForm) // 这里的userForm只有3个属性！没有id!
          if (res.status !== 0) return this.$message.error('更新用户信息失败！')
          // 更新用户信息成功，刷新 Vuex 中的数据
          this.$message.success('更新成功！')
          // 重新让vuex获取下最新的用户数据
          this.$store.dispatch('getUserInfoActions')
        } else {
          // 验证失败
          return false
        }
      })
    },
    // 重置按钮的点击事件
    resetFn () {
      // element-ui提供的重置表单方法(清空this.userForm上的值，vuex里的不能改)，并且还能重置报错提示
      this.$refs.userFormRef.resetFields()
    }
  }
}
</script>

<style lang="less" scoped>
.el-form {
  width: 500px;
}
</style>
