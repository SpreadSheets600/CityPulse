<template>
  <div class="min-h-screen bg-base-100 text-base-content antialiased py-8 px-4 sm:px-6 lg:px-8">
    <main class="max-w-7xl mx-auto">
      <div>
        <div class="mb-8">
          <h2 class="text-3xl font-extrabold text-base-content font-mono tracking-wider uppercase">
            SLA Tracking
          </h2>
          <p class="mt-1 text-sm text-base-content/60 font-sans">
            Compare municipal resolution performance times against SLA response targets.
          </p>
        </div>

        <div v-if="loading" class="flex justify-center py-16">
          <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-primary"></div>
        </div>

        <template v-else>
          <!-- SLA Summary Grid -->
          <div class="grid grid-cols-1 gap-5 sm:grid-cols-3 mb-8">
            <!-- Compliance -->
            <div
              class="bg-base-200 border border-base-300 overflow-hidden shadow-lg rounded-2xl p-5 hover:border-primary/45 transition-all duration-300 flex items-center"
            >
              <div
                class="flex-shrink-0 h-10 w-10 rounded-xl bg-slate-500/10 border border-slate-500/20 flex items-center justify-center"
              >
                <svg
                  class="h-5 w-5 text-base-content/60"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div class="ml-4 flex-1">
                <p class="text-xs font-mono text-base-content/60 uppercase tracking-widest">
                  Overall Compliance
                </p>
                <p
                  class="text-2xl font-extrabold font-mono mt-0.5"
                  :class="
                    overall.compliance_rate >= 80
                      ? 'text-emerald-400'
                      : overall.compliance_rate >= 50
                        ? 'text-yellow-400'
                        : 'text-error'
                  "
                >
                  {{ overall.compliance_rate }}%
                </p>
              </div>
            </div>

            <!-- Avg Time -->
            <div
              class="bg-base-200 border border-base-300 overflow-hidden shadow-lg rounded-2xl p-5 hover:border-primary/45 transition-all duration-300 flex items-center"
            >
              <div
                class="flex-shrink-0 h-10 w-10 rounded-xl bg-slate-500/10 border border-slate-500/20 flex items-center justify-center"
              >
                <svg
                  class="h-5 w-5 text-base-content/60"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div class="ml-4 flex-1">
                <p class="text-xs font-mono text-base-content/60 uppercase tracking-widest">
                  Avg Resolution Time
                </p>
                <p class="text-2xl font-extrabold text-base-content font-mono mt-0.5">
                  {{ overall.avg_resolution_hours }}h
                </p>
              </div>
            </div>

            <!-- Breached -->
            <div
              class="bg-base-200 border border-base-300 overflow-hidden shadow-lg rounded-2xl p-5 hover:border-primary/45 transition-all duration-300 flex items-center"
            >
              <div
                class="flex-shrink-0 h-10 w-10 rounded-xl bg-slate-500/10 border border-slate-500/20 flex items-center justify-center"
              >
                <svg
                  class="h-5 w-5 text-base-content/60"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
              </div>
              <div class="ml-4 flex-1">
                <p class="text-xs font-mono text-base-content/60 uppercase tracking-widest">
                  Issues Breached
                </p>
                <p
                  class="text-2xl font-extrabold font-mono mt-0.5"
                  :class="overall.breached_sla > 0 ? 'text-error' : 'text-emerald-400'"
                >
                  {{ overall.breached_sla }}
                  <span class="text-sm font-normal text-base-content/40"
                    >/ {{ overall.total_resolved }}</span
                  >
                </p>
              </div>
            </div>
          </div>

          <!-- Table -->
          <div class="bg-base-200 border border-base-300 shadow-xl rounded-3xl overflow-hidden">
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-base-300 bg-base-200">
                <thead
                  class="bg-base-300/60 font-mono text-2xs uppercase tracking-wider text-base-content/60"
                >
                  <tr>
                    <th class="px-6 py-4 text-left font-bold">Department</th>
                    <th class="px-6 py-4 text-left font-bold">SLA Target</th>
                    <th class="px-6 py-4 text-left font-bold">Resolved</th>
                    <th class="px-6 py-4 text-left font-bold">Met SLA</th>
                    <th class="px-6 py-4 text-left font-bold">Compliance</th>
                    <th class="px-6 py-4 text-left font-bold">Avg Time</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-base-300/40 text-base-content/90">
                  <tr
                    v-for="row in departments"
                    :key="row.department"
                    class="hover:bg-base-300/10 transition-colors"
                  >
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-base-content">
                      {{ row.department }}
                    </td>
                    <td
                      class="px-6 py-4 whitespace-nowrap text-sm font-mono text-base-content/80 text-xs"
                    >
                      {{ row.sla_hours }}h
                    </td>
                    <td
                      class="px-6 py-4 whitespace-nowrap text-sm font-mono text-base-content/80 text-xs"
                    >
                      {{ row.total_resolved }}
                    </td>
                    <td
                      class="px-6 py-4 whitespace-nowrap text-sm font-mono text-base-content/80 text-xs"
                    >
                      {{ row.met_sla }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-mono">
                      <span
                        :class="
                          row.compliance_rate >= 80
                            ? 'text-emerald-400'
                            : row.compliance_rate >= 50
                              ? 'text-yellow-400'
                              : 'text-error'
                        "
                        class="font-bold"
                      >
                        {{ row.compliance_rate }}%
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-base-content/80">
                      {{ row.avg_resolution_hours }}h
                    </td>
                  </tr>
                  <tr v-if="!departments.length">
                    <td
                      colspan="6"
                      class="px-6 py-8 text-center text-sm font-mono text-base-content/40 bg-base-200"
                    >
                      No department SLA records compiled yet.
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
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
    const resp = await axios.get('/admin/sla')
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

