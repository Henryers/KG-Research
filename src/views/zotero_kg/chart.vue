<template>
  <el-card class="box-card">
    <div id="chart1"></div>
    <div id="chart2"></div>
    <div id="chart3"></div>
  </el-card>
</template>

<script>
import * as echarts from 'echarts'
import { getGraph1API, getGraph2API } from '@/api'

export default {
  data () {
    return {
      // your data properties here
    }
  },
  mounted () {
    this.makeRequest()
  },
  methods: {
    async makeRequest () {
      const { data: res1 } = await getGraph1API()
      const { data: res2 } = await getGraph2API()
      // 拿到 节点json数据 和 关系数组
      const graph = {
        nodes: res1.kg_zotero,
        relationships: []
      }
      const rels_zotero = res2.rels_zotero
      const names = [rels_zotero]
      // 遍历关系数组来构建关系
      for (let i = 0; i < names.length; i++) {
        for (let j = 0; j < names[i].length; j++) { // 遍历检查 rels_nation/rels_gender 等，拿到元素的第一个值(sub)
          let l1 = 0
          let l2 = 0
          for (let k = 0; k < graph.nodes.length; k++) {
            if (graph.nodes[k].n.properties.name === names[i][j][0]) {
              // 每个[0]元素跟节点数组中的name对应，取出节点数组对应节点的identity,将其赋值给k
              l1 = graph.nodes[k].n.identity
              // 找第二个元素，也是用k遍历整个nodes数组，找到后将其identity赋值给l2
              for (let k = 0; k < graph.nodes.length; k++) {
                if (graph.nodes[k].n.properties.name === names[i][j][1]) {
                  l2 = graph.nodes[k].n.identity
                  if (l1 !== l2) { // 不相等才进行相连，自己连自己没意义！！！
                    graph.relationships.push({ source: l1, target: l2, name: names[i].slice(5) })
                    // l1,l2分别作为source和target的值
                  }
                }
              }
            }
          }
        }
      }
      // categories数组用来存放节点类别，分出不同颜色进行展示
      const categories = []
      // 遍历节点数据
      graph.nodes.forEach(function (node) {
        const label = node.n.labels[0] // 注意：这里假设每个节点的"label"属性只有一个元素
        // 遍历categories数组，找到对应的类别，返回该类别对应的索引
        let categoryIndex = categories.findIndex(function (category) {
          return category.name === label
        })
        // 如果当前类别不存在，则添加到categories数组中
        if (categoryIndex === -1) {
          categories.push({ name: label })
          categoryIndex = categories.length - 1 // 使用新添加的类别索引
        }
        node.category = categoryIndex // 每个节点在json数据中都新增一个属性，与"n"平级
      })

      console.log('图数据完整展示：')
      console.log(graph)

      // category属性是关键，确定了每个节点的对应位置！
      // 搞个索引词频表
      const indexs = []
      graph.nodes.forEach(function (node) {
        indexs[node.category] = node.n.labels[0]
      })
      console.log(indexs)
      // 搞个柱状图词频表
      const nums = []
      graph.nodes.forEach(function (node) {
        nums[node.category] = nums[node.category] ? (nums[node.category] + 1) : 1
      })
      console.log(nums)

      // 1.饼状图
      const myChart1 = echarts.init(document.getElementById('chart1')) // 默认主题为亮白色
      // 利用索引表和词频表，生成饼图数据
      const mydata = []
      for (let i = 0; i < indexs.length; i++) {
        mydata.push({
          name: indexs[i],
          value: nums[i]
        })
      }
      // 指定图表的配置项和数据
      const option1 = {
        title: {
          text: 'Zotero Graph',
          subtext: 'Ratio Chart',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'horizontal',
          top: '10%',
          left: 100
        },
        series: {
          name: 'Access From',
          type: 'pie',
          radius: '50%',
          data: mydata,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      }
      // 使用刚指定的配置项和数据显示图表。
      myChart1.setOption(option1)

      // 2.柱状图
      const myChart2 = echarts.init(document.getElementById('chart2')) // 默认主题为亮白色
      const option2 = {
        // 1.上方标题
        title: {
          text: '节点词频统计',
          subtext: 'my layout',
          left: 'center'
        },
        grid: {
          left: '5%',
          right: '15%',
          bottom: '10%',
          containLabel: true
        },
        xAxis: {
          type: 'value'
        },
        yAxis: {
          type: 'category',
          data: indexs
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            data: nums,
            type: 'bar',
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      // 使用刚指定的配置项和数据显示图表。
      myChart2.setOption(option2)

      // 3.折线图
      const myChart3 = echarts.init(document.getElementById('chart3')) // 默认主题为亮白色
      const option3 = {
        // 1.上方标题
        title: {
          text: '节点词频统计',
          subtext: 'my layout',
          left: 'center'
        },
        xAxis: {
          type: 'category',
          data: indexs
        },
        yAxis: {
          type: 'value'
        },
        tooltip: {
          trigger: 'item'
        },
        series: [
          {
            data: nums,
            type: 'line',
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      // 使用刚指定的配置项和数据显示图表。
      myChart3.setOption(option3)
      // 图表3
    }
  }
}
</script>

<style lang="less" scoped>
#chart1{
  display:inline-block;
  width:520px;
  height:600px;
  background-color: #fff;
}
#chart2 {
  display:inline-block;
  width:600px;
  height:600px;
  background-color: #fff;
  vertical-align: top;
}
#chart3 {
  display:inline-block;
  width:1100px; height:500px;
  background-color: #fff;
  vertical-align: top;
}
</style>
