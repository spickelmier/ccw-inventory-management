<template>
  <div class="relative">
    <button
      class="flex items-center gap-2.5 px-3.5 py-2 bg-surface-raised border border-border-subtle rounded-lg cursor-pointer transition-all duration-200 hover:bg-surface-overlay hover:border-border-default font-[inherit]"
      @click="toggleDropdown"
      @blur="handleBlur"
    >
      <div class="w-8 h-8 rounded-full bg-gradient-to-br from-accent to-indigo-700 text-white flex items-center justify-center font-semibold text-xs tracking-wide flex-shrink-0">
        {{ getInitials(currentUser.name) }}
      </div>
      <span class="text-sm font-medium text-text-primary">{{ currentUser.name }}</span>
      <svg
        class="text-text-muted transition-transform duration-200 flex-shrink-0"
        :class="{ 'rotate-180': isDropdownOpen }"
        width="16"
        height="16"
        viewBox="0 0 16 16"
        fill="none"
      >
        <path d="M4 6L8 10L12 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
    </button>

    <div v-if="isDropdownOpen" class="absolute top-[calc(100%+0.5rem)] right-0 min-w-[280px] bg-surface-card border border-border-default rounded-xl shadow-2xl z-[1000] overflow-hidden">
      <div class="p-4 flex gap-3.5 items-center bg-surface-raised">
        <div class="w-12 h-12 rounded-full bg-gradient-to-br from-accent to-indigo-700 text-white flex items-center justify-center font-bold text-base tracking-wide flex-shrink-0">
          {{ getInitials(currentUser.name) }}
        </div>
        <div class="flex-1 min-w-0">
          <div class="font-semibold text-text-primary text-[0.938rem] mb-1">{{ currentUser.name }}</div>
          <div class="text-[0.813rem] text-text-muted truncate">{{ currentUser.email }}</div>
        </div>
      </div>

      <div class="h-px bg-border-subtle my-1"></div>

      <button
        class="w-full flex items-center gap-3 px-4 py-3 bg-transparent border-none text-left cursor-pointer text-sm font-medium text-text-secondary hover:bg-surface-raised transition-colors duration-150 font-[inherit]"
        @mousedown.prevent="showProfileDetails"
      >
        <svg class="text-text-muted flex-shrink-0" width="18" height="18" viewBox="0 0 18 18" fill="none">
          <path d="M9 9C10.6569 9 12 7.65685 12 6C12 4.34315 10.6569 3 9 3C7.34315 3 6 4.34315 6 6C6 7.65685 7.34315 9 9 9Z" stroke="currentColor" stroke-width="1.5"/>
          <path d="M15 15C15 12.7909 12.3137 11 9 11C5.68629 11 3 12.7909 3 15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        {{ t('profile.profileDetails') }}
      </button>

      <button
        class="w-full flex items-center gap-3 px-4 py-3 bg-transparent border-none text-left cursor-pointer text-sm font-medium text-text-secondary hover:bg-surface-raised transition-colors duration-150 font-[inherit]"
        @mousedown.prevent="showTasks"
      >
        <svg class="text-text-muted flex-shrink-0" width="18" height="18" viewBox="0 0 18 18" fill="none">
          <path d="M15 3H3C2.44772 3 2 3.44772 2 4V14C2 14.5523 2.44772 15 3 15H15C15.5523 15 16 14.5523 16 14V4C16 3.44772 15.5523 3 15 3Z" stroke="currentColor" stroke-width="1.5"/>
          <path d="M6 7L8 9L12 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        {{ t('profile.myTasks') }}
        <span v-if="pendingTaskCount > 0" class="ml-auto bg-accent text-white text-xs font-semibold px-2 py-0.5 rounded-full min-w-[20px] text-center">{{ pendingTaskCount }}</span>
      </button>

      <div class="h-px bg-border-subtle my-1"></div>

      <button
        class="w-full flex items-center gap-3 px-4 py-3 bg-transparent border-none text-left cursor-pointer text-sm font-medium text-status-danger hover:bg-red-950 transition-colors duration-150 font-[inherit]"
        @mousedown.prevent="handleLogout"
      >
        <svg class="text-status-danger flex-shrink-0" width="18" height="18" viewBox="0 0 18 18" fill="none">
          <path d="M7 15H4C3.44772 15 3 14.5523 3 14V4C3 3.44772 3.44772 3 4 3H7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          <path d="M11 12L15 9M15 9L11 6M15 9H7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        {{ t('profile.logout') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuth } from '../composables/useAuth'
import { useI18n } from '../composables/useI18n'

const { currentUser, logout, getInitials } = useAuth()
const { t } = useI18n()

const isDropdownOpen = ref(false)
const emit = defineEmits(['show-profile-details', 'show-tasks'])

const pendingTaskCount = computed(() => {
  return currentUser.value.tasks.filter(task => task.status === 'pending').length
})

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value
}

const handleBlur = () => {
  // Delay to allow mousedown events on dropdown items to fire first
  setTimeout(() => {
    isDropdownOpen.value = false
  }, 200)
}

const showProfileDetails = () => {
  isDropdownOpen.value = false
  emit('show-profile-details')
}

const showTasks = () => {
  isDropdownOpen.value = false
  emit('show-tasks')
}

const handleLogout = () => {
  isDropdownOpen.value = false
  logout()
}
</script>
