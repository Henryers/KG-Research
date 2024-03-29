<template>
  <el-card>
    <div style="text-align: center; vertical-align: middle;">
      <el-input class="myInput" v-model="input" type="text" @keyup.enter.native="search1"></el-input>
      <el-button type="primary" @click="search1">点击查询</el-button>
    </div>
    <!-- 渲染图表的容器 -->
    <div style="display: flex;">
      <div id="chart1" style="display:flex; align-items: center; justify-content: center;"></div>
      <div style="display: flex; align-items: center; vertical-align: center;">
        <div class="ver_mid">
          <ul id="mylist" style="display: inline-block;">
            <li>暂无节点</li>
          </ul>
        </div>
      </div>
      <div id="info" style=" align-items: center; justify-content: center;">
        <div class="node_title">节点介绍</div>
        <div class="node_name"></div>
        <div class="node_info"></div>
      </div>
    </div>
  </el-card>
</template>

<script>
import * as echarts from 'echarts'
import { getGraph1API, getGraph2API } from '@/api'

export default {
  name: 'search',
  data () {
    return {
      graph: {},
      graph1: {},
      input: '',
      mylist: null
    }
  },
  mounted () {
    this.mylist = document.getElementById('mylist')
    // const this.graph1 = undefined
    this.getGraphData()
  },
  methods: {
    async getGraphData () {
      const { data: res1 } = await getGraph1API()
      const { data: res2 } = await getGraph2API()
      // 拿到 节点json数据 和 关系数组
      this.graph = {
        nodes: res1.kg_medical,
        relationships: []
      }
      const rels_check = res2.rels_check
      const rels_symptom = res2.rels_symptom
      const rels_acompany = res2.rels_acompany
      const rels_recommanddrug = res2.rels_recommanddrug
      const rels_commonddrug = res2.rels_commonddrug
      const rels_noteat = res2.rels_noteat
      const rels_doeat = res2.rels_doeat
      const rels_recommandeat = res2.rels_recommandeat
      const rels_drug_producer = res2.rels_drug_producer
      const rels_category = res2.rels_category
      const rels_department = res2.rels_department
      const names = [rels_check, rels_symptom, rels_acompany, rels_recommanddrug, rels_commonddrug,
        rels_noteat, rels_doeat, rels_recommandeat, rels_drug_producer, rels_category, rels_department]
      // 遍历关系数组来构建关系
      for (let i = 0; i < names.length; i++) {
        for (let j = 0; j < names[i].length; j++) { // 遍历检查 rels_nation/rels_gender 等，拿到元素的第一个值(sub)
          let l1 = 0
          let l2 = 0
          for (let k = 0; k < this.graph.nodes.length; k++) {
            if (this.graph.nodes[k].n.properties.name === names[i][j][0]) {
              // 每个[0]元素跟节点数组中的name对应，取出节点数组对应节点的identity,将其赋值给k
              l1 = this.graph.nodes[k].n.identity
              // 找第二个元素，也是用k遍历整个nodes数组，找到后将其identity赋值给l2
              for (let k = 0; k < this.graph.nodes.length; k++) {
                if (this.graph.nodes[k].n.properties.name === names[i][j][1]) {
                  l2 = this.graph.nodes[k].n.identity
                  if (l1 !== l2) { // 不相等才进行相连，自己连自己没意义！！！
                    this.graph.relationships.push({ source: l1, target: l2, name: names[i].slice(5) })
                    // l1,l2分别作为source和target的值
                  }
                }
              }
            }
          }
        }
      }

      // 创建一个空的categories数组
      const categories = []

      // 遍历节点数据
      this.graph.nodes.forEach(function (node) {
        const label = node.n.labels[0] // 注意：这里假设每个节点的"label"属性只有一个元素
        let categoryIndex = categories.findIndex(function (category) {
          return category.name === label
        })

        // 如果当前类别不存在，则添加到categories数组中
        if (categoryIndex === -1) {
          categories.push({ name: label })
          categoryIndex = categories.length - 1 // 使用新添加的类别索引
        }
        node.category = categoryIndex
      })

      console.log('完整的图数据：')
      console.log(this.graph)
      // return this.graph
    },
    // 抽取出函数，上面的点击和Enter事件都能触发下面相同的回调函数

    search1 () {
      this.mylist.innerHTML = ''
      this.graph1 = {}
      console.log(this.mylist)
      console.log('点击了button，回调的形参input.value如下:')
      console.log(this.input)
      const nodename = this.input
      console.log('最开始点击input后，初始化的this.graph')
      console.log(this.graph)
      for (let i = 0; i < this.graph.nodes.length; i++) {
        if (this.graph.nodes[i].n.properties.name === nodename) { // 找到当前主节点
          console.log('search1()找到了该主节点了！')
          console.log(this.graph.nodes[i].n.identity)
          // 找到就写入详细信息里面
          document.getElementsByClassName('node_name')[0].innerHTML = this.graph.nodes[i].n.properties.name
          if (this.graph.nodes[i].n.properties.desc === undefined) {
            document.getElementsByClassName('node_info')[0].innerHTML = '暂无详细介绍'
          } else {
            document.getElementsByClassName('node_info')[0].innerHTML = this.graph.nodes[i].n.properties.desc
          }
          this.graph1 = {
            nodes: [
              {
                id: this.graph.nodes[i].n.identity,
                name: this.graph.nodes[i].n.properties.name,
                category: this.graph.nodes[i].n.labels[0]
              }
            ],
            links: []
          }
          // 找到当前主节点的相邻节点，构建他们的集合
          // eslint-disable-next-line no-var
          var set = []
          for (let j = 0; j < this.graph.relationships.length; j++) {
            // console.log(this.graph.relationships[j].source)
            if (this.graph.relationships[j].source === this.graph.nodes[i].n.identity ||
              this.graph.relationships[j].target === this.graph.nodes[i].n.identity) {
              // console.log('执行一下啊！')
              if (!set.includes(this.graph.relationships[j].source)) {
                set.push(this.graph.relationships[j].source)
              }
              if (!set.includes(this.graph.relationships[j].target)) {
                set.push(this.graph.relationships[j].target)
              }
            }
          }
          // 看看我的set集合
          console.log('myfunc()的set集合')
          console.log(set)
          // 根据找到的set集合中的节点，写入this.graph1
          for (let j = 0; j < set.length; j++) {
            for (let k = 0; k < this.graph.nodes.length; k++) {
              if (this.graph.nodes[k].n.identity === set[j] && k !== i) { // 主节点已写入，不要重复写入this.graph1
                this.graph1.nodes.push({
                  id: this.graph.nodes[k].n.identity,
                  name: this.graph.nodes[k].n.properties.name,
                  category: this.graph.nodes[k].n.labels[0]
                })
              }
            }
          }
          // 根据找到的set集合中的节点，写入this.graph1的links，主节点的source为0
          for (let j = 1; j < set.length; j++) {
            this.graph1.links.push({ source: 0, target: j, name: '翻译' })
          }
          console.log('myfunc()的graph1')
          console.log(this.graph1)
          console.log(this.graph1.nodes)
          console.log(this.graph1.nodes[0])
        }
      }

      // 创建一个空的categories1数组
      const categories1 = []

      // 遍历节点数据
      this.graph.nodes.forEach(function (node) {
        const label = node.n.labels[0] // 注意：这里假设每个节点的"label"属性只有一个元素
        let categoryIndex = categories1.findIndex(function (category) {
          return category.name === label
        })

        // 如果当前类别不存在，则添加到categories数组中
        if (categoryIndex === -1) {
          categories1.push({ name: label })
          categoryIndex = categories1.length - 1 // 使用新添加的类别索引
        }
        node.category = categoryIndex
      })

      if (this.graph1 === undefined) {
        alert('未找到该节点！')
      } else {
        // 根据输入的节点名，构建它和它相邻的节点关系图谱
        const chart = echarts.init(document.getElementById('chart1')) // 拿到div的id,然后用js写入数据到chart里(见代码最后一行)
        // 配置项(即配置相关信息)
        const option = {
          // 1.上方标题+动画
          title: {
            text: 'Search_Graph',
            subtext: 'my layout',
            left: 'center'
          },
          animationDurationUpdate: 1500,
          animationEasingUpdate: 'quinticInOut',
          // 2.侧边图例
          legend: {
            orient: 'horizontal',
            top: '60px'
          },
          // 3.悬停显示信息
          tooltip: {
            show: true, // 显示提示框
            formatter: function (params, ticket) {
              if (params.dataType === 'node') {
                return 'id:' + params.data.id + '<br>名称:' + params.data.name
              } else if (params.dataType === 'edge') {
                return '关系: ' + params.data.name // 只能写默认name了，表示a>b，醉了...
              }
              // 根据不同的数据类型(一个是节点，一个是关系线)，显示不同的提示信息
            }
          },
          // 4.图中配置
          series: {
            // 力导向force布局-基本配置
            draggable: true,
            type: 'graph',
            layout: 'force',
            roam: true,
            force: {
              repulsion: 200, // 节点之间斥力的大小
              edgeLength: [40, 100] // 边的长度
            },
            // 4.1 后端json数据+类别
            data: this.graph1.nodes,
            symbolSize: 40,
            categories: categories1,
            // 4.2 关系线
            links: this.graph1.links.map(function (edge) {
              return {
                source: edge.source,
                target: edge.target, // 指明是哪两个节点的关系要加样式(因此数组中有多少组关系就设置多少个连接线样式)
                name: edge.name,
                lineStyle: {
                  opacity: 0.9,
                  width: 2,
                  color: 'source',
                  curveness: 0.3
                },
                symbol: 'arrow' // 箭头
              }
            }),
            // 4.3 标签
            label: {
              show: true,
              position: 'center', // 并将标签显示在节点的右侧,快废弃了...
              formatter: function (params, ticket) {
                return params.data.name.slice(0, 5).concat('...')
                // 标签名太长了，默认只显示前5个字，具体信息悬浮可见
              }
            },
            // 2.4 强调
            emphasis: {
              focus: 'adjacency',
              lineStyle: {
                width: 10
              }
            }
          }
        }

        // 使用刚指定的配置项和数据显示图表，包括基本的图信息，以及动画平滑效果等
        chart.setOption(option)

        // 当浏览器窗口大小改变时，调用 ECharts 的 `resize` 方法重新布局和渲染
        window.onresize = function () {
          chart.resize()
        }

        // 加载chart1图表成功才能加载列表，否则列表单独存在没意义！ （md内部类？！）
        this.mylist = document.getElementById('mylist')
        const data = this.graph1.nodes.map((item) => item.name)

        data.forEach((item) => {
          const li = document.createElement('li')
          li.classList.add('li') // 添加CSS类名  byd不行？？？！！！
          // 那就强行内联！！！byd谁都别拦我加样式！！！
          li.style.listStyle = 'none' // js要驼峰命名法
          li.style.width = '100px'
          li.style.height = '20px'
          li.style.lineHeight = '20px'
          li.style.margin = '3px'
          li.style.borderRadius = '5px'
          li.style.backgroundColor = 'rgb(119, 212, 101)' // 设置背景颜色
          li.textContent = item.slice(0, 5).concat('...')
          li.addEventListener('click', (event) => {
            this.search2(item)
          })
          console.log(this.mylist)
          this.mylist.appendChild(li)
        })
      }
    },

    search2 (value) {
      this.mylist.innerHTML = ''
      console.log(this.mylist)
      console.log('点击了mylist，回调的search2()的形参value如下:')
      console.log(value)
      console.log(this.mylist.length)
      console.log('上面byd长度怎么不为0！！！')
      const nodename = value
      for (let i = 0; i < this.graph.nodes.length; i++) {
        if (this.graph.nodes[i].n.properties.name === nodename) { // 找到当前主节点
          console.log('search2()找到了该主节点了！')
          console.log(this.graph.nodes[i].n.identity)
          // 找到就写入详细信息里面
          document.getElementsByClassName('node_name')[0].innerHTML = this.graph.nodes[i].n.properties.name
          this.graph1 = {
            nodes: [
              {
                id: this.graph.nodes[i].n.identity,
                name: this.graph.nodes[i].n.properties.name,
                category: this.graph.nodes[i].n.labels[0]
              }
            ],
            links: []
          }
          // 找到当前主节点的相邻节点，构建他们的集合
          const set = []
          for (let j = 0; j < this.graph.relationships.length; j++) {
            if (this.graph.relationships[j].source === this.graph.nodes[i].n.identity ||
              this.graph.relationships[j].target === this.graph.nodes[i].n.identity) {
              if (!set.includes(this.graph.relationships[j].source)) {
                set.push(this.graph.relationships[j].source)
              }
              if (!set.includes(this.graph.relationships[j].target)) {
                set.push(this.graph.relationships[j].target)
              }
            }
          }
          // 根据找到的set集合中的节点，写入this.graph1
          for (let j = 0; j < set.length; j++) {
            for (let k = 0; k < this.graph.nodes.length; k++) {
              if (this.graph.nodes[k].n.identity === set[j] && k !== i) { // 主节点已写入，不要重复写入this.graph1
                this.graph1.nodes.push({
                  id: this.graph.nodes[k].n.identity,
                  name: this.graph.nodes[k].n.properties.name,
                  category: this.graph.nodes[k].n.labels[0]
                })
              }
            }
          }
          // 根据找到的set集合中的节点，写入this.graph1的links，主节点的source为0
          for (let j = 1; j < set.length; j++) {
            this.graph1.links.push({ source: 0, target: j, name: '翻译' })
          }
          console.log('search2()找到了该主节点，才能打印以下this.graph1：')
          console.log(this.graph1)
          console.log(this.graph1.nodes)
          console.log(this.graph1.nodes[0])
        }
      }

      // 创建一个空的categories1数组
      const categories1 = []

      // 遍历节点数据
      this.graph.nodes.forEach(function (node) {
        const label = node.n.labels[0] // 注意：这里假设每个节点的"label"属性只有一个元素
        let categoryIndex = categories1.findIndex(function (category) {
          return category.name === label
        })

        // 如果当前类别不存在，则添加到categories数组中
        if (categoryIndex === -1) {
          categories1.push({ name: label })
          categoryIndex = categories1.length - 1 // 使用新添加的类别索引
        }
        node.category = categoryIndex
      })

      if (this.graph1 === undefined) {
        alert('未找到该节点！')
      } else {
        // 根据输入的节点名，构建它和它相邻的节点关系图谱
        const chart = echarts.init(document.getElementById('chart1')) // 拿到div的id,然后用js写入数据到chart里(见代码最后一行)
        // 配置项(即配置相关信息)
        const option = {
          // 1.上方标题+动画
          title: {
            text: 'Search_Graph',
            subtext: 'my layout',
            left: 'center'
          },
          animationDurationUpdate: 1500,
          animationEasingUpdate: 'quinticInOut',
          // 2.侧边图例
          legend: {
            orient: 'horizontal',
            top: '60px'
          },
          // 3.悬停显示信息
          tooltip: {
            show: true, // 显示提示框
            formatter: function (params, ticket) {
              if (params.dataType === 'node') {
                return 'id:' + params.data.id + '<br>名称:' + params.data.name
              } else if (params.dataType === 'edge') {
                return '关系: ' + params.data.name // 只能写默认name了，表示a>b，醉了...
              }
              // 根据不同的数据类型(一个是节点，一个是关系线)，显示不同的提示信息
            }
          },
          // 4.图中配置
          series: {
            // 力导向force布局-基本配置
            draggable: true,
            type: 'graph',
            layout: 'force',
            roam: true,
            force: {
              repulsion: 200, // 节点之间斥力的大小
              edgeLength: [40, 100] // 边的长度
            },
            // 4.1 后端json数据+类别
            data: this.graph1.nodes,
            symbolSize: 40,
            categories: categories1,
            // 4.2 关系线
            links: this.graph1.links.map(function (edge) {
              return {
                source: edge.source,
                target: edge.target, // 指明是哪两个节点的关系要加样式(因此数组中有多少组关系就设置多少个连接线样式)
                name: edge.name,
                lineStyle: {
                  opacity: 0.9,
                  width: 2,
                  color: 'source',
                  curveness: 0.3
                },
                symbol: 'arrow' // 箭头
              }
            }),
            // 4.3 标签
            label: {
              show: true,
              position: 'center', // 并将标签显示在节点的右侧,快废弃了...
              formatter: function (params, ticket) {
                return params.data.name.slice(0, 5).concat('...')
                // 标签名太长了，默认只显示前5个字，具体信息悬浮可见
              }
            },
            // 2.4 强调
            emphasis: {
              focus: 'adjacency',
              lineStyle: {
                width: 10
              }
            }
          }
        }

        // 使用刚指定的配置项和数据显示图表，包括基本的图信息，以及动画平滑效果等
        chart.setOption(option)

        // 当浏览器窗口大小改变时，调用 ECharts 的 `resize` 方法重新布局和渲染
        window.onresize = function () {
          chart.resize()
        }

        // 加载chart1图表成功才能加载列表，否则列表单独存在没意义！ （md内部类？！）
        const mylist = document.getElementById('mylist')
        const data = this.graph1.nodes.map((item) => item.name)

        data.forEach((item) => {
          const li = document.createElement('li')
          li.classList.add('li') // 添加CSS类名  byd不行？？？！！！
          // 那就强行内联！！！byd谁都别拦我加样式！！！
          li.style.listStyle = 'none' // js要驼峰命名法
          li.style.width = '100px'
          li.style.height = '20px'
          li.style.lineHeight = '20px'
          li.style.margin = '3px'
          li.style.borderRadius = '5px'
          li.style.backgroundColor = 'rgb(119, 212, 101)' // 设置背景颜色
          li.textContent = item.slice(0, 5).concat('...')
          li.addEventListener('click', () => {
            // 这里是点击事件的回调函数
            console.log('点击了ul其中一个li:', item)
            this.search2(item)
          })
          mylist.appendChild(li)
        })
      }
    }
  }
}
</script>

<style lang="less" scoped>
#chart1 {
  margin: 40px;
  width: 686px;
  height: 500px;
}

.myInput {
  margin: 20px 20px 0 0;
  width: 600px;
  font-size: 14px;
  border-radius: 1px;
  box-shadow: 0 0 5px #ccc;
  border: none;
}

button {
  font-size: 14px;
}

.node_title {
  margin-top: 30px;
  float: right;
  padding: 30px 20px 0 20px;
  width: 300px;
  height: 50px;
  background-color: rgba(11, 186, 230, 0.688);
  text-align: center;
  font-size: 25px;
  font-weight: bold;
  color: #ffffff;
  box-sizing: content-box;
  clear: right;
  /* 每行只有一个元素，清除右浮动 */
}

.node_name {
  float: right;
  padding: 30px 20px 0 20px;
  background-color: rgba(11, 186, 230, 0.688);
  width: 300px;
  height: 50px;
  font-size: 20px;
  color: #ffffff;
  border-radius: 1px;
  box-sizing: content-box;
  border: none;
  clear: right;
  /* 每行只有一个元素，清除右浮动 */
}

.node_info {
  float: right;
  padding: 30px 20px 0 20px;
  background-color: rgba(11, 186, 230, 0.688);
  width: 300px;
  height: 350px;
  font-size: 16px;
  color: #ffffff;
  border-radius: 1px;
  box-sizing: content-box;
  border: none;
  overflow-y: scroll;
  scrollbar-width: none;
  -ms-overflow-style: none;
  clear: right;
  /* 每行只有一个元素，清除右浮动 */
}

::-webkit-scrollbar {
  display: none
}

.ver_mid {
  display: flex;
  margin-top: 60px;
  height: 400px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

ul {
  margin: 10px;
  vertical-align: middle;
  overflow-y: scroll;
  scrollbar-width: thin;
}

li {
  list-style: none;
  width: 100px;
  height: 20px;
  line-height: 20px;
  margin: 3px;
  background-color: rgb(119, 212, 101);
  border-radius: 5px;
}

.li {
  list-style: none;
  width: 100px;
  height: 20px;
  line-height: 20px;
  margin: 3px;
  background-color: rgb(119, 212, 101);
  border-radius: 5px;
}

li:hover {
  background-color: rgb(126, 246, 166);
  cursor: pointer;
}

.li:hover {
  background-color: rgb(126, 246, 166);
  cursor: pointer;
}
</style>
