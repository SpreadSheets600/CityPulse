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
          <!-- Header -->
          <div class="p-6 md:p-8 border-b border-base-300">
            <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
              <div class="flex-1">
                <h1 class="text-2xl md:text-3xl font-extrabold text-slate-100">
                  {{ issue.title }}
                </h1>
                <div
                  class="mt-3 flex flex-wrap items-center gap-4 text-xs font-mono text-slate-400"
                >
                  <div class="flex items-center">
                    <svg
                      class="w-4 h-4 mr-1.5 text-slate-500"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                      />
                    </svg>
                    Reported by:
                    <span class="text-slate-300 ml-1"
                      >{{ issue.user?.firstname }} {{ issue.user?.lastname }}</span
                    >
                  </div>
                  <div class="flex items-center">
                    <svg
                      class="w-4 h-4 mr-1.5 text-slate-500"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                    {{ formatDate(issue.created_at) }}
                  </div>
                  <div v-if="issue.updated_at !== issue.created_at" class="flex items-center">
                    <svg
                      class="w-4 h-4 mr-1.5 text-slate-500"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 1121.21 8H17"
                      />
                    </svg>
                    Updated: {{ formatDate(issue.updated_at) }}
                  </div>
                </div>
              </div>
              <div class="flex items-center gap-3">
                <span
                  :class="getStatusClass(issue.status)"
                  class="inline-flex items-center px-3 py-1 rounded-full text-2xs font-bold uppercase tracking-wide"
                >
                  {{ issue.status }}
                </span>
                <button
                  @click="toggleUpvote"
                  :class="[
                    'btn btn-sm rounded-xl font-mono cursor-pointer',
                    issue.user_upvoted
                      ? 'btn-primary'
                      : 'btn-outline border-base-300 hover:border-slate-500',
                  ]"
                >
                  <svg
                    class="w-4 h-4 mr-1"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2.5"
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 15l7-7 7 7" />
                  </svg>
                  {{ issue.upvote_count || 0 }}
                </button>
              </div>
            </div>
          </div>

          <!-- Description -->
          <div class="p-6 md:p-8">
            <h3 class="font-mono text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
              Description
            </h3>
            <p class="text-sm text-slate-300 leading-relaxed font-sans">{{ issue.description }}</p>
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
            <h3 class="font-mono text-xs font-bold uppercase tracking-wider text-slate-400 mb-4">
              Details
            </h3>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
              <div v-if="issue.issue_type && issue.issue_type !== 'Unspecified'">
                <span class="text-2xs font-mono text-slate-500 uppercase tracking-widest block"
                  >Issue Type</span
                >
                <span class="mt-1.5 text-sm text-slate-200 flex items-center">
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
                <span class="text-2xs font-mono text-slate-500 uppercase tracking-widest block"
                  >Address</span
                >
                <span class="mt-1.5 text-sm text-slate-200 flex items-center">
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
                <span class="text-2xs font-mono text-slate-500 uppercase tracking-widest block"
                  >Assigned Department</span
                >
                <span class="mt-1.5 text-sm text-slate-200 flex items-center">
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

          <!-- AI Analysis Status -->
          <div v-if="aiVerification" class="border-t border-base-300 p-6 md:p-8 bg-base-200/50">
            <h3
              class="text-xs font-bold font-mono uppercase tracking-wider text-slate-400 mb-4 flex items-center gap-2"
            >
              <svg
                class="w-4.5 h-4.5 text-primary"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                />
              </svg>
              AI Computer Vision Verification
            </h3>
            <div
              :class="{
                'bg-emerald-500/10 border-emerald-500/20 text-emerald-400':
                  aiVerification.status === 'verified',
                'bg-red-500/10 border-red-500/20 text-red-400':
                  aiVerification.status === 'rejected',
                'bg-yellow-500/10 border-yellow-500/20 text-yellow-400':
                  aiVerification.status === 'pending',
              }"
              class="border rounded-2xl p-4 text-xs font-mono leading-relaxed"
            >
              <div class="flex items-center gap-2 mb-2">
                <span
                  :class="{
                    'badge badge-success badge-sm': aiVerification.status === 'verified',
                    'badge badge-error badge-sm': aiVerification.status === 'rejected',
                    'badge badge-warning badge-sm': aiVerification.status === 'pending',
                  }"
                  class="font-bold uppercase tracking-wider"
                  >{{ aiVerification.status }}</span
                >
                <span v-if="aiVerification.verified_at" class="text-slate-500">
                  VERIFIED_AT: {{ new Date(aiVerification.verified_at).toLocaleDateString() }}
                </span>
              </div>
              <p class="text-slate-300 font-sans text-sm">{{ aiVerification.notes }}</p>
            </div>
          </div>

          <!-- Map Location -->
          <div v-if="issue.latitude && issue.longitude" class="border-t border-base-300 p-6 md:p-8">
            <h3 class="font-mono text-xs font-bold uppercase tracking-wider text-slate-400 mb-4">
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
                  url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
                ></l-tile-layer>
                <l-marker :lat-lng="mapCenter">
                  <l-popup>
                    <div class="text-xs text-slate-200">
                      <p class="font-bold mb-1 text-slate-100">{{ issue.title }}</p>
                      <p class="truncate">{{ issue.address }}</p>
                    </div>
                  </l-popup>
                </l-marker>
              </l-map>
            </div>
          </div>

          <!-- Media -->
          <div
            v-if="issue.image_urls?.length > 0 || issue.voice_note_url || issue.video_note_url"
            class="border-t border-base-300 p-6 md:p-8 bg-base-200/30"
          >
            <h3 class="font-mono text-xs font-bold uppercase tracking-wider text-slate-400 mb-6">
              Attached Media
            </h3>
            <div class="space-y-6">
              <div v-if="issue.image_urls && issue.image_urls.length > 0">
                <h4
                  class="text-xs font-mono font-bold text-slate-500 mb-3 flex items-center uppercase tracking-wider"
                >
                  <svg
                    class="w-4 h-4 mr-2 text-slate-500"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                    />
                  </svg>
                  Images ({{ issue.image_urls.length }})
                </h4>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  <img
                    v-for="(url, index) in issue.image_urls"
                    :key="index"
                    :src="url"
                    :alt="`Image ${index + 1}`"
                    class="w-full h-48 object-cover rounded-2xl cursor-pointer hover:opacity-85 hover:scale-[1.02] border border-base-300 transition-all shadow-md"
                    @click="openImageModal(url, issue.image_urls)"
                  />
                </div>
              </div>

              <div v-if="issue.voice_note_url">
                <h4
                  class="text-xs font-mono font-bold text-slate-500 mb-3 flex items-center uppercase tracking-wider"
                >
                  <svg
                    class="w-4 h-4 mr-2 text-slate-500"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
                    />
                  </svg>
                  Voice Note
                </h4>
                <audio controls :src="issue.voice_note_url" class="w-full rounded-xl"></audio>
              </div>

              <div v-if="issue.video_note_url">
                <h4
                  class="text-xs font-mono font-bold text-slate-500 mb-3 flex items-center uppercase tracking-wider"
                >
                  <svg
                    class="w-4 h-4 mr-2 text-slate-500"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"
                    />
                  </svg>
                  Video Note
                </h4>
                <video
                  controls
                  :src="issue.video_note_url"
                  class="w-full max-w-md rounded-2xl border border-base-300 shadow-md bg-black"
                ></video>
              </div>
            </div>
          </div>

          <!-- Updates Section -->
          <div class="border-t border-base-300 p-6 md:p-8">
            <h3 class="font-mono text-xs font-bold uppercase tracking-wider text-slate-400 mb-4">
              Updates Feed
            </h3>
            <div v-if="updates.length === 0" class="text-sm font-mono text-slate-500">
              No updates uploaded yet.
            </div>
            <div v-else class="space-y-4">
              <div
                v-for="u in updates"
                :key="u.id"
                class="bg-base-100/50 border border-base-300 rounded-2xl p-5 shadow-inner"
              >
                <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start mb-3 gap-2">
                  <h4 class="font-bold text-slate-100 text-base">{{ u.title }}</h4>
                  <span class="text-xs font-mono text-slate-500 flex items-center">
                    <svg
                      class="w-3.5 h-3.5 mr-1.5"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                    {{ formatDate(u.created_at) }}
                  </span>
                </div>
                <p class="text-sm text-slate-300 mb-4 font-sans leading-relaxed">{{ u.body }}</p>
                <div class="mb-4">
                  <div class="flex justify-between text-xs font-mono text-slate-400 mb-1">
                    <span>Task Completion Progress</span>
                    <span>{{ u.progress }}%</span>
                  </div>
                  <div class="w-full bg-base-300 rounded-full h-2">
                    <div
                      class="bg-primary h-2 rounded-full transition-all duration-500"
                      :style="{ width: (u.progress || 0) + '%' }"
                    ></div>
                  </div>
                </div>
                <div v-if="u.image_urls && u.image_urls.length > 0">
                  <h5
                    class="text-xs font-mono font-bold text-slate-500 mb-3 uppercase tracking-wider"
                  >
                    Update Attachments
                  </h5>
                  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                    <img
                      v-for="(url, index) in u.image_urls"
                      :key="index"
                      :src="url"
                      :alt="`Update image ${index + 1}`"
                      class="w-full h-24 object-cover rounded-xl cursor-pointer hover:opacity-85 border border-base-300 transition-opacity"
                      @click="openImageModal(url, u.image_urls)"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Comments Section -->
          <div class="border-t border-base-300 p-6 md:p-8 bg-base-200/40">
            <h3 class="font-mono text-xs font-bold uppercase tracking-wider text-slate-400 mb-4">
              Comments ({{ comments.length }})
            </h3>
            <div v-if="comments.length === 0" class="text-sm font-mono text-slate-500 mb-6">
              No public comments.
            </div>
            <div v-else class="space-y-4 mb-6">
              <div
                v-for="c in comments"
                :key="c.id"
                class="bg-base-100/40 border border-base-300 rounded-2xl p-4 shadow-sm"
              >
                <div
                  class="flex items-center justify-between mb-2 gap-2 text-xs font-mono text-slate-500"
                >
                  <span class="font-bold text-slate-300"
                    >{{ c.author?.firstname }} {{ c.author?.lastname }}</span
                  >
                  <span>{{ formatDate(c.created_at) }}</span>
                </div>
                <p class="text-sm text-slate-300 leading-relaxed font-sans">{{ c.body }}</p>
              </div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3">
              <input
                v-model="newComment"
                type="text"
                placeholder="Add a comment..."
                class="input input-bordered flex-1 rounded-xl border-base-300 focus:border-primary focus:ring-1 focus:ring-primary transition-all font-sans text-sm"
                @keyup.enter="submitComment"
              />
              <button
                @click="submitComment"
                :disabled="!newComment.trim()"
                class="btn btn-primary rounded-xl cursor-pointer font-bold px-6"
              >
                Post Comment
              </button>
            </div>
          </div>
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
          <h3 class="text-lg font-bold text-slate-300">Issue not found</h3>
          <p class="mt-1.5 text-sm text-slate-500 font-sans">
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
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from '../api/client'
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'

const route = useRoute()
const issue = ref(null)
const loading = ref(false)
const mapCenter = ref([0, 0])
const updates = ref([])
const comments = ref([])
const newComment = ref('')
const zoom = ref(15)
const aiVerification = ref(null)

const lightboxImages = ref([])
const lightboxIndex = ref(null)

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
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const fetchIssue = async () => {
  loading.value = true
  try {
    const response = await axios.get(`/api/issues/${route.params.id}`)

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
    const resp = await axios.get(`/api/issues/${route.params.id}/updates`)
    updates.value = resp.data.updates || []
  } catch (e) {
    console.error('Failed to fetch updates', e)
  }
}

const openImageModal = (url, images) => {
  const index = images.indexOf(url)
  lightboxImages.value = images
  lightboxIndex.value = index
}

const fetchComments = async () => {
  try {
    const resp = await axios.get(`/api/issues/${route.params.id}/comments`)
    comments.value = resp.data.comments || []
  } catch (e) {
    console.error('Failed to fetch comments', e)
  }
}

const fetchAIVerification = async () => {
  try {
    const resp = await axios.get(`/api/issues/${route.params.id}/verify`)
    aiVerification.value = resp.data.verification
  } catch (e) {
    // Silently ignore
  }
}

const submitComment = async () => {
  if (!newComment.value.trim()) return
  try {
    const resp = await axios.post(`/api/issues/${route.params.id}/comments`, {
      body: newComment.value.trim(),
    })
    comments.value.push(resp.data.comment)
    newComment.value = ''
  } catch (e) {
    console.error('Failed to post comment', e)
  }
}

const toggleUpvote = async () => {
  if (!issue.value) return
  try {
    if (issue.value.user_upvoted) {
      const resp = await axios.delete(`/api/issues/${issue.value.id}/upvote`)
      issue.value.user_upvoted = false
      issue.value.upvote_count = resp.data.upvote_count
    } else {
      const resp = await axios.post(`/api/issues/${issue.value.id}/upvote`)
      issue.value.user_upvoted = true
      issue.value.upvote_count = resp.data.upvote_count
    }
  } catch (e) {
    console.error('Upvote failed', e)
  }
}

onMounted(() => {
  console.log('IssueDetail component mounted, route params:', route.params)
  fetchIssue()
  fetchUpdates()
  fetchComments()
  fetchAIVerification()
})
</script>

<style scoped>
/* Fix popup styling inside dark leaflet map */
::v-deep(.leaflet-popup-content-wrapper) {
  background-color: #0f172a !important;
  color: #f8fafc !important;
  border: 1px solid #334155;
  border-radius: 12px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
}

::v-deep(.leaflet-popup-tip) {
  background-color: #0f172a !important;
  border: 1px solid #334155;
}

::v-deep(.leaflet-container a.leaflet-popup-close-button) {
  color: #94a3b8 !important;
}
</style>
