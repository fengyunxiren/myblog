import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/components/Main'
import ArticleDetail from '@/components/ArticleDetail'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Main
    },
    {
      path: '/articles/:id',
      name: 'ArticleDetail',
      component: ArticleDetail
    }
  ]
})
