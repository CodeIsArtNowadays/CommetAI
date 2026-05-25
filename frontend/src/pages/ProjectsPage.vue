<script setup>
import { ref } from 'vue'
import ProjectCard from '../components/ProjectCard.vue'

const projects = ref([
  {
    id: 1,
    title: 'CommetAI',
    tasks: [
      { id: 1, title: 'Setup Vite + Vue 3' },
      { id: 2, title: 'Build ProjectCard component' },
      { id: 3, title: 'Add dark mode toggle' },
    ]
  },
  {
    id: 2,
    title: 'Backend API',
    tasks: [
      { id: 1, title: 'Create /projects endpoint' },
      { id: 2, title: 'Add authentication' },
    ]
  },
  {
    id: 3,
    title: 'Mobile App',
    tasks: [
      { id: 1, title: 'Design onboarding screens' },
    ]
  },
])
</script>

<template>
  <main class="max-w-6xl mx-auto px-6 py-10">
    <div class="mb-8">
      <h1 class="text-gray-900 dark:text-white text-2xl font-bold mb-1">Your Projects</h1>
      <p class="text-gray-500 text-sm">{{ projects.length }} projects available</p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <ProjectCard
        v-for="project in projects"
        :key="project.id"
        :project="project"
      />
    </div>
  </main>
</template>
