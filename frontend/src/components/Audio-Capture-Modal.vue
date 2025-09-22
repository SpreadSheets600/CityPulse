<template>
    <div v-if="isOpen" class="fixed inset-0 z-[10000] overflow-y-auto" @keydown.esc="closeModal">
        <!-- Backdrop -->
        <div class="fixed inset-0 bg-black/60" @click="closeModal"></div>

        <!-- Modal -->
        <div class="flex items-center justify-center min-h-screen p-4">
            <div class="relative bg-white rounded-lg shadow-xl max-w-md w-full">
                <!-- Header -->
                <div class="flex items-center justify-between p-4 border-b border-gray-200">
                    <h3 class="text-lg font-semibold text-gray-900">Record Audio</h3>
                    <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>

                <!-- Audio Recorder -->
                <div class="p-4">
                    <div class="text-center py-8">
                        <div class="mb-6">
                            <svg class="mx-auto h-16 w-16 text-gray-400" fill="none" stroke="currentColor"
                                viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z">
                                </path>
                            </svg>
                        </div>

                        <!-- Recording Status -->
                        <div v-if="isRecording" class="mb-6">
                            <div class="flex items-center justify-center mb-4">
                                <div class="w-4 h-4 bg-red-500 rounded-full animate-pulse mr-3"></div>
                                <span class="text-lg font-medium text-gray-900">Recording... {{ recordingTime }}</span>
                            </div>

                            <!-- Audio Visualization -->
                            <div class="flex items-end justify-center space-x-1 h-16 mb-4">
                                <div v-for="bar in audioBars" :key="bar.id" :style="{ height: bar.height + 'px' }"
                                    class="w-2 bg-blue-500 rounded-full transition-all duration-100"></div>
                            </div>

                            <button @click="stopRecording"
                                class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-red-600 hover:bg-red-700">
                                <svg class="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 24 24">
                                    <rect x="6" y="4" width="4" height="16"></rect>
                                    <rect x="14" y="4" width="4" height="16"></rect>
                                </svg>
                                Stop Recording
                            </button>
                        </div>

                        <!-- Start Recording -->
                        <div v-else>
                            <p class="text-gray-500 mb-6">Click the button below to start recording</p>
                            <button @click="startRecording" :disabled="loading"
                                class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50">
                                <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5" fill="none"
                                    viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                        stroke-width="4"></circle>
                                    <path class="opacity-75" fill="currentColor"
                                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                    </path>
                                </svg>
                                <svg v-else class="w-6 h-6 mr-2" fill="currentColor" viewBox="0 0 24 24">
                                    <circle cx="12" cy="12" r="10"></circle>
                                </svg>
                                <span v-if="loading">Starting...</span>
                                <span v-else>Start Recording</span>
                            </button>
                        </div>
                    </div>

                    <!-- Controls -->
                    <div class="flex justify-center">
                        <button @click="closeModal"
                            class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                            Cancel
                        </button>
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
import { ref, watch, onUnmounted } from 'vue'

const props = defineProps({
    modelValue: Boolean
})

const emit = defineEmits(['update:modelValue', 'capture'])

const isOpen = ref(false)
const stream = ref(null)
const mediaRecorder = ref(null)
const recordedChunks = ref([])
const loading = ref(false)
const isRecording = ref(false)
const error = ref('')
const recordingTime = ref('00:00')
const recordingInterval = ref(null)
const audioBars = ref([])
const animationFrame = ref(null)

// Watch for modal state changes
watch(() => props.modelValue, (newValue) => {
    isOpen.value = newValue
    if (newValue) {
        // Reset state when opening
        error.value = ''
        stream.value = null
        isRecording.value = false
        recordingTime.value = '00:00'
        audioBars.value = Array.from({ length: 20 }, (_, i) => ({ id: i, height: 4 }))
    } else {
        // Clean up when closing
        stopRecording()
    }
})

watch(isOpen, (newValue) => {
    emit('update:modelValue', newValue)
})

const startRecording = async () => {
    loading.value = true
    error.value = ''

    try {
        const constraints = { audio: true }
        stream.value = await navigator.mediaDevices.getUserMedia(constraints)

        recordedChunks.value = []
        mediaRecorder.value = new MediaRecorder(stream.value)

        mediaRecorder.value.ondataavailable = (event) => {
            if (event.data.size > 0) {
                recordedChunks.value.push(event.data)
            }
        }

        mediaRecorder.value.onstop = () => {
            const blob = new Blob(recordedChunks.value, { type: 'audio/webm' })
            const file = new File([blob], `audio_${Date.now()}.webm`, { type: 'audio/webm' })
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

        // Start audio visualization
        startVisualization()

    } catch (err) {
        console.error('Recording error:', err)
        if (err.name === 'NotAllowedError') {
            error.value = 'Microphone access denied. Please allow microphone permissions and try again.'
        } else if (err.name === 'NotFoundError') {
            error.value = 'No microphone found on this device.'
        } else {
            error.value = 'Unable to access microphone. Please check your microphone settings.'
        }
    } finally {
        loading.value = false
    }
}

const stopRecording = () => {
    if (animationFrame.value) {
        cancelAnimationFrame(animationFrame.value)
        animationFrame.value = null
    }

    if (recordingInterval.value) {
        clearInterval(recordingInterval.value)
        recordingInterval.value = null
    }

    if (mediaRecorder.value && mediaRecorder.value.state === 'recording') {
        mediaRecorder.value.stop()
        isRecording.value = false
    }

    if (stream.value) {
        stream.value.getTracks().forEach(track => track.stop())
        stream.value = null
    }
}

const startVisualization = () => {
    if (!stream.value) return

    const audioContext = new (window.AudioContext || window.webkitAudioContext)()
    const analyser = audioContext.createAnalyser()
    const microphone = audioContext.createMediaStreamSource(stream.value)

    analyser.fftSize = 256
    const bufferLength = analyser.frequencyBinCount
    const dataArray = new Uint8Array(bufferLength)

    microphone.connect(analyser)

    const updateVisualization = () => {
        analyser.getByteFrequencyData(dataArray)

        // Update audio bars
        audioBars.value = audioBars.value.map((bar, index) => {
            const value = dataArray[index * 2] || 0
            const height = Math.max(4, (value / 255) * 60) // Min 4px, max 60px
            return { ...bar, height }
        })

        if (isRecording.value) {
            animationFrame.value = requestAnimationFrame(updateVisualization)
        }
    }

    updateVisualization()
}

const closeModal = () => {
    stopRecording()
    isOpen.value = false
}

onUnmounted(() => {
    stopRecording()
})
</script>
