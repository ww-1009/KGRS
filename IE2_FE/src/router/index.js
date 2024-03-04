import Vue from 'vue'
import Router from 'vue-router'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import Entity from '../components/graph/Entity.vue'
import Type from '../components/graph/Type.vue'
import Porperty from '../components/graph/Porperty.vue'

Vue.use(Router)

const router = new Router({
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login',name: 'Login',component: Login },
    {
      path: '/home',
      component: Home,
      redirect: '/entity',
      children: [
        { path: '/entity', component: Entity },
        { path: '/type', component: Type },
        { path: '/porperty', component: Porperty },
      ]
    }
  ]
})

// const routes = [
//   {
//     path: '/',
//     name: 'Home',
//     component:() =>import('../views/Home.vue'),
//   },

// ]

// const router = new VueRouter({
//   routes
// })

export default router
