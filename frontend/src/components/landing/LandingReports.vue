<template>
  <section id="reports" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 border-t border-base-300/20">
    <div class="flex items-end justify-between mb-12 gap-4">
      <div>
        <span
          class="inline-flex items-center gap-2 text-xs font-bold tracking-widest text-secondary uppercase bg-secondary/8 px-4 py-1.5 rounded-full mb-4 border border-secondary/10"
        >
          <span class="relative flex h-1.5 w-1.5">
            <span
              class="animate-ping absolute inline-flex h-full w-full rounded-full bg-secondary opacity-75"
            ></span>
            <span class="relative inline-flex rounded-full h-1.5 w-1.5 bg-secondary"></span>
          </span>
          Real-time
        </span>
        <h2 class="text-3xl sm:text-4xl font-black tracking-tight text-base-content">
          Live Nearby Reports
        </h2>
      </div>
      <router-link
        to="/login"
        class="hidden sm:inline-flex items-center gap-1.5 text-sm font-bold text-primary hover:text-primary/80 transition-colors shrink-0 group"
      >
        View all
        <svg
          class="w-4 h-4 group-hover:translate-x-0.5 transition-transform"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2.5"
            d="M9 5l7 7-7 7"
          />
        </svg>
      </router-link>
    </div>

    <div
      class="flex gap-5 overflow-x-auto snap-x snap-mandatory pb-4 -mx-2 px-2 scrollbar-thin scrollbar-thumb-base-300 scrollbar-track-transparent"
    >
      <article
        v-for="issue in issues"
        :key="issue.id"
        class="snap-start min-w-[320px] w-[320px] rounded-[1.5rem] overflow-hidden bg-base-200/40 glass-card hover-lift group cursor-pointer border border-base-content/5 hover:border-secondary/30 transition-all duration-300"
      >
        <figure class="relative h-44 overflow-hidden">
          <img
            v-if="issue.image_urls?.length && !brokenImages.includes(issue.id)"
            :src="issue.image_urls[0]"
            :alt="issue.title"
            class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
            @error="emit('imageError', issue.id)"
          />
          <div v-else class="w-full h-full bg-base-300/30 flex items-center justify-center">
            <ImageIcon class="w-10 h-10 text-base-content/25" :stroke-width="1.5" />
          </div>
          <div
            class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent"
          />
          <span
            class="absolute top-3.5 right-3.5 badge badge-sm uppercase font-bold tracking-wider py-2 px-2.5 shadow-lg border-0"
            :class="{
              'badge-warning text-warning-content': issue.status === 'pending',
              'badge-info text-info-content': issue.status === 'in_progress',
              'badge-success text-success-content':
                issue.status === 'resolved' || issue.status === 'verified',
              'badge-error text-error-content': issue.status === 'rejected',
            }"
          >
            {{ issue.status }}
          </span>
        </figure>
        <div class="p-5">
          <h3
            class="font-bold text-[15px] text-base-content line-clamp-1 group-hover:text-primary transition-colors"
          >
            {{ issue.title }}
          </h3>
          <p class="text-xs text-base-content/50 line-clamp-2 leading-relaxed mt-2 h-8">
            {{ issue.description }}
          </p>
          <div
            class="flex items-center justify-between text-xs text-base-content/30 mt-4 pt-3.5 border-t border-base-content/5"
          >
            <span class="inline-flex items-center gap-1.5 font-medium">
              <MapPin class="w-3 h-3 text-primary" :stroke-width="2.5" />
              {{ issue.address?.split(',')[0] || 'Nearby' }}
            </span>
            <span class="font-medium">{{ timeAgo(issue.created_at) }}</span>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup>
import { ImageIcon, MapPin } from '@lucide/vue'

defineProps({
  issues: {
    type: Array,
    required: true,
  },
  brokenImages: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['imageError'])

const timeAgo = (dateString) => {
  const diffInMs = Date.now() - new Date(dateString).getTime()
  const hours = Math.floor(diffInMs / 3600000)
  if (hours < 1) return 'Just now'
  if (hours < 24) return `${hours}h ago`
  return `${Math.floor(hours / 24)}d ago`
}
</script>
