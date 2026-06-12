<template>
  <div class="min-h-screen bg-gray-50">
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900">Audit Log</h2>
          <p class="mt-1 text-sm text-gray-600">Track all admin actions for accountability.</p>
        </div>

        <div v-if="loading" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
        </div>

        <div v-else-if="logs.length > 0" class="bg-white shadow overflow-hidden sm:rounded-md">
          <ul class="divide-y divide-gray-200">
            <li v-for="log in logs" :key="log.id" class="px-4 py-4 sm:px-6">
              <div class="flex items-center justify-between">
                <div class="flex-1">
                  <p class="text-sm font-medium text-gray-900">
                    <span class="font-semibold">{{ log.admin?.firstname }} {{ log.admin?.lastname }}</span>
                    {{ formatAction(log.action) }}
                    <span class="text-indigo-600">{{ log.target_type }} #{{ log.target_id || '' }}</span>
                  </p>
                  <p v-if="log.details" class="text-sm text-gray-500 mt-1">{{ log.details }}</p>
                </div>
                <span class="text-xs text-gray-500 whitespace-nowrap ml-4">{{ formatDate(log.created_at) }}</span>
              </div>
            </li>
          </ul>
        </div>

        <div v-else class="text-center py-12">
          <p class="text-gray-500">No audit log entries yet.</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../api/client'

const logs = ref([])
const loading = ref(false)

const formatAction = (action) => {
  const labels = {
    delete_user: 'deleted',
    update_status: 'updated status of',
    create_department: 'created department',
    assign_department: 'assigned department to',
  }
  return labels[action] || action
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString()
}

const fetchLogs = async () => {
  loading.value = true
  try {
    const resp = await axios.get('/api/admin/audit-log')
    logs.value = resp.data.logs || []
  } catch (e) {
    console.error('Failed to fetch audit log', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchLogs()
})
</script>
