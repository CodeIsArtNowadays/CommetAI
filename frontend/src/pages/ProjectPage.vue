<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import TaskCard from '../components/TaskCard.vue'
import CommitCard from '../components/CommitCard.vue'

const route = useRoute()
const router = useRouter()

const project = ref(null)
const loading = ref(true)
const error = ref(null)
const showDone = ref(false)

// в <script setup> ProjectDetailPage.vue
const formatDate = (str) => {
  if (!str) return '—'
  return new Date(str).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
}

onMounted(async () => {
  try {
    const token = localStorage.getItem('access_token')


    const res = await fetch(`/api/projects/${route.params.id}`, {
      headers: {
        'Authorization': `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHBpcmUiOiIyMDI2LTA2LTAxIDE1OjQ1OjU1LjUzNTMyMCJ9.yBSjh4Gct7CaP0dmiqMM2Ye2OIDDxaUpsLtvIC2AZRo`
      }
    })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    project.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})

const activeTasks = computed(() => project.value?.tasks.filter(t => !t.is_done) ?? [])
const doneTasks   = computed(() => project.value?.tasks.filter(t => t.is_done)  ?? [])

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

    <!-- Loading -->
    <div v-if="loading" class="flex flex-col gap-3 animate-pulse">
      <div class="h-8 w-48 bg-gray-200 dark:bg-gray-800 rounded-lg"></div>
      <div class="h-4 w-72 bg-gray-100 dark:bg-gray-800/60 rounded"></div>
      <div class="mt-6 flex flex-col gap-2">
        <div v-for="i in 3" :key="i" class="h-12 bg-gray-100 dark:bg-gray-800/40 rounded-xl"></div>
      </div>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-center text-red-400 py-20 text-sm">
      Failed to load project: {{ error }}
    </div>

    <!-- Not found -->
    <div v-else-if="!project" class="text-center text-gray-400 dark:text-gray-600 py-20 text-lg">
      Project not found.
    </div>

    <div v-else>
      <!-- Header -->
      <div class="mb-10">
        <div class="flex items-center gap-3 mb-2">
          <img src="../assets/logo2.png" alt="CommetAI" class="h-8" />
          <h1 class="text-gray-900 dark:text-white text-2xl font-bold">{{ project.title }}</h1>
        </div>
        <p class="text-gray-500 dark:text-gray-400 text-sm">{{ project.description ?? 'No description.' }}</p>
        <p class="text-gray-400 dark:text-gray-600 text-xs mt-1 font-mono">
          by {{ project.owner?.username }} · created {{ formatDate(project.created_at) }}
        </p>
      </div>

      <!-- Tasks -->
      <section class="mb-10">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-gray-700 dark:text-gray-300 font-semibold uppercase tracking-wider text-xs">Tasks</h2>
          <span class="text-gray-400 text-xs font-mono">{{ project.tasks.length }} total</span>
        </div>

        <div class="flex flex-col gap-2">
          <TaskCard v-for="task in activeTasks" :key="task.id" :task="task" />
        </div>

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
              <TaskCard v-for="task in doneTasks" :key="task.id" :task="task" />
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
          <CommitCard v-for="commit in project.commits" :key="commit.sha" :commit="commit" />
        </div>
      </section>
    </div>

  </main>
</template>

<style scoped>
.expand-enter-active, .expand-leave-active {
  transition: opacity 0.22s ease, max-height 0.28s cubic-bezier(0.4, 0, 0.2, 1);
  max-height: 1000px;
  overflow: hidden;
}
.expand-enter-from, .expand-leave-to { opacity: 0; max-height: 0; }
</style>
