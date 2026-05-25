<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import TaskCard from '../components/TaskCard.vue'
import CommitCard from '../components/CommitCard.vue'

const route = useRoute()
const router = useRouter()

const showDone = ref(false)

const projects = ref([
  {
    id: 1,
    title: 'CommetAI',
    description: 'Git + Comet + AI project management tool built with Vue 3.',
    tasks: [
      {
        id: 1,
        title: 'Setup Vite + Vue 3',
        description: 'Initialize the project with Vite, Vue 3, Tailwind CSS v4 and Vue Router. Configure aliases and base layout.',
        due_time: '2026-05-20T00:00:00',
        commit_sha: 'a1b2c3d4e5f6',
        is_done: true
      },
      {
        id: 2,
        title: 'Build ProjectCard component',
        description: 'Create a reusable ProjectCard with fixed task slots, hidden task counter, and click navigation.',
        due_time: '2026-05-22T00:00:00',
        commit_sha: 'e4f5g6h7i8j9',
        is_done: true
      },
      {
        id: 3,
        title: 'Add dark mode toggle',
        description: 'Implement theme switcher using useTheme composable with localStorage persistence and immediate watcher.',
        due_time: '2026-05-26T00:00:00',
        commit_sha: null,
        is_done: false
      },
      {
        id: 4,
        title: 'Connect to backend API',
        description: 'Replace all mock data with real fetch calls to the API running on port 8000. Handle loading and error states.',
        due_time: '2026-05-30T00:00:00',
        commit_sha: null,
        is_done: false
      },
      {
        id: 5,
        title: 'Add authentication',
        description: 'Implement JWT-based login flow with protected routes. Store token in localStorage and attach to all API requests.',
        due_time: '2026-06-05T00:00:00',
        commit_sha: null,
        is_done: false
      },
    ],
    commits: [
      {
        id: 1,
        summary: 'init: setup Vite + Vue 3 + Tailwind',
        technical: 'Initialized Vite project with @vitejs/plugin-vue, installed tailwindcss v4 via @tailwindcss/vite, configured @import in style.css.',
        risks: 'Tailwind v4 config differs from v3 — no tailwind.config.js needed.',
        process: 'Followed official Vite + Vue 3 quickstart, then layered Tailwind on top.',
        conventional: true,
        author: 'astronaut_dev'
      },
      {
        id: 2,
        summary: 'feat: add ProjectCard component',
        technical: 'Built ProjectCard.vue with computed taskSlots (fixed 3 slots) and hiddenCount. Uses useRouter for navigation.',
        risks: 'None significant.',
        process: 'Component-first approach, tested with mock data before wiring to page.',
        conventional: true,
        author: 'astronaut_dev'
      },
      {
        id: 3,
        summary: 'feat: dark mode with localStorage',
        technical: 'Created useTheme.js composable. Applies dark class to document.documentElement. Watches isDark with immediate:true.',
        risks: 'Must call useTheme() in App.vue or watch never fires on load.',
        process: 'Debugged missing dark class — root cause was useTheme not called at app level.',
        conventional: true,
        author: 'astronaut_dev'
      },
      {
        id: 4,
        summary: 'fix: router path mismatch /projects vs /project',
        technical: 'Corrected route definition in main.js from /projects/:id to /project/:id to match router.push calls in ProjectCard.',
        risks: 'Any hardcoded links to /projects/:id would 404.',
        process: 'Caught by comparing main.js routes with ProjectCard goToProject function.',
        conventional: true,
        author: 'astronaut_dev'
      },
    ]
  },
  {
    id: 2,
    title: 'Backend API',
    description: 'REST API server on port 8000 for CommetAI.',
    tasks: [
      {
        id: 1,
        title: 'Create /projects endpoint',
        description: 'GET /projects should return a paginated list of all projects with task counts.',
        due_time: '2026-05-28T00:00:00',
        commit_sha: null,
        is_done: false
      },
      {
        id: 2,
        title: 'Add authentication',
        description: 'POST /auth/login accepts email + password, returns signed JWT. Middleware should protect all non-public routes.',
        due_time: '2026-06-03T00:00:00',
        commit_sha: null,
        is_done: false
      },
    ],
    commits: [
      {
        id: 1,
        summary: 'init: fastapi project scaffold',
        technical: 'Created FastAPI app with uvicorn, added basic project structure with routers and models folders.',
        risks: 'No auth yet — all endpoints are public.',
        process: 'Started from FastAPI official template.',
        conventional: true,
        author: 'astronaut_dev'
      },
    ]
  },
  {
    id: 3,
    title: 'Mobile App',
    description: 'Cross-platform mobile client for CommetAI.',
    tasks: [
      {
        id: 1,
        title: 'Design onboarding screens',
        description: 'Create Figma mockups for the full onboarding flow: splash, login, signup, and home.',
        due_time: '2026-06-10T00:00:00',
        commit_sha: null,
        is_done: false
      },
    ],
    commits: []
  },
])

const project = computed(() => projects.value.find(p => p.id === Number(route.params.id)))

const activeTasks = computed(() => project.value?.tasks.filter(t => !t.is_done) ?? [])
const doneTasks = computed(() => project.value?.tasks.filter(t => t.is_done) ?? [])

const goBack = () => router.push('/')
</script>

<template>
  <main class="max-w-4xl mx-auto px-6 py-10">

    <button
      @click="goBack"
      class="flex items-center gap-2 text-gray-400 hover:text-blue-500 dark:hover:text-blue-400 text-sm mb-8 transition-colors"
    >
      ← Back to projects
    </button>

    <div v-if="!project" class="text-center text-gray-400 dark:text-gray-600 py-20 text-lg">
      Project not found.
    </div>

    <div v-else>
      <div class="mb-10">
        <div class="flex items-center gap-3 mb-2">
          <span class="text-3xl">☄️</span>
          <h1 class="text-gray-900 dark:text-white text-2xl font-bold">{{ project.title }}</h1>
        </div>
        <p class="text-gray-500 dark:text-gray-400 text-sm">{{ project.description }}</p>
      </div>

      <!-- Tasks -->
      <section class="mb-10">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-gray-700 dark:text-gray-300 font-semibold uppercase tracking-wider text-xs">Tasks</h2>
          <span class="text-gray-400 text-xs font-mono">{{ project.tasks.length }} total</span>
        </div>

        <!-- Active tasks -->
        <div class="flex flex-col gap-2">
          <TaskCard
            v-for="task in activeTasks"
            :key="task.id"
            :task="task"
          />
        </div>

        <!-- Done tasks toggle -->
        <div v-if="doneTasks.length > 0" class="mt-3">
          <button
            @click="showDone = !showDone"
            class="flex items-center gap-2 text-xs text-gray-400 hover:text-green-500 dark:hover:text-green-400 transition-colors select-none"
          >
            <span class="transition-transform duration-300 inline-block" :class="showDone ? 'rotate-90' : ''">▶</span>
            <span>{{ showDone ? 'Hide' : 'Show' }} completed ({{ doneTasks.length }})</span>
          </button>

          <Transition name="expand">
            <div v-if="showDone" class="flex flex-col gap-2 mt-2">
              <TaskCard
                v-for="task in doneTasks"
                :key="task.id"
                :task="task"
              />
            </div>
          </Transition>
        </div>
      </section>

      <!-- Commits -->
      <section>
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-gray-700 dark:text-gray-300 font-semibold uppercase tracking-wider text-xs">Commits</h2>
          <span class="text-gray-400 text-xs font-mono">{{ project.commits.length }} total</span>
        </div>

        <div v-if="project.commits.length === 0" class="text-gray-400 dark:text-gray-600 text-sm py-6 text-center">
          No commits yet.
        </div>

        <div class="flex flex-col gap-2">
          <CommitCard
            v-for="commit in project.commits"
            :key="commit.id"
            :commit="commit"
          />
        </div>
      </section>
    </div>

  </main>
</template>

<style scoped>
.expand-enter-active,
.expand-leave-active {
  transition: opacity 0.22s ease, max-height 0.28s cubic-bezier(0.4, 0, 0.2, 1);
  max-height: 1000px;
  overflow: hidden;
}
.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
}
</style>
