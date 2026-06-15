<template>
  <div class="min-h-screen bg-base-100 text-base-content antialiased py-8 px-4 sm:px-6 lg:px-8">
    <!-- Main content -->
    <main class="max-w-4xl mx-auto">
      <div>
        <!-- Back button -->
        <div class="mb-8">
          <button
            @click="$router.go(-1)"
            class="btn btn-outline border-base-300 hover:border-slate-500 rounded-xl btn-sm font-mono flex items-center gap-1.5 cursor-pointer"
          >
            <svg
              class="h-4 w-4"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
            </svg>
            Back to Issues
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center py-16">
          <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-primary"></div>
        </div>

        <!-- Issue Details Card -->
        <div
          v-else-if="issue"
          class="bg-base-200 border border-base-300 shadow-xl rounded-3xl overflow-hidden"
        >
          <!-- Header Subcomponent -->
          <IssueDetailHeader :issue="issue" @toggle-upvote="toggleUpvote" />

          <!-- Description -->
          <div class="p-6 md:p-8">
            <h3 class="font-mono text-xs font-bold uppercase tracking-wider text-base-content/60 mb-3">
              Description
            </h3>
            <p class="text-sm text-base-content/80 leading-relaxed font-sans">{{ issue.description }}</p>
          </div>

          <!-- Details Grid -->
          <div
            v-if="
              (issue.issue_type && issue.issue_type !== 'Unspecified') ||
              issue.address ||
              issue.department
            "
            class="border-t border-base-300 p-6 md:p-8 bg-base-200/40"
          >
            <h3 class="font-mono text-xs font-bold uppercase tracking-wider text-base-content/60 mb-4">
              Details
            </h3>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
              <div v-if="issue.issue_type && issue.issue_type !== 'Unspecified'">
                <span class="text-2xs font-mono text-base-content/40 uppercase tracking-widest block"
                  >Issue Type</span
                >
                <span class="mt-1.5 text-sm text-base-content/90 flex items-center">
                  <svg
                    class="w-4 h-4 mr-2 text-primary"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
                    />
                  </svg>
                  {{ issue.issue_type }}
                </span>
              </div>
              <div v-if="issue.address">
                <span class="text-2xs font-mono text-base-content/40 uppercase tracking-widest block"
                  >Address</span
                >
                <span class="mt-1.5 text-sm text-base-content/90 flex items-center">
                  <svg
                    class="w-4 h-4 mr-2 text-secondary"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                    />
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                  </svg>
                  {{ issue.address }}
                </span>
              </div>
              <div v-if="issue.department">
                <span class="text-2xs font-mono text-base-content/40 uppercase tracking-widest block"
                  >Assigned Department</span
                >
                <span class="mt-1.5 text-sm text-base-content/90 flex items-center">
                  <svg
                    class="w-4 h-4 mr-2 text-accent"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                    />
                  </svg>
                  {{ issue.department.name }}
                </span>
              </div>
            </div>
          </div>

          <!-- AI Analysis Subcomponent -->
          <IssueDetailAI :ai="ai" />

          <!-- Map Location -->
          <div v-if="issue.latitude && issue.longitude" class="border-t border-base-300 p-6 md:p-8">
            <h3 class="font-mono text-xs font-bold uppercase tracking-wider text-base-content/60 mb-4">
              Location Map
            </h3>
            <div class="h-72 w-full rounded-2xl overflow-hidden border border-base-300">
              <l-map
                v-model:zoom="zoom"
                :center="mapCenter"
                :use-global-leaflet="false"
                style="height: 100%"
              >
                <!-- Dark map tiles -->
                <l-tile-layer
                  :url="mapTileUrl"
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
                ></l-tile-layer>
                <l-marker :lat-lng="mapCenter">
                  <l-popup>
                    <div class="text-xs text-base-content/90">
                      <p class="font-bold mb-1 text-base-content">{{ issue.title }}</p>
                      <p class="truncate">{{ issue.address }}</p>
                    </div>
                  </l-popup>
                </l-marker>
              </l-map>
            </div>
          </div>

          <!-- Media Subcomponent -->
          <IssueDetailMedia :issue="issue" @open-image="handleOpenImage" />

          <!-- Updates Subcomponent -->
          <IssueDetailUpdates :updates="updates" @open-image="handleOpenImage" />

          <!-- Comments Subcomponent -->
          <IssueDetailComments :comments="comments" @submit-comment="submitComment" />
        </div>

        <!-- Error State -->
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
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"
            />
          </svg>
          <h3 class="text-lg font-bold text-base-content/80">Issue not found</h3>
          <p class="mt-1.5 text-sm text-base-content/40 font-sans">
            The issue you're looking for doesn't exist or you don't have permission to view it.
          </p>
        </div>
      </div>
    </main>

    <!-- Image Lightbox -->
    <ImageLightbox
      :visible="lightboxIndex !== null"
      :images="lightboxImages"
      :index="lightboxIndex"
      @close="lightboxIndex = null"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import router from '../router'
import axios from '../api/client'
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'

// Subcomponents
import IssueDetailHeader from '../components/issue/IssueDetailHeader.vue'
import IssueDetailAI from '../components/issue/IssueDetailAI.vue'
import IssueDetailMedia from '../components/issue/IssueDetailMedia.vue'
import IssueDetailUpdates from '../components/issue/IssueDetailUpdates.vue'
import IssueDetailComments from '../components/issue/IssueDetailComments.vue'

const route = useRoute()
const routeParams = computed(() => route?.params || router.currentRoute.value?.params || {})
const issue = ref(null)
const loading = ref(false)
const mapCenter = ref([0, 0])
const updates = ref([])
const comments = ref([])
const zoom = ref(15)

const ai = computed(() => issue.value?.ai_analysis || null)

const lightboxImages = ref([])
const lightboxIndex = ref(null)

const fetchIssue = async () => {
  loading.value = true
  try {
    const response = await axios.get(`/issues/${routeParams.value.id}`)

    if (response.status === 200) {
      issue.value = response.data.issue
      if (issue.value.latitude && issue.value.longitude) {
        mapCenter.value = [parseFloat(issue.value.latitude), parseFloat(issue.value.longitude)]
      }
    } else {
      console.error('Failed to fetch issue')
    }
  } catch (error) {
    console.error('Error fetching issue:', error)
  } finally {
    loading.value = false
  }
}

const fetchUpdates = async () => {
  try {
    const resp = await axios.get(`/issues/${routeParams.value.id}/updates`)
    updates.value = resp.data.updates || []
  } catch (e) {
    console.error('Failed to fetch updates', e)
  }
}

const handleOpenImage = ({ url, images }) => {
  const index = images.indexOf(url)
  lightboxImages.value = images
  lightboxIndex.value = index
}

const fetchComments = async () => {
  try {
    const resp = await axios.get(`/issues/${routeParams.value.id}/comments`)
    comments.value = resp.data.comments || []
  } catch (e) {
    console.error('Failed to fetch comments', e)
  }
}

const submitComment = async (commentText) => {
  try {
    const resp = await axios.post(`/issues/${routeParams.value.id}/comments`, {
      body: commentText,
    })
    comments.value.push(resp.data.comment)
  } catch (e) {
    console.error('Failed to post comment', e)
  }
}

const toggleUpvote = async () => {
  if (!issue.value) return
  try {
    if (issue.value.user_upvoted) {
      const resp = await axios.delete(`/issues/${issue.value.id}/upvote`)
      issue.value.user_upvoted = false
      issue.value.upvote_count = resp.data.upvote_count
    } else {
      const resp = await axios.post(`/issues/${issue.value.id}/upvote`)
      issue.value.user_upvoted = true
      issue.value.upvote_count = resp.data.upvote_count
    }
  } catch (e) {
    console.error('Upvote failed', e)
  }
}

onMounted(() => {
  console.log('IssueDetail component mounted, route params:', routeParams.value)
  fetchIssue()
  fetchUpdates()
  fetchComments()
})

// Dynamic theme-aware map logic
const currentTheme = ref(localStorage.getItem('theme') || 'citypulse')
const isDark = computed(() => ['citypulse-dark', 'dark', 'sunset', 'dim'].includes(currentTheme.value))

const mapTileUrl = computed(() => {
  return isDark.value
    ? 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
    : 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png'
})

const handleThemeChange = (event) => {
  currentTheme.value = event.detail
}

onMounted(() => {
  window.addEventListener('theme-changed', handleThemeChange)
})

onUnmounted(() => {
  window.removeEventListener('theme-changed', handleThemeChange)
})
</script>

