<template>
  <div class="relative">
    <button
      class="flex items-center gap-2 px-3.5 py-2 bg-surface-raised border border-border-subtle rounded-lg cursor-pointer transition-all duration-200 hover:bg-surface-overlay hover:border-border-default font-[inherit] text-sm text-text-secondary"
      @click="toggleDropdown"
      @blur="handleBlur"
    >
      <svg
        width="20"
        height="20"
        viewBox="0 0 20 20"
        fill="none"
        class="text-text-muted flex-shrink-0"
      >
        <circle cx="10" cy="10" r="7.5" stroke="currentColor" stroke-width="1.5"/>
        <path d="M3 10H17" stroke="currentColor" stroke-width="1.5"/>
        <path d="M10 3C10 3 7.5 5.5 7.5 10C7.5 14.5 10 17 10 17" stroke="currentColor" stroke-width="1.5"/>
        <path d="M10 3C10 3 12.5 5.5 12.5 10C12.5 14.5 10 17 10 17" stroke="currentColor" stroke-width="1.5"/>
      </svg>
      <span class="font-medium">{{ localeName }}</span>
      <svg
        width="16"
        height="16"
        viewBox="0 0 16 16"
        fill="none"
        class="text-text-muted transition-transform duration-200 flex-shrink-0"
        :class="{ 'rotate-180': isDropdownOpen }"
      >
        <path d="M4 6L8 10L12 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
    </button>

    <div v-if="isDropdownOpen" class="absolute top-[calc(100%+0.5rem)] right-0 min-w-[160px] bg-surface-card border border-border-default rounded-xl shadow-2xl z-[1000] overflow-hidden">
      <button
        v-for="locale in availableLocales"
        :key="locale"
        class="w-full flex items-center justify-between gap-3 px-4 py-3 bg-transparent border-none text-left cursor-pointer text-sm font-medium text-text-secondary hover:bg-surface-raised transition-colors duration-150 font-[inherit]"
        :class="{ 'bg-indigo-950 text-accent': currentLocale === locale }"
        @mousedown.prevent="selectLanguage(locale)"
      >
        <span class="flex-1">{{ getLanguageName(locale) }}</span>
        <svg
          v-if="currentLocale === locale"
          width="18"
          height="18"
          viewBox="0 0 18 18"
          fill="none"
          class="text-accent flex-shrink-0"
        >
          <path d="M4 9L7.5 12.5L14 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from '../composables/useI18n'

const { currentLocale, setLocale, availableLocales, localeName } = useI18n()

const isDropdownOpen = ref(false)

const languageNames = {
  en: 'English',
  ja: '日本語'
}

const getLanguageName = (locale) => {
  return languageNames[locale] || locale
}

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value
}

const handleBlur = () => {
  // Delay to allow mousedown events on dropdown items to fire first
  setTimeout(() => {
    isDropdownOpen.value = false
  }, 200)
}

const selectLanguage = (locale) => {
  setLocale(locale)
  isDropdownOpen.value = false
}
</script>
