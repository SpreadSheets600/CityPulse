<template>
  <!-- Main modal -->
  <div
    :class="['fixed inset-0 z-50', { 'flex sm:items-center sm:justify-center': isOpen }]"
    tabindex="-1"
    :aria-hidden="!isOpen"
    v-if="isOpen"
  >
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-black/60 backdrop-blur-sm" @click="closeModal"></div>

    <!-- Modal content -->
    <div
      class="relative bg-base-200 border border-base-300 rounded-t-2xl sm:rounded-2xl shadow-2xl w-full sm:max-w-2xl sm:mx-4 sm:my-6 h-[100dvh] sm:h-auto sm:max-h-[90vh] flex flex-col overflow-hidden text-base-content font-sans"
    >
      <!-- Modal header -->
      <div
        class="flex items-center justify-between p-4 md:p-5 border-b border-base-300 sticky top-0 bg-base-200 rounded-t-2xl sm:rounded-t"
      >
        <h3 class="text-lg font-bold text-slate-100 font-mono tracking-wider uppercase">
          Report New Issue
        </h3>
        <button
          type="button"
          class="text-slate-400 bg-transparent hover:bg-base-300 hover:text-slate-100 rounded-lg text-sm w-8 h-8 inline-flex justify-center items-center cursor-pointer"
          @click="closeModal"
        >
          <svg
            class="w-3.5 h-3.5"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 14 14"
          >
            <path
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
            />
          </svg>
          <span class="sr-only">Close modal</span>
        </button>
      </div>

      <!-- Modal body / form -->
      <form class="p-5 md:p-6 overflow-y-auto flex-1 space-y-4" @submit.prevent="submitIssue">
        <div class="grid gap-4 grid-cols-1 sm:grid-cols-2">
          <!-- Title (full width) -->
          <div class="col-span-2">
            <label for="title" class="label"
              ><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider"
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
          <div class="col-span-2">
            <label for="issueType" class="label"
              ><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider"
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

          <!-- Location selector (full width) -->
          <div class="col-span-2">
            <label class="label"
              ><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider"
                >Location</span
              ></label
            >
            <LocationSelector v-model="formData.location" />
          </div>

          <!-- Description (full) -->
          <div class="col-span-2">
            <label for="description" class="label"
              ><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider"
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

          <!-- Images (full) -->
          <div class="col-span-2">
            <label for="images" class="label"
              ><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider"
                >Images * (at least one required)</span
              ></label
            >

            <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 mb-3">
              <input
                id="images"
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
                title="Take Photo"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"
                  ></path>
                  <circle cx="12" cy="13" r="3" />
                </svg>
                <span class="ml-1">Take Photo</span>
              </button>
            </div>

            <div v-if="imagePreviews.length > 0" class="mt-4 grid grid-cols-3 sm:grid-cols-4 gap-4">
              <div
                v-for="(preview, index) in imagePreviews"
                :key="index"
                class="relative aspect-square rounded-xl overflow-hidden border border-base-300"
              >
                <img :src="preview" alt="Preview" class="w-full h-full object-cover" />
                <button
                  type="button"
                  @click="removeImage(index)"
                  class="absolute top-1 right-1 bg-red-500 hover:bg-red-600 text-white rounded-full w-6 h-6 flex items-center justify-center transition-colors cursor-pointer font-bold"
                >
                  ×
                </button>
              </div>
            </div>
          </div>

          <!-- Voice Note -->
          <div class="col-span-2 sm:col-span-1">
            <label for="voiceNote" class="label"
              ><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider"
                >Voice Note (optional)</span
              ></label
            >

            <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 mb-3">
              <input
                id="voiceNote"
                type="file"
                accept="audio/*"
                @change="handleVoiceNoteUpload"
                class="file-input file-input-bordered file-input-secondary w-full rounded-xl"
              />
              <button
                type="button"
                @click="showAudioModal = true"
                class="btn btn-secondary rounded-xl flex items-center justify-center gap-2 cursor-pointer font-bold px-5"
                title="Record Audio"
              >
                <svg
                  v-if="isRecordingAudio"
                  class="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <rect x="6" y="4" width="4" height="16"></rect>
                  <rect x="14" y="4" width="4" height="16"></rect>
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
                  ></path>
                </svg>
                <span class="ml-1">Record</span>
              </button>
            </div>

            <div
              v-if="formData.voiceNote"
              class="mt-2 p-3 bg-base-100 border border-base-300 rounded-xl"
            >
              <div class="flex items-center gap-2 text-xs font-mono text-slate-300">
                <svg
                  class="w-5 h-5 text-secondary"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
                  ></path>
                </svg>
                <span class="truncate">{{ formData.voiceNote.name }}</span>
                <button
                  type="button"
                  @click="formData.voiceNote = null"
                  class="text-error ml-auto cursor-pointer"
                >
                  <svg
                    class="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Video Note -->
          <div class="col-span-2 sm:col-span-1">
            <label for="videoNote" class="label"
              ><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider"
                >Video Note (optional)</span
              ></label
            >

            <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 mb-3">
              <input
                id="videoNote"
                type="file"
                accept="video/*"
                @change="handleVideoNoteUpload"
                class="file-input file-input-bordered file-input-primary w-full rounded-xl"
              />
              <button
                type="button"
                @click="showVideoModal = true"
                class="btn btn-primary rounded-xl flex items-center justify-center gap-2 cursor-pointer font-bold px-5"
                title="Record Video"
              >
                <svg
                  v-if="isRecordingVideo"
                  class="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <rect x="6" y="4" width="4" height="16"></rect>
                  <rect x="14" y="4" width="4" height="16"></rect>
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
                  ></path>
                </svg>
                <span class="ml-1">Record</span>
              </button>
            </div>

            <div
              v-if="formData.videoNote"
              class="mt-2 p-3 bg-base-100 border border-base-300 rounded-xl"
            >
              <div class="flex items-center gap-2 text-xs font-mono text-slate-300">
                <svg
                  class="w-5 h-5 text-primary"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
                  ></path>
                </svg>
                <span class="truncate">{{ formData.videoNote.name }}</span>
                <button
                  type="button"
                  @click="formData.videoNote = null"
                  class="text-error ml-auto cursor-pointer"
                >
                  <svg
                    class="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div
          class="flex flex-col sm:flex-row justify-end gap-2 sm:gap-4 sticky bottom-0 bg-base-200 p-4 border-t border-base-300 rounded-b-2xl sm:rounded-b"
        >
          <button
            type="button"
            @click="closeModal"
            class="btn order-2 sm:order-1 rounded-xl cursor-pointer"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="loading || !isFormValid"
            class="btn btn-primary order-1 sm:order-2 inline-flex items-center justify-center rounded-xl cursor-pointer font-bold px-6 shadow-lg shadow-blue-500/10"
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
            <span v-else>Report Issue</span>
          </button>
        </div>

        <div
          v-if="error"
          class="border border-error/20 bg-error/5 text-error text-center text-xs font-mono p-3 rounded-xl mt-4"
        >
          {{ error }}
        </div>
      </form>
    </div>
  </div>

  <!-- Media Capture Modals -->
  <PhotoCaptureModal v-model="showPhotoModal" @capture="addCapturedImage" />
  <VideoCaptureModal v-model="showVideoModal" @capture="formData.videoNote = $event" />
  <AudioCaptureModal v-model="showAudioModal" @capture="formData.voiceNote = $event" />
</template>

<script setup>
import { ref, computed } from 'vue'

import LocationSelector from './Location-Selector.vue'
import PhotoCaptureModal from './Photo-Capture-Modal.vue'
import VideoCaptureModal from './Video-Capture-Modal.vue'
import AudioCaptureModal from './Audio-Capture-Modal.vue'
import axios from '../api/client'

const props = defineProps({
  modelValue: Boolean,
})

const emit = defineEmits(['update:modelValue', 'cancel', 'success'])

// Modal state
const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
})

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

// Media capture state
// Modal states
const showPhotoModal = ref(false)
const showVideoModal = ref(false)
const showAudioModal = ref(false)
// Icon state used in template (kept simple; modals manage actual recording)
const isRecordingAudio = ref(false)
const isRecordingVideo = ref(false)

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

// Media capture functions
const addCapturedImage = (file) => {
  formData.value.images.push(file)

  // Create preview
  const reader = new FileReader()
  reader.onload = (e) => {
    imagePreviews.value.push(e.target.result)
  }
  reader.readAsDataURL(file)
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
    videoNote: null,
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
/* Improve safe-area on iOS */
@supports (padding: max(0px)) {
  .p-safe-b {
    padding-bottom: max(env(safe-area-inset-bottom), 1rem);
  }
}
</style>
