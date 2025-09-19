<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Main content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="flex justify-between items-center mb-8">
          <h2 class="text-2xl font-bold text-gray-900">My Issues</h2>
          <button @click="showCreateForm = true"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
            <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            Report New Issue
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
        </div>

        <!-- Issues list -->
        <div v-else-if="issues.length > 0" class="bg-white shadow overflow-hidden sm:rounded-md">
          <ul class="divide-y divide-gray-200">
            <li v-for="issue in issues" :key="issue.id" class="hover:bg-gray-50">
              <div class="px-4 py-4 sm:px-6">
                <div class="flex items-center justify-between">
                  <div class="flex items-center">
                    <p class="text-sm font-medium text-indigo-600 truncate">{{ issue.title }}</p>
                    <span :class="getStatusClass(issue.status)"
                      class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                      {{ issue.status }}
                    </span>
                  </div>
                  <div class="flex items-center text-sm text-gray-500">
                    <p>{{ formatDate(issue.created_at) }}</p>
                  </div>
                </div>
                <div class="mt-2">
                  <p class="text-sm text-gray-600 line-clamp-2">{{ issue.description }}</p>
                  <div class="mt-2 flex items-center space-x-4 text-xs text-gray-500">
                    <span v-if="issue.issue_type && issue.issue_type !== 'Unspecified'">
                      Type: {{ issue.issue_type }}
                    </span>
                    <span v-if="issue.address">
                      📍 {{ issue.address }}
                    </span>
                    <span v-if="issue.image_urls && issue.image_urls.length > 0">
                      📷 {{ issue.image_urls.length }} image{{ issue.image_urls.length > 1 ? 's' :
                        '' }}
                    </span>
                  </div>
                </div>
              </div>
            </li>
          </ul>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No issues reported</h3>
          <p class="mt-1 text-sm text-gray-500">Get started by reporting your first issue.</p>
          <div class="mt-6">
            <button @click="showCreateForm = true"
              class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
              <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Report New Issue
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Create Issue Form Modal -->
    <div v-if="showCreateForm" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click="showCreateForm = false">
      <div class="relative top-4 mx-auto p-5 w-full max-w-2xl" @click.stop>
        <IssueForm @cancel="showCreateForm = false" @success="onIssueCreated" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import IssueForm from '../components/Issue-Form.vue'
import axios from '../api/client'

const issues = ref([])
const showCreateForm = ref(false)
const loading = ref(false)

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

const fetchIssues = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/issues/my-issues')

    if (response.status === 200) {
      issues.value = response.data.issues
    } else {
      console.error('Failed to fetch issues')
    }
  } catch (error) {
    console.error('Error fetching issues:', error)
  } finally {
    loading.value = false
  }
}

const onIssueCreated = (newIssue) => {
  showCreateForm.value = false
  issues.value.unshift(newIssue) // Add to the beginning of the list
}

onMounted(() => {
  fetchIssues()
})
</script>
