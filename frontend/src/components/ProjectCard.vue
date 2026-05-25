<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  project: Object
})

const router = useRouter()

const SLOTS = 3

const taskSlots = computed(() => {
  const slots = props.project.tasks?.slice(0, SLOTS) ?? []
  while (slots.length < SLOTS) slots.push(null)
  return slots
})

const hiddenCount = computed(() => {
  const total = props.project.tasks?.length ?? 0
  return Math.max(0, total - SLOTS)
})

const goToProject = () => {
  router.push(`/projects/${props.project.id}`)
}

</script>

<template>
  <div
    @click="goToProject"
    class="group bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 hover:border-blue-400 dark:hover:border-blue-700/60 rounded-2xl p-5 cursor-pointer transition-all duration-200 hover:shadow-lg hover:shadow-blue-100 dark:hover:shadow-blue-950/50"
  >
    <div class="flex items-start justify-between mb-4">
      <h3 class="text-gray-900 dark:text-white font-semibold text-base group-hover:text-blue-600 dark:group-hover:text-blue-300 transition-colors">
        {{ project.title }}
      </h3>
      <span class="text-2xl opacity-40 group-hover:opacity-80 transition-opacity">☄️</span>
    </div>

    <div>
      <p class="text-gray-400 dark:text-gray-500 text-xs uppercase tracking-wider mb-2">Tasks</p>
      <div class="flex flex-col gap-1">
        <div
          v-for="(task, index) in taskSlots"
          :key="index"
          class="flex items-center gap-2 text-sm h-5"
        >
          <template v-if="task">
            <span class="w-1 h-1 rounded-full bg-blue-500 flex-shrink-0"></span>
            <span class="text-gray-500 dark:text-gray-400">{{ task.title }}</span>
          </template>
          <template v-else>
            <span class="invisible">placeholder</span>
          </template>
        </div>
      </div>
      <p v-if="hiddenCount > 0" class="text-blue-500/60 text-xs mt-2 font-mono">
        +{{ hiddenCount }} more tasks
      </p>
    </div>
  </div>
</template>
