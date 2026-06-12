<template>
  <div class="min-h-screen bg-base-100 text-base-content antialiased py-8 px-4 sm:px-6 lg:px-8">
    <main class="max-w-7xl mx-auto">
      <div>
        <div class="mb-8">
          <h2 class="text-3xl font-extrabold text-base-content font-mono tracking-wider uppercase">
            Audit Log
          </h2>
          <p class="mt-1 text-sm text-base-content/60 font-sans">
            Track all administrative system events and database updates.
          </p>
        </div>

        <div v-if="loading" class="flex justify-center py-16">
          <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-primary"></div>
        </div>

        <div
          v-else-if="logs.length > 0"
          class="bg-base-200 border border-base-300 shadow-xl rounded-3xl overflow-hidden"
        >
          <ul class="divide-y divide-base-300">
            <li
              v-for="log in logs"
              :key="log.id"
              class="p-5 sm:px-8 hover:bg-base-300/10 transition-colors"
            >
              <div class="flex items-center justify-between">
                <div class="flex-1">
                  <p class="text-sm font-sans text-base-content/90">
                    <span class="font-bold text-base-content font-mono mr-1.5"
                      >{{ log.admin?.firstname }} {{ log.admin?.lastname }}</span
                    >
                    {{ formatAction(log.action) }}
                    <span class="text-primary font-mono ml-1.5"
                      >{{ log.target_type }} #{{ log.target_id || '' }}</span
                    >
                  </p>
                  <p
                    v-if="log.details"
                    class="text-xs text-base-content/60 font-mono mt-1 bg-base-100/50 p-2.5 rounded-lg border border-base-300/50"
                  >
                    {{ log.details }}
                  </p>
                </div>
                <span class="text-xs font-mono text-base-content/40 whitespace-nowrap ml-4">{{
                  formatDate(log.created_at)
                }}</span>
              </div>
            </li>
          </ul>
        </div>

        <div
          v-else
          class="text-center py-16 border border-dashed border-base-300 rounded-3xl bg-base-200/40"
        >
          <p class="text-base-content/40 text-sm">No audit log entries captured yet.</p>
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

<style scoped>
/* Scoped styles */
</style>
