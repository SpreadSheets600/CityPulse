<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-3xl font-bold mb-6 text-gray-900">Admin Dashboard</h1>

      <!-- Loading and Error States -->
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Loading issues...</p>
      </div>

      <div v-if="error" class="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-sm text-red-800">{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div v-else-if="issues.length === 0" class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No issues found</h3>
        <p class="mt-1 text-sm text-gray-500">Get started by waiting for users to report issues.</p>
      </div>

      <div v-else>
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Total Issues</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ issues.length }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Pending</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ getStatusCount('pending') }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">In Progress</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ getStatusCount('in_progress') }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Resolved</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ getStatusCount('resolved') }}</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Map Section -->
        <div class="bg-white shadow rounded-lg mb-6">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Issues Map</h3>
            <div class="map-container h-72 sm:h-96">
              <l-map v-model:zoom="zoom" :center="center" :use-global-leaflet="false" style="height: 100%;">
                <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'></l-tile-layer>
                <l-marker v-for="issue in issues.filter(i => i.status === 'pending')" :key="issue.id"
                  :lat-lng="[issue.latitude, issue.longitude]">
                  <l-popup>
                    <div class="w-48 sm:w-56">
                      <div class="space-y-1 text-sm">
                        <p><strong>Type:</strong> {{ issue.issue_type }}</p>
                        <p><strong>Address:</strong> {{ issue.address }}</p>
                      </div>
                      <div class="mt-3">
                        <router-link :to="{ name: 'AdminIssueManage', params: { id: issue.id } }"
                          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-gray-200 hover:bg-gray-300">
                          Manage
                        </router-link>
                      </div>
                    </div>
                  </l-popup>
                </l-marker>
              </l-map>
            </div>
          </div>
        </div>

        <!-- Issues List -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-4">
              <h3 class="text-lg leading-6 font-medium text-gray-900">Recent Issues</h3>
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
                <button @click="selectedStatus = 'rejected'"
                  :class="[selectedStatus === 'rejected' ? 'bg-red-500 text-white' : 'bg-gray-200 text-gray-700', 'px-2 py-0.5 text-xs rounded-md hover:bg-opacity-80']">
                  Rejected
                </button>
                <button @click="selectedStatus = 'verified'"
                  :class="[selectedStatus === 'verified' ? 'bg-purple-500 text-white' : 'bg-gray-200 text-gray-700', 'px-2 py-0.5 text-xs rounded-md hover:bg-opacity-80']">
                  Verified
                </button>
              </div>
            </div>
            <div v-if="filteredIssues.length === 0" class="text-center py-8">
              <p class="text-gray-500">No issues found for the selected filter.</p>
            </div>
            <div v-else class="space-y-4">
              <div v-for="issue in filteredIssues.slice(0, 10)" :key="issue.id"
                class="border border-gray-200 rounded-lg hover:border-base-300 hover:shadow-md transition-all duration-200 bg-white">
                <router-link :to="{ name: 'AdminIssueManage', params: { id: issue.id } }"
                  class="block p-4 hover:bg-gray-50 rounded-lg">
                  <!-- Header -->
                  <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-2">
                    <p class="text-sm font-medium text-indigo-600 truncate">{{ issue.title }}</p>
                    <div class="flex items-center text-sm text-gray-500 mt-1 sm:mt-0">
                      <span :class="getStatusColor(issue.status)"
                        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium mr-2">
                        {{ issue.status }}
                      </span>
                      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      {{ new Date(issue.created_at).toLocaleDateString() }}
                    </div>
                  </div>

                  <!-- Description -->
                  <p class="text-sm text-gray-600 line-clamp-2 mb-3">{{ issue.description }}</p>

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
                      Reported by {{ issue.user?.firstname }} {{ issue.user?.lastname }}
                    </div>
                    <div v-if="issue.updated_at !== issue.created_at" class="flex items-center">
                      <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      Updated {{ new Date(issue.updated_at).toLocaleDateString() }}
                    </div>
                  </div>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import axios from '../api/client'
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'

const authStore = useAuthStore()
const issues = ref([])
const loading = ref(false)
const error = ref('')
const zoom = ref(13)
const center = ref([28.6139, 77.2090])
const selectedStatus = ref('all')

const isAdmin = computed(() => authStore.isAdmin)

const filteredIssues = computed(() => {
  if (selectedStatus.value === 'all') {
    return issues.value
  }
  return issues.value.filter(issue => issue.status === selectedStatus.value)
})

const fetchIssues = async () => {
  if (!isAdmin.value) {
    error.value = 'Access denied. Admin privileges required.'
    return
  }

  loading.value = true
  error.value = ''
  try {
    const response = await axios.get('/api/admin/issues')
    issues.value = response.data.issues
    if (issues.value.length > 0) {
      // Center map on first issue
      center.value = [issues.value[0].latitude, issues.value[0].longitude]
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to fetch issues'
  } finally {
    loading.value = false
  }
}



const getStatusCount = (status) => {
  return issues.value.filter(issue => issue.status === status).length
}

const getStatusColor = (status) => {
  const colors = {
    pending: 'bg-yellow-100 text-yellow-800',
    in_progress: 'bg-blue-100 text-blue-800',
    resolved: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800',
    verified: 'bg-purple-100 text-purple-800'
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}

onMounted(() => {
  fetchIssues()
})
</script>

<style scoped>
.map-container {
  border-radius: 0.5rem;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-clamp: 2;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  line-clamp: 3;
  overflow: hidden;
}

/* Custom marker colors based on status */
.leaflet-marker-icon {
  filter: hue-rotate(0deg);
}

.leaflet-marker-icon.pending {
  filter: hue-rotate(45deg);
  /* Yellow tint */
}

.leaflet-marker-icon.in_progress {
  filter: hue-rotate(200deg);
  /* Blue tint */
}

.leaflet-marker-icon.resolved {
  filter: hue-rotate(120deg);
  /* Green tint */
}

.leaflet-marker-icon.rejected {
  filter: hue-rotate(0deg);
  /* Red tint */
}

.leaflet-marker-icon.verified {
  filter: hue-rotate(270deg);
  /* Purple tint */
}
</style>
