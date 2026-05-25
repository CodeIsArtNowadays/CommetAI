import { createRouter, createWebHistory } from 'vue-router'
import ProjectsPage from '../pages/ProjectsPage.vue'
import ProjectPage from '../pages/ProjectPage.vue'
import LandingPage from '../pages/LandingPage.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: LandingPage },
    { path: '/projects', component: ProjectsPage },
    // :id - динамический параметр, как <int:id> в Flask/FastAPI
    { path: '/projects/:id', component: ProjectPage },
  ]
})

export default router
