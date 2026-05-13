<template>
  <div>
    <div class="page-header">
      <h2>{{ t('demand.title') }}</h2>
      <p>{{ t('demand.description') }}</p>
    </div>

    <div v-if="loading" class="loading">{{ t('common.loading') }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div class="grid gap-6 mb-8 [grid-template-columns:repeat(auto-fit,minmax(320px,1fr))]">
        <div class="bg-surface-card border border-border-subtle border-l-4 border-l-status-success rounded-xl p-6 transition-all duration-200 hover:border-border-default hover:shadow-lg">
          <div class="flex items-center gap-4 mb-4 pb-4 border-b border-border-subtle">
            <div class="w-12 h-12 flex items-center justify-center rounded-xl text-[1.75rem] font-bold flex-shrink-0 bg-emerald-900/40 text-status-success">↑</div>
            <div>
              <div class="text-[0.813rem] font-semibold text-text-muted uppercase tracking-wider">{{ t('demand.increasingDemand') }}</div>
              <div class="text-2xl font-bold text-text-primary mt-1">{{ t('demand.itemsCount', { count: getForecastsByTrend('increasing').length }) }}</div>
            </div>
          </div>
          <div class="flex flex-col gap-3">
            <div v-for="item in getForecastsByTrend('increasing').slice(0, 5)" :key="item.id" class="flex justify-between items-center py-2 px-3 bg-surface-raised rounded-md transition-colors hover:bg-surface-overlay">
              <span class="text-sm text-text-primary font-medium flex-1 overflow-hidden text-ellipsis whitespace-nowrap mr-4">{{ item.item_name }}</span>
              <span class="text-[0.813rem] font-bold flex-shrink-0 text-status-success">+{{ getChangePercent(item) }}%</span>
            </div>
            <div v-if="getForecastsByTrend('increasing').length > 5" class="text-[0.813rem] text-text-muted italic text-center py-2">
              +{{ getForecastsByTrend('increasing').length - 5 }} {{ t('demand.more') }}
            </div>
          </div>
        </div>

        <div class="bg-surface-card border border-border-subtle border-l-4 border-l-accent rounded-xl p-6 transition-all duration-200 hover:border-border-default hover:shadow-lg">
          <div class="flex items-center gap-4 mb-4 pb-4 border-b border-border-subtle">
            <div class="w-12 h-12 flex items-center justify-center rounded-xl text-[1.75rem] font-bold flex-shrink-0 bg-indigo-900/40 text-accent">→</div>
            <div>
              <div class="text-[0.813rem] font-semibold text-text-muted uppercase tracking-wider">{{ t('demand.stableDemand') }}</div>
              <div class="text-2xl font-bold text-text-primary mt-1">{{ t('demand.itemsCount', { count: getForecastsByTrend('stable').length }) }}</div>
            </div>
          </div>
          <div class="flex flex-col gap-3">
            <div v-for="item in getForecastsByTrend('stable').slice(0, 5)" :key="item.id" class="flex justify-between items-center py-2 px-3 bg-surface-raised rounded-md transition-colors hover:bg-surface-overlay">
              <span class="text-sm text-text-primary font-medium flex-1 overflow-hidden text-ellipsis whitespace-nowrap mr-4">{{ item.item_name }}</span>
              <span class="text-[0.813rem] font-bold flex-shrink-0 text-text-muted">{{ getChangePercent(item) }}%</span>
            </div>
            <div v-if="getForecastsByTrend('stable').length > 5" class="text-[0.813rem] text-text-muted italic text-center py-2">
              +{{ getForecastsByTrend('stable').length - 5 }} {{ t('demand.more') }}
            </div>
          </div>
        </div>

        <div class="bg-surface-card border border-border-subtle border-l-4 border-l-status-danger rounded-xl p-6 transition-all duration-200 hover:border-border-default hover:shadow-lg">
          <div class="flex items-center gap-4 mb-4 pb-4 border-b border-border-subtle">
            <div class="w-12 h-12 flex items-center justify-center rounded-xl text-[1.75rem] font-bold flex-shrink-0 bg-red-900/40 text-status-danger">↓</div>
            <div>
              <div class="text-[0.813rem] font-semibold text-text-muted uppercase tracking-wider">{{ t('demand.decreasingDemand') }}</div>
              <div class="text-2xl font-bold text-text-primary mt-1">{{ t('demand.itemsCount', { count: getForecastsByTrend('decreasing').length }) }}</div>
            </div>
          </div>
          <div class="flex flex-col gap-3">
            <div v-for="item in getForecastsByTrend('decreasing').slice(0, 5)" :key="item.id" class="flex justify-between items-center py-2 px-3 bg-surface-raised rounded-md transition-colors hover:bg-surface-overlay">
              <span class="text-sm text-text-primary font-medium flex-1 overflow-hidden text-ellipsis whitespace-nowrap mr-4">{{ item.item_name }}</span>
              <span class="text-[0.813rem] font-bold flex-shrink-0 text-status-danger">{{ getChangePercent(item) }}%</span>
            </div>
            <div v-if="getForecastsByTrend('decreasing').length > 5" class="text-[0.813rem] text-text-muted italic text-center py-2">
              +{{ getForecastsByTrend('decreasing').length - 5 }} {{ t('demand.more') }}
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('demand.demandForecasts') }}</h3>
        </div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>{{ t('demand.table.sku') }}</th>
                <th>{{ t('demand.table.itemName') }}</th>
                <th>{{ t('demand.table.currentDemand') }}</th>
                <th>{{ t('demand.table.forecastedDemand') }}</th>
                <th>{{ t('demand.table.change') }}</th>
                <th>{{ t('demand.table.trend') }}</th>
                <th>{{ t('demand.table.period') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="forecast in forecasts" :key="forecast.id">
                <td><strong>{{ forecast.item_sku }}</strong></td>
                <td>{{ forecast.item_name }}</td>
                <td>{{ forecast.current_demand }}</td>
                <td><strong>{{ forecast.forecasted_demand }}</strong></td>
                <td>
                  <span :style="{ color: getChangeColor(forecast) }">
                    {{ getChangePercent(forecast) }}%
                  </span>
                </td>
                <td>
                  <span :class="['badge', forecast.trend]">
                    {{ t(`trends.${forecast.trend}`) }}
                  </span>
                </td>
                <td>{{ translatePeriod(forecast.period) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue'
import { api } from '../api'
import { useFilters } from '../composables/useFilters'
import { useI18n } from '../composables/useI18n'

export default {
  name: 'Demand',
  setup() {
    const { t } = useI18n()
    const loading = ref(true)
    const error = ref(null)
    const allForecasts = ref([])
    const inventoryItems = ref([])

    // Use shared filters
    const { selectedLocation, selectedCategory, getCurrentFilters } = useFilters()

    // Filter forecasts based on inventory filters
    const forecasts = computed(() => {
      if (selectedLocation.value === 'all' && selectedCategory.value === 'all') {
        return allForecasts.value
      }

      // Get SKUs of items that match the filters
      const validSkus = new Set(inventoryItems.value.map(item => item.sku))
      return allForecasts.value.filter(f => validSkus.has(f.item_sku))
    })

    const loadForecasts = async () => {
      try {
        loading.value = true
        const filters = getCurrentFilters()

        const [forecastsData, inventoryData] = await Promise.all([
          api.getDemandForecasts(),
          api.getInventory({
            warehouse: filters.warehouse,
            category: filters.category
          })
        ])

        allForecasts.value = forecastsData
        inventoryItems.value = inventoryData
      } catch (err) {
        error.value = 'Failed to load demand forecasts: ' + err.message
      } finally {
        loading.value = false
      }
    }

    // Watch for filter changes and reload data
    watch([selectedLocation, selectedCategory], () => {
      loadForecasts()
    })

    const getForecastsByTrend = (trend) => {
      return forecasts.value.filter(f => f.trend === trend)
    }

    const getChangePercent = (forecast) => {
      const change = ((forecast.forecasted_demand - forecast.current_demand) / forecast.current_demand * 100).toFixed(1)
      return change > 0 ? `+${change}` : change
    }

    const getChangeColor = (forecast) => {
      const change = forecast.forecasted_demand - forecast.current_demand
      const changePercent = Math.abs((change / forecast.current_demand) * 100)

      // If change is within ±2%, consider it stable and show blue
      if (changePercent <= 2) {
        return '#60a5fa' // Blue for stable
      }

      if (change > 0) return '#34d399' // Green for increasing
      if (change < 0) return '#f87171' // Red for decreasing
      return '#60a5fa' // Blue for no change
    }

    const translatePeriod = (period) => {
      // Period values like "Next 3 months", "Q1 2025", "30 days", etc.
      const { currentLocale } = useI18n()
      if (currentLocale.value === 'ja') {
        return period
          .replace(/Next\s+/i, '次の')
          .replace(/\s+months/i, 'か月')
          .replace(/\s+month/i, 'か月')
          .replace(/\s+days/i, '日間')
          .replace(/\s+day/i, '日')
          .replace('Q1', '第1四半期')
          .replace('Q2', '第2四半期')
          .replace('Q3', '第3四半期')
          .replace('Q4', '第4四半期')
      }
      return period
    }

    onMounted(loadForecasts)

    return {
      t,
      loading,
      error,
      forecasts,
      getForecastsByTrend,
      getChangePercent,
      getChangeColor,
      translatePeriod
    }
  }
}
</script>
