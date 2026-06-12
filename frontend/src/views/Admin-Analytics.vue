<template>
  <div class="min-h-screen bg-base-100 text-base-content antialiased py-8 px-4 sm:px-6 lg:px-8">
    <main class="max-w-7xl mx-auto">
      <div>
        <div class="mb-8">
          <h2 class="text-3xl font-extrabold text-slate-100 font-mono tracking-wider uppercase">
            Analytics Dashboard
          </h2>
          <p class="mt-1 text-sm text-slate-400 font-sans">
            Overview of municipal response indicators and neighborhood reporting metrics.
          </p>
        </div>

        <div v-if="loading" class="flex justify-center py-16">
          <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-primary"></div>
        </div>

        <template v-else>
          <!-- Stats Grid -->
          <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
            <div
              v-for="stat in summaryCards"
              :key="stat.label"
              class="bg-base-200 border border-base-300 overflow-hidden shadow-lg rounded-2xl p-5 hover:border-primary/45 transition-all duration-300"
            >
              <dt class="text-xs font-mono text-slate-500 uppercase tracking-widest truncate">
                {{ stat.label }}
              </dt>
              <dd class="mt-2 text-3xl font-extrabold text-slate-100 font-mono">
                {{ stat.value }}
              </dd>
            </div>
          </div>

          <!-- Charts -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            <div class="bg-base-200 border border-base-300 rounded-3xl p-6 shadow-xl">
              <h3 class="text-xs font-bold font-mono text-slate-400 uppercase tracking-wider mb-4">
                Issues by Status
              </h3>
              <div class="h-64">
                <Doughnut
                  v-if="statusChartData"
                  :data="statusChartData"
                  :options="doughnutOptions"
                />
              </div>
            </div>
            <div class="bg-base-200 border border-base-300 rounded-3xl p-6 shadow-xl">
              <h3 class="text-xs font-bold font-mono text-slate-400 uppercase tracking-wider mb-4">
                Monthly Trend
              </h3>
              <div class="h-64">
                <Bar v-if="trendChartData" :data="trendChartData" :options="barOptions" />
              </div>
            </div>
          </div>

          <!-- Type Breakdown & Dept Breakdown -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div class="bg-base-200 border border-base-300 rounded-3xl p-6 shadow-xl">
              <h3 class="text-xs font-bold font-mono text-slate-400 uppercase tracking-wider mb-6">
                Issues by Type
              </h3>
              <div v-if="Object.keys(typeBreakdown).length" class="space-y-4">
                <div v-for="(count, type) in typeBreakdown" :key="type" class="flex items-center">
                  <span class="text-sm text-slate-300 w-40 truncate font-mono text-xs">{{
                    type
                  }}</span>
                  <div class="flex-1 mx-3 bg-base-300 rounded-full h-3 overflow-hidden">
                    <div
                      class="bg-indigo-500 h-3 rounded-full"
                      :style="{ width: (count / maxTypeCount) * 100 + '%' }"
                    ></div>
                  </div>
                  <span class="text-sm font-bold text-slate-100 w-12 text-right font-mono">{{
                    count
                  }}</span>
                </div>
              </div>
              <p v-else class="text-slate-500 text-sm font-mono">No data collected yet.</p>
            </div>
            <div class="bg-base-200 border border-base-300 rounded-3xl p-6 shadow-xl">
              <h3 class="text-xs font-bold font-mono text-slate-400 uppercase tracking-wider mb-6">
                Issues by Department
              </h3>
              <div v-if="Object.keys(deptBreakdown).length" class="space-y-4">
                <div v-for="(count, dept) in deptBreakdown" :key="dept" class="flex items-center">
                  <span class="text-sm text-slate-300 w-40 truncate font-mono text-xs">{{
                    dept
                  }}</span>
                  <div class="flex-1 mx-3 bg-base-300 rounded-full h-3 overflow-hidden">
                    <div
                      class="bg-emerald-500 h-3 rounded-full"
                      :style="{ width: (count / maxDeptCount) * 100 + '%' }"
                    ></div>
                  </div>
                  <span class="text-sm font-bold text-slate-100 w-12 text-right font-mono">{{
                    count
                  }}</span>
                </div>
              </div>
              <p v-else class="text-slate-500 text-sm font-mono">No data collected yet.</p>
            </div>
          </div>
        </template>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
} from 'chart.js'
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
    datasets: [
      {
        data: Object.values(statusBreakdown.value),
        backgroundColor: labels.map((l) => statusColors[l] || '#6b7280'),
      },
    ],
  }
})

const trendChartData = computed(() => {
  if (!monthlyTrend.value.length) return null
  return {
    labels: monthlyTrend.value.map((t) => `${t.year}-${String(t.month).padStart(2, '0')}`),
    datasets: [
      {
        label: 'Issues',
        data: monthlyTrend.value.map((t) => t.count),
        backgroundColor: '#3b82f6',
      },
    ],
  }
})

const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        color: '#94a3b8',
        font: { family: 'Fira Code', size: 10 },
      },
    },
  },
}

const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    y: {
      beginAtZero: true,
      ticks: { stepSize: 1, color: '#94a3b8', font: { family: 'Fira Code', size: 10 } },
      grid: { color: '#1e293b' },
    },
    x: {
      ticks: { color: '#94a3b8', font: { family: 'Fira Code', size: 10 } },
      grid: { color: '#1e293b' },
    },
  },
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

<style scoped>
/* Scoped styles */
</style>
