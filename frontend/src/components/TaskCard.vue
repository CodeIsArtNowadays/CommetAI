<script setup>
import { ref } from 'vue'

const props = defineProps({
  task: Object
})

const open = ref(false)
const toggle = () => { open.value = !open.value }

const formatDate = (str) => {
  if (!str) return '—'
  return new Date(str).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
}
</script>

<template>
  <div>
    <div
      @click="toggle"
      :class="[
        'flex items-center justify-between px-4 py-3 bg-white dark:bg-gray-900 border cursor-pointer transition-all duration-200 select-none',
        open
          ? 'rounded-t-xl border-blue-400 dark:border-blue-700 border-b-transparent'
          : 'rounded-xl border-gray-200 dark:border-gray-800 hover:border-blue-400 dark:hover:border-blue-700/60'
      ]"
    >
      <div class="flex items-center gap-3">
        <span :class="['w-2 h-2 rounded-full flex-shrink-0', task.is_done ? 'bg-green-500' : 'bg-yellow-400']"></span>
        <span class="text-gray-800 dark:text-gray-200 text-sm font-semibold">{{ task.title }}</span>
      </div>
      <div class="flex items-center gap-3">
        <span class="text-gray-500 dark:text-gray-400 text-xs font-mono font-medium">{{ formatDate(task.due_time) }}</span>
        <span
          class="text-gray-400 text-xs transition-transform duration-300"
          :class="open ? 'rotate-180' : ''"
        >▼</span>
      </div>
    </div>

    <Transition name="expand">
      <div
        v-if="open"
        class="px-4 py-4 bg-white dark:bg-gray-900 border border-t-0 border-blue-400 dark:border-blue-700 rounded-b-xl"
      >
        <div class="flex flex-col gap-3 text-sm">
          <p class="text-gray-500 dark:text-gray-400 leading-relaxed">{{ task.description || '—' }}</p>

          <div class="flex items-center justify-between pt-2 border-t border-gray-100 dark:border-gray-800">
            <div class="flex items-center gap-2 text-gray-400 text-xs">
              <span>Due:</span>
              <span class="font-mono text-gray-600 dark:text-gray-300">{{ formatDate(task.due_time) }}</span>
            </div>
            <div v-if="task.commit_sha" class="flex items-center gap-2 text-xs">
              <span class="text-gray-400">Commit:</span>
              <span class="font-mono text-blue-500 dark:text-blue-400">{{ task.commit_sha.slice(0, 7) }}</span>
            </div>
            <span v-else class="text-gray-300 dark:text-gray-700 text-xs font-mono">no commit</span>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.expand-enter-active,
.expand-leave-active {
  transition: opacity 0.22s ease, max-height 0.28s cubic-bezier(0.4, 0, 0.2, 1);
  max-height: 300px;
  overflow: hidden;
}
.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
}
</style>
