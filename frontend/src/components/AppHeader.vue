<script setup>
import { useTheme } from "../composables/useTheme.js";
import { useAuth } from "../composables/useAuth.js";

defineProps({
    username: { type: String, required: true },
});

const { isDark, toggle } = useTheme();
const { logout } = useAuth();
</script>

<template>
    <header
        class="border-b border-gray-800 dark:border-gray-800 bg-white dark:bg-gray-950 px-6 py-4 transition-colors duration-300"
    >
        <div class="max-w-6xl mx-auto flex items-center justify-between">
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
                    <span
                        class="absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-white shadow transition-transform duration-300"
                        :class="isDark ? 'translate-x-6' : 'translate-x-0'"
                    />
                    <span
                        class="absolute inset-0 flex items-center pointer-events-none"
                        :class="isDark ? 'justify-start pl-1' : 'justify-end pr-1'"
                    >
                        <span class="text-xs">{{ isDark ? "🌙" : "☀️" }}</span>
                    </span>
                </button>

                <!-- Username + Logout -->
                <div
                    class="flex items-center gap-2 bg-gray-100 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-full px-4 py-1.5 transition-colors duration-300"
                >
                    <div class="w-2 h-2 rounded-full bg-blue-400"></div>
                    <span class="text-gray-700 dark:text-gray-300 text-sm font-mono">
                        {{ username }}
                    </span>
                    <button
                        @click="logout"
                        class="ml-1 text-gray-400 hover:text-red-400 transition-colors duration-200"
                        title="Logout"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                            <polyline points="16 17 21 12 16 7"/>
                            <line x1="21" y1="12" x2="9" y2="12"/>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    </header>
</template>
