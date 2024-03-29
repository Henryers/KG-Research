<template>
  <el-card class="box-card">
    <div style="width: 1100px; height: 600px;" id="graph2"></div>
  </el-card>
</template>

<script>
import * as echarts from 'echarts'
import { getGraph1API, getGraph2API } from '@/api'

export default {
  data () {
    return {
      myjson: ''
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
      for (let i = 0; i < names.length; i++) {
        for (let j = 0; j < names[i].length; j++) { // 遍历检查 rels_nation/rels_gender 等，拿到元素的第一个值(sub)
          let l1 = 0
          let l2 = 0
          for (let k = 0; k < graph.nodes.length; k++) {
            if (graph.nodes[k].n.properties.name === names[i][j][0]) {
              // 每个[0]元素跟节点数组中的name对应，取出节点数组对应节点的identity,将其赋值给k
              l1 = graph.nodes[k].n.identity
              // console.log(l1)
              // 找第二个元素，也是用k遍历整个nodes数组，找到后将其identity赋值给l2
              for (let k = 0; k < graph.nodes.length; k++) {
                if (graph.nodes[k].n.properties.name === names[i][j][1]) {
                  l2 = graph.nodes[k].n.identity
                  // console.log(l2)
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

      // 创建一个空的categories数组
      const categories = []

      // 遍历节点数据
      graph.nodes.forEach(function (node) {
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

      console.log('数据？')
      console.log(graph)

      // 基于准备好的dom，初始化echarts实例
      const myChart = echarts.init(document.getElementById('graph2')) // 默认主题为亮白色
      // 指定图表的配置项和数据(去ECharts里面拿！)
      const option = {
        // 1.上方标题
        title: {
          text: 'Zotero Graph',
          subtext: 'my knowledge',
          left: 'center'
        },
        animationDurationUpdate: 1500,
        animationEasingUpdate: 'quinticInOut',
        // 2.图中配置
        series: [
          {
            // 力导向force布局-基本配置
            draggable: true,
            type: 'graph',
            layout: 'force',
            roam: true,
            force: {
              repulsion: 200, // 节点之间斥力的大小
              edgeLength: [100, 180] // 边的长度
            },
            // 2.1 后端json数据+类别
            data: graph.nodes,
            symbolSize: 50,
            categories: categories,
            // 2.2 关系线
            links: graph.relationships.map(function (edge) {
              return {
                source: edge.source,
                target: edge.target, // 指明是哪两个节点的关系要加样式(因此数组中有多少组关系就设置多少个连接线样式)
                name: edge.name,
                lineStyle: {
                  opacity: 0.9,
                  width: 2,
                  color: 'source',
                  curveness: 0.3
                }
                // symbol:"arrow",        //箭头
              }
            }),
            // 2.3 标签
            label: {
              show: true,
              position: 'bottom', // 并将标签显示在节点的右侧,快废弃了...
              formatter: function (params, ticket) {
                return params.data.n.properties.name.slice(0, 6).concat('...')
                // 标签名太长了，默认只显示前8个字，具体信息悬浮可见
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
        ],
        // 3.侧边图例
        legend: {
          orient: 'vertical',
          right: '20px'
        },
        // 4.悬停显示信息
        tooltip: {
          show: true, // 显示提示框
          formatter: function (params, ticket) {
            if (params.dataType === 'node') {
              return 'id:' + params.data.n.identity + '<br>名称:' + params.data.n.properties.name
            } else if (params.dataType === 'edge') {
              return '关系: ' + params.data.name // 只能写默认name了，表示a>b，醉了...
            }
            // 根据不同的数据类型(一个是节点，一个是关系线)，显示不同的提示信息
          }
        }
      }

      // 使用刚指定的配置项和数据显示图表
      myChart.setOption(option)
    }
  }
}
</script>

<style></style>
