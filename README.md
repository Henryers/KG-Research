# KG-Rearch —— 知识图谱的关联与图形化展示研究

## 1. 项目简介
本项目致力于研究知识图谱，主要从网上数据集、个人笔记和其他相关资料中获取数据，探索其中的实体和之间的关系，并提取出三元组存储到图数据库neo4j中。最终导出json数据并利用echarts在前端做图形化展示

## 2. 功能介绍
### 2.1 基本登录注册等功能
登录该系统时，用户可以注册一个账号后进行登录，在个人中心选项卡中，用户可以进行更换头像、修改密码等个人信息的操作。点击右上角可退出登录。
### 2.1 图数据库展示
在前端网页中，用户点击相关专题的全屏展示，会以图的形式展示该部分数据集下的实体以及之间的密切关联
### 2.2 简单问答
用户询问对应专题中的内容，系统会给出相应的回答，不过数据集大小有限，超出语料库内容的问题，系统暂时无法给予处理。
### 2.3 图表展示
除了图结构，用户点击数据图表还可以查看其他结构的数据展示分布，比如饼图、折线图、柱状图的展现形式。
### 2.4 知识检索
用户点击知识检索板块，在输入框中进行节点搜索，会展示出以该节点为中心的所有关联节点，并以图的方式呈现在下方。
同时，在图的右侧有这些节点对应的列表，点击列表中对应的内容，会进行节点关联搜索跳转，从而查看以相邻节点为中心的关系图。
### 2.5 自制图谱
用户在相应输入框中可以进行节点和关系的增删改查，同时会在右侧展现对应的自制图谱关系图，实现diy自制图谱

## 3. 技术实现
技术栈： `python + neo4j + mysql + vue2 + node.js`
### 3.1 数据收集和预处理

### 3.2 实体关系抽取

### 3.3 构建三元组，存入neo4j

### 3.4 导出json数据进行关系图构建

### 3.5 前端图谱展示 + 其他功能

## 4. 总结与展望
本项目为作者`大一 —— 大二学年的大创项目`，基本实现了知识图谱的数据采集、处理、存储过程并进行可视化展示，取得较好成果。当然也有很多不足之处，如智能问答并没有结合深度学习展开，vue2技术栈现已有些过时等等。由于水平有限，并没有做得多么深入，不过还是希望这个较为简单的项目，能对初步踏入知识图谱领域研究的人带来帮助。最后，如果觉得本项目对你有帮助的话，求求点个star吧，谢谢了~