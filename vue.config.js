const { defineConfig } = require('@vue/cli-service')

// 需要排除的包对象
let externals = {}
// 需要配置CDN链接
let CDN = { css: [], js: [] }
// 判断是否是生产环境
const isProduction = process.env.NODE_ENV === 'production'
// 如何是生产环境，需要执行以下逻辑
if (isProduction) {
  externals = {
    /**
      * externals 对象属性解析：
      * '包名': '在项目中引入的名字'
      * 以 element-ui 举例 我再 main.js 里是以
      * import ELEMENT from 'element-ui'
      * Vue.use(ELEMENT)
      * 这样引入的，所以我的 externals 的属性值应该是 ELEMENT
      * 一定要去main.js设置
    */
    echarts: 'echarts',
    vue: 'Vue',
    'vue-router': 'VueRouter',
    vuex: 'Vuex',
    axios: 'axios',
    dayjs: 'dayjs',
    'element-ui': 'ELEMENT',
    'vue-quill-editor': 'VueQuillEditor',
    'vuex-persistedstate': 'createPersistedState'
  }
  CDN = {
    css: [
      'https://unpkg.com/element-ui@2.15.8/lib/theme-chalk/index.css',
      'https://unpkg.com/quill@1.3.7/dist/quill.core.css',
      'https://unpkg.com/quill@1.3.7/dist/quill.snow.css',
      'https://unpkg.com/quill@1.3.7/dist/quill.bubble.css'
    ],
    js: [
      'https://unpkg.com/echarts@5.4.1/dist/echarts.min.js',
      'https://unpkg.com/vue@2.6.14/dist/vue.js',
      'https://unpkg.com/vue-router@3.5.1/dist/vue-router.js',
      'https://unpkg.com/vuex@3.6.2/dist/vuex.js',
      'https://unpkg.com/axios@1.2.2/dist/axios.min.js',
      'https://unpkg.com/dayjs@1.11.7/dayjs.min.js',
      'https://unpkg.com/element-ui@2.15.12/lib/index.js',
      'https://unpkg.com/quill@1.3.7/dist/quill.js',
      'https://unpkg.com/vue-quill-editor@3.0.6/dist/vue-quill-editor.js',
      'https://unpkg.com/vuex-persistedstate@3.2.1/dist/vuex-persistedstate.umd.js'
    ]
  }
}
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
  // 影响打包时，index.html引入其他资源的前缀地址
  publicPath: process.env.NODE_ENV === 'production' ? './' : '/',
  configureWebpack: {
    // provide the app's title in webpack's name field, so that
    // it can be accessed in index.html to inject the correct title.
    externals: externals // 如果是开发环境，排除空对象/(不排除,用本地的)，如果是生产环境，排除externals里面的包对象
  },
  chainWebpack (config) {
    // 注入cdn变量，打包时会执行
    config.plugin('html').tap(args => {
      args[0].cdn = CDN // 配置CDN 给插件
      return args
    })
  }
})
