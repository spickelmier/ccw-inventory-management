<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen" class="modal-overlay" @click="close">
        <div class="modal-container max-w-[900px]" @click.stop>
          <div class="modal-header">
            <h3 class="modal-title">{{ t('tasks.title') }}</h3>
            <button class="close-button" @click="close">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M15 5L5 15M5 5L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <div class="modal-body">
            <!-- Add Task Form -->
            <div class="bg-surface-raised rounded-xl p-6 mb-6">
              <div class="flex gap-4 mb-4 last:mb-0">
                <div class="flex flex-col gap-2 flex-1">
                  <label for="task-title" class="text-sm font-semibold text-text-secondary">{{ t('tasks.taskTitle') }}</label>
                  <input
                    id="task-title"
                    v-model="newTask.title"
                    type="text"
                    :placeholder="t('tasks.taskTitlePlaceholder')"
                    class="px-3 py-3 border-2 border-border-default rounded-lg text-sm bg-surface-card text-text-primary font-[inherit] focus:outline-none focus:border-accent transition-colors"
                    @keyup.enter="handleAddTask"
                  />
                </div>
              </div>

              <div class="flex gap-4 mb-4 last:mb-0">
                <div class="flex flex-col gap-2 flex-1">
                  <label for="task-priority" class="text-sm font-semibold text-text-secondary">{{ t('tasks.priority') }}</label>
                  <select
                    id="task-priority"
                    v-model="newTask.priority"
                    class="px-3 py-3 border-2 border-border-default rounded-lg text-sm bg-surface-card text-text-primary cursor-pointer font-[inherit] focus:outline-none focus:border-accent transition-colors"
                  >
                    <option value="high">{{ t('priority.high') }}</option>
                    <option value="medium">{{ t('priority.medium') }}</option>
                    <option value="low">{{ t('priority.low') }}</option>
                  </select>
                </div>

                <div class="flex flex-col gap-2 flex-1">
                  <label for="task-due-date" class="text-sm font-semibold text-text-secondary">{{ t('tasks.dueDate') }}</label>
                  <input
                    id="task-due-date"
                    v-model="newTask.dueDate"
                    type="date"
                    class="px-3 py-3 border-2 border-border-default rounded-lg text-sm bg-surface-card text-text-primary font-[inherit] focus:outline-none focus:border-accent transition-colors"
                  />
                </div>

                <div class="flex items-end">
                  <button @click="handleAddTask" class="px-7 py-3 bg-gradient-to-br from-accent to-indigo-700 text-white border-none rounded-lg font-semibold cursor-pointer whitespace-nowrap hover:-translate-y-0.5 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:!transform-none" :disabled="!newTask.title.trim() || !newTask.dueDate">
                    {{ t('tasks.addTask') }}
                  </button>
                </div>
              </div>
            </div>

            <div class="h-px bg-border-subtle my-8"></div>

            <!-- Tasks List -->
            <div v-if="sortedTasks.length === 0" class="text-center py-12 text-text-muted text-lg italic">
              {{ t('tasks.noTasks') }}
            </div>

            <div v-else class="flex flex-col gap-3">
              <div
                v-for="task in sortedTasks"
                :key="task.id"
                class="bg-surface-raised border-2 border-border-subtle rounded-xl p-4 transition-all hover:border-border-default"
                :class="{
                  'border-l-4 border-l-status-danger': task.priority === 'high',
                  'border-l-4 border-l-status-warning': task.priority === 'medium',
                  'border-l-4 border-l-accent': task.priority === 'low',
                  'opacity-60': task.status === 'completed'
                }"
              >
                <div class="flex justify-between items-start mb-3 gap-4">
                  <div class="flex items-center gap-3 flex-1">
                    <input
                      type="checkbox"
                      :checked="task.status === 'completed'"
                      @change="$emit('toggle-task', task.id)"
                      class="w-5 h-5 cursor-pointer shrink-0 accent-violet-500"
                    />
                    <span
                      class="flex-1 cursor-pointer select-none text-base font-semibold leading-snug"
                      :class="{ 'line-through text-text-muted': task.status === 'completed', 'text-text-primary': task.status !== 'completed' }"
                      @click="$emit('toggle-task', task.id)"
                    >{{ task.title }}</span>
                  </div>
                  <button @click="$emit('delete-task', task.id)" class="w-7 h-7 bg-status-danger text-white border-none rounded-md text-xl flex items-center justify-center p-0 cursor-pointer transition-all hover:scale-110 shrink-0" title="Delete task">
                    ×
                  </button>
                </div>

                <div class="flex items-center gap-4">
                  <span
                    class="text-[0.688rem] font-semibold uppercase py-1 px-2.5 rounded"
                    :class="{ 'bg-red-900/40 text-status-danger': task.priority === 'high', 'bg-amber-900/40 text-status-warning': task.priority === 'medium', 'bg-blue-900/40 text-status-info': task.priority === 'low' }"
                  >
                    {{ translatePriority(task.priority) }}
                  </span>
                  <div class="flex items-center gap-2 text-[0.813rem] text-text-muted">
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                      <rect x="2" y="3" width="10" height="9" rx="1" stroke="currentColor" stroke-width="1.2"/>
                      <path d="M4.5 1.5V4.5M9.5 1.5V4.5M2 6H12" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                    </svg>
                    {{ formatDueDate(task.dueDate) }}
                  </div>
                  <span
                    class="text-xs font-semibold py-1 px-2.5 rounded ml-auto"
                    :class="{ 'bg-red-900/40 text-status-danger': getStatusClass(task.dueDate, task.status) === 'overdue', 'bg-amber-900/40 text-status-warning': getStatusClass(task.dueDate, task.status) === 'urgent', 'bg-blue-900/40 text-status-info': getStatusClass(task.dueDate, task.status) === 'upcoming', 'bg-emerald-900/40 text-status-success': getStatusClass(task.dueDate, task.status) === 'completed' }"
                  >
                    {{ getStatusText(task.dueDate, task.status) }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn-secondary" @click="close">{{ t('profileDetails.close') }}</button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script>
import { ref, computed } from 'vue'
import { useI18n } from '../composables/useI18n'

export default {
  name: 'TasksModal',
  props: {
    isOpen: {
      type: Boolean,
      required: true
    },
    tasks: {
      type: Array,
      default: () => []
    }
  },
  emits: ['close', 'add-task', 'delete-task', 'toggle-task'],
  setup(props, { emit }) {
    const { t, currentLocale } = useI18n()
    const newTask = ref({
      title: '',
      priority: 'medium',
      dueDate: ''
    })

    const sortedTasks = computed(() => {
      // Don't sort - just return tasks in their current order (newest first)
      return [...props.tasks]
    })

    const close = () => {
      emit('close')
    }

    const handleAddTask = () => {
      if (newTask.value.title.trim() && newTask.value.dueDate) {
        emit('add-task', {
          title: newTask.value.title.trim(),
          priority: newTask.value.priority,
          dueDate: newTask.value.dueDate
        })
        newTask.value = {
          title: '',
          priority: 'medium',
          dueDate: ''
        }
      }
    }

    const formatDueDate = (dateString) => {
      const date = new Date(dateString)
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      const dueDate = new Date(date)
      dueDate.setHours(0, 0, 0, 0)

      const diffTime = dueDate - today
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

      const isJapanese = currentLocale.value === 'ja'

      if (diffDays === 0) return isJapanese ? '今日' : 'today'
      if (diffDays === 1) return isJapanese ? '明日' : 'tomorrow'
      if (diffDays === -1) return isJapanese ? '昨日' : 'yesterday'
      if (diffDays < 0) return isJapanese ? `${Math.abs(diffDays)}日前` : `${Math.abs(diffDays)} days ago`
      if (diffDays < 7) return isJapanese ? `${diffDays}日後` : `in ${diffDays} days`

      const locale = isJapanese ? 'ja-JP' : 'en-US'
      return date.toLocaleDateString(locale, {
        month: 'short',
        day: 'numeric',
        year: date.getFullYear() !== today.getFullYear() ? 'numeric' : undefined
      })
    }

    const getStatusClass = (dueDate, status) => {
      if (status === 'completed') return 'completed'

      const today = new Date()
      today.setHours(0, 0, 0, 0)
      const due = new Date(dueDate)
      due.setHours(0, 0, 0, 0)

      const diffTime = due - today
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

      if (diffDays < 0) return 'overdue'
      if (diffDays <= 1) return 'urgent'
      return 'upcoming'
    }

    const getStatusText = (dueDate, status) => {
      const isJapanese = currentLocale.value === 'ja'

      if (status === 'completed') return isJapanese ? '完了' : 'Completed'

      const statusClass = getStatusClass(dueDate, status)
      if (statusClass === 'overdue') return isJapanese ? '期限超過' : 'Overdue'
      if (statusClass === 'urgent') return isJapanese ? 'もうすぐ期限' : 'Due Soon'
      return isJapanese ? '予定' : 'Upcoming'
    }

    const translatePriority = (priority) => {
      const priorityMap = {
        'high': t('priority.high'),
        'medium': t('priority.medium'),
        'low': t('priority.low')
      }
      return priorityMap[priority] || priority
    }

    return {
      t,
      newTask,
      sortedTasks,
      close,
      handleAddTask,
      formatDueDate,
      getStatusClass,
      getStatusText,
      translatePriority
    }
  }
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.9);
}
</style>
