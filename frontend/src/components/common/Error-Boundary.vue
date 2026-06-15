<template>
  <div v-if="error" class="flex flex-col items-center justify-center min-h-[50vh] p-8 text-center">
    <div class="alert alert-error max-w-md">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6 shrink-0 stroke-current"
        fill="none"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      <div>
        <h3 class="font-bold">Something Went Wrong</h3>
        <p class="text-sm opacity-80">{{ error.message }}</p>
      </div>
    </div>
    <button class="btn btn-outline btn-sm mt-4" @click="retry">Try Again</button>
  </div>
  <slot v-else />
</template>

<script setup>
import { ref, onErrorCaptured } from 'vue'

const error = ref(null)

onErrorCaptured((err) => {
  error.value = err
  return false
})

function retry() {
  error.value = null
}
</script>
