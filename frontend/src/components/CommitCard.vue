<script setup>
import { ref, computed } from 'vue'

const props = defineProps({ commit: Object })

const open = ref(false)
const toggle = () => { open.value = !open.value }

// commit_info приходит как JSON-строка
const info = computed(() => {
  try { return JSON.parse(props.commit.commit_info) }
  catch { return null }
})

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
      <div class="flex items-center gap-3 min-w-0">
        <span class="text-gray-300 dark:text-gray-600 font-mono text-xs flex-shrink-0">●</span>
        <span class="text-gray-800 dark:text-gray-200 text-sm font-semibold truncate">{{ commit.summary }}</span>
      </div>
      <div class="flex items-center gap-3 flex-shrink-0 ml-3">
        <span class="text-gray-500 dark:text-gray-400 text-xs font-medium">{{ commit.author }}</span>
        <span class="text-gray-400 text-xs transition-transform duration-300" :class="open ? 'rotate-180' : ''">▼</span>
      </div>
    </div>

    <Transition name="expand">
      <div
        v-if="open"
        class="px-4 py-4 bg-white dark:bg-gray-900 border border-t-0 border-blue-400 dark:border-blue-700 rounded-b-xl"
      >
        <div class="flex flex-col gap-3 text-sm">

          <div class="flex items-start justify-between gap-4">
            <p class="text-gray-600 dark:text-gray-400 leading-snug">{{ commit.summary }}</p>
            <span :class="[
              'flex-shrink-0 text-xs px-2 py-0.5 rounded-full font-mono',
              commit.conventional_commits
                ? 'bg-green-100 dark:bg-green-900/40 text-green-600 dark:text-green-400'
                : 'bg-gray-100 dark:bg-gray-800 text-gray-400'
            ]">
              {{ commit.conventional_commits ? 'conventional ✓' : 'non-conventional' }}
            </span>
          </div>

          <div v-if="commit.technical" class="flex flex-col gap-1">
            <span class="text-xs font-semibold uppercase tracking-wider text-blue-400 dark:text-blue-500">Technical</span>
            <p class="text-gray-500 dark:text-gray-400 leading-relaxed">{{ commit.technical }}</p>
          </div>

          <div v-if="commit.risks" class="flex flex-col gap-1">
            <span class="text-xs font-semibold uppercase tracking-wider text-yellow-500 dark:text-yellow-400">Risks</span>
            <p class="text-gray-500 dark:text-gray-400 leading-relaxed">{{ commit.risks }}</p>
          </div>

          <div v-if="commit.process" class="flex flex-col gap-1">
            <span class="text-xs font-semibold uppercase tracking-wider text-purple-400 dark:text-purple-500">Process</span>
            <p class="text-gray-500 dark:text-gray-400 leading-relaxed">{{ commit.process }}</p>
          </div>

          <!-- Данные из commit_info -->
          <div v-if="info" class="flex flex-col gap-1 pt-2 border-t border-gray-100 dark:border-gray-800">
            <span class="text-xs font-semibold uppercase tracking-wider text-gray-400">Diff</span>
            <p class="text-gray-400 dark:text-gray-500 text-xs font-mono">
              +{{ info.diffs?.additions }} / -{{ info.diffs?.deletions }}
              · {{ info.diffs?.files?.length }} file(s)
              · {{ formatDate(info.commit_created) }}
            </p>
          </div>

          <div class="flex items-center justify-between pt-2 border-t border-gray-100 dark:border-gray-800 text-xs text-gray-400">
            <span>Author: <span class="text-gray-600 dark:text-gray-300">{{ commit.author }}</span></span>
            <span class="font-mono text-gray-300 dark:text-gray-700">{{ commit.sha.slice(0, 7) }}</span>
          </div>

        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.expand-enter-active, .expand-leave-active {
  transition: opacity 0.22s ease, max-height 0.28s cubic-bezier(0.4, 0, 0.2, 1);
  max-height: 500px;
  overflow: hidden;
}
.expand-enter-from, .expand-leave-to { opacity: 0; max-height: 0; }
</style>
