<template>
  <div>
    <div class="page-header">
      <h2>{{ t('reports.title') }}</h2>
      <p>{{ t('reports.description') }}</p>
    </div>

    <div v-if="loading" class="loading">{{ t('reports.loading') }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <!-- Quarterly Performance -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('reports.quarterly.title') }}</h3>
        </div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>{{ t('reports.quarterly.quarter') }}</th>
                <th>{{ t('reports.quarterly.totalOrders') }}</th>
                <th>{{ t('reports.quarterly.totalRevenue') }}</th>
                <th>{{ t('reports.quarterly.avgOrderValue') }}</th>
                <th>{{ t('reports.quarterly.fulfillmentRate') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="q in quarterlyData" :key="q.quarter">
                <td><strong>{{ q.quarter }}</strong></td>
                <td>{{ q.total_orders }}</td>
                <td>${{ formatNumber(q.total_revenue) }}</td>
                <td>${{ formatNumber(q.avg_order_value) }}</td>
                <td>
                  <span :class="getFulfillmentClass(q.fulfillment_rate)">
                    {{ q.fulfillment_rate }}%
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Monthly Trends Chart -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('reports.monthlyTrend.title') }}</h3>
        </div>
        <div class="py-8 px-4 min-h-[300px] pb-12">
          <div class="flex items-end justify-around h-[250px] gap-2">
            <div v-for="month in monthlyData" :key="month.month" class="flex flex-col items-center flex-1 max-w-[80px]">
              <div class="h-[200px] flex items-end w-full">
                <div
                  class="w-full bg-gradient-to-t from-accent to-accent-hover rounded-t transition-all cursor-pointer hover:opacity-80"
                  :style="{ height: getBarHeight(month.revenue) + 'px' }"
                  :title="'$' + formatNumber(month.revenue)"
                ></div>
              </div>
              <div class="bar-label">{{ formatMonth(month.month) }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Month-over-Month Comparison -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('reports.momAnalysis.title') }}</h3>
        </div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>{{ t('reports.momAnalysis.month') }}</th>
                <th>{{ t('reports.momAnalysis.orders') }}</th>
                <th>{{ t('reports.momAnalysis.revenue') }}</th>
                <th>{{ t('reports.momAnalysis.change') }}</th>
                <th>{{ t('reports.momAnalysis.growthRate') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(month, index) in monthlyData" :key="month.month">
                <td><strong>{{ formatMonth(month.month) }}</strong></td>
                <td>{{ month.order_count }}</td>
                <td>${{ formatNumber(month.revenue) }}</td>
                <td>
                  <span v-if="index > 0" :class="getChangeClass(month.revenue, monthlyData[index - 1].revenue)">
                    {{ getChangeValue(month.revenue, monthlyData[index - 1].revenue) }}
                  </span>
                  <span v-else>-</span>
                </td>
                <td>
                  <span v-if="index > 0" :class="getChangeClass(month.revenue, monthlyData[index - 1].revenue)">
                    {{ getGrowthRate(month.revenue, monthlyData[index - 1].revenue) }}
                  </span>
                  <span v-else>-</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Summary Stats -->
      <div class="stats-grid">
        <div class="stat-card border-l-4 border-l-accent">
          <div class="stat-label">{{ t('reports.stats.totalRevenueYTD') }}</div>
          <div class="stat-value">${{ formatNumber(totalRevenue) }}</div>
        </div>
        <div class="stat-card border-l-4 border-l-status-info">
          <div class="stat-label">{{ t('reports.stats.avgMonthlyRevenue') }}</div>
          <div class="stat-value">${{ formatNumber(avgMonthlyRevenue) }}</div>
        </div>
        <div class="stat-card border-l-4 border-l-status-success">
          <div class="stat-label">{{ t('reports.stats.totalOrdersYTD') }}</div>
          <div class="stat-value">{{ totalOrders }}</div>
        </div>
        <div class="stat-card border-l-4 border-l-status-warning">
          <div class="stat-label">{{ t('reports.stats.bestQuarter') }}</div>
          <div class="stat-value">{{ bestQuarter }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from '../composables/useI18n'
import { api } from '../api'

export default {
  name: 'Reports',
  setup() {
    const { t, currentLocale } = useI18n()

    const loading = ref(true)
    const error = ref(null)
    const quarterlyData = ref([])
    const monthlyData = ref([])

    // Computed summary stats
    const totalRevenue = computed(() =>
      monthlyData.value.reduce((sum, m) => sum + m.revenue, 0)
    )

    const avgMonthlyRevenue = computed(() =>
      monthlyData.value.length ? totalRevenue.value / monthlyData.value.length : 0
    )

    const totalOrders = computed(() =>
      monthlyData.value.reduce((sum, m) => sum + m.order_count, 0)
    )

    const bestQuarter = computed(() => {
      if (!quarterlyData.value.length) return ''
      return quarterlyData.value.reduce((best, q) =>
        q.total_revenue > best.total_revenue ? q : best
      ).quarter
    })

    // Computed max revenue for O(n) bar height calculation
    const maxRevenue = computed(() =>
      Math.max(...monthlyData.value.map(m => m.revenue), 0)
    )

    const loadData = async () => {
      try {
        loading.value = true
        error.value = null
        quarterlyData.value = await api.getQuarterlyReports()
        monthlyData.value = await api.getMonthlyTrends()
      } catch (err) {
        error.value = t('common.error')
        console.error('Failed to load reports:', err)
      } finally {
        loading.value = false
      }
    }

    const formatNumber = (num) => {
      return Number(num).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    }

    const formatMonth = (monthStr) => {
      const [year, month] = monthStr.split('-')
      const date = new Date(Number(year), Number(month) - 1, 1)
      return new Intl.DateTimeFormat(
        currentLocale.value === 'ja' ? 'ja-JP' : 'en-US',
        { month: 'short', year: 'numeric' }
      ).format(date)
    }

    const getBarHeight = (revenue) => {
      if (maxRevenue.value === 0) return 0
      return (revenue / maxRevenue.value) * 200
    }

    const getFulfillmentClass = (rate) => {
      if (rate >= 90) {
        return 'badge success'
      } else if (rate >= 75) {
        return 'badge warning'
      } else {
        return 'badge danger'
      }
    }

    const getChangeValue = (current, previous) => {
      const change = current - previous
      if (change > 0) {
        return '+$' + formatNumber(change)
      } else if (change < 0) {
        return '-$' + formatNumber(Math.abs(change))
      } else {
        return '$0.00'
      }
    }

    const getChangeClass = (current, previous) => {
      const change = current - previous
      if (change > 0) {
        return 'positive-change'
      } else if (change < 0) {
        return 'negative-change'
      } else {
        return ''
      }
    }

    const getGrowthRate = (current, previous) => {
      if (previous === 0) {
        return 'N/A'
      }
      const rate = ((current - previous) / previous) * 100
      const sign = rate > 0 ? '+' : ''
      return sign + rate.toFixed(1) + '%'
    }

    onMounted(() => loadData())

    return {
      t,
      loading,
      error,
      quarterlyData,
      monthlyData,
      totalRevenue,
      avgMonthlyRevenue,
      totalOrders,
      bestQuarter,
      loadData,
      formatNumber,
      formatMonth,
      getBarHeight,
      getFulfillmentClass,
      getChangeValue,
      getChangeClass,
      getGrowthRate
    }
  }
}
</script>

<style scoped>
.bar-label {
  margin-top: 1.5rem;
  font-size: 0.75rem;
  color: #94a3b8;
  text-align: center;
  transform: rotate(-45deg);
  white-space: nowrap;
  transform-origin: top center;
}

.positive-change {
  color: #34d399;
  font-weight: 600;
}

.negative-change {
  color: #f87171;
  font-weight: 600;
}
</style>
