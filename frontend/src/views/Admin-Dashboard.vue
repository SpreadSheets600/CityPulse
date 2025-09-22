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
                <l-marker v-for="issue in issues" :key="issue.id" :lat-lng="[issue.latitude, issue.longitude]">
                  <l-popup>
                    <div class="max-w-sm">
                      <h3 class="font-bold text-lg mb-2">{{ issue.title }}</h3>
                      <p class="text-sm text-gray-600 mb-2">{{ issue.description }}</p>
                      <div class="space-y-1 mb-3">
                        <p class="text-sm"><strong>Status:</strong>
                          <span :class="getStatusColor(issue.status)" class="px-2 py-1 rounded text-xs font-medium">
                            {{ issue.status }}
                          </span>
                        </p>
                        <p class="text-sm"><strong>Type:</strong> {{ issue.issue_type }}</p>
                        <p class="text-sm"><strong>Address:</strong> {{ issue.address }}</p>
                        <p class="text-sm"><strong>Created:</strong> {{ new Date(issue.created_at).toLocaleDateString()
                        }}</p>
                      </div>
                      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                        <router-link :to="{ name: 'AdminIssueManage', params: { id: issue.id } }"
                          class="w-full text-center bg-indigo-600 text-white px-3 py-2 rounded text-sm hover:bg-indigo-700 transition-colors">
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
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Recent Issues</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
              <div v-for="issue in issues.slice(0, 9)" :key="issue.id"
                class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start mb-3">
                  <h4 class="text-sm font-medium text-gray-900 line-clamp-2 mb-2 sm:mb-0">{{ issue.title }}</h4>
                  <span :class="getStatusColor(issue.status)"
                    class="px-2 py-1 rounded-full text-xs font-medium whitespace-nowrap self-start sm:self-auto">
                    {{ issue.status }}
                  </span>
                </div>
                <p class="text-sm text-gray-600 mb-3 line-clamp-3">{{ issue.description }}</p>
                <div class="space-y-1 text-xs text-gray-500 mb-3">
                  <p><strong>Type:</strong> {{ issue.issue_type }}</p>
                  <p><strong>Location:</strong> {{ issue.address }}</p>
                  <p><strong>Date:</strong> {{ new Date(issue.created_at).toLocaleDateString() }}</p>
                </div>
                <div class="flex flex-col sm:flex-row gap-2">
                  <router-link :to="{ name: 'AdminIssueManage', params: { id: issue.id } }"
                    class="w-full text-center bg-indigo-600 text-white px-3 py-2 rounded text-sm hover:bg-indigo-700 transition-colors">
                    Manage
                  </router-link>
                </div>
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

const isAdmin = computed(() => authStore.isAdmin)

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
