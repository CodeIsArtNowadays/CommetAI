import { createRouter, createWebHistory } from 'vue-router'
import ProjectsPage from '../pages/ProjectsPage.vue'
import ProjectPage  from '../pages/ProjectPage.vue'
import LandingPage  from '../pages/LandingPage.vue'

const routes = [
  { path: '/', component: LandingPage },
  { path: '/projects', component: ProjectsPage, meta: { requiresAuth: true } },
  { path: '/projects/:id', component: ProjectPage, meta: { requiresAuth: true } },
  { path: '/callback/github', component: () => import('../pages/GithubCallbackPage.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const token = localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !token) return '/'
})

export default router
