<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen && product" class="modal-overlay" @click="close">
        <div class="modal-container max-w-[700px]" @click.stop>
          <div class="modal-header">
            <h3 class="modal-title">{{ t('productModal.title') }}</h3>
            <button class="close-button" @click="close">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M15 5L5 15M5 5L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <div class="modal-body">
            <div class="flex items-center gap-5 pb-6 border-b border-border-subtle mb-8">
              <div class="w-16 h-16 bg-gradient-to-br from-accent to-indigo-700 rounded-xl flex items-center justify-center text-white shrink-0">
                <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                  <rect x="8" y="12" width="32" height="28" rx="2" stroke="currentColor" stroke-width="2.5"/>
                  <path d="M16 8V16M32 8V16M8 20H40" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <h4 class="text-2xl font-bold text-text-primary m-0 mb-2">{{ product.name }}</h4>
                <div class="text-sm text-text-muted font-mono">SKU: {{ product.sku }}</div>
              </div>
              <span class="badge shrink-0" :class="getStockBadgeClass(product.stockLevel)">
                {{ translateStockLevel(product.stockLevel) }}
              </span>
            </div>

            <div class="info-grid">
              <div class="info-item">
                <div class="info-label">{{ t('productModal.category') }}</div>
                <div class="info-value">{{ product.category }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">{{ t('productModal.warehouse') }}</div>
                <div class="info-value">{{ product.warehouse }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">{{ t('productModal.unitsOrdered') }}</div>
                <div class="info-value">{{ product.unitsOrdered }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">{{ t('productModal.totalRevenue') }}</div>
                <div class="info-value">{{ currencySymbol }}{{ product.revenue.toLocaleString() }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">{{ t('productModal.currentStock') }}</div>
                <div class="info-value">{{ product.quantityOnHand }} {{ t('productModal.units') }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">{{ t('productModal.reorderPoint') }}</div>
                <div class="info-value">{{ product.reorderPoint }} {{ t('productModal.units') }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">{{ t('productModal.firstOrderDate') }}</div>
                <div class="info-value">{{ formatDate(product.firstOrderDate) }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">{{ t('productModal.stockStatus') }}</div>
                <div class="info-value">
                  <span class="badge" :class="getStockBadgeClass(product.stockLevel)">
                    {{ translateStockLevel(product.stockLevel) }}
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

const { t, currentCurrency } = useI18n()

const currencySymbol = computed(() => {
  return currentCurrency.value === 'JPY' ? '¥' : '$'
})

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  product: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close'])

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

const getStockBadgeClass = (stockLevel) => {
  if (stockLevel === 'In Stock') return 'success'
  if (stockLevel === 'Low Stock') return 'warning'
  if (stockLevel === 'Out of Stock') return 'danger'
  return 'info'
}

const translateStockLevel = (stockLevel) => {
  const stockMap = {
    'In Stock': t('status.inStock'),
    'Low Stock': t('status.lowStock')
  }
  return stockMap[stockLevel] || stockLevel
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
