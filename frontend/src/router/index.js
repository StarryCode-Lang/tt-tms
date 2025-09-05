// 路由配置
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import RegisterStudent from '../views/RegisterStudent.vue'
import RegisterCoach from '../views/RegisterCoach.vue'
import Dashboard from '../views/Dashboard.vue'
import CampusManagement from '../views/CampusManagement.vue'
import Profile from '../views/Profile.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/register/student', component: RegisterStudent },
  { path: '/register/coach', component: RegisterCoach },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/campus', component: CampusManagement, meta: { requiresAuth: true, role: 'super_admin' } },
  { path: '/profile', component: Profile, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.role && role !== to.meta.role) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router