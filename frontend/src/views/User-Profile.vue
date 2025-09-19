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

        <!-- My Issues -->
        <div class="mt-8 bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">My Issues</h3>
            <div v-if="myIssues.length === 0" class="text-center py-8">
              <p class="text-gray-500">You haven't reported any issues yet.</p>
              <router-link to="/issues"
                class="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
                Report Your First Issue
              </router-link>
            </div>
            <div v-else class="space-y-4">
              <div v-for="issue in myIssues" :key="issue.id" class="border rounded-lg p-4">
                <div class="flex items-center justify-between">
                  <h4 class="text-sm font-medium text-gray-900">{{ issue.title }}</h4>
                  <span :class="getStatusClass(issue.status)"
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                    {{ issue.status }}
                  </span>
                </div>
                <p class="mt-1 text-sm text-gray-600">{{ issue.description }}</p>
                <p class="mt-2 text-xs text-gray-500">{{ formatDate(issue.created_at) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()

const user = computed(() => authStore.user)
const myIssues = ref([])

const getStatusClass = (status) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-800',
    in_progress: 'bg-blue-100 text-blue-800',
    resolved: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800',
    verified: 'bg-purple-100 text-purple-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

onMounted(() => {
  // TODO: Fetch user's issues from API
  myIssues.value = [
    {
      id: 1,
      title: 'Pothole on Main Street',
      description: 'Large pothole causing traffic issues',
      status: 'pending',
      created_at: '2024-01-15T10:00:00Z'
    }
  ]
})
</script>
