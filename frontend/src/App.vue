<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 transition-colors duration-300">
    <AppHeader v-if="isAuthenticated" :username="user?.username" />
    <RouterView />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import AppHeader from './components/AppHeader.vue'
import { useTheme } from './composables/useTheme.js'
import { useAuth } from './composables/useAuth.js'

useTheme()

const { isAuthenticated, user, fetchUser } = useAuth()
onMounted(() => fetchUser())
</script>
