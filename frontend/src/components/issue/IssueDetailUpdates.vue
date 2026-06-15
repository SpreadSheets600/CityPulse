<template>
  <div class="border-t border-base-300 p-6 md:p-8">
    <h3 class="font-mono text-xs font-bold uppercase tracking-wider text-base-content/60 mb-4">
      Updates Feed
    </h3>
    <div v-if="updates.length === 0" class="text-sm font-mono text-base-content/40">
      No updates uploaded yet.
    </div>
    <div v-else class="space-y-4">
      <div
        v-for="u in updates"
        :key="u.id"
        class="bg-base-100/50 border border-base-300 rounded-2xl p-5 shadow-inner"
      >
        <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start mb-3 gap-2">
          <h4 class="font-bold text-base-content text-base">{{ u.title }}</h4>
          <span class="text-xs font-mono text-base-content/40 flex items-center">
            <svg
              class="w-3.5 h-3.5 mr-1.5"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            {{ formatDate(u.created_at) }}
          </span>
        </div>
        <p class="text-sm text-base-content/80 mb-4 font-sans leading-relaxed">{{ u.body }}</p>
        <div class="mb-4">
          <div class="flex justify-between text-xs font-mono text-base-content/60 mb-1">
            <span>Task Completion Progress</span>
            <span>{{ u.progress }}%</span>
          </div>
          <div class="w-full bg-base-300 rounded-full h-2">
            <div
              class="bg-primary h-2 rounded-full transition-all duration-500"
              :style="{ width: (u.progress || 0) + '%' }"
            ></div>
          </div>
        </div>
        <div v-if="u.image_urls && u.image_urls.length > 0">
          <h5
            class="text-xs font-mono font-bold text-base-content/40 mb-3 uppercase tracking-wider"
          >
            Update Attachments
          </h5>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
            <img
              v-for="(url, index) in u.image_urls"
              :key="index"
              :src="url"
              :alt="`Update image ${index + 1}`"
              class="w-full h-24 object-cover rounded-xl cursor-pointer hover:opacity-85 border border-base-300 transition-opacity"
              @click="$emit('open-image', { url, images: u.image_urls })"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  updates: {
    type: Array,
    required: true,
  },
})

defineEmits(['open-image'])

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>
