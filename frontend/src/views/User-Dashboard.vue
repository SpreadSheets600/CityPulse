<template>
  <div class="min-h-screen bg-base-100">
    <!-- Main content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900">Welcome Back, {{ user?.firstname }}!</h2>
          <p class="mt-1 text-sm text-gray-600">Here's what's happening in your city.</p>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
          <div class="bg-base-200 overflow-hidden shadow rounded-lg">
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

          <div class="bg-base-200 overflow-hidden shadow rounded-lg">
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

          <div class="bg-base-200 overflow-hidden shadow rounded-lg">
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

          <div class="bg-base-200 overflow-hidden shadow rounded-lg">
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

        <!-- Quick Actions -->
        <div class="bg-base-200 shadow rounded-lg mb-8">
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
                class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-base-200 hover:bg-gray-50">
                View My Issues
              </router-link>
            </div>
          </div>
        </div>

        <!-- Recent issues -->
        <div class="bg-base-200 shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-4">
              <h3 class="text-lg leading-6 font-medium text-gray-900 truncate">Recent Issues</h3>
              <div class="flex flex-wrap gap-2 mt-2 sm:mt-0">
                <button @click="selectedStatus = 'all'"
                  :class="[selectedStatus === 'all' ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-700', 'px-2 py-0.5 text-xs rounded-md hover:bg-opacity-80']">
                  All
                </button>
                <button @click="selectedStatus = 'pending'"
                  :class="[selectedStatus === 'pending' ? 'bg-yellow-500 text-white' : 'bg-gray-200 text-gray-700', 'px-2 py-0.5 text-xs rounded-md hover:bg-opacity-80']">
                  Pending
                </button>
                <button @click="selectedStatus = 'in_progress'"
                  :class="[selectedStatus === 'in_progress' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700', 'px-2 py-0.5 text-xs rounded-md hover:bg-opacity-80']">
                  In Progress
                </button>
                <button @click="selectedStatus = 'resolved'"
                  :class="[selectedStatus === 'resolved' ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-700', 'px-2 py-0.5 text-xs rounded-md hover:bg-opacity-80']">
                  Resolved
                </button>
              </div>
            </div>
            <div v-if="filteredIssues.length === 0" class="text-center py-8">
              <p class="text-gray-500">No issues found.</p>
            </div>
            <div v-else class="space-y-4">
              <div v-for="issue in filteredIssues" :key="issue.id"
                class="border border-gray-200 rounded-lg hover:border-base-300 hover:shadow-md transition-all duration-200 bg-white">
                <router-link :to="`/issues/${issue.id}`" class="block p-4 hover:bg-gray-50 rounded-lg">
                  <!-- Header -->
                  <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-2">
                    <p class="text-sm font-medium text-indigo-600 truncate">{{ issue.title }}</p>
                    <div class="flex items-center text-sm text-gray-500 mt-1 sm:mt-0">
                      <span :class="getStatusClass(issue.status)"
                        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium mr-2">
                        {{ issue.status }}
                      </span>
                      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      {{ formatDate(issue.created_at) }}
                    </div>
                  </div>

                  <!-- Details Row -->
                  <div class="flex flex-wrap items-center gap-3 text-xs text-gray-500 mb-3">
                    <span v-if="issue.issue_type && issue.issue_type !== 'Unspecified'" class="flex items-center">
                      <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                      </svg>
                      {{ issue.issue_type }}
                    </span>
                    <span v-if="issue.address" class="flex items-center">
                      <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      {{ issue.address }}
                    </span>
                  </div>

                  <!-- Media Row -->
                  <div v-if="issue.image_urls?.length > 0 || issue.video_note_url || issue.voice_note_url"
                    class="flex items-center gap-3 text-xs text-gray-500 mb-3">
                    <span v-if="issue.image_urls && issue.image_urls.length > 0" class="flex items-center">
                      <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      {{ issue.image_urls.length }} image{{ issue.image_urls.length > 1 ? 's' : '' }}
                    </span>
                    <span v-if="issue.video_note_url" class="flex items-center">
                      <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                      </svg>
                      Video
                    </span>
                    <span v-if="issue.voice_note_url" class="flex items-center">
                      <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                      </svg>
                      Audio
                    </span>
                  </div>

                  <!-- Footer -->
                  <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between text-xs text-gray-500">
                    <div class="flex items-center mb-1 sm:mb-0">
                      <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      Posted by {{ issue.user?.firstname }} {{ issue.user?.lastname }}
                    </div>
                    <div v-if="issue.updated_at !== issue.created_at" class="flex items-center">
                      <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      Updated {{ formatDate(issue.updated_at) }}
                    </div>
                  </div>
                </router-link>
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
    return allIssues.value.slice(0, 10)
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
