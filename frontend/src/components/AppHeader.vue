<script setup>
import { useTheme } from "../composables/useTheme.js";

defineProps({
    username: { type: String, required: true },
});

const { isDark, toggle } = useTheme();
</script>

<template>
    <header
        class="border-b border-gray-800 dark:border-gray-800 bg-white dark:bg-gray-950 px-6 py-4 transition-colors duration-300"
    >
        <div class="max-w-6xl mx-auto flex items-center justify-between">
            <!-- Логотип -->
            <!-- Logo -->
            <RouterLink to="/projects">
                <div class="flex items-center gap-2">
                    <img
                        src="../assets/logo2.png"
                        alt="CommetAI"
                        class="h-8"
                    />
                    <span
                        class="text-gray-900 dark:text-white font-bold tracking-tight"
                        >CommetAI</span
                    >
                </div>
            </RouterLink>

            <!-- Правая часть -->
            <div class="flex items-center gap-4">
                <!-- Свитчер темы -->
                <button
                    @click="toggle"
                    class="relative w-12 h-6 rounded-full transition-colors duration-300 focus:outline-none"
                    :class="isDark ? 'bg-blue-600' : 'bg-gray-300'"
                >
                    <!-- Кружок -->
                    <span
                        class="absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-white shadow transition-transform duration-300"
                        :class="isDark ? 'translate-x-6' : 'translate-x-0'"
                    />
                    <!-- Иконка внутри кружка -->
                    <span
                        class="absolute inset-0 flex items-center pointer-events-none"
                        :class="
                            isDark ? 'justify-start pl-1' : 'justify-end pr-1'
                        "
                    >
                        <span class="text-xs">{{ isDark ? "🌙" : "☀️" }}</span>
                    </span>
                </button>

                <!-- Username -->
                <div
                    class="flex items-center gap-2 bg-gray-100 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-full px-4 py-1.5 transition-colors duration-300"
                >
                    <div class="w-2 h-2 rounded-full bg-blue-400"></div>
                    <span
                        class="text-gray-700 dark:text-gray-300 text-sm font-mono"
                        >{{ username }}</span
                    >
                </div>
            </div>
        </div>
    </header>
</template>
