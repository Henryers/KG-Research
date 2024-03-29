<template>
  <div>
    <div class="main1">
      <div class="icon1"></div>
      <div class="header1">supermemo,最好用的知识记忆神器~</div>
      <div class="box1-1">
        <div class="title-1">supermemo简介</div>
        <div class="text">由卡片构成的知识学习记忆软件，通过制作摘录、问答卡片以及定义概念组等方式进行学习记忆</div>
        <div class="jpg1-1"></div>
      </div>
      <div class="box1-2">
        <div class="title-1">supermemo特点</div>
        <div class="text">1. 不同于其他主流的知识管理笔记软件，supermemo没有精美的UI界面，而是注重于对知识进行有效记忆，减少遗忘</div>
        <div class="text">2. 它利用间隔学习等算法，为我们安排学习计划。我们也可以根据知识的重要性，
          利用supermemo的优先级队列来为不同知识设置优先级，从而来让其提供更符合我们需求的复习计划</div>
        <div class="jpg1-2"></div>
      </div>
    </div>
    <div class="main2">
      <div class="icon2"></div>
      <div class="header2">文本导入及相关操作</div>
      <div class="box2-1">
        <div class="title-2">导入功能</div>
        <div class="text2-1">在外部阅读文献时，对想要的字段进行剪切，然后在supermemo中Ctrl+N进行导入，
          会自动在默认概念组下新建摘录元素，存入目标字段</div>
        <div class="jpg2-1"></div>
      </div>
      <div class="box2-2">
        <div class="title-2">基本操作</div>
        <div class="jpg2-2"></div>
        <div class="text2-2">
          1. 新建摘录元素，将所要的句段粘贴进去，之后分段进行阅读
          <br> <br>
          2. 对想要学习记忆的地方进行挖空处理，选中想要挖空的地方，按 Alt + Z 自动生成问答卡片
          <br> <br>
          3. 设置概念组，对不同概念组设置不同的优先级，从而对知识的重要性进行排序归类，
          今后学习中，supermemo会更多地显示这些卡片供您复习
        </div>
      </div>
    </div>
    <div class="main3">
      <div class="icon1"></div>
      <div class="header1">与Zotero联动</div>
      <div class="jpg3-1"></div>
      <div class="box3-2">
        <br>
        <div class="title-2">高亮注释导入</div>
        <br>
        <div class="text">1. 在Zotero中进行高亮批注和注释的操作</div>
        <br>
        <div class="text">2. 我们利用Zotero的API，调用个人Zotero的Library库，获取其中所有的item条目信息，
          并根据需要进行筛选，即可将高亮批注与注释提取出来</div>
        <br>
        <div class="text">3. 提取完成后，将其内容复制，并在supermemo相应位置中进行粘贴即可</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'memory'
}
</script>

<style lang="less" scoped>
.main1 {
  position: relative;
  width: 100%;
  height: 800px;
  background-color: #ffffff;
}

.header1 {
  position: absolute;
  left: 300px;
  width: 700px;
  height: 120px;
  background-color: #ffffff;
  font-size: 40px;
  font-family: 优设标题黑;
  line-height: 120px;
  color: #3e0089;
}

.box1-1 {
  position: absolute;
  left: 100px;
  top: 120px;
  display: inline-block;
  width: 380px;
  height: 580px;
  border-radius: 15px;
  background-color: #F7BC61;
}

.box1-2 {
  position: absolute;
  right: 100px;
  top: 120px;
  display: inline-block;
  width: 560px;
  height: 580px;
  border-radius: 15px;
  background-color: #F7BC61;
}

.title-1 {
  font-size: 30px;
  line-height: 80px;
  font-weight: bold;
  text-align: center;
  color: #ffffff;
}

.title-2 {
  font-size: 30px;
  line-height: 80px;
  font-weight: bold;
  text-align: center;
  color: #e99922;
}

.text {
  margin: 0 40px;
  font-size: 16px;
  line-height: 30px;
}

.main2 {
  position: relative;
  width: 100%;
  height: 900px;
  background-color: #F7BC61;
}

.header2 {
  position: absolute;
  left: 400px;
  width: 600px;
  height: 120px;
  font-size: 40px;
  font-family: 优设标题黑;
  line-height: 120px;
  color: #3e0089;
}

.box2-1 {
  position: absolute;
  left: 100px;
  top: 120px;
  display: inline-block;
  width: 950px;
  height: 250px;
  border-radius: 15px;
  background-color: #ffffff;
}

.text2-1 {
  width: 300px;
  margin: 0 50px;
  font-size: 16px;
  line-height: 30px;
}

.box2-2 {
  position: absolute;
  left: 100px;
  top: 450px;
  display: inline-block;
  width: 950px;
  height: 400px;
  border-radius: 15px;
  background-color: #ffffff;
}

.text2-2 {
  position: absolute;
  right: 0;
  top: 80px;
  width: 380px;
  margin: 0 50px;
  font-size: 16px;
  line-height: 30px;
}

.main3 {
  position: relative;
  width: 100%;
  height: 650px;
  background-color: #fff;
}

.box3-2 {
  position: absolute;
  right: 80px;
  top: 120px;
  display: inline-block;
  width: 480px;
  height: 500px;
  border-radius: 15px;
  background-color: #ffffff;
}

a {
  text-decoration: none;
}

.icon1 {
  position: absolute;
  left: 100px;
  top: 10px;
  width: 100px;
  height: 100px;
  background-image: url(@/assets/images/2supermemo.jpg);
  background-size: 100px 100px;
}

.icon2 {
  position: absolute;
  left: 100px;
  top: 40px;
  width: 150px;
  height: 40px;
  background-image: url(@/assets/images/icon1.jpg);
  background-size: 150px 40px;
}

.jpg1-1 {
  position: absolute;
  left: 40px;
  top: 220px;
  width: 280px;
  height: 300px;
  background-image: url(@/assets/images/1supermemo.jpg);
  background-size: 300px 300px;
  border-radius: 15px;
}

.jpg1-2 {
  position: absolute;
  left: 40px;
  top: 300px;
  width: 480px;
  height: 250px;
  background-image: url(@/assets/images/3supermemo.jpg);
  background-size: 500px 250px;
  border-radius: 15px;
}

.jpg2-1 {
  position: absolute;
  left: 400px;
  top: 90px;
  width: 500px;
  height: 120px;
  background-image: url(@/assets/images/4supermemo.jpg);
  background-size: 500px 120px;
  border-radius: 15px;
}

.jpg2-2 {
  position: absolute;
  left: 50px;
  top: 80px;
  width: 420px;
  height: 280px;
  background-image: url(@/assets/images/5supermemo.jpg);
  background-size: 420px 280px;
  border-radius: 15px;
}

.jpg3-1 {
  position: absolute;
  left: 100px;
  top: 150px;
  width: 480px;
  height: 400px;
  background-image: url(@/assets/images/6supermemo.jpg);
  background-size: 480px 400px;
  border-radius: 15px;
}
</style>
