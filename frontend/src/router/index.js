import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SandboxView from '../views/SandboxView.vue'
import TutorialListView from '../views/TutorialListView.vue'
import TutorialView from '../views/TutorialView.vue'
import SharedGraphView from '../views/SharedGraphView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/sandbox', name: 'sandbox', component: SandboxView },
  { path: '/tutorials', name: 'tutorials', component: TutorialListView },
  { path: '/tutorial/:id', name: 'tutorial', component: TutorialView, props: true },
  { path: '/share/:token', name: 'shared', component: SharedGraphView, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
