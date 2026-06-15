<template>
  <div class="min-h-screen bg-base-100 text-base-content antialiased py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8 gap-4">
        <div>
          <h1 class="text-3xl font-extrabold text-base-content font-mono tracking-wider uppercase">
            Report New Issue
          </h1>
          <p class="text-xs text-base-content/60 mt-1">
            Submit geolocated media evidence for verification
          </p>
        </div>
        <button
          @click="$router.go(-1)"
          class="btn btn-outline border-base-300 hover:border-slate-500 rounded-xl btn-sm font-mono flex items-center gap-1.5 cursor-pointer"
        >
          <svg
            class="h-4 w-4"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Back To Issues
        </button>
      </div>

      <!-- Form Card -->
      <div class="bg-base-200 border border-base-300 shadow-xl rounded-3xl overflow-hidden mb-6">
        <form @submit.prevent="submitIssue" class="divide-y divide-base-300 flex flex-col">
          <!-- Basic Information -->
          <div class="p-6 md:p-8">
            <h2
              class="text-lg font-bold font-mono text-base-content/90 mb-6 uppercase tracking-wider text-xs"
            >
              1. Basic Information
            </h2>
            <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
              <!-- Title -->
              <div class="sm:col-span-2">
                <label for="title" class="label"
                  ><span
                    class="label-text font-mono text-xs text-base-content/60 uppercase tracking-wider"
                    >Issue Title *</span
                  ></label
                >
                <input
                  id="title"
                  v-model="formData.title"
                  type="text"
                  required
                  placeholder="Brief description of the issue"
                  class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary focus:ring-1 focus:ring-primary transition-all font-sans"
                />
              </div>

              <!-- Issue Type -->
              <div class="sm:col-span-2 md:col-span-1">
                <label for="issueType" class="label"
                  ><span
                    class="label-text font-mono text-xs text-base-content/60 uppercase tracking-wider"
                    >Issue Type</span
                  ></label
                >
                <select
                  id="issueType"
                  v-model="formData.issueType"
                  class="select select-bordered w-full rounded-xl border-base-300 focus:border-primary focus:ring-1 focus:ring-primary transition-all font-mono text-xs"
                >
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
                <label for="description" class="label"
                  ><span
                    class="label-text font-mono text-xs text-base-content/60 uppercase tracking-wider"
                    >Description *</span
                  ></label
                >
                <textarea
                  id="description"
                  v-model="formData.description"
                  required
                  rows="4"
                  placeholder="Detailed description of the issue..."
                  class="textarea textarea-bordered w-full rounded-xl border-base-300 focus:border-primary focus:ring-1 focus:ring-primary transition-all font-sans"
                ></textarea>
              </div>
            </div>
          </div>

          <!-- Location -->
          <div class="p-6 md:p-8 bg-base-200/50">
            <h2
              class="text-lg font-bold font-mono text-base-content/90 mb-6 uppercase tracking-wider text-xs"
            >
              2. Location Capture
            </h2>
            <LocationSelector v-model="formData.location" :auto-locate="true" />
          </div>

          <!-- Media -->
          <div class="p-6 md:p-8">
            <h2
              class="text-lg font-bold font-mono text-base-content/90 mb-6 uppercase tracking-wider text-xs"
            >
              3. Attach Media Evidence
            </h2>

            <!-- Images -->
            <div class="mb-8">
              <label class="label"
                ><span class="label-text font-mono text-xs text-base-content/60 uppercase tracking-wider"
                  >Images (At least one required) *</span
                ></label
              >

              <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 mb-4">
                <input
                  ref="imageInput"
                  type="file"
                  multiple
                  accept="image/*"
                  @change="handleImageUpload"
                  class="file-input file-input-bordered file-input-primary w-full rounded-xl"
                />
                <button
                  type="button"
                  @click="showPhotoModal = true"
                  class="btn btn-accent rounded-xl flex items-center justify-center gap-2 cursor-pointer font-bold px-5"
                >
                  <svg
                    class="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"
                    />
                    <circle cx="12" cy="13" r="3" />
                  </svg>
                  Take Photo
                </button>
              </div>

              <!-- Image Previews -->
              <div
                v-if="imagePreviews.length > 0"
                class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-4 mt-4"
              >
                <div
                  v-for="(preview, index) in imagePreviews"
                  :key="index"
                  class="relative group aspect-square rounded-xl overflow-hidden border border-base-300"
                >
                  <img :src="preview" alt="Preview" class="w-full h-full object-cover" />
                  <button
                    type="button"
                    @click="removeImage(index)"
                    class="absolute top-1.5 right-1.5 bg-red-500 hover:bg-red-600 text-white rounded-full w-6 h-6 flex items-center justify-center transition-colors shadow-lg cursor-pointer font-bold"
                  >
                    ×
                  </button>
                </div>
              </div>
            </div>

            <!-- Voice Note -->
            <div class="mb-8">
              <label class="label"
                ><span class="label-text font-mono text-xs text-base-content/60 uppercase tracking-wider"
                  >Voice Note (optional)</span
                ></label
              >

              <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 mb-4">
                <input
                  type="file"
                  accept="audio/*"
                  @change="handleVoiceNoteUpload"
                  class="file-input file-input-bordered file-input-secondary w-full rounded-xl"
                />
                <button
                  type="button"
                  @click="showAudioModal = true"
                  class="btn btn-secondary rounded-xl flex items-center justify-center gap-2 cursor-pointer font-bold px-5"
                >
                  <svg
                    class="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
                    />
                  </svg>
                  Record Audio
                </button>
              </div>

              <!-- Voice Note Preview -->
              <div
                v-if="formData.voiceNote"
                class="bg-base-100 border border-base-300 p-4 rounded-xl mt-2"
              >
                <div class="flex items-center justify-between">
                  <div class="flex items-center font-mono text-xs text-base-content/80">
                    <svg
                      class="w-5 h-5 text-secondary mr-2"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
                      />
                    </svg>
                    <span class="truncate">{{ formData.voiceNote.name }}</span>
                  </div>
                  <button
                    type="button"
                    @click="formData.voiceNote = null"
                    class="text-error hover:text-red-400 cursor-pointer"
                  >
                    <svg
                      class="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Video Note -->
            <div>
              <label class="label"
                ><span class="label-text font-mono text-xs text-base-content/60 uppercase tracking-wider"
                  >Video Note (optional)</span
                ></label
              >

              <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 mb-4">
                <input
                  type="file"
                  accept="video/*"
                  @change="handleVideoNoteUpload"
                  class="file-input file-input-bordered file-input-primary w-full rounded-xl"
                />
                <button
                  type="button"
                  @click="showVideoModal = true"
                  class="btn btn-primary rounded-xl flex items-center justify-center gap-2 cursor-pointer font-bold px-5"
                >
                  <svg
                    class="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
                    />
                  </svg>
                  Record Video
                </button>
              </div>

              <!-- Video Note Preview -->
              <div
                v-if="formData.videoNote"
                class="bg-base-100 border border-base-300 p-4 rounded-xl mt-2"
              >
                <div class="flex items-center justify-between">
                  <div class="flex items-center font-mono text-xs text-base-content/80">
                    <svg
                      class="w-5 h-5 text-primary mr-2"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
                      />
                    </svg>
                    <span class="truncate">{{ formData.videoNote.name }}</span>
                  </div>
                  <button
                    type="button"
                    @click="formData.videoNote = null"
                    class="text-error hover:text-red-400 cursor-pointer"
                  >
                    <svg
                      class="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Submit -->
          <div class="p-6 md:p-8 bg-base-200/80 sticky bottom-0 z-10 border-t border-base-300">
            <div class="flex flex-col sm:flex-row sm:justify-end gap-3">
              <router-link to="/issues" class="btn btn-ghost rounded-xl cursor-pointer">
                Cancel
              </router-link>
              <button
                type="submit"
                :disabled="loading || !isFormValid"
                class="btn btn-primary rounded-xl cursor-pointer font-bold px-8 shadow-lg shadow-blue-500/10"
              >
                <span v-if="loading" class="flex items-center gap-2">
                  <svg
                    class="animate-spin h-5 w-5 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      class="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      stroke-width="4"
                    ></circle>
                    <path
                      class="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  SUBMITTING...
                </span>
                <span v-else>SUBMIT INCIDENT REPORT</span>
              </button>
            </div>
          </div>
        </form>
      </div>

      <div
        v-if="error"
        class="border border-error/20 bg-error/5 text-error text-center text-xs font-mono p-4 rounded-xl mt-6"
      >
        {{ error }}
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
import LocationSelector from '../components/issue/Location-Selector.vue'
import PhotoCaptureModal from '../components/issue/Photo-Capture-Modal.vue'
import VideoCaptureModal from '../components/issue/Video-Capture-Modal.vue'
import AudioCaptureModal from '../components/issue/Audio-Capture-Modal.vue'
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
  videoNote: null,
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
  return (
    formData.value.title.trim() &&
    formData.value.description.trim() &&
    formData.value.location &&
    formData.value.images.length > 0
  )
})

// Methods
const handleImageUpload = (event) => {
  const files = Array.from(event.target.files || [])

  // Validate file sizes
  const maxSize = 15 * 1024 * 1024 // 15MB
  const invalidFiles = files.filter((file) => file.size > maxSize)

  if (invalidFiles.length > 0) {
    error.value = 'Some images are too large. Maximum size is 15MB per image.'
    return
  }

  formData.value.images = files

  // Create previews
  imagePreviews.value = []
  files.forEach((file) => {
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
    formData.value.images.forEach((file) => dt.items.add(file))
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

    const response = await axios.post('/issues/report', formDataToSend)

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

