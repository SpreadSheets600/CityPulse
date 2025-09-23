<template>
  <div v-if="isOpen" class="fixed inset-0 z-[10000] overflow-y-auto" @keydown.esc="closeModal">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-base-300/60" @click="closeModal"></div>

    <!-- Modal -->
    <div class="flex items-center justify-center min-h-screen p-4">
      <div class="relative bg-base-100 rounded-lg shadow-xl max-w-md w-full">
        <!-- Header -->
        <div class="flex items-center justify-between p-4 border-b border-base-200">
          <h3 class="text-lg font-semibold">Take Photo</h3>
          <button @click="closeModal" class="btn btn-ghost btn-sm">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <!-- Camera Preview -->
        <div class="p-4">
          <div v-if="!stream" class="text-center py-8">
            <div class="mb-4">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z">
                </path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
            </div>
            <p class="opacity-60 mb-4">Camera access required</p>
            <button @click="startCamera" :disabled="loading" class="btn btn-primary">
              <span v-if="loading">Starting Camera...</span>
              <span v-else>Start Camera</span>
            </button>
          </div>

          <div v-else class="space-y-4">
            <!-- Video Preview -->
            <div class="relative">
              <video ref="videoElement" autoplay playsinline muted
                class="w-full h-64 bg-black rounded-lg object-cover"></video>
              <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2">
                <button @click="capturePhoto" :disabled="capturing" class="btn btn-circle">
                  <svg class="w-8 h-8 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z">
                    </path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Controls -->
            <div class="flex justify-between">
              <button @click="switchCamera" v-if="hasMultipleCameras" class="btn">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15">
                  </path>
                </svg>
                Switch Camera
              </button>
              <button @click="closeModal" class="btn">
                Cancel
              </button>
            </div>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="px-4 pb-4">
          <div class="alert alert-error">
            <span class="text-sm">{{ error }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'capture'])

const isOpen = ref(false)
const stream = ref(null)
const videoElement = ref(null)
const loading = ref(false)
const capturing = ref(false)
const error = ref('')
const currentCameraIndex = ref(0)
const availableCameras = ref([])
const isVideoReady = ref(false)

// Watch for modal state changes
watch(() => props.modelValue, async (newValue) => {
  isOpen.value = newValue
  if (newValue) {
    // Reset state when opening and auto-start camera for better UX
    error.value = ''
    isVideoReady.value = false
    stream.value = null
    try {
      await startCamera()
    } catch {
      // keep error message if set inside startCamera
    }
  } else {
    // Clean up when closing
    stopCamera()
  }
})

watch(isOpen, (newValue) => {
  emit('update:modelValue', newValue)
})

// Computed
const hasMultipleCameras = computed(() => availableCameras.value.length > 1)

const startCamera = async () => {
  loading.value = true
  error.value = ''
  isVideoReady.value = false

  try {
    // Build constraints: prefer deviceId if we already discovered cameras
    let videoConstraints
    if (availableCameras.value.length > 0) {
      const target = availableCameras.value[currentCameraIndex.value % availableCameras.value.length]
      videoConstraints = { deviceId: { exact: target.deviceId }, width: { ideal: 1280 }, height: { ideal: 720 } }
    } else {
      // Hint to use environment camera when possible (mobile). Desktop will choose default.
      videoConstraints = { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } }
    }

    stream.value = await navigator.mediaDevices.getUserMedia({ video: videoConstraints })

    // After permission, enumerate to get full device list with labels
    try {
      const devices = await navigator.mediaDevices.enumerateDevices()
      availableCameras.value = devices.filter(d => d.kind === 'videoinput')
    } catch {
      // Non-fatal
    }

    if (videoElement.value) {
      videoElement.value.srcObject = stream.value
      // Wait until metadata is loaded to ensure videoWidth/Height are available
      await new Promise((resolve) => {
        const onReady = () => {
          isVideoReady.value = true
          videoElement.value?.removeEventListener('loadedmetadata', onReady)
          resolve()
        }
        if (videoElement.value.readyState >= 1 && videoElement.value.videoWidth && videoElement.value.videoHeight) {
          isVideoReady.value = true
          resolve()
        } else {
          videoElement.value.addEventListener('loadedmetadata', onReady, { once: true })
        }
        // Also try to play to kick off rendering
        videoElement.value.play?.().catch(() => { })
      })
    }
  } catch (err) {
    console.error('Camera error:', err)
    if (err?.name === 'NotAllowedError') {
      error.value = 'Camera access denied. Please allow camera permissions and try again.'
    } else if (err?.name === 'NotFoundError' || err?.name === 'OverconstrainedError') {
      error.value = 'No suitable camera found on this device.'
    } else {
      error.value = 'Unable to access camera. Please check your camera settings.'
    }
    throw err
  } finally {
    loading.value = false
  }
}

const switchCamera = async () => {
  if (availableCameras.value.length <= 1) return

  stopCamera()
  currentCameraIndex.value = (currentCameraIndex.value + 1) % availableCameras.value.length
  await startCamera()
}

const capturePhoto = async () => {
  if (!stream.value || !videoElement.value) return
  if (!isVideoReady.value) {
    // Wait briefly in case metadata is still settling
    await new Promise(r => setTimeout(r, 100))
  }

  capturing.value = true

  try {
    const track = stream.value.getVideoTracks?.()[0]
    const settings = track?.getSettings?.() || {}
    const vw = videoElement.value.videoWidth || settings.width || 1280
    const vh = videoElement.value.videoHeight || settings.height || Math.round((vw * 9) / 16)

    const canvas = document.createElement('canvas')
    canvas.width = vw
    canvas.height = vh
    const ctx = canvas.getContext('2d')
    ctx.drawImage(videoElement.value, 0, 0, vw, vh)

    const makeFile = (blob) => {
      const safeBlob = blob instanceof Blob ? blob : new Blob([], { type: 'image/jpeg' })
      const file = new File([safeBlob], `photo_${Date.now()}.jpg`, { type: 'image/jpeg' })
      emit('capture', file)
      closeModal()
    }

    // Prefer toBlob but fall back to dataURL when null (Safari quirks)
    canvas.toBlob((blob) => {
      if (blob) return makeFile(blob)
      try {
        const dataUrl = canvas.toDataURL('image/jpeg', 0.8)
        const byteString = atob(dataUrl.split(',')[1])
        const ab = new ArrayBuffer(byteString.length)
        const ia = new Uint8Array(ab)
        for (let i = 0; i < byteString.length; i++) ia[i] = byteString.charCodeAt(i)
        makeFile(new Blob([ab], { type: 'image/jpeg' }))
      } catch (e) {
        console.error('toDataURL fallback failed', e)
        error.value = 'Failed to capture photo. Please try again.'
      }
    }, 'image/jpeg', 0.8)
  } catch (err) {
    console.error('Photo capture error:', err)
    error.value = 'Failed to capture photo. Please try again.'
  } finally {
    capturing.value = false
  }
}

const stopCamera = () => {
  if (stream.value) {
    stream.value.getTracks().forEach(track => track.stop())
    stream.value = null
  }
  isVideoReady.value = false
}

const closeModal = () => {
  stopCamera()
  isOpen.value = false
}
</script>
