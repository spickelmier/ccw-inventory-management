<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen && costData" class="modal-overlay" @click="close">
        <div class="modal-container max-w-[600px]" @click.stop>
          <div class="modal-header">
            <h3 class="modal-title">{{ costData.month }} {{ t('costModal.titleSuffix') }}</h3>
            <button class="close-button" @click="close">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M15 5L5 15M5 5L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <div class="modal-body">
            <div class="mb-8">
              <div class="p-6 rounded-xl text-center bg-gradient-to-br from-accent to-indigo-700 text-white">
                <div class="text-sm font-semibold uppercase tracking-wider opacity-90 mb-2">{{ t('costModal.totalCosts') }}</div>
                <div class="text-[2.25rem] font-bold">{{ currencySymbol }}{{ totalCosts.toLocaleString() }}</div>
              </div>
            </div>

            <div class="flex flex-col gap-4">
              <div class="p-5 rounded-xl border-2 border-accent/30 bg-indigo-900/20">
                <div class="flex items-center gap-4 mb-2">
                  <div class="w-12 h-12 rounded-xl flex items-center justify-center text-white shrink-0 bg-accent">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                      <rect x="4" y="6" width="16" height="14" rx="2" stroke="currentColor" stroke-width="2"/>
                      <path d="M8 6V4M16 6V4M4 10H20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                  </div>
                  <div class="flex-1">
                    <div class="font-semibold text-text-primary text-base mb-1">{{ t('costModal.procurement') }}</div>
                    <div class="text-2xl font-bold text-text-primary">{{ currencySymbol }}{{ costData.procurement.toLocaleString() }}</div>
                  </div>
                </div>
                <div class="text-sm text-text-muted font-medium">{{ getProcurementPercentage() }}{{ t('costModal.ofTotal') }}</div>
              </div>

              <div class="p-5 rounded-xl border-2 border-violet-400/30 bg-violet-900/20">
                <div class="flex items-center gap-4 mb-2">
                  <div class="w-12 h-12 rounded-xl flex items-center justify-center text-white shrink-0 bg-violet-500">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                      <circle cx="12" cy="12" r="8" stroke="currentColor" stroke-width="2"/>
                      <path d="M12 8V12L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                  </div>
                  <div class="flex-1">
                    <div class="font-semibold text-text-primary text-base mb-1">{{ t('costModal.operational') }}</div>
                    <div class="text-2xl font-bold text-text-primary">{{ currencySymbol }}{{ costData.operational.toLocaleString() }}</div>
                  </div>
                </div>
                <div class="text-sm text-text-muted font-medium">{{ getOperationalPercentage() }}{{ t('costModal.ofTotal') }}</div>
              </div>

              <div class="p-5 rounded-xl border-2 border-cyan-400/30 bg-cyan-900/20">
                <div class="flex items-center gap-4 mb-2">
                  <div class="w-12 h-12 rounded-xl flex items-center justify-center text-white shrink-0 bg-cyan-500">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                      <circle cx="12" cy="8" r="4" stroke="currentColor" stroke-width="2"/>
                      <path d="M6 20C6 16.6863 8.68629 14 12 14C15.3137 14 18 16.6863 18 20" stroke="currentColor" stroke-width="2"/>
                    </svg>
                  </div>
                  <div class="flex-1">
                    <div class="font-semibold text-text-primary text-base mb-1">{{ t('costModal.labor') }}</div>
                    <div class="text-2xl font-bold text-text-primary">{{ currencySymbol }}{{ costData.labor.toLocaleString() }}</div>
                  </div>
                </div>
                <div class="text-sm text-text-muted font-medium">{{ getLaborPercentage() }}{{ t('costModal.ofTotal') }}</div>
              </div>

              <div class="p-5 rounded-xl border-2 border-amber-400/30 bg-amber-900/20">
                <div class="flex items-center gap-4 mb-2">
                  <div class="w-12 h-12 rounded-xl flex items-center justify-center text-white shrink-0 bg-amber-500">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                      <path d="M3 12L5 10M5 10L12 3L19 10M5 10V20C5 20.5523 5.44772 21 6 21H9M19 10L21 12M19 10V20C19 20.5523 18.5523 21 18 21H15M9 21C9 21 9 18 9 16C9 14 10 14 12 14C14 14 15 14 15 16C15 18 15 21 15 21M9 21H15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                  </div>
                  <div class="flex-1">
                    <div class="font-semibold text-text-primary text-base mb-1">{{ t('costModal.overhead') }}</div>
                    <div class="text-2xl font-bold text-text-primary">{{ currencySymbol }}{{ costData.overhead.toLocaleString() }}</div>
                  </div>
                </div>
                <div class="text-sm text-text-muted font-medium">{{ getOverheadPercentage() }}{{ t('costModal.ofTotal') }}</div>
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

const { t, currentCurrency } = useI18n()

const currencySymbol = computed(() => {
  return currentCurrency.value === 'JPY' ? '¥' : '$'
})

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  costData: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close'])

const totalCosts = computed(() => {
  if (!props.costData) return 0
  return props.costData.procurement + props.costData.operational +
         props.costData.labor + props.costData.overhead
})

const getProcurementPercentage = () => {
  if (!props.costData || totalCosts.value === 0) return 0
  return ((props.costData.procurement / totalCosts.value) * 100).toFixed(1)
}

const getOperationalPercentage = () => {
  if (!props.costData || totalCosts.value === 0) return 0
  return ((props.costData.operational / totalCosts.value) * 100).toFixed(1)
}

const getLaborPercentage = () => {
  if (!props.costData || totalCosts.value === 0) return 0
  return ((props.costData.labor / totalCosts.value) * 100).toFixed(1)
}

const getOverheadPercentage = () => {
  if (!props.costData || totalCosts.value === 0) return 0
  return ((props.costData.overhead / totalCosts.value) * 100).toFixed(1)
}

const close = () => {
  emit('close')
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
