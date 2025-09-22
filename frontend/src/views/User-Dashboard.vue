<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Main content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900">Welcome back, {{ user?.firstname }}!</h2>
          <p class="mt-1 text-sm text-gray-600">Here's what's happening in your city.</p>
        </div>

        <!-- Stats cards -->
        <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Total Issues</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ stats.totalIssues }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Pending</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ stats.pendingIssues }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">In Progress</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ stats.inProgressIssues }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Resolved</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ stats.resolvedIssues }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick actions -->
        <div class="bg-white shadow rounded-lg mb-8">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Quick Actions</h3>
            <div class="flex flex-wrap gap-4">
              <router-link to="/issues/create"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
                <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                Report New Issue
              </router-link>
              <router-link to="/issues"
                class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                View My Issues
              </router-link>
            </div>
          </div>
        </div>

        <!-- Recent issues -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-4">
              <h3 class="text-lg leading-6 font-medium text-gray-900 truncate">Recent Issues</h3>
              <div class="flex flex-wrap gap-2 mt-2 sm:mt-0">
                <button @click="selectedStatus = 'all'"
                  :class="[selectedStatus === 'all' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700', 'px-2 py-0.5 text-xs rounded-md']">
                  All
                </button>
                <button @click="selectedStatus = 'pending'"
                  :class="[selectedStatus === 'pending' ? 'bg-yellow-500 text-white' : 'bg-gray-200 text-gray-700', 'px-2 py-0.5 text-xs rounded-md']">
                  Pending
                </button>
                <button @click="selectedStatus = 'in_progress'"
                  :class="[selectedStatus === 'in_progress' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700', 'px-2 py-0.5 text-xs rounded-md']">
                  In Progress
                </button>
                <button @click="selectedStatus = 'resolved'"
                  :class="[selectedStatus === 'resolved' ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-700', 'px-2 py-0.5 text-xs rounded-md']">
                  Resolved
                </button>
              </div>
            </div>
            <div v-if="filteredIssues.length === 0" class="text-center py-8">
              <p class="text-gray-500">No issues found.</p>
            </div>
            <div v-else class="space-y-4">
              <div v-for="issue in filteredIssues" :key="issue.id" class="border border-gray-200 rounded-lg p-4">
                <div class="flex items-center justify-between">
                  <h4 class="text-sm font-medium text-gray-900">{{ issue.title }}</h4>
                  <span :class="getStatusClass(issue.status)"
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                    {{ issue.status }}
                  </span>
                </div>
                <p class="mt-1 text-sm text-gray-600">{{ issue.description }}</p>
                <p class="mt-2 text-xs text-gray-500">{{ formatDate(issue.created_at) }}</p>
              </div>
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

const authStore = useAuthStore()

const user = computed(() => authStore.user)

const selectedStatus = ref('all')
const allIssues = ref([])

const stats = computed(() => {
  const issues = allIssues.value
  return {
    totalIssues: issues.length,
    pendingIssues: issues.filter(i => i.status === 'pending').length,
    inProgressIssues: issues.filter(i => i.status === 'in_progress').length,
    resolvedIssues: issues.filter(i => i.status === 'resolved').length
  }
})

const filteredIssues = computed(() => {
  if (selectedStatus.value === 'all') {
    return allIssues.value.slice(0, 10) // Show latest 10
  }
  return allIssues.value.filter(issue => issue.status === selectedStatus.value).slice(0, 10)
})

const getStatusClass = (status) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-800',
    in_progress: 'bg-blue-100 text-blue-800',
    resolved: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800',
    verified: 'bg-purple-100 text-purple-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const fetchData = async () => {
  try {
    const response = await axios.get('/api/issues')
    if (response.status === 200) {
      // Sort by created_at descending
      allIssues.value = response.data.issues.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    }
  } catch (error) {
    console.error('Error fetching issues:', error)
  }
}

onMounted(() => {
  fetchData()
})
</script>
