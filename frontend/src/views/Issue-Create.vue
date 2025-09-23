<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto py-4 px-3 sm:py-8 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex justify-between items-center mb-8">
          <h1 class="text-2xl sm:text-3xl font-bold text-gray-900">Report New Issue</h1>
          <button @click="$router.go(-1)" class="inline-flex items-center text-indigo-600 hover:text-indigo-500">
            <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            Back To Issues
          </button>
        </div>
      </div>

      <!-- Form Card -->
      <div class="bg-white shadow-lg rounded-t-2xl sm:rounded-lg overflow-hidden">
        <form @submit.prevent="submitIssue" class="divide-y divide-gray-200 flex flex-col">
          <!-- Basic Information -->
          <div class="px-4 sm:px-6 py-5 sm:py-8">
            <h2 class="text-lg sm:text-xl font-semibold text-gray-900 mb-4 sm:mb-6">Basic Information</h2>
            <div class="grid grid-cols-1 gap-4 sm:gap-6 sm:grid-cols-2">
              <!-- Title -->
              <div class="sm:col-span-2">
                <label for="title" class="block text-sm font-medium text-gray-700 mb-2">
                  Issue Title *
                </label>
                <input id="title" v-model="formData.title" type="text" required
                  placeholder="Brief description of the issue"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500" />
              </div>

              <!-- Issue Type -->
              <div>
                <label for="issueType" class="block text-sm font-medium text-gray-700 mb-2">
                  Issue Type
                </label>
                <select id="issueType" v-model="formData.issueType"
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500">
                  <option value="Unspecified">Select issue type</option>
                  <option value="Pothole">Pothole</option>
                  <option value="Street Light">Street Light</option>
                  <option value="Water Supply">Water Supply</option>
                  <option value="Sewage">Sewage</option>
                  <option value="Garbage">Garbage</option>
                  <option value="Traffic">Traffic</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <!-- Description -->
              <div class="sm:col-span-2">
                <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
                  Description *
                </label>
                <textarea id="description" v-model="formData.description" required rows="4"
                  placeholder="Detailed description of the issue..."
                  class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"></textarea>
              </div>
            </div>
          </div>

          <!-- Location -->
          <div class="px-4 sm:px-6 py-5 sm:py-8">
            <h2 class="text-lg sm:text-xl font-semibold text-gray-900 mb-4 sm:mb-6">Location</h2>
            <LocationSelector v-model="formData.location" :auto-locate="true" />
          </div>

          <!-- Media -->
          <div class="px-4 sm:px-6 py-5 sm:py-8">
            <h2 class="text-lg sm:text-xl font-semibold text-gray-900 mb-4 sm:mb-6">Media</h2>

            <!-- Images -->
            <div class="mb-6 sm:mb-8">
              <label class="block text-sm font-medium text-gray-700 mb-4">
                Images *
              </label>

              <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 sm:gap-4 mb-4">
                <input ref="imageInput" type="file" multiple accept="image/*" @change="handleImageUpload"
                  class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" />
                <button type="button" @click="showPhotoModal = true"
                  class="w-full sm:w-auto inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700">
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z">
                    </path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  </svg>
                  Take Photo
                </button>
              </div>

              <!-- Image Previews -->
              <div v-if="imagePreviews.length > 0"
                class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-2 sm:gap-4">
                <div v-for="(preview, index) in imagePreviews" :key="index" class="relative group">
                  <img :src="preview" alt="Preview"
                    class="w-full h-20 sm:h-24 object-cover rounded-lg border border-gray-200" />
                  <button type="button" @click="removeImage(index)"
                    class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                    ×
                  </button>
                </div>
              </div>
            </div>

            <!-- Voice Note -->
            <div class="mb-6 sm:mb-8">
              <label class="block text-sm font-medium text-gray-700 mb-4">
                Voice Note (optional)
              </label>

              <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 sm:gap-4 mb-4">
                <input type="file" accept="audio/*" @change="handleVoiceNoteUpload"
                  class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100" />
                <button type="button" @click="showAudioModal = true"
                  class="w-full sm:w-auto inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700">
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z">
                    </path>
                  </svg>
                  Record Audio
                </button>
              </div>

              <!-- Voice Note Preview -->
              <div v-if="formData.voiceNote" class="bg-gray-50 p-4 rounded-lg">
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <svg class="w-5 h-5 text-purple-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z">
                      </path>
                    </svg>
                    <span class="text-sm font-medium text-gray-900">{{ formData.voiceNote.name
                    }}</span>
                  </div>
                  <button type="button" @click="formData.voiceNote = null" class="text-red-500 hover:text-red-700">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12">
                      </path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Video Note -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-4">
                Video Note (optional)
              </label>

              <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 sm:gap-4 mb-4">
                <input type="file" accept="video/*" @change="handleVideoNoteUpload"
                  class="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" />
                <button type="button" @click="showVideoModal = true"
                  class="w-full sm:w-auto inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z">
                    </path>
                  </svg>
                  Record Video
                </button>
              </div>

              <!-- Video Note Preview -->
              <div v-if="formData.videoNote" class="bg-gray-50 p-4 rounded-lg">
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <svg class="w-5 h-5 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z">
                      </path>
                    </svg>
                    <span class="text-sm font-medium text-gray-900">{{ formData.videoNote.name
                    }}</span>
                  </div>
                  <button type="button" @click="formData.videoNote = null" class="text-red-500 hover:text-red-700">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12">
                      </path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Submit -->
          <div class="px-4 sm:px-6 py-4 sm:py-8 bg-gray-50 sticky bottom-0 z-10">
            <div class="flex flex-col sm:flex-row sm:justify-end gap-2 sm:gap-4">
              <router-link to="/issues"
                class="w-full sm:w-auto inline-flex items-center justify-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
                Cancel
              </router-link>
              <button type="submit" :disabled="loading || !isFormValid"
                class="w-full sm:w-auto inline-flex items-center justify-center px-6 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed">
                <span v-if="loading" class="flex items-center">
                  <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                    viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                    </path>
                  </svg>
                  Submitting...
                </span>
                <span v-else>Report Issue</span>
              </button>
            </div>
          </div>
        </form>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="mt-6 bg-red-50 border border-red-200 rounded-md p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z">
              </path>
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-sm text-red-800">{{ error }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Media Capture Modals -->
    <PhotoCaptureModal v-model="showPhotoModal" @capture="addCapturedImage" />
    <VideoCaptureModal v-model="showVideoModal" @capture="formData.videoNote = $event" />
    <AudioCaptureModal v-model="showAudioModal" @capture="formData.voiceNote = $event" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import LocationSelector from '../components/Location-Selector.vue'
import PhotoCaptureModal from '../components/Photo-Capture-Modal.vue'
import VideoCaptureModal from '../components/Video-Capture-Modal.vue'
import AudioCaptureModal from '../components/Audio-Capture-Modal.vue'
import axios from '../api/client'

const router = useRouter()

// Reactive data
const formData = ref({
  title: '',
  issueType: 'Unspecified',
  description: '',
  location: null,
  images: [],
  voiceNote: null,
  videoNote: null
})

const imagePreviews = ref([])
const loading = ref(false)
const error = ref('')
const imageInput = ref(null)

// Modal states
const showPhotoModal = ref(false)
const showVideoModal = ref(false)
const showAudioModal = ref(false)

// Computed
const isFormValid = computed(() => {
  return formData.value.title.trim() &&
    formData.value.description.trim() &&
    formData.value.location &&
    formData.value.images.length > 0
})

// Methods
const handleImageUpload = (event) => {
  const files = Array.from(event.target.files || [])

  // Validate file sizes
  const maxSize = 15 * 1024 * 1024 // 15MB
  const invalidFiles = files.filter(file => file.size > maxSize)

  if (invalidFiles.length > 0) {
    error.value = 'Some images are too large. Maximum size is 15MB per image.'
    return
  }

  formData.value.images = files

  // Create previews
  imagePreviews.value = []
  files.forEach(file => {
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreviews.value.push(e.target.result)
    }
    reader.readAsDataURL(file)
  })
}

const handleVoiceNoteUpload = (event) => {
  const file = event.target.files && event.target.files[0]
  if (file) formData.value.voiceNote = file
}

const handleVideoNoteUpload = (event) => {
  const file = event.target.files && event.target.files[0]
  if (file) formData.value.videoNote = file
}

const addCapturedImage = (file) => {
  formData.value.images.push(file)

  // Create preview
  const reader = new FileReader()
  reader.onload = (e) => {
    imagePreviews.value.push(e.target.result)
  }
  reader.readAsDataURL(file)
}

const removeImage = (index) => {
  formData.value.images.splice(index, 1)
  imagePreviews.value.splice(index, 1)

  // Update file input
  if (imageInput.value) {
    const dt = new DataTransfer()
    formData.value.images.forEach(file => dt.items.add(file))
    imageInput.value.files = dt.files
  }
}

const submitIssue = async () => {
  if (!isFormValid.value) return

  loading.value = true
  error.value = ''

  try {
    const formDataToSend = new FormData()

    formDataToSend.append('title', formData.value.title.trim())
    formDataToSend.append('description', formData.value.description.trim())
    formDataToSend.append('issue_type', formData.value.issueType)

    if (formData.value.location) {
      formDataToSend.append('latitude', formData.value.location.latitude.toString())
      formDataToSend.append('longitude', formData.value.location.longitude.toString())
      if (formData.value.location.address) {
        formDataToSend.append('address', formData.value.location.address)
      }
    }

    formData.value.images.forEach((image) => {
      formDataToSend.append('images', image)
    })

    if (formData.value.voiceNote) {
      formDataToSend.append('voice_note', formData.value.voiceNote)
    }
    if (formData.value.videoNote) {
      formDataToSend.append('video_note', formData.value.videoNote)
    }

    const response = await axios.post('/api/issues/report', formDataToSend)

    if (response.status === 201 || response.status === 200) {
      router.push('/issues')
    } else {
      error.value = response.data?.error || 'Failed to report issue'
    }
  } catch (err) {
    error.value = 'Network Error. Please Try Again.'
    console.error('Issue submission error:', err)
  } finally {
    loading.value = false
  }
}
</script>
