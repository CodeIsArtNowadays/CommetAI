<script setup>
import { ref, onMounted } from 'vue'
import { useAuth } from '../composables/useAuth.js'
import ProjectCard from '../components/ProjectCard.vue'

const { authHeaders } = useAuth()

const projects = ref([])
const isLoading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await fetch('/api/projects/', {
      headers: authHeaders.value
    })
    if (!res.ok) throw new Error('Failed to fetch projects')
    projects.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    isLoading.value = false
  }
})
</script>


<template>
  <main class="max-w-6xl mx-auto px-6 py-10">
    <div class="mb-8">
      <h1 class="text-gray-900 dark:text-white text-2xl font-bold mb-1">Your Projects</h1>
      <p class="text-gray-500 text-sm">{{ projects.length }} projects available</p>
    </div>

    <!-- Loading -->
    <div v-if="isLoading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="n in 3"
        :key="n"
        class="h-48 rounded-2xl bg-gray-100 dark:bg-gray-800 animate-pulse"
      />
    </div>

    <!-- Error -->
    <div
      v-else-if="error"
      class="text-red-500 text-sm bg-red-50 dark:bg-red-900/20 px-4 py-3 rounded-xl"
    >
      {{ error }}
    </div>

    <!-- Projects -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <ProjectCard
        v-for="project in projects"
        :key="project.id"
        :project="project"
      />
    </div>
  </main>
</template>
