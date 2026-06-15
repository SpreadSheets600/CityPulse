<template>
  <div
    v-if="issue.image_urls?.length > 0 || issue.voice_note_url || issue.video_note_url"
    class="border-t border-base-300 p-6 md:p-8 bg-base-200/30"
  >
    <h3 class="font-mono text-xs font-bold uppercase tracking-wider text-base-content/60 mb-6">
      Attached Media
    </h3>
    <div class="space-y-6">
      <div v-if="issue.image_urls && issue.image_urls.length > 0">
        <h4
          class="text-xs font-mono font-bold text-base-content/40 mb-3 flex items-center uppercase tracking-wider"
        >
          <svg
            class="w-4 h-4 mr-2 text-base-content/40"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
            />
          </svg>
          Images ({{ issue.image_urls.length }})
        </h4>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <img
            v-for="(url, index) in issue.image_urls"
            :key="index"
            :src="url"
            :alt="`Image ${index + 1}`"
            class="w-full h-48 object-cover rounded-2xl cursor-pointer hover:opacity-85 hover:scale-[1.02] border border-base-300 transition-all shadow-md"
            @click="$emit('open-image', { url, images: issue.image_urls })"
          />
        </div>
      </div>

      <div v-if="issue.voice_note_url">
        <h4
          class="text-xs font-mono font-bold text-base-content/40 mb-3 flex items-center uppercase tracking-wider"
        >
          <svg
            class="w-4 h-4 mr-2 text-base-content/40"
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
          Voice Note
        </h4>
        <audio controls :src="issue.voice_note_url" class="w-full rounded-xl"></audio>
      </div>

      <div v-if="issue.video_note_url">
        <h4
          class="text-xs font-mono font-bold text-base-content/40 mb-3 flex items-center uppercase tracking-wider"
        >
          <svg
            class="w-4 h-4 mr-2 text-base-content/40"
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
          Video Note
        </h4>
        <video
          controls
          :src="issue.video_note_url"
          class="w-full max-w-md rounded-2xl border border-base-300 shadow-md bg-black"
        ></video>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  issue: {
    type: Object,
    required: true,
  },
})

defineEmits(['open-image'])
</script>
