<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Main content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="mb-8">
          <h2 class="text-2xl font-bold text-gray-900">Profile</h2>
          <p class="mt-1 text-sm text-gray-600">Manage your account information.</p>
        </div>

        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div class="flex items-center mb-6">
              <div class="flex-shrink-0">
                <img v-if="profilePictureUrl" :src="profilePictureUrl" alt="Profile"
                  class="w-16 h-16 rounded-full object-cover" />
                <div v-else
                  class="w-16 h-16 rounded-full bg-indigo-600 flex items-center justify-center text-white font-medium text-xl">
                  {{ userInitials }}
                </div>
              </div>
              <div class="ml-4">
                <h3 class="text-lg leading-6 font-medium text-gray-900">{{ user?.firstname }} {{ user?.lastname }}</h3>
                <p class="text-sm text-gray-500">{{ user?.email }}</p>
              </div>
            </div>

            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Personal Information</h3>
            <dl class="grid grid-cols-1 gap-x-4 gap-y-8 sm:grid-cols-2">
              <div class="sm:col-span-1">
                <dt class="text-sm font-medium text-gray-500">First Name</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ user?.firstname }}</dd>
              </div>
              <div class="sm:col-span-1">
                <dt class="text-sm font-medium text-gray-500">Last Name</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ user?.lastname }}</dd>
              </div>
              <div class="sm:col-span-1">
                <dt class="text-sm font-medium text-gray-500">Email</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ user?.email }}</dd>
              </div>
              <div class="sm:col-span-1">
                <dt class="text-sm font-medium text-gray-500">Phone</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ user?.phone }}</dd>
              </div>
              <div class="sm:col-span-2">
                <dt class="text-sm font-medium text-gray-500">Address</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ user?.address }}</dd>
              </div>
              <div class="sm:col-span-1">
                <dt class="text-sm font-medium text-gray-500">Role</dt>
                <dd class="mt-1 text-sm text-gray-900 capitalize">{{ user?.role }}</dd>
              </div>
              <div class="sm:col-span-1">
                <dt class="text-sm font-medium text-gray-500">Member Since</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ formatDate(user?.created_at) }}</dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const user = computed(() => authStore.user)

const userInitials = computed(() => {
  if (!user.value) return 'U'
  const first = user.value.firstname?.charAt(0) || ''
  const last = user.value.lastname?.charAt(0) || ''
  return (first + last).toUpperCase() || 'U'
})

const profilePictureUrl = computed(() => {
  if (!user.value) return null
  return user.value.profile_picture || `https://api.dicebear.com/9.x/notionists-neutral/svg?seed=${user.value.firstname}${user.value.lastname}`
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}
</script>
