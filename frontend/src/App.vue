<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 transition-colors duration-300">
    <AppHeader username="astronaut_dev" />
    <RouterView />
  </div>
</template>

<script setup>
import AppHeader from './components/AppHeader.vue'
import { useTheme } from './composables/useTheme.js'

useTheme() // ← этого достаточно, watch с immediate:true сработает сразу
</script>
