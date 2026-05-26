<script setup>
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '../composables/useAuth.js'

const router = useRouter()
const route = useRoute()
const { setToken, fetchUser } = useAuth()

onMounted(async () => {
  const code = route.query.code
  const res = await fetch(`/api/auth/callback/github?code=${code}`)
  const token = await res.json()  // вместо res.text()
  setToken(token.trim())
  
  console.log('status:', res.status)
  console.log('token:', token)  // ← что реально приходит?

  setToken(token.trim())
  await fetchUser()
  router.push('/projects')
})

</script>

<template>
  <div class="min-h-screen flex items-center justify-center text-gray-500 dark:text-gray-400">
    Signing in...
  </div>
</template>
