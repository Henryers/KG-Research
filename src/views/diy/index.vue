<template>
  <el-card>
    <div style="width: 650px; height: 600px; display: inline-block; vertical-align: top;">
      <div style="margin: 20px">
        <span>添加节点</span>
        <el-input class="myInput" v-model="node0" ref="node0" placeholder="请输入节点"></el-input>
        <el-button type="primary" @click="add_node" ref="btn1">添加</el-button>
      </div>
      <div style="margin: 20px">
        <span>添加关系</span>
        <el-input class="myInput" v-model="node1" ref="node1" placeholder="请输入节点1"></el-input>
        <el-input class="myInput" v-model="rels" ref="rels" placeholder="请输入关系"></el-input>
        <el-input class="myInput" v-model="node2" ref="node2" placeholder="请输入节点2"></el-input>
        <el-button type="primary" @click="add_rel" ref="btn2">添加</el-button>
      </div>
      <div style="margin: 20px">
        <span>删除节点</span>
        <el-input class="myInput" v-model="del_node0" ref="del_node0" placeholder="请输入节点"></el-input>
        <el-button type="primary" @click="del_node" ref="btn3">删除</el-button>
      </div>
      <div style="margin: 20px">
        <span>删除关系</span>
        <el-input class="myInput" v-model="del_node1" ref="del_node1" placeholder="请输入节点1"></el-input>
        <el-input class="myInput" v-model="del_node2" ref="del_node2" placeholder="请输入节点2"></el-input>
        <el-button type="primary" @click="del_rel" ref="btn4">删除</el-button>
      </div>
    </div>
    <!-- 渲染图表的容器 -->
    <div ref="graph1" style="width: 450px; height: 600px; display: inline-block;"></div>
  </el-card>
</template>

<script>
import * as echarts from 'echarts'
export default {
  name: 'Diy',
  data () {
    return {
      node0: '',
      node1: '',
      node2: '',
      rels: '',
      btn1: '',
      btn2: '',
      // 删除
      del_node0: '',
      del_node1: '',
      del_node2: '',
      btn3: '',
      btn4: '',
      graph: {
        nodes: [],
        links: []
      },
      rels_arr: [],
      myChart: '',
      option: {}
    }
  },
  mounted () {
    // 在dom元素挂载后，才能获取到元素对象
    // 新增
    this.btn1 = this.$refs.btn1
    this.btn2 = this.$refs.btn2
    // 删除
    this.btn3 = this.$refs.btn3
    this.btn4 = this.$refs.btn4
  },
  methods: {
    // 1. 添加节点
    add_node () {
      let judge = true
      for (let i = 0; i < this.graph.nodes.length; i++) {
        if (this.graph.nodes[i].properties.name === this.node0) {
          alert('节点已存在！')
          judge = false
        }
      }
      if (judge) {
        this.graph.nodes.push({
          identity: this.graph.nodes.length,
          labels: ['Person'],
          properties: { name: this.node0 }
        })
      }
      if (this.myChart === '') {
        this.myChart = echarts.init(this.$refs.graph1)
      }
      this.option = {
      // 1.上方标题+动画
        title: {
          text: 'Words_Graph',
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
          // 可能是echart封装好的，这里的data就是一个节点对象，表示鼠标移动到当前位置的节点
            if (params.dataType === 'node') {
              return 'id:' + params.data.identity + '<br>名称:' + params.data.properties.name
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
          data: this.graph.nodes,
          symbolSize: 40,
          // categories: categories,
          // 4.2 关系线
          links: this.graph.links.map(function (edge) {
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
              console.log(params.data)
              if (params.data.properties.name.length <= 5) {
                return params.data.properties.name
              } else {
                return params.data.properties.name.slice(0, 5).concat('...')
              // 标签名太长了，默认只显示前5个字，具体信息悬浮可见
              }
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
      // 使用刚指定的配置项和数据显示图表
      this.myChart.setOption(this.option)
      // 最后看看全貌
      console.log('增加节点：')
      console.log(this.graph)
    },
    // 2. 添加关系
    add_rel () {
      // 遍历关系数组，判断关系是否存在
      for (let i = 0; i < this.rels_arr.length; i++) {
        if (this.rels_arr[i].includes(this.node1) && this.rels_arr[i].includes(this.node2)) {
          alert('关系已存在！')
          return
        }
      }
      const arr = []
      arr[0] = this.node1
      arr[1] = this.node2
      this.rels_arr.push(arr)
      console.log(this.rels_arr)
      // 设置节点集合，记录初始和目标节点的id
      const set = []
      let this_judge = true
      // 添加节点1
      for (let i = 0; i < this.graph.nodes.length; i++) {
        if (this.graph.nodes[i].properties.name === this.node1) {
          alert('节点1已存在！')
          // 存在？把id记录下来
          set.push(this.graph.nodes[i].identity)
          this_judge = false
          break
        }
      }
      if (this_judge) {
        this.graph.nodes.push({
          identity: this.graph.nodes.length,
          labels: ['Person'],
          properties: { name: this.node1 }
        })
        set.push(this.graph.nodes.length - 1)
      }
      this_judge = true
      // 添加节点2
      for (let i = 0; i < this.graph.nodes.length; i++) {
        if (this.graph.nodes[i].properties.name === this.node2) {
          alert('节点2已存在！')
          // 存在？把id记录下来
          set.push(this.graph.nodes[i].identity)
          this_judge = false
          break
        }
      }
      if (this_judge) {
        this.graph.nodes.push({
          identity: this.graph.nodes.length,
          labels: ['Person'],
          properties: { name: this.node2 }
        })
        set.push(this.graph.nodes.length - 1)
      }
      // 添加关系边
      for (let j = 1; j < set.length; j++) {
        this.graph.links.push({ source: set[0], target: set[1], name: this.rels })
      }
      // ''说明是第一次，需要初始化
      if (this.myChart === '') {
        this.myChart = echarts.init(this.$refs.graph1)
      }
      // 不知道为什么this.option要重写一遍才能更新，不能直接放在created里面
      this.option = {
        // 1.上方标题+动画
        title: {
          text: 'Words_Graph',
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
            // 可能是echart封装好的，这里的data就是一个节点对象，表示鼠标移动到当前位置的节点
            if (params.dataType === 'node') {
              return 'id:' + params.data.identity + '<br>名称:' + params.data.properties.name
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
          data: this.graph.nodes,
          symbolSize: 40,
          // categories: categories,
          // 4.2 关系线
          links: this.graph.links.map(function (edge) {
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
              if (params.data.properties.name.length <= 5) {
                return params.data.properties.name
              } else {
                return params.data.properties.name.slice(0, 5).concat('...')
                // 标签名太长了，默认只显示前5个字，具体信息悬浮可见
              }
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
      // 使用刚指定的配置项和数据显示图表
      this.myChart.setOption(this.option)
      // 最后看看全貌
      console.log('增加关系：')
      console.log(this.graph)
    },
    // 3. 删除节点
    del_node () {
      let judge = false
      for (let i = 0; i < this.graph.nodes.length; i++) {
        if (this.graph.nodes[i].properties.name === this.del_node0) {
          // 节点存在，进行删除(删除之前先记录它的所有信息)
          const del_id = this.graph.nodes[i]
          this.graph.nodes.splice(i, 1)
          // 重置节点索引
          for (let i = 0; i < this.graph.nodes.length; i++) {
            this.graph.nodes[i].identity = i
          }
          // 重置关系数组
          // 先将links置空，反正数据都在rels_arr里面，之后重构关系也是根据rels_arr来的
          this.graph.links = []
          // 再将二维关系数组rels_arr中，含有value.properties.name的一维数组删除
          for (let i = 0; i < this.rels_arr.length; i++) {
            if (this.rels_arr[i].includes(del_id.properties.name)) {
              this.rels_arr.splice(i, 1)
              i--
            }
          }
          // 调用重置关系函数
          this.resetRels()
          judge = true
        }
      }
      if (!judge) {
        alert('节点不存在！')
      }
      if (this.myChart === '') {
        this.myChart = echarts.init(this.$refs.graph1)
      }
      this.option = {
        // 1.上方标题+动画
        title: {
          text: 'Words_Graph',
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
            // 可能是echart封装好的，这里的data就是一个节点对象，表示鼠标移动到当前位置的节点
            if (params.dataType === 'node') {
              return 'id:' + params.data.identity + '<br>名称:' + params.data.properties.name
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
          data: this.graph.nodes,
          symbolSize: 40,
          // categories: categories,
          // 4.2 关系线
          links: this.graph.links.map(function (edge) {
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
              if (params.data.properties.name.length <= 5) {
                return params.data.properties.name
              } else {
                return params.data.properties.name.slice(0, 5).concat('...')
                // 标签名太长了，默认只显示前5个字，具体信息悬浮可见
              }
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
      // 使用刚指定的配置项和数据显示图表
      this.myChart.setOption(this.option)
      // 最后看看全貌
      console.log('删除节点：')
      console.log(this.graph)
    },
    // 4. 删除关系
    del_rel () {
      let this_judge = true
      // 遍历关系数组，判断关系是否存在
      for (let i = 0; i < this.rels_arr.length; i++) {
        if (this.rels_arr[i].includes(this.del_node1) && this.rels_arr[i].includes(this.del_node2)) {
          this.rels_arr.splice(i, 1)
          // 重置关系图谱
          this.graph.links = []
          this.resetRels()
          this_judge = false
          break
        }
      }
      if (this_judge) {
        alert('关系不存在！')
        return
      }
      if (this.myChart === '') {
        this.myChart = echarts.init(this.$refs.graph1)
      }
      this.option = {
        // 1.上方标题+动画
        title: {
          text: 'Words_Graph',
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
              return 'id:' + params.data.identity + '<br>名称:' + params.data.properties.name
            } else if (params.dataType === 'edge') {
              return '关系: ' + params.data.name // 只能写默认name了，表示a>b，醉了...
            }
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
          data: this.graph.nodes,
          symbolSize: 40,
          // 4.2 关系线
          links: this.graph.links.map(function (edge) {
            return {
              source: edge.source,
              target: edge.target,
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
              if (params.data.properties.name.length <= 5) {
                return params.data.properties.name
              } else {
                return params.data.properties.name.slice(0, 5).concat('...')
                // 标签名太长了，默认只显示前5个字，具体信息悬浮可见
              }
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
      // 使用刚指定的配置项和数据显示图表
      this.myChart.setOption(this.option)
      // 最后看看全貌
      console.log('删除关系：')
      console.log(this.graph)
    },
    resetRels (value) {
      // 重置关系数组
      for (let i = 0; i < this.rels_arr.length; i++) { // 遍历检查 rels_nation/rels_gender 等，拿到元素的第一个值(sub)
        let k1 = 0
        let k2 = 0
        for (let j = 0; j < this.graph.nodes.length; j++) {
          if (this.graph.nodes[j].properties.name === this.rels_arr[i][0]) {
            // 每个[0]元素跟节点数组中的name对应，取出节点数组对应节点的identity,将其赋值给j
            k1 = this.graph.nodes[j].identity
            // console.log(k1)
            // 找第二个元素，也是用j遍历整个nodes数组，找到后将其identity赋值给k2
            for (let j = 0; j < this.graph.nodes.length; j++) {
              if (this.graph.nodes[j].properties.name === this.rels_arr[i][1]) {
                k2 = this.graph.nodes[j].identity
                // console.log(k2)
                if (k1 !== k2) { // 不相等才进行相连，自己连自己没意义！！！
                  this.graph.links.push({ source: k1, target: k2, name: this.rels_arr.slice(5) })
                  // k1,k2分别作为source和target的值
                }
              }
            }
          }
        }
      }
    }
  }
}
</script>

<style lang="less" scoped>
span {
  margin-right: 20px;
  font-size: 16px;
}

.myInput {
  margin-top: 20px;
  width: 100px;
  font-size: 12px;
  border-radius: 1px;
  box-shadow: 0 0 5px #ccc;
  border: none;
  outline: none;
}
// el-button会继承原生的button样式
button {
  margin-left: 30px;
  font-size: 14px;
  text-align: center;
  border: none;
  border-radius: 10px;
}
</style>
