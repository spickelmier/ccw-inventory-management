<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen && backlogItem" class="modal-overlay" @click="close">
        <div class="modal-container max-w-[700px]" @click.stop>
          <div class="modal-header">
            <h3 class="modal-title">{{ t('backlogModal.title') }}</h3>
            <button class="close-button" @click="close">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M15 5L5 15M5 5L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <div class="modal-body">
            <div class="flex items-center gap-5 pb-6 border-b border-border-subtle mb-6">
              <div class="w-16 h-16 bg-gradient-to-br from-status-danger to-red-700 rounded-xl flex items-center justify-center text-white shrink-0">
                <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                  <path d="M24 8L24 28M24 34L24 36" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
                  <circle cx="24" cy="24" r="18" stroke="currentColor" stroke-width="3"/>
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <h4 class="text-2xl font-bold text-text-primary m-0 mb-2">{{ translateProductName(backlogItem.item_name) }}</h4>
                <div class="text-sm text-text-muted font-mono">SKU: {{ backlogItem.item_sku }}</div>
              </div>
              <span class="badge shrink-0" :class="backlogItem.priority">
                {{ backlogItem.priority }} {{ t('backlogModal.priority') }}
              </span>
            </div>

            <div class="grid grid-cols-2 gap-4 mb-8">
              <div class="p-5 rounded-xl border-2 border-red-800 bg-red-900/20">
                <div class="text-[0.813rem] font-semibold uppercase tracking-wider text-text-muted mb-2">{{ t('backlogModal.shortageAmount') }}</div>
                <div class="text-[1.875rem] font-bold text-status-danger">{{ shortage }} {{ t('backlogModal.units') }}</div>
              </div>
              <div class="p-5 rounded-xl border-2 border-amber-700 bg-amber-900/20">
                <div class="text-[0.813rem] font-semibold uppercase tracking-wider text-text-muted mb-2">{{ t('backlogModal.daysDelayed') }}</div>
                <div class="text-[1.875rem] font-bold text-status-warning">{{ backlogItem.days_delayed }} {{ t('backlogModal.days') }}</div>
              </div>
            </div>

            <div class="info-grid">
              <div class="info-item">
                <div class="info-label">{{ t('backlogModal.orderId') }}</div>
                <div class="info-value font-mono text-accent">{{ backlogItem.order_id }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">{{ t('backlogModal.itemSku') }}</div>
                <div class="info-value font-mono text-accent">{{ backlogItem.item_sku }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">{{ t('backlogModal.quantityNeeded') }}</div>
                <div class="info-value">{{ backlogItem.quantity_needed }} {{ t('backlogModal.units') }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">{{ t('backlogModal.quantityAvailable') }}</div>
                <div class="info-value">{{ backlogItem.quantity_available }} {{ t('backlogModal.units') }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">{{ t('backlogModal.expectedDate') }}</div>
                <div class="info-value">{{ formatDate(backlogItem.expected_date) }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">{{ t('backlogModal.status') }}</div>
                <div class="info-value">
                  <span class="badge danger">{{ t('status.backordered') }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn-secondary" @click="close">{{ t('common.close') }}</button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from '../composables/useI18n'

const { t, translateProductName } = useI18n()

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  backlogItem: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close'])

const shortage = computed(() => {
  if (!props.backlogItem) return 0
  return props.backlogItem.quantity_needed - props.backlogItem.quantity_available
})

const close = () => {
  emit('close')
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.2s ease;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.95);
}
</style>
