import Vue from 'vue'
import VueRouter from 'vue-router'
import MainComponent from '../components/MainComponent.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    alias: ['/home', '/cms-pdmv'],
    name: 'MainComponent',
    component: MainComponent
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
