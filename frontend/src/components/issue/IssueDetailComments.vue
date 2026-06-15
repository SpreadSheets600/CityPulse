<template>
  <div class="border-t border-base-300 p-6 md:p-8 bg-base-200/40">
    <h3 class="font-mono text-xs font-bold uppercase tracking-wider text-base-content/60 mb-4">
      Comments ({{ comments.length }})
    </h3>
    <div v-if="comments.length === 0" class="text-sm font-mono text-base-content/40 mb-6">
      No public comments.
    </div>
    <div v-else class="space-y-4 mb-6">
      <div
        v-for="c in comments"
        :key="c.id"
        class="bg-base-100/40 border border-base-300 rounded-2xl p-4 shadow-sm"
      >
        <div
          class="flex items-center justify-between mb-2 gap-2 text-xs font-mono text-base-content/40"
        >
          <span class="font-bold text-base-content/80"
            >{{ c.author?.firstname }} {{ c.author?.lastname }}</span
          >
          <span>{{ formatDate(c.created_at) }}</span>
        </div>
        <p class="text-sm text-base-content/80 leading-relaxed font-sans">{{ c.body }}</p>
      </div>
    </div>

    <div class="flex flex-col sm:flex-row gap-3">
      <input
        v-model="commentText"
        type="text"
        placeholder="Add a comment..."
        class="input input-bordered flex-1 rounded-xl border-base-300 focus:border-primary focus:ring-1 focus:ring-primary transition-all font-sans text-sm"
        @keyup.enter="onSubmit"
      />
      <button
        @click="onSubmit"
        :disabled="!commentText.trim()"
        class="btn btn-primary rounded-xl cursor-pointer font-bold px-6"
      >
        Post Comment
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  comments: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['submit-comment'])

const commentText = ref('')

const onSubmit = () => {
  if (!commentText.value.trim()) return
  emit('submit-comment', commentText.value.trim())
  commentText.value = ''
}

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
