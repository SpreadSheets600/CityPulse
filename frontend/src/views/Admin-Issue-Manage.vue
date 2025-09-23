<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-5xl mx-auto">
      <div class="mb-6 flex items-center justify-between">
        <h1 class="text-2xl font-bold">Manage Issue</h1>
        <router-link to="/admin-dashboard" class="text-indigo-600 hover:text-indigo-800">← Back</router-link>
      </div>

      <div v-if="loading" class="text-center py-10">Loading...</div>
      <div v-else-if="error" class="text-red-600 py-2">{{ error }}</div>

      <div v-else-if="issue">
        <!-- Issue Details -->
        <div class="bg-base-200 border border-gray-200 rounded-lg p-4 sm:p-6 mb-6">
          <div class="flex items-start justify-between mb-4">
            <div class="flex-1">
              <h2 class="text-xl font-semibold mb-2">{{ issue.title }}</h2>
              <p class="text-gray-600 mb-4">{{ issue.description }}</p>
            </div>
            <span :class="getStatusClass(issue.status)"
              class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ml-4">
              {{ issue.status }}
            </span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 text-sm text-gray-500 mb-4">
            <div class="flex items-center">
              <svg class="w-4 h-4 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
              <strong>Type : </strong> {{ issue.issue_type }}
            </div>
            <div class="flex items-center">
              <svg class="w-4 h-4 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <strong>Created : </strong> {{ new Date(issue.created_at).toLocaleDateString() }}
            </div>
            <div v-if="issue.updated_at !== issue.created_at" class="flex items-center">
              <svg class="w-4 h-4 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <strong>Updated : </strong> {{ new Date(issue.updated_at).toLocaleDateString() }}
            </div>
            <div class="flex items-center">
              <svg class="w-4 h-4 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <strong>Reported By : </strong> {{ issue.user?.firstname }} {{ issue.user?.lastname }}
            </div>
          </div>

          <div class="flex items-center text-sm text-gray-500 mb-4">
            <svg class="w-4 h-4 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <strong>Address : </strong> {{ issue.address }}
          </div>

          <!-- Location -->
          <div v-if="issue.latitude && issue.longitude" class="pt-4">
            <h3 class="text-lg font-medium text-gray-900 mb-3">Location</h3>
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

          <!-- Media Section -->
          <div v-if="issue.image_urls?.length > 0 || issue.video_note_url || issue.voice_note_url" class=" pt-4">
            <h3 class="text-lg font-medium text-gray-900 mb-3">Media Attachments</h3>
            <div class="space-y-4">
              <div v-if="issue.image_urls && issue.image_urls.length > 0">
                <h4 class="text-sm font-medium text-gray-500 mb-2 flex items-center">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  Images ({{ issue.image_urls.length }})
                </h4>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  <img v-for="(url, index) in issue.image_urls" :key="index" :src="url" :alt="`Image ${index + 1}`"
                    class="w-full h-32 object-cover rounded-lg cursor-pointer hover:opacity-90 transition-opacity"
                    @click="openImageModal(url)" />
                </div>
              </div>
              <div v-if="issue.voice_note_url">
                <h4 class="text-sm font-medium text-gray-500 mb-2 flex items-center">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                  </svg>
                  Voice Note
                </h4>
                <audio controls :src="issue.voice_note_url" class="w-full"></audio>
              </div>
              <div v-if="issue.video_note_url">
                <h4 class="text-sm font-medium text-gray-500 mb-2 flex items-center">
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
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Update status -->
          <div class="bg-base-200 border border-gray-200 rounded-lg p-4 sm:p-6">
            <h3 class="font-semibold mb-4">Update Status</h3>
            <select v-model="status" class="select select-bordered w-full">
              <option value="pending">Pending</option>
              <option value="in_progress">In Progress</option>
              <option value="resolved">Resolved</option>
              <option value="rejected">Rejected</option>
              <option value="verified">Verified</option>
            </select>
            <button @click="saveStatus" class="btn btn-primary mt-2 w-full">Save Status</button>
          </div>

          <!-- Assign department -->
          <div class="bg-base-200 border border-gray-200 rounded-lg p-4 sm:p-6">
            <h3 class="font-semibold mb-4">Assign Department</h3>
            <select v-model="departmentId" class="select select-bordered w-full">
              <option disabled value="">Select Department</option>
              <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
            </select>
            <button @click="assignDepartment" class="btn btn-success mt-2 w-full">Assign Department</button>
          </div>
        </div>

        <!-- Post update -->
        <div class="bg-base-200 border border-gray-200 rounded-lg p-4 sm:p-6 mt-6">
          <h3 class="font-semibold mb-4">Post Update</h3>
          <input v-model="updateTitle" type="text" placeholder="Update title" class="input input-bordered w-full" />
          <textarea v-model="updateBody" rows="4" placeholder="Update details"
            class="textarea textarea-bordered mt-2 w-full"></textarea>
          <div class="mb-4">
            <label class="block text-md font-medium mt-2 mb-2">Progress : {{ progress }}%</label>
            <input v-model.number="progress" type="range" min="0" max="100" class="w-full" />
          </div>
          <input type="file" multiple accept="image/*" @change="onUpdateFileChange" class="file-input w-full" />
          <button @click="postUpdate" class="btn btn-primary mt-2 w-full">Publish Update</button>
        </div>

        <!-- Existing updates -->
        <div class="bg-base-200 border border-gray-200 rounded-lg p-4 sm:p-6 mt-6">
          <h3 class="font-semibold mb-4">Updates</h3>
          <div v-if="updates.length === 0" class="text-sm text-gray-500 py-4">No updates yet.</div>
          <div v-else class="space-y-4">
            <div v-for="u in updates" :key="u.id" class="bg-white border border-gray-200 rounded-lg p-4">
              <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start mb-2">
                <h4 class="font-medium mb-1 sm:mb-0">{{ u.title }}</h4>
                <span class="text-xs text-gray-500">{{ new Date(u.created_at).toLocaleString() }}</span>
              </div>
              <p class="text-sm text-gray-700 mb-2">{{ u.body }}</p>
              <div class="text-xs text-gray-500 mb-2">Progress: {{ u.progress }}%</div>
              <div v-if="u.image_urls && u.image_urls.length > 0" class="mt-3">
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                  <img v-for="(url, index) in u.image_urls" :key="index" :src="url" :alt="`Update image ${index + 1}`"
                    class="w-full h-24 object-cover rounded" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Image Lightbox -->
        <ImageLightbox :visible="lightboxIndex !== null" :images="lightboxImages" :index="lightboxIndex"
          @close="lightboxIndex = null" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import { useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'
import axios from '../api/client'
import 'leaflet/dist/leaflet.css'

const route = useRoute()

const issue = ref(null)
const loading = ref(false)
const error = ref('')

const status = ref('pending')
const departments = ref([])
const departmentId = ref('')

const updateTitle = ref('')
const updateBody = ref('')
const progress = ref(0)

const updates = ref([])

const updateFiles = ref([])

const zoom = ref(15)
const mapCenter = ref([0, 0])

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

const loadIssue = async () => {
  loading.value = true
  try {
    const resp = await axios.get(`/api/issues/${route.params.id}`)
    issue.value = resp.data.issue
    status.value = issue.value.status
    if (issue.value?.department_id) {
      departmentId.value = issue.value.department_id
    }
    if (issue.value.latitude && issue.value.longitude) {
      mapCenter.value = [parseFloat(issue.value.latitude), parseFloat(issue.value.longitude)]
    }
  } catch (e) {
    error.value = e.response?.data?.error || 'Failed to load issue'
  } finally {
    loading.value = false
  }
}

const loadDepartments = async () => {
  try {
    const resp = await axios.get('/api/admin/departments')
    departments.value = resp.data.departments
  } catch (e) {
    console.error(e)
  }
}

const loadUpdates = async () => {
  try {
    const resp = await axios.get(`/api/issues/${route.params.id}/updates`)
    updates.value = resp.data.updates
  } catch (e) {
    console.error(e)
  }
}

const saveStatus = async () => {
  try {
    const resp = await axios.put(`/api/admin/issues/${route.params.id}/status`, { status: status.value })
    issue.value = resp.data.issue
  } catch (e) {
    alert(e.response?.data?.error || 'Failed to update status')
  }
}

const assignDepartment = async () => {
  if (!departmentId.value) return
  try {
    const resp = await axios.put(`/api/admin/issues/${route.params.id}/department`, { department_id: departmentId.value })
    issue.value = resp.data.issue
  } catch (e) {
    alert(e.response?.data?.error || 'Failed to assign department')
  }
}

const postUpdate = async () => {
  if (!updateTitle.value) return alert('Title is required')

  const formData = new FormData()
  formData.append('title', updateTitle.value)
  formData.append('body', updateBody.value)
  formData.append('progress', progress.value.toString())

  updateFiles.value.forEach(file => {
    formData.append('images', file)
  })

  try {
    await axios.post(`/api/admin/issues/${route.params.id}/updates`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    updateTitle.value = ''
    updateBody.value = ''
    progress.value = 0
    updateFiles.value = []
    await loadUpdates()
  } catch (e) {
    alert(e.response?.data?.error || 'Failed to post update')
  }
}

const onUpdateFileChange = (event) => {
  updateFiles.value = Array.from(event.target.files)
}

const openImageModal = (url) => {
  const index = issue.value.image_urls.indexOf(url)
  lightboxImages.value = issue.value.image_urls
  lightboxIndex.value = index
}

onMounted(async () => {
  await loadIssue()
  await Promise.all([loadDepartments(), loadUpdates()])
})
</script>
