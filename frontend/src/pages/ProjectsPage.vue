<script setup>
import { ref, onMounted } from 'vue'
import ProjectCard from '../components/ProjectCard.vue'

const projects = ref([])
const isLoading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const response = await fetch('/api/projects/', {
      headers: {
        'Authorization': `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHBpcmUiOiIyMDI2LTA2LTAxIDE1OjQ1OjU1LjUzNTMyMCJ9.yBSjh4Gct7CaP0dmiqMM2Ye2OIDDxaUpsLtvIC2AZRo`
      }
    })

    if (!response.ok) throw new Error('Failed to fetch projects')

    projects.value = await response.json()
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
