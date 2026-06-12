<template>
  <div class="min-h-screen bg-gray-50">
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900">Analytics Dashboard</h2>
          <p class="mt-1 text-sm text-gray-600">Overview of city issue reporting activity.</p>
        </div>

        <div v-if="loading" class="flex justify-center py-12">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
        </div>

        <template v-else>
          <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
            <div v-for="stat in summaryCards" :key="stat.label" class="bg-white overflow-hidden shadow rounded-lg px-4 py-5 sm:p-6">
              <dt class="text-sm font-medium text-gray-500 truncate">{{ stat.label }}</dt>
              <dd class="mt-1 text-3xl font-semibold text-gray-900">{{ stat.value }}</dd>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <div class="bg-white shadow rounded-lg p-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Issues by Status</h3>
              <div class="h-64">
                <Doughnut v-if="statusChartData" :data="statusChartData" :options="doughnutOptions" />
              </div>
            </div>
            <div class="bg-white shadow rounded-lg p-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Monthly Trend</h3>
              <div class="h-64">
                <Bar v-if="trendChartData" :data="trendChartData" :options="barOptions" />
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="bg-white shadow rounded-lg p-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Issues by Type</h3>
              <div v-if="Object.keys(typeBreakdown).length" class="space-y-3">
                <div v-for="(count, type) in typeBreakdown" :key="type" class="flex items-center">
                  <span class="text-sm text-gray-700 w-40 truncate">{{ type }}</span>
                  <div class="flex-1 mx-3 bg-gray-200 rounded-full h-4">
                    <div
                      class="bg-indigo-500 h-4 rounded-full"
                      :style="{ width: (count / maxTypeCount * 100) + '%' }"
                    ></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900 w-12 text-right">{{ count }}</span>
                </div>
              </div>
              <p v-else class="text-gray-500 text-sm">No data yet.</p>
            </div>
            <div class="bg-white shadow rounded-lg p-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Issues by Department</h3>
              <div v-if="Object.keys(deptBreakdown).length" class="space-y-3">
                <div v-for="(count, dept) in deptBreakdown" :key="dept" class="flex items-center">
                  <span class="text-sm text-gray-700 w-40 truncate">{{ dept }}</span>
                  <div class="flex-1 mx-3 bg-gray-200 rounded-full h-4">
                    <div
                      class="bg-emerald-500 h-4 rounded-full"
                      :style="{ width: (count / maxDeptCount * 100) + '%' }"
                    ></div>
                  </div>
                  <span class="text-sm font-medium text-gray-900 w-12 text-right">{{ count }}</span>
                </div>
              </div>
              <p v-else class="text-gray-500 text-sm">No data yet.</p>
            </div>
          </div>
        </template>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js'
import { Doughnut, Bar } from 'vue-chartjs'
import axios from '../api/client'

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement)

const loading = ref(false)
const summary = ref({})
const statusBreakdown = ref({})
const typeBreakdown = ref({})
const deptBreakdown = ref({})
const monthlyTrend = ref([])

const summaryCards = computed(() => [
  { label: 'Total Issues', value: summary.value.total_issues || 0 },
  { label: 'Registered Citizens', value: summary.value.total_users || 0 },
  { label: 'Departments', value: summary.value.total_departments || 0 },
  { label: 'Avg Resolution (hrs)', value: summary.value.avg_resolution_hours || 0 },
])

const maxTypeCount = computed(() => {
  const vals = Object.values(typeBreakdown.value)
  return vals.length ? Math.max(...vals) : 1
})

const maxDeptCount = computed(() => {
  const vals = Object.values(deptBreakdown.value)
  return vals.length ? Math.max(...vals) : 1
})

const statusColors = {
  pending: '#f59e0b',
  in_progress: '#3b82f6',
  resolved: '#10b981',
  rejected: '#ef4444',
  verified: '#8b5cf6',
}

const statusChartData = computed(() => {
  const labels = Object.keys(statusBreakdown.value)
  if (!labels.length) return null
  return {
    labels,
    datasets: [{
      data: Object.values(statusBreakdown.value),
      backgroundColor: labels.map(l => statusColors[l] || '#6b7280'),
    }],
  }
})

const trendChartData = computed(() => {
  if (!monthlyTrend.value.length) return null
  return {
    labels: monthlyTrend.value.map(t => `${t.year}-${String(t.month).padStart(2, '0')}`),
    datasets: [{
      label: 'Issues',
      data: monthlyTrend.value.map(t => t.count),
      backgroundColor: '#6366f1',
    }],
  }
})

const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { position: 'bottom' } },
}

const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } },
}

const fetchAnalytics = async () => {
  loading.value = true
  try {
    const resp = await axios.get('/api/admin/analytics')
    summary.value = resp.data.summary || {}
    statusBreakdown.value = resp.data.status_breakdown || {}
    typeBreakdown.value = resp.data.type_breakdown || {}
    deptBreakdown.value = resp.data.department_breakdown || {}
    monthlyTrend.value = resp.data.monthly_trend || []
  } catch (e) {
    console.error('Failed to fetch analytics', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchAnalytics()
})
</script>
