import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const token = ref(localStorage.getItem('access_token') ?? null)
const user = ref(JSON.parse(localStorage.getItem('auth_user') ?? 'null'))

export function useAuth() {
  const router = useRouter()

  const isAuthenticated = computed(() => !!token.value)

  const setToken = (t) => {
    token.value = t
    localStorage.setItem('access_token', t)
  }

  const setUser = (u) => {
    user.value = u
    localStorage.setItem('auth_user', JSON.stringify(u))
  }

  const fetchUser = async () => {
    if (!token.value) return
    try {
      const res = await fetch('/api/auth/profile', {
        headers: { 'Authorization': `Bearer ${token.value}` }
      })
      const data = await res.json()
      setUser(data) // { username: 'asd' }
    } catch {
      // тихо игнорируем
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('auth_user')
    router.push('/')
  }

  const authHeaders = computed(() => ({
    'Authorization': `Bearer ${token.value}`,
    'Content-Type': 'application/json'
  }))

  return { token, user, isAuthenticated, setToken, setUser, fetchUser, logout, authHeaders }
}
