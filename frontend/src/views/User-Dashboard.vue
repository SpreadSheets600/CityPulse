<template>
  <div class="min-h-screen bg-base-100 text-base-content antialiased">
    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div>
        <!-- Welcome Header -->
        <div class="mb-8">
          <h2 class="text-3xl font-extrabold text-base-content">
            Welcome Back, {{ user?.firstname }}!
          </h2>
          <p class="mt-1.5 text-sm text-base-content/60">
            Monitor active geofences and verify community reports in real time.
          </p>
        </div>

        <!-- Stats Cards Grid -->
        <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-5 mb-8">
          <!-- Reputation Card -->
          <div
            class="bg-base-200 border border-base-300 overflow-hidden shadow-lg rounded-2xl p-5 hover:border-primary/40 transition-all duration-300 flex flex-col justify-between"
          >
            <div class="flex items-center">
              <div
                class="flex-shrink-0 h-10 w-10 rounded-xl bg-yellow-500/10 border border-yellow-500/20 flex items-center justify-center"
              >
                <svg
                  class="h-5 w-5 text-yellow-400"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z"
                  />
                </svg>
              </div>
              <div class="ml-4 flex-1">
                <p class="text-xs font-mono text-base-content/60 uppercase tracking-wider">Reputation</p>
                <p class="text-2xl font-extrabold text-base-content font-mono mt-0.5">
                  {{ reputation.total_points || 0 }}
                </p>
              </div>
            </div>
            <div class="mt-4">
              <ReputationBadge
                :trust-level="reputation.trust_level"
                :total-points="reputation.total_points"
              />
            </div>
          </div>

          <!-- Total Issues -->
          <div
            class="bg-base-200 border border-base-300 overflow-hidden shadow-lg rounded-2xl p-5 hover:border-primary/40 transition-all duration-300 flex items-center"
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
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <div class="ml-4 flex-1">
              <p class="text-xs font-mono text-base-content/60 uppercase tracking-wider">Total Issues</p>
              <p class="text-2xl font-extrabold text-base-content font-mono mt-0.5">
                {{ stats.totalIssues }}
              </p>
            </div>
          </div>

          <!-- Pending Issues -->
          <div
            class="bg-base-200 border border-base-300 overflow-hidden shadow-lg rounded-2xl p-5 hover:border-primary/40 transition-all duration-300 flex items-center"
          >
            <div
              class="flex-shrink-0 h-10 w-10 rounded-xl bg-yellow-500/10 border border-yellow-500/20 flex items-center justify-center"
            >
              <svg
                class="h-5 w-5 text-yellow-400"
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
              <p class="text-xs font-mono text-base-content/60 uppercase tracking-wider">Pending</p>
              <p class="text-2xl font-extrabold text-base-content font-mono mt-0.5">
                {{ stats.pendingIssues }}
              </p>
            </div>
          </div>

          <!-- In Progress -->
          <div
            class="bg-base-200 border border-base-300 overflow-hidden shadow-lg rounded-2xl p-5 hover:border-primary/40 transition-all duration-300 flex items-center"
          >
            <div
              class="flex-shrink-0 h-10 w-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center"
            >
              <svg
                class="h-5 w-5 text-blue-400"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
            </div>
            <div class="ml-4 flex-1">
              <p class="text-xs font-mono text-base-content/60 uppercase tracking-wider">In Progress</p>
              <p class="text-2xl font-extrabold text-base-content font-mono mt-0.5">
                {{ stats.inProgressIssues }}
              </p>
            </div>
          </div>

          <!-- Resolved -->
          <div
            class="bg-base-200 border border-base-300 overflow-hidden shadow-lg rounded-2xl p-5 hover:border-primary/40 transition-all duration-300 flex items-center"
          >
            <div
              class="flex-shrink-0 h-10 w-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center"
            >
              <svg
                class="h-5 w-5 text-emerald-400"
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
              <p class="text-xs font-mono text-base-content/60 uppercase tracking-wider">Resolved</p>
              <p class="text-2xl font-extrabold text-base-content font-mono mt-0.5">
                {{ stats.resolvedIssues }}
              </p>
            </div>
          </div>
        </div>

        <!-- Quick Actions & Filters Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          <!-- Quick Actions -->
          <div class="bg-base-200 border border-base-300 shadow-lg rounded-3xl p-6 lg:col-span-1">
            <h3
              class="text-lg font-bold text-base-content mb-4 font-mono uppercase tracking-wide text-xs"
            >
              Quick Actions
            </h3>
            <div class="flex flex-col gap-3">
              <router-link
                to="/issues/create"
                class="btn btn-primary rounded-xl flex items-center justify-center gap-2 font-bold py-3.5"
              >
                <svg
                  class="h-5 w-5"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2.5"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                </svg>
                Report New Issue
              </router-link>
              <router-link
                to="/issues"
                class="btn btn-outline border-base-300 hover:border-slate-500 rounded-xl flex items-center justify-center gap-2 font-bold py-3.5"
              >
                <svg
                  class="h-5 w-5"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2"
                  />
                </svg>
                View My Reports
              </router-link>
            </div>
          </div>

          <!-- Search & Filter -->
          <div class="bg-base-200 border border-base-300 shadow-lg rounded-3xl p-6 lg:col-span-2">
            <h3
              class="text-lg font-bold text-base-content mb-4 font-mono uppercase tracking-wide text-xs"
            >
              Search & Filter
            </h3>
            <div class="flex flex-col sm:flex-row gap-4">
              <div class="relative flex-1">
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Search issues by keyword..."
                  class="input input-bordered w-full rounded-xl pl-10 border-base-300 focus:border-primary focus:ring-1 focus:ring-primary transition-all font-sans"
                  @input="debouncedFetch"
                />
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                  <svg
                    class="h-5 w-5 text-base-content/40"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                    />
                  </svg>
                </div>
              </div>

              <select
                v-model="filterStatus"
                class="select select-bordered rounded-xl border-base-300 focus:border-primary font-mono text-xs"
                @change="fetchData"
              >
                <option value="">Status: All</option>
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="resolved">Resolved</option>
                <option value="rejected">Rejected</option>
                <option value="verified">Verified</option>
              </select>

              <select
                v-model="filterType"
                class="select select-bordered rounded-xl border-base-300 focus:border-primary font-mono text-xs"
                @change="fetchData"
              >
                <option value="">Type: All</option>
                <option value="Road Damage">Road Damage</option>
                <option value="Water Supply">Water Supply</option>
                <option value="Electricity">Electricity</option>
                <option value="Waste Management">Waste Management</option>
                <option value="Public Safety">Public Safety</option>
                <option value="Unspecified">Unspecified</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Recent Issues List -->
        <div class="bg-base-200 border border-base-300 shadow-lg rounded-3xl p-6">
          <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-6 gap-4">
            <div>
              <h3 class="text-xl font-bold text-base-content">Recent Activity Feed</h3>
              <p class="text-xs text-base-content/60 mt-0.5">
                Showing nearest reported incident notifications
              </p>
            </div>

            <!-- Technical Status Tabs -->
            <div class="flex flex-wrap gap-2">
              <button
                @click="selectedStatus = 'all'"
                :class="[
                  selectedStatus === 'all'
                    ? 'bg-primary text-white border-primary'
                    : 'bg-base-100 text-base-content/60 border-base-300 hover:text-base-content/80',
                  'px-3 py-1.5 text-xs font-mono border rounded-xl transition-all duration-200 cursor-pointer',
                ]"
              >
                ALL
              </button>
              <button
                @click="selectedStatus = 'pending'"
                :class="[
                  selectedStatus === 'pending'
                    ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
                    : 'bg-base-100 text-base-content/60 border-base-300 hover:text-base-content/80',
                  'px-3 py-1.5 text-xs font-mono border rounded-xl transition-all duration-200 cursor-pointer',
                ]"
              >
                PENDING
              </button>
              <button
                @click="selectedStatus = 'in_progress'"
                :class="[
                  selectedStatus === 'in_progress'
                    ? 'bg-blue-500/20 text-blue-400 border-blue-500/30'
                    : 'bg-base-100 text-base-content/60 border-base-300 hover:text-base-content/80',
                  'px-3 py-1.5 text-xs font-mono border rounded-xl transition-all duration-200 cursor-pointer',
                ]"
              >
                IN PROGRESS
              </button>
              <button
                @click="selectedStatus = 'resolved'"
                :class="[
                  selectedStatus === 'resolved'
                    ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
                    : 'bg-base-100 text-base-content/60 border-base-300 hover:text-base-content/80',
                  'px-3 py-1.5 text-xs font-mono border rounded-xl transition-all duration-200 cursor-pointer',
                ]"
              >
                RESOLVED
              </button>
            </div>
          </div>

          <div
            v-if="filteredIssues.length === 0"
            class="text-center py-12 border border-dashed border-base-300 rounded-2xl bg-base-100/30"
          >
            <svg
              class="mx-auto h-12 w-12 text-slate-600 mb-3"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.5"
                d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <p class="text-base-content/40 text-sm">
              No recent matching reports found in this neighborhood.
            </p>
          </div>

          <div v-else class="space-y-4">
            <div
              v-for="issue in filteredIssues"
              :key="issue.id"
              class="border border-base-300 rounded-2xl hover:border-primary/40 hover:shadow-lg transition-all duration-300 bg-base-100/30 overflow-hidden"
            >
              <router-link :to="`/issues/${issue.id}`" class="block p-5 hover:bg-base-300/10">
                <!-- Header -->
                <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start mb-3 gap-2">
                  <div>
                    <p
                      class="text-lg font-bold text-base-content transition-colors group-hover:text-primary"
                    >
                      {{ issue.title }}
                    </p>
                    <p class="text-xs text-base-content/60 mt-1 font-sans line-clamp-1">
                      {{ issue.description }}
                    </p>
                  </div>
                  <div
                    class="flex items-center text-xs font-mono text-base-content/40 mt-1 sm:mt-0 gap-3"
                  >
                    <span
                      :class="getStatusClass(issue.status)"
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-2xs font-bold uppercase tracking-wide"
                    >
                      {{ issue.status }}
                    </span>
                    <span class="flex items-center">
                      <svg
                        class="w-3.5 h-3.5 mr-1"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                        />
                      </svg>
                      {{ formatDate(issue.created_at) }}
                    </span>
                  </div>
                </div>

                <!-- Details & Tags Row -->
                <div
                  class="flex flex-wrap items-center gap-3 text-xs font-mono text-base-content/40 border-b border-base-300/50 pb-3.5 mb-3.5"
                >
                  <span
                    v-if="issue.issue_type && issue.issue_type !== 'Unspecified'"
                    class="flex items-center rounded-md bg-blue-500/5 px-2 py-0.5 border border-blue-500/10 text-blue-400"
                  >
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
                      />
                    </svg>
                    {{ issue.issue_type }}
                  </span>

                  <span v-if="issue.address" class="flex items-center">
                    <svg
                      class="w-3 h-3 mr-1 text-base-content/40"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                      />
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                      />
                    </svg>
                    {{ issue.address }}
                  </span>
                </div>

                <!-- Footer & User Info -->
                <div
                  class="flex flex-col sm:flex-row sm:items-center sm:justify-between text-xs text-base-content/40 font-mono"
                >
                  <div class="flex items-center mb-1 sm:mb-0">
                    <svg
                      class="w-3.5 h-3.5 mr-1.5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                      />
                    </svg>
                    Reported by:
                    <span class="text-base-content/80 ml-1"
                      >{{ issue.user?.firstname }} {{ issue.user?.lastname }}</span
                    >
                  </div>

                  <div
                    v-if="issue.updated_at !== issue.created_at"
                    class="flex items-center mt-1 sm:mt-0"
                  >
                    <svg
                      class="w-3.5 h-3.5 mr-1.5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 1121.21 8H17"
                      />
                    </svg>
                    Updated: {{ formatDate(issue.updated_at) }}
                  </div>
                </div>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import axios from '../api/client'
import ReputationBadge from '../components/ReputationBadge.vue'

const authStore = useAuthStore()

const user = computed(() => authStore.user)

const selectedStatus = ref('all')
const allIssues = ref([])
const searchQuery = ref('')
const filterStatus = ref('')
const filterType = ref('')
const reputation = ref({})
let debounceTimer = null

const stats = computed(() => {
  const issues = allIssues.value
  return {
    totalIssues: issues.length,
    pendingIssues: issues.filter((i) => i.status === 'pending').length,
    inProgressIssues: issues.filter((i) => i.status === 'in_progress').length,
    resolvedIssues: issues.filter((i) => i.status === 'resolved').length,
  }
})

const filteredIssues = computed(() => {
  if (selectedStatus.value === 'all') {
    return allIssues.value.slice(0, 10)
  }
  return allIssues.value.filter((issue) => issue.status === selectedStatus.value).slice(0, 10)
})

const getStatusClass = (status) => {
  const classes = {
    pending: 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20',
    in_progress: 'bg-blue-500/10 text-blue-400 border border-blue-500/20',
    resolved: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
    rejected: 'bg-red-500/10 text-red-400 border border-red-500/20',
    verified: 'bg-purple-500/10 text-purple-400 border border-purple-500/20',
  }
  return classes[status] || 'bg-slate-500/10 text-base-content/60 border border-slate-500/20'
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const debouncedFetch = () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(fetchData, 300)
}

const fetchData = async () => {
  try {
    const params = { page: 1, per_page: 50 }
    if (searchQuery.value) params.search = searchQuery.value
    if (filterStatus.value) params.status = filterStatus.value
    if (filterType.value) params.issue_type = filterType.value

    const response = await axios.get('/api/issues', { params })
    if (response.status === 200) {
      allIssues.value = response.data.issues
    }
  } catch (error) {
    console.error('Error fetching issues:', error)
  }
}

onMounted(async () => {
  fetchData()
  try {
    const { data } = await axios.get('/api/users/me/reputation')
    reputation.value = data.reputation
  } catch (e) {
    console.error('Failed to load reputation:', e)
  }
})
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  line-clamp: 1;
  overflow: hidden;
}
</style>
