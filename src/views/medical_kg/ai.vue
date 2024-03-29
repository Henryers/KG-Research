<template>
  <el-card>
    <div class="mainground">
      <div>
        <div class="tips">我是小小AI,请问有什么问题需要我回答吗？</div>
        <div class="show"></div>
        <div style="text-align: center;">
          <!-- 下面两个行内元素会在同一行显示，并且根据其内容自动调整宽度 -->
          <el-input class="myInput" v-model="input" placeholder="请输入您的问题" @keyup.enter.native="handleQuestion"></el-input>
          <el-button type="primary" @click="handleQuestion">submit</el-button>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script>
import { getGraph2API } from '@/api'

export default {
  name: 'ai',
  data () {
    return {
      // your data properties here
      input: '',
      alleach: 'tmp',
      question: '',
      answer: '你他妈有病啊！！！sbj',
      rels_check: [],
      rels_symptom: [],
      rels_acompany: [],
      rels_recommanddrug: [],
      rels_commonddrug: [],
      rels_noteat: [],
      rels_doeat: [],
      rels_recommandeat: [],
      rels_drug_producer: [],
      rels_category: [],
      rels_department: []
    }
  },
  mounted () {
    // 此时元素才被挂载到页面上，才能获取到，data()中应该先初始化为空，这里再this.xxx来赋值
    this.answer = document.querySelector('.show')
    console.log(this.answer) // 输出类型
    console.log('this.answer type:', typeof this.answer) // 输出类型
    console.log('this.answer content:', this.answer) // 输出内容
    this.makeRequest()
  },
  methods: {
    async makeRequest () {
      const { data: res } = await getGraph2API()
      // 拿到关系数组
      this.rels_check = res.rels_check
      this.rels_symptom = res.rels_symptom
      this.rels_acompany = res.rels_acompany
      this.rels_recommanddrug = res.rels_recommanddrug
      this.rels_commonddrug = res.rels_commonddrug
      this.rels_noteat = res.rels_noteat
      this.rels_doeat = res.rels_doeat
      this.rels_recommandeat = res.rels_recommandeat
      this.rels_drug_producer = res.rels_drug_producer
      this.rels_category = res.rels_category
      this.rels_department = res.rels_department
    },
    // 处理问答函数
    QA (list, type) {
      console.log('byd还不九九九七！！')
      console.log(this)
      console.log(this.answer)
      this.answer.innerHTML = '' // 每次调用生成回答的函数，都要把原来的内容清空
      console.log(this.answer)
      const tmpArray = [] // 暂存后面的答案数组
      let count = 0 // 有效回答计数
      for (let i = 0; i < list.length; i++) {
        if (this.question.includes(list[i][0])) {
          this.alleach = list[i][0]
          tmpArray.push(list[i][1] + ' ')
          count++ // 每个有效回答都会计数
        }
      }
      if (count !== 0) { // 找到有效回答
        // 将前半部分的字符串跟后面的答案数组拼接，再写入最终answer元素中
        this.answer.innerHTML += `${this.alleach}${type} ${tmpArray.join(' ')}`
      } else if (count === 0) { // 无法找到有效回答
        this.answer.innerHTML = '很抱歉，根据目前的语料库，暂时无法为您提供解答！'
      }
    },
    // 把整个事件抽取成一个函数
    handleQuestion () {
      this.question = this.input // 获取输入的问题
      // 根据问题类型，传入不同参数进行函数调用
      let type = ''
      if (this.question.includes('检查') || this.question.includes('体检')) {
        type = '要进行的检查有: '
        this.this.QA(this.rels_check, type)
      } else if (this.question.includes('症状') || this.question.includes('病症') || this.question.includes('特点')) {
        type = '可能具有的发病症状有: '
        this.QA(this.rels_symptom, type)
      } else if (this.question.includes('相关') || this.question.includes('疾病') || this.question.includes('并发症')) {
        type = '的相关疾病有: '
        this.QA(this.rels_acompany, type)
      } else if (this.question.includes('推荐药物') || this.question.includes('用什么药') || this.question.includes('吃什么药')) {
        type = '推荐吃的药有: '
        this.QA(this.rels_recommanddrug, type)
      } else if (this.question.includes('常用药') || this.question.includes('便药')) {
        type = '的常用药物有: '
        this.QA(this.rels_commonddrug, type)
      } else if (this.question.includes('不可以吃') || this.question.includes('不能吃') || this.question.includes('忌口')) {
        type = '不可以吃: '
        this.QA(this.rels_noteat, type)
      } else if (this.question.includes('可以吃') || this.question.includes('要吃') || this.question.includes('能吃') || this.question.includes('吃什么')) {
        type = '可以吃: '
        this.QA(this.rels_doeat, type)
      } else if (this.question.includes('推荐吃') || this.question.includes('最好吃')) {
        type = '推荐吃: '
        this.QA(this.rels_recommandeat, type)
      } else if (this.question.includes('厂商') || this.question.includes('商家')) {
        type = '生产的具体药物有: '
        this.QA(this.rels_drug_producer, type)
      } else if (this.question.includes('科室') || this.question.includes('科')) {
        type = '对应的科室是: '
        this.QA(this.rels_category, type)
      } else if (this.question.includes('大科室') || this.question.includes('主科室')) {
        type = '对应的大科室是: '
        this.QA(this.rels_department, type)
      } else {
        this.QA(this.rels_department, type)
      }
    }
  }
}
</script>

<style scoped>
.mainground {
  display: flex;
  width: 100%;
  height: 70vh;
}

.tips {
  margin: 20px 220px;
  width: 730px;
  height: 100px;
  color: #309ee2;
  font-size: 30px;
  text-align: center;
}

.show {
  margin: 20px 220px;
  width: 730px;
  height: 300px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 0 10px #ccc;
  text-align: center;
  line-height: 100px;
}

.myInput {
  width: 610px;
  font-size: 18px;
  border-radius: 1px;
  box-shadow: 0 0 5px #ccc;
  border: none;
  outline: none;
}

button {
  margin-left: 30px;
  font-size: 18px;
  text-align: center;
  border: none;
}
</style>
