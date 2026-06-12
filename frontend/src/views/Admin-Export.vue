<template>
  <div class="min-h-screen bg-gray-50">
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900">Export Reports</h2>
          <p class="mt-1 text-sm text-gray-600">Download issue data as CSV for reporting and analysis.</p>
        </div>

        <div class="bg-white shadow rounded-lg p-6 max-w-lg">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Filter by Status</label>
              <select v-model="filters.status" class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm">
                <option value="">All statuses</option>
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="resolved">Resolved</option>
                <option value="rejected">Rejected</option>
                <option value="verified">Verified</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Filter by Type</label>
              <input v-model="filters.issue_type" type="text" placeholder="e.g. Pothole, Streetlight"
                class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm" />
            </div>

            <div class="pt-4">
              <button @click="downloadCSV"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Download CSV
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import axios from '../api/client'

const filters = reactive({
  status: '',
  issue_type: '',
})

const downloadCSV = async () => {
  const params = {}
  if (filters.status) params.status = filters.status
  if (filters.issue_type) params.issue_type = filters.issue_type

  try {
    const resp = await axios.get('/api/admin/export', { params, responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([resp.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'citypulse_issues.csv')
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  } catch (e) {
    console.error('Failed to export', e)
  }
}
</script>
