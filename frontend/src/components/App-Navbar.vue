<template>
  <nav class="bg-white shadow">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex">
          <div class="flex-shrink-0 flex items-center">
            <router-link to="/" class="text-xl font-bold text-gray-900 hover:text-gray-700">
              CityPulse
            </router-link>
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <router-link to="/" :class="[
            'px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200',
            $route.name === 'Dashboard'
              ? 'bg-indigo-100 text-indigo-700'
              : 'text-gray-700 hover:text-gray-900 hover:bg-gray-100'
          ]">
            Dashboard
          </router-link>
          <router-link to="/issues" :class="[
            'px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200',
            $route.name === 'Issues'
              ? 'bg-indigo-100 text-indigo-700'
              : 'text-gray-700 hover:text-gray-900 hover:bg-gray-100'
          ]">
            Issues
          </router-link>
          <router-link to="/profile" :class="[
            'px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200',
            $route.name === 'Profile'
              ? 'bg-indigo-100 text-indigo-700'
              : 'text-gray-700 hover:text-gray-900 hover:bg-gray-100'
          ]">
            Profile
          </router-link>
          <button @click="handleLogout"
            class="bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200">
            Logout
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
/* Additional styles if needed */
</style>
