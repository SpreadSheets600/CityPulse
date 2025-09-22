<template>
    <div v-if="isOpen" class="fixed inset-0 z-[10000] overflow-y-auto" @keydown.esc="closeModal">
        <!-- Backdrop -->
        <div class="fixed inset-0 bg-black/60" @click="closeModal"></div>

        <!-- Modal -->
        <div class="flex items-center justify-center min-h-screen p-4">
            <div class="relative bg-white rounded-lg shadow-xl max-w-lg w-full">
                <!-- Header -->
                <div class="flex items-center justify-between p-4 border-b border-gray-200">
                    <h3 class="text-lg font-semibold text-gray-900">Record Video</h3>
                    <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>

                <!-- Video Recorder -->
                <div class="p-4">
                    <div v-if="!stream" class="text-center py-8">
                        <div class="mb-4">
                            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor"
                                viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z">
                                </path>
                            </svg>
                        </div>
                        <p class="text-gray-500 mb-4">Camera and microphone access required</p>
                        <button @click="startRecording" :disabled="loading"
                            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50">
                            <span v-if="loading">Starting Camera...</span>
                            <span v-else>Start Recording</span>
                        </button>
                    </div>

                    <div v-else class="space-y-4">
                        <!-- Video Preview -->
                        <div class="relative">
                            <video ref="videoElement" autoplay playsinline muted
                                class="w-full h-64 bg-black rounded-lg object-cover"></video>

                            <!-- Recording Indicator -->
                            <div v-if="isRecording" class="absolute top-4 left-4 flex items-center">
                                <div class="w-3 h-3 bg-red-500 rounded-full animate-pulse mr-2"></div>
                                <span class="text-white text-sm font-medium">REC {{ recordingTime }}</span>
                            </div>

                            <!-- Controls -->
                            <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-4">
                                <button v-if="!isRecording" @click="startRecording"
                                    class="bg-red-600 hover:bg-red-700 text-white rounded-full p-4 shadow-lg">
                                    <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
                                        <circle cx="12" cy="12" r="10"></circle>
                                    </svg>
                                </button>
                                <button v-else @click="stopRecording"
                                    class="bg-white hover:bg-gray-50 text-gray-700 rounded-full p-4 shadow-lg">
                                    <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
                                        <rect x="6" y="4" width="4" height="16"></rect>
                                        <rect x="14" y="4" width="4" height="16"></rect>
                                    </svg>
                                </button>
                            </div>
                        </div>

                        <!-- Recording Status -->
                        <div v-if="isRecording" class="text-center">
                            <p class="text-sm text-gray-600">Recording... Click stop when finished</p>
                        </div>

                        <!-- Controls -->
                        <div class="flex justify-between">
                            <button @click="switchCamera" v-if="hasMultipleCameras"
                                class="inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15">
                                    </path>
                                </svg>
                                Switch Camera
                            </button>
                            <button @click="closeModal"
                                class="inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                                Cancel
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Error Message -->
                <div v-if="error" class="px-4 pb-4">
                    <div class="bg-red-50 border border-red-200 rounded-md p-3">
                        <p class="text-sm text-red-800">{{ error }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, computed, onUnmounted } from 'vue'

const props = defineProps({
    modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'capture'])

const isOpen = ref(false)
const stream = ref(null)
const videoElement = ref(null)
const mediaRecorder = ref(null)
const recordedChunks = ref([])
const loading = ref(false)
const isRecording = ref(false)
const error = ref('')
const recordingTime = ref('00:00')
const recordingInterval = ref(null)
const currentCameraIndex = ref(0)
const availableCameras = ref([])
const isVideoReady = ref(false)
const selectedMimeType = ref('')

// Watch for modal state changes
watch(() => props.modelValue, async (newValue) => {
    isOpen.value = newValue
    if (newValue) {
        // Reset state when opening and auto-start camera
        error.value = ''
        stream.value = null
        isRecording.value = false
        recordingTime.value = '00:00'
        isVideoReady.value = false
        try {
            await startCamera()
        } catch {
            // error message handled within startCamera
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
        // Prefer deviceId if available; otherwise hint facingMode
        let videoConstraints
        if (availableCameras.value.length > 0) {
            const target = availableCameras.value[currentCameraIndex.value % availableCameras.value.length]
            videoConstraints = { deviceId: { exact: target.deviceId }, width: { ideal: 1280 }, height: { ideal: 720 } }
        } else {
            videoConstraints = { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } }
        }

        stream.value = await navigator.mediaDevices.getUserMedia({ video: videoConstraints, audio: true })

        // refresh device list with labels after permission
        try {
            const devices = await navigator.mediaDevices.enumerateDevices()
            availableCameras.value = devices.filter(d => d.kind === 'videoinput')
        } catch (e) {
            // Non-fatal: device enumeration can fail without affecting recording
            // console.debug('enumerateDevices failed', e)
            void e
        }

        if (videoElement.value) {
            videoElement.value.srcObject = stream.value
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
                videoElement.value.play?.().catch(() => { })
            })
        }
    } catch (err) {
        console.error('Camera error:', err)
        if (err?.name === 'NotAllowedError') {
            error.value = 'Camera and microphone access denied. Please allow permissions and try again.'
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

const pickSupportedMimeType = () => {
    const candidates = [
        'video/webm;codecs=vp9,opus',
        'video/webm;codecs=vp8,opus',
        'video/webm',
        'video/mp4;codecs=h264,aac',
        'video/mp4'
    ]
    for (const type of candidates) {
        if (window.MediaRecorder && MediaRecorder.isTypeSupported?.(type)) return type
    }
    return ''
}

const startRecording = async () => {
    if (!stream.value) {
        await startCamera()
        if (!stream.value) return
    }

    try {
        recordedChunks.value = []
        const type = pickSupportedMimeType()
        selectedMimeType.value = type || ''
        const options = type ? { mimeType: type } : undefined
        mediaRecorder.value = new MediaRecorder(stream.value, options)

        mediaRecorder.value.ondataavailable = (event) => {
            if (event.data.size > 0) {
                recordedChunks.value.push(event.data)
            }
        }

        mediaRecorder.value.onstop = () => {
            const fallbackType = selectedMimeType.value || 'video/webm'
            const blob = new Blob(recordedChunks.value, { type: fallbackType })
            // choose extension based on mime
            const ext = fallbackType.includes('mp4') ? 'mp4' : 'webm'
            const file = new File([blob], `video_${Date.now()}.${ext}`, { type: fallbackType })
            emit('capture', file)
            closeModal()
        }

        mediaRecorder.value.start()
        isRecording.value = true

        // Start recording timer
        let seconds = 0
        recordingInterval.value = setInterval(() => {
            seconds++
            const mins = Math.floor(seconds / 60).toString().padStart(2, '0')
            const secs = (seconds % 60).toString().padStart(2, '0')
            recordingTime.value = `${mins}:${secs}`
        }, 1000)

    } catch (err) {
        console.error('Recording error:', err)
        error.value = 'Failed to start recording. Please try again.'
    }
}

const stopRecording = () => {
    if (mediaRecorder.value && mediaRecorder.value.state === 'recording') {
        mediaRecorder.value.stop()
        isRecording.value = false

        if (recordingInterval.value) {
            clearInterval(recordingInterval.value)
            recordingInterval.value = null
        }
    }
}

const stopCamera = () => {
    if (recordingInterval.value) {
        clearInterval(recordingInterval.value)
        recordingInterval.value = null
    }

    if (mediaRecorder.value && mediaRecorder.value.state === 'recording') {
        mediaRecorder.value.stop()
    }

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

onUnmounted(() => {
    stopCamera()
})
</script>
