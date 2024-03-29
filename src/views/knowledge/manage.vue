<template>
  <div class="main1">
    <div class="box1">
      <div class="title">知识来源</div>
      <div class="Text">电子书籍</div>
      <div class="text">学校官网的图书馆</div>
      <a href="https://zlibrary-asia.se/" target="_blank">Z-Library，全球最大电子书库</a>
      <a href="https://www.pdfdrive.com/" target="_blank">PDF-Drive，提供大量PDF电子书下载</a>
      <a href="https://www.jiumodiary.com/" target="_blank">鸠摩搜书</a>
      <div class="Text">教师课件</div>
      <div class="text">比如老师的ppt、习题资料等等</div>
      <div class="Text">研究论文</div>
      <a href="https://www.cnki.net/" target="_blank">中国知网</a>
      <a href="https://www.webofscience.com/wos/alldb/basic-search" target="_blank">Web of Science</a>
      <div class="text">...</div>
    </div>
    <div class="box2">
      <div class="title">笔记整理</div>
      <div class="Text">Zotero</div>
      <div class="text">pdf论文可以直接存入Zotero</div>
      <div class="Text">Obsidian</div>
      <div class="text">带有许多概念交错连接的知识，可以存入obsidian，建立双向链接，使知识联系更紧密</div>
      <div class="Text">知犀思维导图</div>
      <div class="text">可为大量知识建立大纲，整理好逻辑思路</div>
      <div class="Text">其他</div>
      <div class="text">Notion，OneNote等笔记软件，也不失为一种选择，可以建立知识库，也支持索引查找</div>
    </div>
    <div class="box3">
      <div class="title">格式转换</div>
      <div class="Text">获取PDF</div>
      <div class="text">word、ppt、epub等格式的文件可通过以下方法转为pdf</div>
      <a href="https://www.online-convert.com/" target="_blank">Online convert</a>
      <div class="Text">文字版PDF</div>
      <div class="text">若pdf文件是扫描版，则可通过以下工具转为文字版，存入Zotero后即可进行高亮或者注释操作</div>
      <a href="https://tools.pdf24.org/zh/ocr-pdf#s=1685668470842" target="_blank">PDF-OCR</a>
    </div>
  </div>
</template>

<script>
export default {
  name: 'manage'
}
</script>

<style lang="less" scoped>
.main1 {
  position: relative;
  width: 100%;
  height: 701px;
  background-color: #bc2a2a;
}

.box1 {
  position: absolute;
  left: 70px;
  top: 60px;
  width: 320px;
  height: 580px;
  background-color: #ffffff;
}

.box2 {
  position: absolute;
  left: 420px;
  top: 60px;
  width: 320px;
  height: 580px;
  background-color: #ffffff;
}

.box3 {
  position: absolute;
  left: 770px;
  top: 60px;
  width: 320px;
  height: 580px;
  background-color: #ffffff;
}

.title {
  background-color: #eeeeee;
  font-size: 40px;
  font-family: 优设标题黑;
  line-height: 80px;
  text-align: center;
  color: #f82a2a;
}

.Text {
  font-size: 24px;
  font-family: 楷体;
  font-weight: bold;
  line-height: 30px;
  margin: 30px 30px 10px;
  color: #3e0089;
}

.text {
  font-size: 16px;
  line-height: 20px;
  margin: 5px 30px;
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

a.special {
  font-size: 25px;
  font-weight: bold;
}

.main1 a {
  display: block;
  margin: 0 30px;
  text-decoration: none;
  color: #8018e9;
  font-size: 16px;
  line-height: 25px;
}

.admin {
  position: absolute;
  right: 80px;
  top: 10px;
  width: 60px;
  height: 60px;
  background-image: url(@/assets/images/admin.svg);
  background-size: 60px 60px;
}</style>
