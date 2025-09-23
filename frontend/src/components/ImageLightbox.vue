<template>
    <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75"
        @click="close">
        <div class="relative max-w-4xl max-h-full p-4">
            <!-- Close button -->
            <button @click="close" class="absolute top-2 right-2 z-10 btn btn-circle btn-ghost text-white">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>

            <!-- Image -->
            <img :src="currentImage" alt="Lightbox image" class="max-w-full max-h-full object-contain rounded-lg" />

            <!-- Navigation buttons -->
            <button v-if="images.length > 1" @click.stop="prev"
                class="absolute left-2 top-1/2 transform -translate-y-1/2 btn btn-circle btn-ghost text-white">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
            </button>

            <button v-if="images.length > 1" @click.stop="next"
                class="absolute right-2 top-1/2 transform -translate-y-1/2 btn btn-circle btn-ghost text-white">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
            </button>

            <!-- Image counter -->
            <div v-if="images.length > 1"
                class="absolute bottom-4 left-1/2 transform -translate-x-1/2 text-white text-sm">
                {{ currentIndex + 1 }} / {{ images.length }}
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
    visible: {
        type: Boolean,
        default: false
    },
    images: {
        type: Array,
        default: () => []
    },
    index: {
        type: Number,
        default: 0
    }
})

const emit = defineEmits(['close'])

const currentIndex = ref(props.index)
const currentImage = ref('')

const close = () => {
    emit('close')
}

const next = () => {
    currentIndex.value = (currentIndex.value + 1) % props.images.length
}

const prev = () => {
    currentIndex.value = currentIndex.value === 0 ? props.images.length - 1 : currentIndex.value - 1
}

watch(() => props.index, (newIndex) => {
    currentIndex.value = newIndex
})

watch(() => props.images, (newImages) => {
    if (newImages.length > 0) {
        currentImage.value = newImages[currentIndex.value]
    }
}, { immediate: true })

watch(currentIndex, (newIndex) => {
    if (props.images.length > 0) {
        currentImage.value = props.images[newIndex]
    }
})
</script>
