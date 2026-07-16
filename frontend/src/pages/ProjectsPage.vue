<script setup>
import { ref, onMounted } from 'vue'
import { useAuth } from '../composables/useAuth.js'
import ProjectCard from '../components/ProjectCard.vue'

const { authHeaders } = useAuth()

const projects = ref([])
const isLoading = ref(true)
const error = ref(null)

// --- Modal state ---
const showModal = ref(false)
const creating = ref(false)
const createError = ref(null)
const form = ref({ title: '', description: '' })

onMounted(async () => {
  await fetchProjects()
})

async function fetchProjects() {
  try {
    isLoading.value = true
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
}

function openModal() {
  form.value = { title: '', description: '' }
  createError.value = null
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

async function createProject() {
  if (!form.value.title.trim()) {
    createError.value = 'Title is required'
    return
  }

  creating.value = true
  createError.value = null

  try {
    const body = { title: form.value.title.trim() }
    if (form.value.description.trim()) {
      body.description = form.value.description.trim()
    }

    const res = await fetch('/api/projects/', {
      method: 'POST',
      headers: {
        ...authHeaders.value,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    })

    if (!res.ok) throw new Error('Failed to create project')

    const newProject = await res.json()
    projects.value.unshift(newProject)
    closeModal()
  } catch (e) {
    createError.value = e.message
  } finally {
    creating.value = false
  }
}
</script>

<template>
  <main class="max-w-6xl mx-auto px-6 py-10">

    <!-- Header -->
    <div class="mb-8 flex items-center justify-between">
      <div>
        <h1 class="text-gray-900 dark:text-white text-2xl font-bold mb-1">Your Projects</h1>
        <p class="text-gray-500 text-sm">{{ projects.length }} projects available</p>
      </div>
      <button
        @click="openModal"
        class="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold text-white transition-opacity hover:opacity-90"
        style="background-color: #BB080B;"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        New Project
      </button>
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

    <!-- Modal Overlay -->
    <Transition name="fade">
      <div
        v-if="showModal"
        class="fixed inset-0 z-50 flex items-center justify-center px-4"
        style="background: rgba(0,0,0,0.45);"
        @click.self="closeModal"
      >
        <Transition name="slide-up">
          <div
            v-if="showModal"
            class="w-full max-w-md rounded-2xl p-6 shadow-2xl"
            style="background: #FFFFFF;"
          >
            <!-- Modal Header -->
            <div class="flex items-center justify-between mb-5">
              <h2 class="text-base font-bold" style="color: #1A1A1A;">New Project</h2>
              <button
                @click="closeModal"
                class="w-7 h-7 flex items-center justify-center rounded-full transition-colors hover:bg-gray-100"
                style="color: #6B6B6B;"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <!-- Form -->
            <div class="flex flex-col gap-4">

              <!-- Title -->
              <div class="flex flex-col gap-1.5">
                <label class="text-xs font-semibold uppercase tracking-widest" style="color: #BB080B;">
                  Title <span style="color: #BB080B;">*</span>
                </label>
                <input
                  v-model="form.title"
                  type="text"
                  placeholder="My awesome project"
                  class="w-full px-3 py-2.5 rounded-xl text-sm outline-none transition-all"
                  style="border: 1.5px solid #E0E0E0; color: #1A1A1A;"
                  :style="{ borderColor: createError && !form.title.trim() ? '#BB080B' : '#E0E0E0' }"
                  @keydown.enter="createProject"
                  @focus="e => e.target.style.borderColor = '#BB080B'"
                  @blur="e => e.target.style.borderColor = '#E0E0E0'"
                />
              </div>

              <!-- Description -->
              <div class="flex flex-col gap-1.5">
                <label class="text-xs font-semibold uppercase tracking-widest" style="color: #6B6B6B;">
                  Description <span class="font-normal normal-case tracking-normal" style="color: #AAAAAA;">(optional)</span>
                </label>
                <textarea
                  v-model="form.description"
                  placeholder="What is this project about?"
                  rows="3"
                  class="w-full px-3 py-2.5 rounded-xl text-sm outline-none resize-none transition-all"
                  style="border: 1.5px solid #E0E0E0; color: #1A1A1A;"
                  @focus="e => e.target.style.borderColor = '#BB080B'"
                  @blur="e => e.target.style.borderColor = '#E0E0E0'"
                />
              </div>

              <!-- Error -->
              <p v-if="createError" class="text-xs" style="color: #BB080B;">
                {{ createError }}
              </p>

              <!-- Actions -->
              <div class="flex gap-3 pt-1">
                <button
                  @click="closeModal"
                  class="flex-1 py-2.5 rounded-xl text-sm font-semibold transition-colors hover:bg-gray-100"
                  style="color: #6B6B6B; border: 1.5px solid #E0E0E0;"
                >
                  Cancel
                </button>
                <button
                  @click="createProject"
                  :disabled="creating"
                  class="flex-1 py-2.5 rounded-xl text-sm font-semibold text-white transition-opacity"
                  :class="creating ? 'opacity-60 cursor-not-allowed' : 'hover:opacity-90'"
                  style="background-color: #BB080B;"
                >
                  <span v-if="creating" class="flex items-center justify-center gap-2">
                    <svg class="w-4 h-4 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
                    </svg>
                    Creating...
                  </span>
                  <span v-else>Create</span>
                </button>
              </div>

            </div>
          </div>
        </Transition>
      </div>
    </Transition>

  </main>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.slide-up-enter-active, .slide-up-leave-active { transition: transform 0.2s ease, opacity 0.2s ease; }
.slide-up-enter-from, .slide-up-leave-to { transform: translateY(16px); opacity: 0; }
</style>

