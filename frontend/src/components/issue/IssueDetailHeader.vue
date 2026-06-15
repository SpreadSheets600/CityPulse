<template>
  <div class="p-6 md:p-8 border-b border-base-300">
    <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
      <div class="flex-1">
        <h1 class="text-2xl md:text-3xl font-extrabold text-base-content">
          {{ issue.title }}
        </h1>
        <div class="mt-3 flex flex-wrap items-center gap-4 text-xs font-mono text-base-content/60">
          <div class="flex items-center">
            <span class="text-base-content/40 mr-1.5 font-bold uppercase tracking-wider">Reported By:</span>
            <span class="text-base-content/80 font-semibold">
              {{ issue.user?.firstname }} {{ issue.user?.lastname }}
            </span>
          </div>
          <div class="flex items-center">
            <span class="text-base-content/40 mr-1.5 font-bold uppercase tracking-wider">Created:</span>
            <span class="text-base-content/80">{{ formatDate(issue.created_at) }}</span>
          </div>
          <div v-if="issue.updated_at !== issue.created_at" class="flex items-center">
            <span class="text-base-content/40 mr-1.5 font-bold uppercase tracking-wider">Updated:</span>
            <span class="text-base-content/80">{{ formatDate(issue.updated_at) }}</span>
          </div>
        </div>
      </div>
      <div class="flex items-center gap-3">
        <span
          :class="getStatusClass(issue.status)"
          class="inline-flex items-center px-3 py-1 rounded-full text-2xs font-bold uppercase tracking-wide"
        >
          {{ issue.status }}
        </span>
        <button
          @click="$emit('toggle-upvote')"
          :class="[
            'btn btn-sm rounded-xl font-mono cursor-pointer',
            issue.user_upvoted
              ? 'btn-primary'
              : 'btn-outline border-base-300 hover:border-slate-500',
          ]"
        >
          <svg
            class="w-4 h-4 mr-1"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M5 15l7-7 7 7" />
          </svg>
          {{ issue.upvote_count || 0 }}
        </button>
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

defineEmits(['toggle-upvote'])

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

const getStatusClass = (status) => {
  const classes = {
    pending: 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20',
    in_progress: 'bg-blue-500/10 text-blue-400 border border-blue-500/20',
    resolved: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
    rejected: 'bg-red-500/10 text-red-400 border border-red-500/20',
    verified: 'bg-purple-500/10 text-purple-400 border border-purple-500/20',
  }
  return classes[status] || 'bg-slate-500/10 text-base-content/60 border border-slate-500/20'
}
</script>
