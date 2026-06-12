<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="text-center">
      <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6">
        <h2 class="text-lg font-medium text-red-800">Authentication Failed</h2>
        <p class="mt-2 text-sm text-red-600">{{ error }}</p>
        <router-link to="/login" class="mt-4 inline-block text-indigo-600 hover:underline">
          Back to Login
        </router-link>
      </div>
      <div v-else>
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto"></div>
        <p class="mt-4 text-base-content/60">Completing authentication...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import routerInstance from '../router'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const error = ref('')

onMounted(() => {
  const token = route?.query?.token || routerInstance.currentRoute.value?.query?.token
  if (token) {
    authStore.setToken(token)
    authStore
      .initializeAuth()
      .then(() => {
        router.push('/')
      })
      .catch(() => {
        error.value = 'Failed to load user profile.'
      })
  } else {
    error.value = 'No authentication token received.'
  }
})
</script>
