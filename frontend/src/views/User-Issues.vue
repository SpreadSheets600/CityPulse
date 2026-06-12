<template>
  <div class="min-h-screen bg-base-100 text-base-content antialiased py-8 px-4 sm:px-6 lg:px-8">
    <!-- Main content -->
    <main class="max-w-7xl mx-auto">
      <div>
        <div
          class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4"
        >
          <div>
            <h2 class="text-3xl font-extrabold text-slate-100 font-mono tracking-wider uppercase">
              My Reported Issues
            </h2>
            <p class="text-sm text-slate-400 mt-1">
              Track updates and SLA responses for your submissions
            </p>
          </div>
          <router-link
            to="/issues/create"
            class="btn btn-primary rounded-xl flex items-center justify-center gap-2 font-bold py-3 px-5 shadow-lg shadow-blue-500/10 cursor-pointer"
          >
            <svg
              class="h-5 w-5"
              fill="none"
              stroke="currentColor"
              stroke-width="2.5"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
            </svg>
            Report New Issue
          </router-link>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center py-16">
          <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-primary"></div>
        </div>

        <!-- Issues list -->
        <div
          v-else-if="issues.length > 0"
          class="bg-base-200 border border-base-300 shadow-xl rounded-3xl overflow-hidden"
        >
          <ul class="divide-y divide-base-300">
            <li
              v-for="issue in issues"
              :key="issue.id"
              class="hover:bg-base-300/10 transition-colors"
            >
              <router-link :to="`/issues/${issue.id}`" class="block p-5 sm:px-8">
                <!-- Header -->
                <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start mb-3 gap-2">
                  <div>
                    <p class="text-lg font-bold text-slate-100">{{ issue.title }}</p>
                    <p class="text-xs text-slate-400 mt-1 line-clamp-2 leading-relaxed font-sans">
                      {{ issue.description }}
                    </p>
                  </div>
                  <div
                    class="flex items-center text-xs font-mono text-slate-500 mt-1 sm:mt-0 gap-3"
                  >
                    <span
                      :class="getStatusClass(issue.status)"
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-2xs font-bold uppercase tracking-wide"
                    >
                      {{ issue.status }}
                    </span>
                    <span class="flex items-center">
                      <svg
                        class="w-3.5 h-3.5 mr-1"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                        />
                      </svg>
                      {{ formatDate(issue.created_at) }}
                    </span>
                  </div>
                </div>

                <!-- Details Row -->
                <div
                  class="flex flex-wrap items-center gap-3 text-xs font-mono text-slate-500 pt-1"
                >
                  <span
                    v-if="issue.issue_type && issue.issue_type !== 'Unspecified'"
                    class="flex items-center rounded-md bg-blue-500/5 px-2 py-0.5 border border-blue-500/10 text-blue-400"
                  >
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
                      />
                    </svg>
                    {{ issue.issue_type }}
                  </span>

                  <span v-if="issue.address" class="flex items-center">
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                      />
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                      />
                    </svg>
                    {{ issue.address }}
                  </span>

                  <span v-if="issue.department" class="flex items-center">
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                      />
                    </svg>
                    Dept: <span class="text-slate-300 ml-1">{{ issue.department.name }}</span>
                  </span>
                </div>

                <!-- Media Row -->
                <div
                  v-if="
                    issue.image_urls?.length > 0 || issue.video_note_url || issue.voice_note_url
                  "
                  class="flex items-center gap-3 text-xs font-mono text-slate-500 mt-2"
                >
                  <span
                    v-if="issue.image_urls && issue.image_urls.length > 0"
                    class="flex items-center"
                  >
                    <svg
                      class="w-3.5 h-3.5 mr-1"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                      />
                    </svg>
                    {{ issue.image_urls.length }} image{{ issue.image_urls.length > 1 ? 's' : '' }}
                  </span>

                  <span v-if="issue.video_note_url" class="flex items-center">
                    <svg
                      class="w-3.5 h-3.5 mr-1"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
                      />
                    </svg>
                    Video
                  </span>

                  <span v-if="issue.voice_note_url" class="flex items-center">
                    <svg
                      class="w-3.5 h-3.5 mr-1"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
                      />
                    </svg>
                    Audio
                  </span>
                </div>

                <!-- Footer updates -->
                <div
                  v-if="issue.updated_at !== issue.created_at"
                  class="flex items-center text-xs font-mono text-slate-500 mt-2.5 pt-2.5 border-t border-base-300/30"
                >
                  <svg
                    class="w-3.5 h-3.5 mr-1.5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M4 4v5h.582m15.356 2A8.001 8.001 0 1121.21 8H17"
                    />
                  </svg>
                  Updated: {{ formatDate(issue.updated_at) }}
                </div>
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Empty State -->
        <div
          v-else
          class="text-center py-16 border border-dashed border-base-300 rounded-3xl bg-base-200/40"
        >
          <svg
            class="mx-auto h-12 w-12 text-slate-600 mb-3"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          <h3 class="text-lg font-bold text-slate-300">No issues reported</h3>
          <p class="mt-1.5 text-sm text-slate-500">
            Get started by reporting your first neighborhood issue.
          </p>
          <div class="mt-6">
            <router-link
              to="/issues/create"
              class="btn btn-primary rounded-xl font-bold px-6 shadow-lg shadow-blue-500/10 cursor-pointer"
            >
              Report New Issue
            </router-link>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../api/client'

const issues = ref([])
const loading = ref(false)

const getStatusClass = (status) => {
  const classes = {
    pending: 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20',
    in_progress: 'bg-blue-500/10 text-blue-400 border border-blue-500/20',
    resolved: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
    rejected: 'bg-red-500/10 text-red-400 border border-red-500/20',
    verified: 'bg-purple-500/10 text-purple-400 border border-purple-500/20',
  }
  return classes[status] || 'bg-slate-500/10 text-slate-400 border border-slate-500/20'
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

onMounted(() => {
  fetchIssues()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-clamp: 2;
  overflow: hidden;
}
</style>
