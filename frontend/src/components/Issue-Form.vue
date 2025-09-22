<template>
  <!-- Main modal -->
  <div :class="['fixed inset-0 z-50 overflow-y-auto', { 'flex items-center justify-center': isOpen }]" tabindex="-1"
    :aria-hidden="!isOpen" v-if="isOpen">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-gray-900/50 bg-opacity-50" @click="closeModal"></div>

    <!-- Modal content -->
    <div class="relative bg-white rounded-lg shadow-lg max-w-2xl w-full mx-4 my-6 max-h-[90vh] overflow-y-auto">
      <!-- Modal header -->
      <div
        class="flex items-center justify-between p-4 md:p-5 border-b rounded-t border-gray-200 sticky top-0 bg-white">
        <h3 class="text-lg font-semibold text-gray-900">
          Report New Issue
        </h3>
        <button type="button"
          class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 inline-flex justify-center items-center"
          @click="closeModal">
          <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
          </svg>
          <span class="sr-only">Close modal</span>
        </button>
      </div>

      <!-- Modal body / form -->
      <form class="p-4 md:p-5" @submit.prevent="submitIssue">
        <div class="grid gap-4 mb-4 grid-cols-2">
          <!-- Title (full width) -->
          <div class="col-span-2">
            <label for="title" class="block mb-2 text-sm font-medium text-gray-900">Issue Title *</label>
            <input id="title" v-model="formData.title" type="text" required placeholder="Brief description of the issue"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5" />
          </div>

          <!-- Issue Type (full width on mobile, half on larger screens) -->
          <div class="col-span-2">
            <label for="issueType" class="block mb-2 text-sm font-medium text-gray-900">Issue Type</label>
            <select id="issueType" v-model="formData.issueType"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5">
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

          <!-- Location selector (full width) -->
          <div class="col-span-2">
            <label class="block mb-2 text-sm font-medium text-gray-900">Location</label>
            <LocationSelector v-model="formData.location" />
          </div>

          <!-- Description (full) -->
          <div class="col-span-2">
            <label for="description" class="block mb-2 text-sm font-medium text-gray-900">Description *</label>
            <textarea id="description" v-model="formData.description" required rows="4"
              placeholder="Detailed description of the issue..."
              class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300"></textarea>
          </div>

          <!-- Images (full) -->
          <div class="col-span-2">
            <label for="images" class="block mb-2 text-sm font-medium text-gray-900">Images * (at least one
              required)</label>
            <input id="images" ref="imageInput" type="file" multiple accept="image/*" @change="handleImageUpload"
              class="block w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 p-2.5" />
            <p class="text-sm text-gray-600 mt-1">Select one or more images (max 15MB each)</p>

            <div v-if="imagePreviews.length > 0" class="mt-4 grid grid-cols-2 sm:grid-cols-3 gap-4">
              <div v-for="(preview, index) in imagePreviews" :key="index" class="relative">
                <img :src="preview" alt="Preview" class="w-full h-24 object-cover rounded-lg border" />
                <button type="button" @click="removeImage(index)"
                  class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs">×</button>
              </div>
            </div>
          </div>

          <!-- Voice Note (full width on mobile, half on larger screens) -->
          <div class="col-span-2 sm:col-span-1">
            <label for="voiceNote" class="block mb-2 text-sm font-medium text-gray-900">Voice Note (optional)</label>
            <input id="voiceNote" type="file" accept="audio/*" @change="handleVoiceNoteUpload"
              class="block w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 p-2.5" />
          </div>

          <!-- Video Note (full width on mobile, half on larger screens) -->
          <div class="col-span-2 sm:col-span-1">
            <label for="videoNote" class="block mb-2 text-sm font-medium text-gray-900">Video Note (optional)</label>
            <input id="videoNote" type="file" accept="video/*" @change="handleVideoNoteUpload"
              class="block w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 p-2.5" />
          </div>
        </div>

        <div
          class="flex flex-col sm:flex-row justify-end space-y-2 sm:space-y-0 sm:space-x-4 sticky bottom-0 bg-white pt-4 border-t">
          <button type="button" @click="closeModal"
            class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 order-2 sm:order-1">
            Cancel
          </button>
          <button type="submit" :disabled="loading || !isFormValid"
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed order-1 sm:order-2 inline-flex items-center justify-center">
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

        <div v-if="error" class="text-red-600 text-sm text-center mt-3">
          {{ error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

import LocationSelector from './Location-Selector.vue'
import axios from '../api/client'

const props = defineProps({
  modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'cancel', 'success'])

// Modal state
const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

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

const closeModal = () => {
  isOpen.value = false
  // Reset form
  formData.value = {
    title: '',
    issueType: 'Unspecified',
    description: '',
    location: null,
    images: [],
    voiceNote: null,
    videoNote: null
  }
  imagePreviews.value = []
  error.value = ''
  if (imageInput.value) {
    imageInput.value.value = ''
  }
  emit('cancel')
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
      emit('success', response.data.issue)
      isOpen.value = false
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

<style scoped>
/* keep modal centered when visible */
</style>
