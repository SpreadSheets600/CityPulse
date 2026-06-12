<template>
  <div class="min-h-screen bg-gray-50">
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900">SLA Tracking</h2>
          <p class="mt-1 text-sm text-gray-600">Resolution time vs SLA targets by department.</p>
        </div>

        <div v-if="loading" class="flex justify-center py-12">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
        </div>

        <template v-else>
          <div class="grid grid-cols-1 gap-5 sm:grid-cols-3 mb-8">
            <div class="bg-white overflow-hidden shadow rounded-lg px-4 py-5 sm:p-6">
              <dt class="text-sm font-medium text-gray-500 truncate">Overall Compliance</dt>
              <dd class="mt-1 text-3xl font-semibold" :class="overall.compliance_rate >= 80 ? 'text-green-600' : overall.compliance_rate >= 50 ? 'text-yellow-600' : 'text-red-600'">
                {{ overall.compliance_rate }}%
              </dd>
            </div>
            <div class="bg-white overflow-hidden shadow rounded-lg px-4 py-5 sm:p-6">
              <dt class="text-sm font-medium text-gray-500 truncate">Avg Resolution Time</dt>
              <dd class="mt-1 text-3xl font-semibold text-gray-900">{{ overall.avg_resolution_hours }}h</dd>
            </div>
            <div class="bg-white overflow-hidden shadow rounded-lg px-4 py-5 sm:p-6">
              <dt class="text-sm font-medium text-gray-500 truncate">Issues Breached</dt>
              <dd class="mt-1 text-3xl font-semibold" :class="overall.breached_sla > 0 ? 'text-red-600' : 'text-green-600'">
                {{ overall.breached_sla }} / {{ overall.total_resolved }}
              </dd>
            </div>
          </div>

          <div class="bg-white shadow overflow-hidden sm:rounded-lg">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Department</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">SLA Target</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Resolved</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Met SLA</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Compliance</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Avg Time</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="row in departments" :key="row.department">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ row.department }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ row.sla_hours }}h</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ row.total_resolved }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ row.met_sla }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm">
                    <span :class="row.compliance_rate >= 80 ? 'text-green-600' : row.compliance_rate >= 50 ? 'text-yellow-600' : 'text-red-600'" class="font-medium">
                      {{ row.compliance_rate }}%
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ row.avg_resolution_hours }}h</td>
                </tr>
                <tr v-if="!departments.length">
                  <td colspan="6" class="px-6 py-4 text-center text-sm text-gray-500">No department data yet.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </template>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../api/client'

const loading = ref(false)
const departments = ref([])
const overall = ref({})

const fetchSLA = async () => {
  loading.value = true
  try {
    const resp = await axios.get('/api/admin/sla')
    departments.value = resp.data.departments || []
    overall.value = resp.data.overall || {}
  } catch (e) {
    console.error('Failed to fetch SLA report', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchSLA()
})
</script>
