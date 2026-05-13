<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen && inventoryItem" class="modal-overlay" @click="close">
        <div class="modal-container max-w-[700px]" @click.stop>
          <div class="modal-header">
            <h3 class="modal-title">{{ t('inventoryModal.title') }}</h3>
            <button class="close-button" @click="close">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M15 5L5 15M5 5L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <div class="modal-body">
            <div class="flex items-center gap-5 pb-6 border-b border-border-subtle mb-6">
              <div class="w-16 h-16 rounded-xl flex items-center justify-center text-white shrink-0"
                   :class="{
                     'bg-gradient-to-br from-status-success to-emerald-700': getStockIconClass() === 'success-icon',
                     'bg-gradient-to-br from-status-warning to-amber-700': getStockIconClass() === 'warning-icon',
                     'bg-gradient-to-br from-status-danger to-red-700': getStockIconClass() === 'danger-icon'
                   }">
                <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                  <rect x="8" y="12" width="32" height="28" rx="2" stroke="currentColor" stroke-width="2.5"/>
                  <path d="M16 8V16M32 8V16M8 20H40" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                  <path d="M16 28H32M16 34H24" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <h4 class="text-2xl font-bold text-text-primary m-0 mb-2">{{ translateProductName(inventoryItem.name) }}</h4>
                <div class="text-sm text-text-muted font-mono">SKU: {{ inventoryItem.sku }}</div>
              </div>
              <span class="badge shrink-0" :class="getStockStatusClass()">
                {{ getStockStatus() }}
              </span>
            </div>

            <div class="grid grid-cols-2 gap-4 mb-8">
              <div class="p-5 rounded-xl border-2 border-accent/30 bg-indigo-900/20">
                <div class="text-[0.813rem] font-semibold uppercase tracking-wider text-text-muted mb-2">{{ t('inventoryModal.quantityOnHand') }}</div>
                <div class="text-[1.875rem] font-bold text-text-primary">{{ inventoryItem.quantity_on_hand }} {{ t('inventoryModal.units') }}</div>
              </div>
              <div class="p-5 rounded-xl border-2"
                   :class="{
                     'border-status-success/30 bg-emerald-900/20': getSummaryCardClass() === 'success-card',
                     'border-status-warning/30 bg-amber-900/20': getSummaryCardClass() === 'warning-card',
                     'border-status-danger/30 bg-red-900/20': getSummaryCardClass() === 'danger-card'
                   }">
                <div class="text-[0.813rem] font-semibold uppercase tracking-wider text-text-muted mb-2">{{ t('inventoryModal.stockLevel') }}</div>
                <div class="text-[1.875rem] font-bold text-text-primary">{{ stockPercentage }}%</div>
                <div class="text-xs text-text-muted mt-1">{{ t('inventoryModal.vsReorderPoint') }}</div>
              </div>
            </div>

            <div class="info-grid">
              <div class="info-item">
                <div class="info-label">{{ t('inventoryModal.category') }}</div>
                <div class="info-value">{{ inventoryItem.category }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">{{ t('inventoryModal.location') }}</div>
                <div class="info-value">{{ inventoryItem.location }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">{{ t('inventoryModal.reorderPoint') }}</div>
                <div class="info-value">{{ inventoryItem.reorder_point }} {{ t('inventoryModal.units') }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">{{ t('inventoryModal.unitsRemaining') }}</div>
                <div class="info-value">
                  <span :class="inventoryItem.quantity_on_hand <= inventoryItem.reorder_point ? 'text-status-danger' : 'text-status-success'">
                    {{ inventoryItem.quantity_on_hand - inventoryItem.reorder_point }} {{ t('inventoryModal.units') }}
                  </span>
                </div>
              </div>

              <div class="info-item">
                <div class="info-label">{{ t('inventoryModal.unitCost') }}</div>
                <div class="info-value">{{ currencySymbol }}{{ inventoryItem.unit_cost.toFixed(2) }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">{{ t('inventoryModal.totalValue') }}</div>
                <div class="info-value text-lg text-accent font-bold">
                  {{ currencySymbol }}{{ totalValue.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2}) }}
                </div>
              </div>

              <div class="info-item">
                <div class="info-label">{{ t('inventoryModal.warehouse') }}</div>
                <div class="info-value">{{ translateWarehouse(inventoryItem.location) }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">{{ t('inventoryModal.status') }}</div>
                <div class="info-value">
                  <span :class="['badge', getStockStatusClass()]">
                    {{ getStockStatus() }}
                  </span>
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

const { t, currentCurrency, translateProductName, translateWarehouse } = useI18n()

const currencySymbol = computed(() => {
  return currentCurrency.value === 'JPY' ? '¥' : '$'
})

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  inventoryItem: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close'])

const totalValue = computed(() => {
  if (!props.inventoryItem) return 0
  return props.inventoryItem.quantity_on_hand * props.inventoryItem.unit_cost
})

const stockPercentage = computed(() => {
  if (!props.inventoryItem || props.inventoryItem.reorder_point === 0) return 0
  return Math.round((props.inventoryItem.quantity_on_hand / props.inventoryItem.reorder_point) * 100)
})

const close = () => {
  emit('close')
}

const getStockStatusKey = () => {
  if (!props.inventoryItem) return 'unknown'
  if (props.inventoryItem.quantity_on_hand <= props.inventoryItem.reorder_point) {
    return 'lowStock'
  } else if (props.inventoryItem.quantity_on_hand <= props.inventoryItem.reorder_point * 1.5) {
    return 'adequate'
  } else {
    return 'inStock'
  }
}

const getStockStatus = () => {
  const key = getStockStatusKey()
  if (key === 'unknown') return '-'
  return t(`status.${key}`)
}

const getStockStatusClass = () => {
  const key = getStockStatusKey()
  if (key === 'lowStock') return 'danger'
  if (key === 'adequate') return 'warning'
  return 'success'
}

const getStockIconClass = () => {
  const key = getStockStatusKey()
  if (key === 'lowStock') return 'danger-icon'
  if (key === 'adequate') return 'warning-icon'
  return 'success-icon'
}

const getSummaryCardClass = () => {
  const key = getStockStatusKey()
  if (key === 'lowStock') return 'danger-card'
  if (key === 'adequate') return 'warning-card'
  return 'success-card'
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
