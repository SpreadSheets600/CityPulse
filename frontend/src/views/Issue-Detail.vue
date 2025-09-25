<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Main content -->
    <main class="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <!-- Back button -->
        <div class="mb-6">
          <button @click="$router.go(-1)" class="inline-flex items-center text-indigo-600 hover:text-indigo-500">
            <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Back to Issues
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
        </div>

        <!-- Issue Details -->
        <div v-else-if="issue" class="bg-white shadow overflow-hidden sm:rounded-lg">
          <!-- Header -->
          <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <h1 class="text-2xl font-bold text-gray-900">{{ issue.title }}</h1>
                <div class="mt-2 flex flex-wrap items-center gap-4 text-sm text-gray-500">
                  <div class="flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    Reported by {{ issue.user?.firstname }} {{ issue.user?.lastname }}
                  </div>
                  <div class="flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {{ formatDate(issue.created_at) }}
                  </div>
                  <div v-if="issue.updated_at !== issue.created_at" class="flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Updated {{ formatDate(issue.updated_at) }}
                  </div>
                </div>
              </div>
              <span :class="getStatusClass(issue.status)"
                class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ml-4">
                {{ issue.status }}
              </span>
            </div>
          </div>

          <!-- Description -->
          <div class="border-t border-gray-200 px-4 py-5 sm:px-6">
            <h3 class="text-lg font-medium text-gray-900 mb-3">Description</h3>
            <p class="text-sm text-gray-700 leading-relaxed">{{ issue.description }}</p>
          </div>

          <!-- Details -->
          <div v-if="(issue.issue_type && issue.issue_type !== 'Unspecified') || issue.address || issue.department"
            class="border-t border-gray-200 px-4 py-5 sm:px-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Details</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div v-if="issue.issue_type && issue.issue_type !== 'Unspecified'">
                <dt class="text-sm font-medium text-gray-500">Issue Type</dt>
                <dd class="mt-1 text-sm text-gray-900 flex items-center">
                  <svg class="w-4 h-4 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                  </svg>
                  {{ issue.issue_type }}
                </dd>
              </div>
              <div v-if="issue.address">
                <dt class="text-sm font-medium text-gray-500">Address</dt>
                <dd class="mt-1 text-sm text-gray-900 flex items-center">
                  <svg class="w-4 h-4 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  {{ issue.address }}
                </dd>
              </div>
              <div v-if="issue.department">
                <dt class="text-sm font-medium text-gray-500">Assigned Department</dt>
                <dd class="mt-1 text-sm text-gray-900 flex items-center">
                  <svg class="w-4 h-4 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                  {{ issue.department.name }}
                </dd>
              </div>
            </div>
          </div>

          <!-- Location -->
          <div v-if="issue.latitude && issue.longitude" class="border-t border-gray-200 px-4 py-5 sm:px-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Location</h3>
            <div class="h-64 w-full rounded-lg overflow-hidden border">
              <l-map v-model:zoom="zoom" :center="mapCenter" :use-global-leaflet="false" style="height: 100%;">
                <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'></l-tile-layer>
                <l-marker :lat-lng="mapCenter">
                  <l-popup>
                    <div class="text-sm">
                      <p class="font-semibold">{{ issue.title }}</p>
                      <p>{{ issue.address }}</p>
                    </div>
                  </l-popup>
                </l-marker>
              </l-map>
            </div>
          </div>

          <!-- Media -->
          <div v-if="issue.image_urls?.length > 0 || issue.voice_note_url || issue.video_note_url"
            class="border-t border-gray-200 px-4 py-5 sm:px-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Media</h3>
            <div class="space-y-6">
              <div v-if="issue.image_urls && issue.image_urls.length > 0">
                <h4 class="text-sm font-medium text-gray-500 mb-3 flex items-center">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  Images ({{ issue.image_urls.length }})
                </h4>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  <img v-for="(url, index) in issue.image_urls" :key="index" :src="url" :alt="`Image ${index + 1}`"
                    class="w-full h-48 object-cover rounded-lg cursor-pointer hover:opacity-90 transition-opacity shadow-sm"
                    @click="openImageModal(url, issue.image_urls)" />
                </div>
              </div>
              <div v-if="issue.voice_note_url">
                <h4 class="text-sm font-medium text-gray-500 mb-3 flex items-center">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                  </svg>
                  Voice Note
                </h4>
                <audio controls :src="issue.voice_note_url" class="w-full"></audio>
              </div>
              <div v-if="issue.video_note_url">
                <h4 class="text-sm font-medium text-gray-500 mb-3 flex items-center">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  Video Note
                </h4>
                <video controls :src="issue.video_note_url" class="w-full max-w-md rounded-lg"></video>
              </div>
            </div>
          </div>

          <!-- Updates section -->
          <div class="border-t border-gray-200 px-4 py-5 sm:px-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Updates</h3>
            <div v-if="updates.length === 0" class="text-sm text-gray-500">No updates yet.</div>
            <div v-else class="space-y-4">
              <div v-for="u in updates" :key="u.id" class="bg-gray-50 border border-gray-200 rounded-lg p-4">
                <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start mb-3">
                  <h4 class="font-semibold text-gray-900 mb-1 sm:mb-0">{{ u.title }}</h4>
                  <span class="text-xs text-gray-500 flex items-center">
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {{ formatDate(u.created_at) }}
                  </span>
                </div>
                <p class="text-sm text-gray-700 mb-3">{{ u.body }}</p>
                <div class="mb-3">
                  <div class="flex justify-between text-xs text-gray-500 mb-1">
                    <span>Progress</span>
                    <span>{{ u.progress }}%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-indigo-600 h-2 rounded-full" :style="{ width: (u.progress || 0) + '%' }"></div>
                  </div>
                </div>
                <div v-if="u.image_urls && u.image_urls.length > 0">
                  <h5 class="text-sm font-medium text-gray-500 mb-2">Update Images</h5>
                  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                    <img v-for="(url, index) in u.image_urls" :key="index" :src="url" :alt="`Update image ${index + 1}`"
                      class="w-full h-24 object-cover rounded cursor-pointer hover:opacity-90 transition-opacity"
                      @click="openImageModal(url, u.image_urls)" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Error State -->
        <div v-else class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">Issue not found</h3>
          <p class="mt-1 text-sm text-gray-500">The issue you're looking for doesn't exist or you don't have
            permission to view it.</p>
        </div>
      </div>
    </main>

    <!-- Image Lightbox -->
    <ImageLightbox :visible="lightboxIndex !== null" :images="lightboxImages" :index="lightboxIndex"
      @close="lightboxIndex = null" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '../api/client'
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'


const route = useRoute()
const issue = ref(null)
const loading = ref(false)
const mapCenter = ref([0, 0])
const updates = ref([])
const zoom = ref(15)

const lightboxImages = ref([])
const lightboxIndex = ref(null)

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
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const fetchIssue = async () => {
  loading.value = true
  try {
    const response = await axios.get(`/api/issues/${route.params.id}`)

    if (response.status === 200) {
      issue.value = response.data.issue
      if (issue.value.latitude && issue.value.longitude) {
        mapCenter.value = [parseFloat(issue.value.latitude), parseFloat(issue.value.longitude)]
      }
    } else {
      console.error('Failed to fetch issue')
    }
  } catch (error) {
    console.error('Error fetching issue:', error)
  } finally {
    loading.value = false
  }
}

const fetchUpdates = async () => {
  try {
    const resp = await axios.get(`/api/issues/${route.params.id}/updates`)
    updates.value = resp.data.updates || []
  } catch (e) {
    console.error('Failed to fetch updates', e)
  }
}

const openImageModal = (url, images) => {
  const index = images.indexOf(url)
  lightboxImages.value = images
  lightboxIndex.value = index
}

onMounted(() => {
  console.log('IssueDetail component mounted, route params:', route.params)
  fetchIssue()
  fetchUpdates()
})
</script>
