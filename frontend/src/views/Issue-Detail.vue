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
          <div class="px-4 py-5 sm:px-6">
            <div class="flex items-center justify-between">
              <h3 class="text-lg leading-6 font-medium text-gray-900">{{ issue.title }}</h3>
              <span :class="getStatusClass(issue.status)"
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                {{ issue.status }}
              </span>
            </div>
            <p class="mt-1 max-w-2xl text-sm text-gray-500">{{ formatDate(issue.created_at) }}</p>
          </div>
          <div class="border-t border-gray-200">
            <dl>
              <div class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Description</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ issue.description }}
                </dd>
              </div>
              <div v-if="issue.issue_type && issue.issue_type !== 'Unspecified'"
                class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Issue Type</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ issue.issue_type }}</dd>
              </div>
              <div v-if="issue.address" class="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Address</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ issue.address }}</dd>
              </div>
              <div v-if="issue.latitude && issue.longitude"
                class="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Location</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <p class="mb-2">{{ issue.latitude }}, {{ issue.longitude }}</p>
                  <div class="h-64 w-full rounded-lg overflow-hidden border">
                    <iframe
                      :src="`https://www.openstreetmap.org/export/embed.html?bbox=${mapCenter[1] - 0.01},${mapCenter[0] - 0.01},${mapCenter[1] + 0.01},${mapCenter[0] + 0.01}&layer=mapnik&marker=${mapCenter[0]},${mapCenter[1]}`"
                      width="100%" height="100%" style="border: none;">
                    </iframe>
                  </div>
                </dd>
              </div>
              <div v-if="issue.image_urls && issue.image_urls.length > 0" class="bg-gray-50 px-4 py-5 sm:px-6">
                <dt class="text-sm font-medium text-gray-500 mb-2">Images</dt>
                <dd class="mt-1 sm:mt-0">
                  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    <img v-for="(url, index) in issue.image_urls" :key="index" :src="url" :alt="`Image ${index + 1}`"
                      class="w-full h-48 object-cover rounded-lg cursor-pointer" @click="openImageModal(url)" />
                  </div>
                </dd>
              </div>
              <div v-if="issue.voice_note_url" class="bg-white px-4 py-5 sm:px-6">
                <dt class="text-sm font-medium text-gray-500 mb-2">Voice Note</dt>
                <dd class="mt-1 sm:mt-0">
                  <audio controls :src="issue.voice_note_url" class="w-full"></audio>
                </dd>
              </div>
              <div v-if="issue.video_note_url" class="bg-gray-50 px-4 py-5 sm:px-6">
                <dt class="text-sm font-medium text-gray-500 mb-2">Video Note</dt>
                <dd class="mt-1 sm:mt-0">
                  <video controls :src="issue.video_note_url" class="w-full max-w-md rounded-lg"></video>
                </dd>
              </div>
            </dl>
          </div>

          <!-- Updates section -->
          <div class="border-t border-gray-200 px-4 py-5 sm:px-6">
            <h4 class="text-md font-medium text-gray-900 mb-3">Updates</h4>
            <div v-if="updates.length === 0" class="text-sm text-gray-500">No updates yet.</div>
            <div v-else class="space-y-4">
              <div v-for="u in updates" :key="u.id" class="border rounded-md p-3">
                <div class="flex items-center justify-between">
                  <h5 class="font-semibold">{{ u.title }}</h5>
                  <span class="text-xs text-gray-500">{{ formatDate(u.created_at) }}</span>
                </div>
                <p class="text-sm text-gray-700 mt-1">{{ u.body }}</p>
                <div class="mt-2">
                  <div class="flex justify-between text-xs text-gray-500">
                    <span>Progress</span>
                    <span>{{ u.progress }}%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded h-2 mt-1">
                    <div class="bg-indigo-600 h-2 rounded" :style="{ width: (u.progress || 0) + '%' }"></div>
                  </div>
                </div>
                <div v-if="u.image_urls && u.image_urls.length > 0" class="mt-3">
                  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                    <img v-for="(url, index) in u.image_urls" :key="index" :src="url" :alt="`Update image ${index + 1}`"
                      class="w-full h-24 object-cover rounded cursor-pointer" @click="openImageModal(url)" />
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

    <!-- Image Modal -->
    <div v-if="selectedImage"
      class="fixed inset-0 bg-gray-600 bg-opacity-75 overflow-y-auto h-full w-full z-50 flex items-center justify-center"
      @click="closeImageModal">
      <div class="relative max-w-4xl max-h-full p-4">
        <img :src="selectedImage" alt="Full size image" class="max-w-full max-h-full object-contain" />
        <button @click="closeImageModal" class="absolute top-2 right-2 text-white text-2xl">&times;</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '../api/client'


const route = useRoute()
const issue = ref(null)
const loading = ref(false)
const selectedImage = ref(null)
const mapCenter = ref([0, 0])
const updates = ref([])

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

const openImageModal = (url) => {
  selectedImage.value = url
}

const closeImageModal = () => {
  selectedImage.value = null
}

onMounted(() => {
  console.log('IssueDetail component mounted, route params:', route.params)
  fetchIssue()
  fetchUpdates()
})
</script>
