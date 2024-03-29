<template>
  <div>
    <div class="main">
      <div class="icon"></div>
      <div class="main-title1">知识图谱的关联与</div>
      <div class="main-title2">图形化展示研究</div>
      <div class="main-title3">Knowledge Connect</div>
      <div class="jpg1"></div>
    </div>
    <div class="banner-white">
      <div class="banner-title-r">知识项目</div>
      <div class="banner-content-r">医疗知识图谱，展示疾病、症状等方面的联系，还有问答AI，为您提供良好服务！</div>
      <el-link class="banner-more-r" type="primary" :underline="false" @click="$router.push('/chart2')">了解更多>></el-link>
      <div class="jpg2"></div>
    </div>
    <div class="banner-grey">
      <div class="banner-title-l">知识管理</div>
      <div class="banner-content-l">各种知识管理软件与方法，为您打造独特的个人知识黄金库！</div>
      <el-link class="banner-more-l" type="primary" :underline="false" @click="$router.push('/manage')">了解更多>></el-link>
      <div class="jpg3"></div>
    </div>
    <div class="banner-white">
      <div class="banner-title-r">知识记忆</div>
      <div class="banner-content-r">supermemo的灵活使用，帮你做好渐进学习，最大程度帮你记忆重要知识！</div>
      <el-link class="banner-more-r" type="primary" :underline="false" @click="$router.push('/memory')">了解更多>></el-link>
      <div class="jpg4"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'my-home'
}
</script>

<style lang="less" scoped>
@keyframes bgAnimation {
  0% {
    background-position: 0 50%;
  }

  50% {
    background-position: 100% 50%;
  }

  100% {
    background-position: 0 50%;
  }
}

.main {
  position: relative;
  height: 650px;
  justify-content: center;
  align-items: center;
  background: linear-gradient(130deg, #48029e, #3904c0, #140377, #3a0485, #5704bc, #3d07d2, #370376, #1d0262);
  background-size: 600%;
  animation: bgAnimation 15s linear infinite;
}

.main-title1 {
  position: absolute;
  width: 500px;
  height: 80px;
  left: 100px;
  top: 250px;
  font-size: 50px;
  font-weight: 600;
  line-height: 70px;
  text-align: left;
  color: #ffffff;
}

.main-title2 {
  position: absolute;
  width: 500px;
  height: 80px;
  left: 100px;
  top: 320px;
  font-size: 50px;
  font-weight: 600;
  line-height: 70px;
  text-align: left;
  color: #ffffff;
}

.main-title3 {
  position: absolute;
  width: 500px;
  height: 50px;
  left: 100px;
  top: 420px;
  font-size: 30px;
  font-weight: 400;
  line-height: 50px;
  text-align: left;
  color: #ffffff;
}

.banner-white {
  position: relative;
  height: 500px;
  background-color: #ffffff;
}

.banner-grey {
  position: relative;
  height: 500px;
  background-color: #ededed;
}

.banner-title-l {
  position: absolute;
  width: 300px;
  height: 80px;
  left: 100px;
  top: 80px;
  font-size: 50px;
  font-weight: 600;
  line-height: 70px;
  color: #4e0894;
}

.banner-content-l {
  position: absolute;
  width: 400px;
  left: 100px;
  top: 200px;
  font-size: 25px;
  font-weight: 500;
  line-height: 50px;
  color: #000000;
}

.banner-title-r {
  position: absolute;
  width: 300px;
  height: 80px;
  left: 600px;
  top: 80px;
  font-size: 50px;
  font-weight: 600;
  line-height: 70px;
  color: #4e0894;
}

.banner-content-r {
  position: absolute;
  width: 450px;
  left: 600px;
  top: 200px;
  font-size: 25px;
  font-weight: 500;
  line-height: 50px;
  color: #000000;
}

.banner-more-l {
  position: absolute;
  width: 200px;
  height: 50px;
  left: 55px;
  top: 360px;
  font-size: 20px;
  font-weight: 500;
  line-height: 50px;
  color: #6b14e5;
}

.banner-more-r {
  position: absolute;
  width: 200px;
  height: 50px;
  left: 555px;
  top: 360px;
  font-size: 20px;
  font-weight: 500;
  line-height: 50px;
  color: #6b14e5;
}

.end {
  position: relative;
  height: 100px;
  background-color: #000000;
}

.end-left {
  position: absolute;
  left: 100px;
  display: inline-block;
  height: 100px;
  width: 600px;
  font-size: 20px;
  font-weight: 500;
  text-align: left;
  line-height: 100px;
  color: aliceblue;
}

.end-right {
  position: absolute;
  right: 100px;
  display: inline-block;
  height: 100px;
  width: 200px;
  font-size: 20px;
  font-weight: 500;
  text-align: right;
  line-height: 100px;
  color: aliceblue;
}

a {
  text-decoration: none;
}

.top-right a {
  width: 200px;
  padding: 0 50px;
  text-decoration: none;
  color: #000000;
  border-right: 1px solid #ffffff;
  font-size: 20px;
  font-weight: 400;
  line-height: 80px;
  color: aliceblue;
}

.icon {
  position: absolute;
  left: 100px;
  top: 100px;
  width: 100px;
  height: 100px;
  background-image: url(@/assets/images/icon.svg);
  background-size: 100px 100px;
}

.jpg1 {
  position: absolute;
  float: right;
  background-image: url(@/assets/images/graph1.jpg);
  width: 480px;
  height: 380px;
  background-size: 480px 380px;
  top: 100px;
  right: 100px;
  border-radius: 10px;
}

.jpg2 {
  position: absolute;
  float: left;
  background-image: url(@/assets/images/project2.jpg);
  width: 450px;
  height: 350px;
  background-size: 450px 350px;
  top: 60px;
  left: 100px;
  border-radius: 10px;
}

.jpg3 {
  position: absolute;
  float: right;
  background-image: url(@/assets/images/control3.jpg);
  width: 450px;
  height: 350px;
  background-size: 450px 350px;
  top: 60px;
  right: 100px;
  border-radius: 10px;
}

.jpg4 {
  position: absolute;
  float: right;
  background-image: url(@/assets/images/supermemo4.jpg);
  width: 450px;
  height: 350px;
  background-size: 450px 350px;
  top: 60px;
  left: 100px;
  border-radius: 10px;
}
</style>
