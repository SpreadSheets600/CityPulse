<template>
  <div class="space-y-3" v-if="loading">
    <template v-for="n in rows" :key="n">
      <div class="flex items-center gap-4">
        <div v-if="avatar" class="skeleton h-12 w-12 shrink-0 rounded-full"></div>
        <div class="flex-1 space-y-2">
          <div class="skeleton h-4 w-full" :style="{ width: widths[(n - 1) % widths.length] }"></div>
          <div v-if="lines > 1" class="skeleton h-4 w-3/4"></div>
        </div>
      </div>
    </template>
  </div>
  <slot v-else />
</template>

<script setup>
defineProps({
  loading: { type: Boolean, default: false },
  rows: { type: Number, default: 3 },
  lines: { type: Number, default: 2 },
  avatar: { type: Boolean, default: false },
  widths: { type: Array, default: () => ['100%', '85%', '90%', '75%'] },
})
</script>
