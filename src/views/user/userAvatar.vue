<template>
  <el-card class="box-card">
    <div slot="header" class="clearfix">
      <span>更换头像</span>
    </div>
    <div>
      <!-- 图片，用来展示用户选择的头像 -->
      <img class="the_img" v-if="!avatar" src="../../assets/images/avatar.jpg" alt="" />
      <img class="the_img" v-else :src="avatar" alt="" />

      <!-- 按钮区域 -->
      <div class="btn-box">
        <input type="file" accept="image/*" style="display: none;" ref="iptRef" @change="onFileChange" />
        <el-button type="primary" icon="el-icon-plus" @click="chooseImg">选择</el-button>
        <el-button type="success" icon="el-icon-upload" :disabled="avatar === ''" @click="uploadFn">上传</el-button>
      </div>
    </div>
  </el-card>
</template>

<script>
import { updateAvatarAPI } from '@/api'
export default {
  name: 'UserAvatar',
  data () {
    return {
      avatar: ''
    }
  },
  methods: {
    // 选择图片->点击事件->让选择框出现
    chooseImg () {
      // 模拟点击input框的行为，通过点击按钮触发另一个input框的事件，移花接木
      // 否则直接调用input框，其样式不太好改
      // this.$refs.iptRef获取的是原生的dom对象，而不是组件对象
      this.$refs.iptRef.click()
    },
    // 在选择框中选择图片后触发的改变事件：预览
    onFileChange (e) {
      // 获取用户选择的文件列表（伪数组）
      const files = e.target.files
      if (files.length === 0) {
        // 没有选择图片(点了取消)
        this.avatar = ''
      } else {
        // 选择了图片
        console.log(files[0])
        // 文件 -> base64字符串进行存储，字符串放到相应数据库中
        // 1. 创建 FileReader 对象
        const fr = new FileReader()
        // 2. 调用 readAsDataURL 函数，读取文件内容
        fr.readAsDataURL(files[0])
        // 3. 监听 fr 的 onload 事件，文件转为base64字符串成功后会触发该事件
        fr.onload = (e) => {
          // 4. 通过 e.target.result 获取到读取的结果，值是字符串（base64 格式的字符串）
          this.avatar = e.target.result
          console.log('avatar')
          console.log(this.avatar)
        }
      }
    },
    // 上传头像
    async uploadFn () {
      console.log('上传头像的响应1')
      console.log(this.avatar)
      const { data: res } = await updateAvatarAPI(this.avatar)
      console.log('上传头像的响应2')
      console.log(res)
      if (res.status !== 0) return this.$message.error(res.message)
      // 更新头像成功
      this.$message.success(res.message)
      // 让vuex的actions再次请求到后台，获取更新后的数据(如果之前后台响应了res状态码和图片地址的话，则可以直接调用mutations)
      this.$store.dispatch('getUserInfoActions')
    }
  }
}
</script>

<style lang="less" scoped>
.btn-box {
  margin-top: 10px;
}

.preview {
  object-fit: cover;
}

.the_img {
  width: 300px;
  height: 300px;
}
</style>
