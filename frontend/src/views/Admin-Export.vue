<template>
  <div class="min-h-screen bg-base-100 text-base-content antialiased py-8 px-4 sm:px-6 lg:px-8">
    <main class="max-w-7xl mx-auto">
      <div>
        <div class="mb-8">
          <h2 class="text-3xl font-extrabold text-slate-100 font-mono tracking-wider uppercase">
            Export Reports
          </h2>
          <p class="mt-1 text-sm text-slate-400 font-sans">
            Download aggregated issue database snapshots as CSV for external analytics.
          </p>
        </div>

        <div class="bg-base-200 border border-base-300 rounded-3xl p-6 md:p-8 shadow-xl max-w-lg">
          <div class="space-y-5">
            <div>
              <label class="label"
                ><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider"
                  >Filter by Status</span
                ></label
              >
              <select
                v-model="filters.status"
                class="select select-bordered w-full rounded-xl border-base-300 focus:border-primary font-mono text-xs"
              >
                <option value="">All statuses</option>
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="resolved">Resolved</option>
                <option value="rejected">Rejected</option>
                <option value="verified">Verified</option>
              </select>
            </div>

            <div>
              <label class="label"
                ><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider"
                  >Filter by Type</span
                ></label
              >
              <input
                v-model="filters.issue_type"
                type="text"
                placeholder="e.g. Pothole, Streetlight"
                class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary font-sans text-sm"
              />
            </div>

            <div class="pt-4">
              <button
                @click="downloadCSV"
                class="btn btn-primary w-full rounded-xl font-bold py-3 flex items-center justify-center gap-2 cursor-pointer shadow-lg shadow-blue-500/10"
              >
                <svg
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2.5"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                  />
                </svg>
                DOWNLOAD CSV EXPORT
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

<style scoped>
/* Scoped styles */
</style>
