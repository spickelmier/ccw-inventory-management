<template>
  <div class="bg-surface-card border-b border-border-subtle py-3 sticky top-[70px] z-[90]">
    <div class="max-w-[1600px] mx-auto px-8 flex items-center gap-4">
      <div class="flex items-center gap-4 flex-1 flex-wrap">
        <div class="flex items-center gap-2">
          <label class="text-xs font-semibold text-text-muted whitespace-nowrap">{{ t('filters.timePeriod') }}</label>
          <select v-model="selectedPeriod" class="px-3 py-1.5 border border-border-default rounded-md text-[0.813rem] text-text-primary bg-surface-raised appearance-none cursor-pointer transition-all font-medium min-w-[140px] focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 hover:border-border-default">
            <option value="all">{{ t('filters.allMonths') }}</option>
            <option value="2025-01">{{ t('months.january') }}</option>
            <option value="2025-02">{{ t('months.february') }}</option>
            <option value="2025-03">{{ t('months.march') }}</option>
            <option value="2025-04">{{ t('months.april') }}</option>
            <option value="2025-05">{{ t('months.may') }}</option>
            <option value="2025-06">{{ t('months.june') }}</option>
            <option value="2025-07">{{ t('months.july') }}</option>
            <option value="2025-08">{{ t('months.august') }}</option>
            <option value="2025-09">{{ t('months.september') }}</option>
            <option value="2025-10">{{ t('months.october') }}</option>
            <option value="2025-11">{{ t('months.november') }}</option>
            <option value="2025-12">{{ t('months.december') }}</option>
          </select>
        </div>
        <div class="flex items-center gap-2">
          <label class="text-xs font-semibold text-text-muted whitespace-nowrap">{{ t('filters.location') }}</label>
          <select v-model="selectedLocation" class="px-3 py-1.5 border border-border-default rounded-md text-[0.813rem] text-text-primary bg-surface-raised appearance-none cursor-pointer transition-all font-medium min-w-[140px] focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 hover:border-border-default">
            <option value="all">{{ t('filters.all') }}</option>
            <option value="San Francisco">{{ t('warehouses.sanFrancisco') }}</option>
            <option value="London">{{ t('warehouses.london') }}</option>
            <option value="Tokyo">{{ t('warehouses.tokyo') }}</option>
          </select>
        </div>
        <div class="flex items-center gap-2">
          <label class="text-xs font-semibold text-text-muted whitespace-nowrap">{{ t('filters.category') }}</label>
          <select v-model="selectedCategory" class="px-3 py-1.5 border border-border-default rounded-md text-[0.813rem] text-text-primary bg-surface-raised appearance-none cursor-pointer transition-all font-medium min-w-[140px] focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 hover:border-border-default">
            <option value="all">{{ t('filters.all') }}</option>
            <option value="circuit boards">{{ t('categories.circuitBoards') }}</option>
            <option value="sensors">{{ t('categories.sensors') }}</option>
            <option value="actuators">{{ t('categories.actuators') }}</option>
            <option value="controllers">{{ t('categories.controllers') }}</option>
            <option value="power supplies">{{ t('categories.powerSupplies') }}</option>
          </select>
        </div>
        <div class="flex items-center gap-2">
          <label class="text-xs font-semibold text-text-muted whitespace-nowrap">{{ t('filters.orderStatus') }}</label>
          <select v-model="selectedStatus" class="px-3 py-1.5 border border-border-default rounded-md text-[0.813rem] text-text-primary bg-surface-raised appearance-none cursor-pointer transition-all font-medium min-w-[140px] focus:outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 hover:border-border-default">
            <option value="all">{{ t('filters.all') }}</option>
            <option value="delivered">{{ t('status.delivered') }}</option>
            <option value="shipped">{{ t('status.shipped') }}</option>
            <option value="processing">{{ t('status.processing') }}</option>
            <option value="backordered">{{ t('status.backordered') }}</option>
          </select>
        </div>
      </div>
      <button
        class="flex items-center justify-center p-[0.4rem] bg-surface-raised border border-border-subtle rounded-md text-text-muted cursor-pointer transition-all flex-shrink-0 hover:bg-surface-overlay hover:border-border-default hover:text-text-primary disabled:opacity-30 disabled:cursor-not-allowed"
        @click="resetFilters"
        :disabled="!hasActiveFilters"
        :title="t('filters.resetFilters')"
      >
        <svg class="w-[18px] h-[18px]" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
import { useFilters } from '../composables/useFilters'
import { useI18n } from '../composables/useI18n'

export default {
  name: 'FilterBar',
  setup() {
    const {
      selectedPeriod,
      selectedLocation,
      selectedCategory,
      selectedStatus,
      hasActiveFilters,
      resetFilters
    } = useFilters()

    const { t } = useI18n()

    return {
      t,
      selectedPeriod,
      selectedLocation,
      selectedCategory,
      selectedStatus,
      hasActiveFilters,
      resetFilters
    }
  }
}
</script>
