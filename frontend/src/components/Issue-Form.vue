<template>
  <div class="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow">
    <h2 class="text-2xl font-bold text-gray-900 mb-6">Report New Issue</h2>

    <form @submit.prevent="submitIssue" class="space-y-6">
      <!-- Title -->
      <div>
        <label for="title" class="block text-sm font-medium text-gray-700 mb-2">
          Issue Title *
        </label>
        <input id="title" v-model="formData.title" type="text" required placeholder="Brief description of the issue"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" />
      </div>

      <!-- Issue Type -->
      <div>
        <label for="issueType" class="block text-sm font-medium text-gray-700 mb-2">
          Issue Type
        </label>
        <select id="issueType" v-model="formData.issueType"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500">
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
      <div>
        <label for="description" class="block text-sm font-medium text-gray-700 mb-2">
          Description *
        </label>
        <textarea id="description" v-model="formData.description" required rows="4"
          placeholder="Detailed description of the issue..."
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"></textarea>
      </div>

      <!-- Location Selector -->
      <LocationSelector v-model="formData.location" />

      <!-- Images -->
      <div>
        <label for="images" class="block text-sm font-medium text-gray-700 mb-2">
          Images * (at least one required)
        </label>
        <input id="images" ref="imageInput" type="file" multiple accept="image/*" @change="handleImageUpload"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" />
        <p class="text-sm text-gray-600 mt-1">
          Select one or more images (max 15MB each)
        </p>

        <!-- Image Preview -->
        <div v-if="imagePreviews.length > 0" class="mt-4 grid grid-cols-2 md:grid-cols-3 gap-4">
          <div v-for="(preview, index) in imagePreviews" :key="index" class="relative">
            <img :src="preview" alt="Preview" class="w-full h-24 object-cover rounded-lg border" />
            <button @click="removeImage(index)"
              class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs">
              ×
            </button>
          </div>
        </div>
      </div>

      <!-- Voice Note -->
      <div>
        <label for="voiceNote" class="block text-sm font-medium text-gray-700 mb-2">
          Voice Note (optional)
        </label>
        <input id="voiceNote" type="file" accept="audio/*" @change="handleVoiceNoteUpload"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" />
        <p class="text-sm text-gray-600 mt-1">
          Record or upload an audio description
        </p>
      </div>

      <!-- Video Note -->
      <div>
        <label for="videoNote" class="block text-sm font-medium text-gray-700 mb-2">
          Video Note (optional)
        </label>
        <input id="videoNote" type="file" accept="video/*" @change="handleVideoNoteUpload"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" />
        <p class="text-sm text-gray-600 mt-1">
          Upload a video showing the issue
        </p>
      </div>

      <!-- Submit Button -->
      <div class="flex justify-end space-x-4">
        <button type="button" @click="$emit('cancel')"
          class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50">
          Cancel
        </button>
        <button type="submit" :disabled="loading || !isFormValid"
          class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed">
          <span v-if="loading" class="flex items-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
              viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4">
              </circle>
              <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
              </path>
            </svg>
            Submitting...
          </span>
          <span v-else>Report Issue</span>
        </button>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="text-red-600 text-sm text-center">
        {{ error }}
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

import LocationSelector from './Location-Selector.vue'
import axios from '../api/client'

const router = useRouter()

// Emits
const emit = defineEmits(['cancel', 'success'])

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

// Computed
const isFormValid = computed(() => {
  return formData.value.title.trim() &&
    formData.value.description.trim() &&
    formData.value.location &&
    formData.value.images.length > 0
})

// Methods
const handleImageUpload = (event) => {
  const files = Array.from(event.target.files)

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
  const file = event.target.files[0]
  if (file) {
    formData.value.voiceNote = file
  }
}

const handleVideoNoteUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    formData.value.videoNote = file
  }
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

    console.log(formDataToSend)

    const response = await axios.post('/api/issues/report', formDataToSend)

    if (response.status === 201 || response.status === 200) {

      console.log('Response Data :', response.data)

      emit('success', response.data.issue)
      router.push('/issues')
    } else {
      error.value = response.data.error || 'Failed to report issue'
    }

    console.log('Issue reported successfully : ', response.data)

  } catch (err) {
    error.value = 'Network Error. Please Try Again.'
    console.error('Issue submission error:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Additional styles if needed */
</style>
