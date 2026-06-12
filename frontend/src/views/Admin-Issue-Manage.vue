<template>
  <div class="min-h-screen bg-base-100 text-base-content antialiased py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-5xl mx-auto">
      <div class="mb-8 flex items-center justify-between gap-4">
        <div>
          <h1 class="text-3xl font-extrabold text-base-content font-mono tracking-wider uppercase">
            Manage Issue
          </h1>
          <p class="text-xs text-base-content/60 mt-1">
            Update dispatch status and run AI verification diagnostics
          </p>
        </div>
        <router-link
          to="/admin-dashboard"
          class="btn btn-outline border-base-300 hover:border-slate-500 rounded-xl btn-sm font-mono cursor-pointer"
        >
          ← Back
        </router-link>
      </div>

      <div v-if="loading" class="text-center py-16">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-primary mx-auto"></div>
        <p class="mt-4 text-base-content/60 font-mono text-xs">PULLING RECORD DETAILS...</p>
      </div>
      <div
        v-else-if="error"
        class="border border-error/20 bg-error/5 text-error text-center text-xs font-mono p-4 rounded-xl mb-6"
      >
        {{ error }}
      </div>

      <div v-else-if="issue" class="space-y-6">
        <!-- Issue Details Card -->
        <div class="bg-base-200 border border-base-300 shadow-xl rounded-3xl p-6 md:p-8">
          <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-6">
            <div class="flex-1">
              <h2 class="text-2xl font-bold text-base-content mb-3">{{ issue.title }}</h2>
              <p class="text-sm text-base-content/80 leading-relaxed font-sans">
                {{ issue.description }}
              </p>
            </div>
            <span
              :class="getStatusClass(issue.status)"
              class="inline-flex items-center px-3 py-1 rounded-full text-2xs font-bold uppercase tracking-wide"
            >
              {{ issue.status }}
            </span>
          </div>

          <div
            class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 text-xs font-mono text-base-content/60 border-t border-base-300/50 pt-5 mb-5"
          >
            <div class="flex items-center">
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
              <span
                >Type : <strong class="text-base-content/90 ml-1">{{ issue.issue_type }}</strong></span
              >
            </div>
            <div class="flex items-center">
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
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span
                >Created :
                <strong class="text-base-content/90 ml-1">{{
                  new Date(issue.created_at).toLocaleDateString()
                }}</strong></span
              >
            </div>
            <div v-if="issue.updated_at !== issue.created_at" class="flex items-center">
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
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span
                >Updated :
                <strong class="text-base-content/90 ml-1">{{
                  new Date(issue.updated_at).toLocaleDateString()
                }}</strong></span
              >
            </div>
            <div class="flex items-center">
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
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                />
              </svg>
              <span
                >Reporter :
                <strong class="text-base-content/90 ml-1"
                  >{{ issue.user?.firstname }} {{ issue.user?.lastname }}</strong
                ></span
              >
            </div>
          </div>

          <div class="flex items-center text-xs font-mono text-base-content/60 mb-6">
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
                d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
              />
            </svg>
            <span
              >Address : <strong class="text-base-content/90 ml-1">{{ issue.address }}</strong></span
            >
          </div>

          <!-- Location Map -->
          <div v-if="issue.latitude && issue.longitude" class="pt-4 border-t border-base-300/40">
            <h3 class="font-mono text-xs font-bold uppercase tracking-wider text-base-content/60 mb-3">
              Geographic Location
            </h3>
            <div class="h-64 w-full rounded-2xl overflow-hidden border border-base-300">
              <l-map
                v-model:zoom="zoom"
                :center="mapCenter"
                :use-global-leaflet="false"
                style="height: 100%"
              >
                <l-tile-layer
                   :url="mapTileUrl" attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
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

          <!-- Media Section -->
          <div
            v-if="issue.image_urls?.length > 0 || issue.video_note_url || issue.voice_note_url"
            class="pt-6 mt-6 border-t border-base-300/40"
          >
            <h3 class="font-mono text-xs font-bold uppercase tracking-wider text-base-content/60 mb-4">
              Media Evidence
            </h3>
            <div class="space-y-6">
              <div v-if="issue.image_urls && issue.image_urls.length > 0">
                <h4
                  class="text-xs font-mono font-bold text-base-content/40 mb-3 flex items-center uppercase tracking-wider"
                >
                  <svg
                    class="w-4 h-4 mr-2"
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
                    class="w-full h-32 object-cover rounded-xl cursor-pointer border border-base-300 hover:opacity-85 hover:scale-[1.02] transition-all"
                    @click="openImageModal(url)"
                  />
                </div>
              </div>
              <div v-if="issue.voice_note_url">
                <h4
                  class="text-xs font-mono font-bold text-base-content/40 mb-3 flex items-center uppercase tracking-wider"
                >
                  <svg
                    class="w-4 h-4 mr-2"
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
                  class="text-xs font-mono font-bold text-base-content/40 mb-3 flex items-center uppercase tracking-wider"
                >
                  <svg
                    class="w-4 h-4 mr-2"
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
                  class="w-full max-w-md rounded-2xl border border-base-300 bg-black"
                ></video>
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Update status -->
          <div class="bg-base-200 border border-base-300 shadow-xl rounded-3xl p-6 md:p-8">
            <h3 class="text-xs font-bold font-mono text-base-content/60 uppercase tracking-widest mb-4">
              Update Status
            </h3>
            <select
              v-model="status"
              class="select select-bordered w-full rounded-xl border-base-300 font-mono text-xs focus:border-primary"
            >
              <option value="pending">Pending</option>
              <option value="in_progress">In Progress</option>
              <option value="resolved">Resolved</option>
              <option value="rejected">Rejected</option>
              <option value="verified">Verified</option>
            </select>
            <button
              @click="saveStatus"
              class="btn btn-primary mt-4 w-full rounded-xl font-bold cursor-pointer"
            >
              Save Status
            </button>
          </div>

          <!-- Assign department -->
          <div class="bg-base-200 border border-base-300 shadow-xl rounded-3xl p-6 md:p-8">
            <h3 class="text-xs font-bold font-mono text-base-content/60 uppercase tracking-widest mb-4">
              Assign Department
            </h3>
            <p v-if="issue.department" class="mb-3 text-xs font-mono text-base-content/60">
              Current Department:
              <span class="font-bold text-base-content/90">{{ issue.department.name }}</span>
            </p>
            <select
              v-model="departmentId"
              class="select select-bordered w-full rounded-xl border-base-300 font-mono text-xs focus:border-primary"
            >
              <option disabled value="">Select Department</option>
              <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
            </select>
            <button
              @click="assignDepartment"
              class="btn btn-accent mt-4 w-full rounded-xl font-bold cursor-pointer"
            >
              Assign Department
            </button>
          </div>
        </div>

        <!-- AI Verification Panel -->
        <div class="bg-base-200 border border-base-300 shadow-xl rounded-3xl p-6 md:p-8">
          <div class="flex items-center justify-between mb-4 gap-2">
            <h3
              class="text-xs font-bold font-mono text-base-content/60 uppercase tracking-widest flex items-center gap-2"
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
            <button
              @click="runVerification"
              :disabled="verifying || !issue.image_urls?.length"
              class="btn btn-sm btn-outline border-base-300 hover:border-slate-500 rounded-xl font-mono cursor-pointer"
            >
              <span v-if="verifying" class="loading loading-spinner loading-xs mr-1"></span>
              {{ verifying ? 'ANALYZING...' : 'RUN AI DIAGNOSTIC' }}
            </button>
          </div>

          <div v-if="!verification && !verifying" class="text-xs font-mono text-base-content/40 py-4">
            Trigger visual inspection. Locally hosted AI models will parse the coordinates and match
            objects inside the attachment payload.
          </div>

          <div v-if="verification" class="space-y-4">
            <!-- Verification Status Banner -->
            <div
              :class="{
                'bg-emerald-500/10 border-emerald-500/20 text-emerald-400':
                  verification.status === 'consistent',
                'bg-red-500/10 border-red-500/20 text-red-400':
                  verification.status === 'misleading',
                'bg-yellow-500/10 border-yellow-500/20 text-yellow-400':
                  verification.status === 'uncertain',
              }"
              class="border rounded-2xl p-4 font-mono text-xs leading-relaxed"
            >
              <div class="flex items-start gap-3">
                <div class="flex-shrink-0 mt-0.5">
                  <svg
                    v-if="verification.status === 'consistent'"
                    class="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <svg
                    v-else-if="verification.status === 'misleading'"
                    class="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"
                    />
                  </svg>
                  <svg
                    v-else
                    class="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                </div>
                <div>
                  <p class="font-bold text-base-content">{{ verification.message }}</p>
                  <div class="mt-2 flex flex-wrap gap-4 text-base-content/60">
                    <span
                      >REPORTED_TYPE: <strong>{{ verification.reported_type }}</strong></span
                    >
                    <span
                      >AI_DETECTION: <strong>{{ verification.ai_category }}</strong></span
                    >
                    <span
                      >CONFIDENCE:
                      <strong>{{ (verification.ai_confidence * 100).toFixed(1) }}%</strong></span
                    >
                  </div>
                </div>
              </div>
            </div>

            <!-- Per-image detections -->
            <div v-if="detections.length > 0">
              <h4 class="text-xs font-mono font-bold text-base-content/40 uppercase tracking-wider mb-3">
                Visual Inspection Details
              </h4>
              <div class="space-y-3">
                <div
                  v-for="det in detections"
                  :key="det.image_index"
                  class="bg-base-100/40 border border-base-300 rounded-2xl p-4 text-xs font-mono"
                >
                  <div class="flex items-center justify-between mb-2">
                    <span class="font-bold text-base-content/80"
                      >File Object {{ det.image_index + 1 }}</span
                    >
                    <span
                      :class="{
                        'badge badge-success badge-sm':
                          det.category !== 'Unspecified' && det.category !== 'error',
                        'badge badge-warning badge-sm': det.category === 'Unspecified',
                        'badge badge-error badge-sm': det.category === 'error',
                      }"
                      class="font-bold uppercase tracking-wider"
                      >{{ det.category }}</span
                    >
                  </div>
                  <div v-if="det.detections?.length > 0" class="flex flex-wrap gap-2 mt-2">
                    <span
                      v-for="(d, i) in det.detections"
                      :key="i"
                      class="inline-flex items-center px-2 py-1 rounded bg-base-300 border border-base-300/40 text-base-content/80 text-2xs"
                    >
                      {{ d.label }} ({{ (d.confidence * 100).toFixed(0) }}%)
                    </span>
                  </div>
                  <div v-if="det.error" class="text-error text-2xs mt-1">{{ det.error }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Post update -->
        <div class="bg-base-200 border border-base-300 shadow-xl rounded-3xl p-6 md:p-8">
          <h3 class="text-xs font-bold font-mono text-base-content/60 uppercase tracking-widest mb-4">
            Post SLA Milestone Update
          </h3>
          <input
            v-model="updateTitle"
            type="text"
            placeholder="Update milestone title"
            class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary font-sans text-sm"
          />
          <textarea
            v-model="updateBody"
            rows="4"
            placeholder="Update milestone details..."
            class="textarea textarea-bordered mt-3 w-full rounded-xl border-base-300 focus:border-primary font-sans"
          ></textarea>

          <div class="my-4">
            <label class="block text-xs font-mono text-base-content/60 uppercase tracking-wider mb-2"
              >SLA Task Progress : {{ progress }}%</label
            >
            <input
              v-model.number="progress"
              type="range"
              min="0"
              max="100"
              class="range range-primary"
            />
          </div>

          <input
            type="file"
            multiple
            accept="image/*"
            @change="onUpdateFileChange"
            class="file-input file-input-bordered file-input-primary w-full rounded-xl"
          />
          <button
            @click="postUpdate"
            class="btn btn-primary mt-4 w-full rounded-xl font-bold cursor-pointer shadow-lg shadow-blue-500/10"
          >
            PUBLISH SLA UPDATE
          </button>
        </div>

        <!-- Existing updates -->
        <div class="bg-base-200 border border-base-300 shadow-xl rounded-3xl p-6 md:p-8">
          <h3 class="text-xs font-bold font-mono text-base-content/60 uppercase tracking-widest mb-4">
            Past Milestones
          </h3>
          <div v-if="updates.length === 0" class="text-sm font-mono text-base-content/40 py-4">
            No update files posted.
          </div>
          <div v-else class="space-y-4">
            <div
              v-for="u in updates"
              :key="u.id"
              class="bg-base-100/50 border border-base-300 rounded-2xl p-5 shadow-inner"
            >
              <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start mb-3 gap-2">
                <h4 class="font-bold text-base-content text-base">{{ u.title }}</h4>
                <span class="text-xs font-mono text-base-content/40">{{
                  new Date(u.created_at).toLocaleString()
                }}</span>
              </div>
              <p class="text-sm text-base-content/80 mb-3 font-sans leading-relaxed">{{ u.body }}</p>

              <div class="mb-3">
                <div class="flex justify-between text-xs font-mono text-base-content/60 mb-1">
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

              <div v-if="u.image_urls && u.image_urls.length > 0" class="mt-4">
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                  <img
                    v-for="(url, index) in u.image_urls"
                    :key="index"
                    :src="url"
                    :alt="`Update image ${index + 1}`"
                    class="w-full h-24 object-cover rounded-xl border border-base-300 hover:opacity-85 transition-opacity"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Image Lightbox -->
        <ImageLightbox
          :visible="lightboxIndex !== null"
          :images="lightboxImages"
          :index="lightboxIndex"
          @close="lightboxIndex = null"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import { useRoute } from 'vue-router'
import router from '../router'
import { ref, onMounted, computed } from 'vue'
import axios from '../api/client'
import 'leaflet/dist/leaflet.css'

const route = useRoute()
const routeParams = computed(() => route?.params || router.currentRoute.value?.params || {})

const issue = ref(null)
const loading = ref(false)
const error = ref('')

const status = ref('pending')
const departments = ref([])
const departmentId = ref('')

const updateTitle = ref('')
const updateBody = ref('')
const progress = ref(0)

const updates = ref([])

const updateFiles = ref([])

const zoom = ref(15)
const mapCenter = ref([0, 0])

const lightboxImages = ref([])
const lightboxIndex = ref(null)

const verifying = ref(false)
const verification = ref(null)
const detections = ref([])

const getStatusClass = (status) => {
  const classes = {
    pending: 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20',
    in_progress: 'bg-blue-500/10 text-blue-400 border border-blue-500/20',
    resolved: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
    rejected: 'bg-red-500/10 text-red-400 border border-red-500/20',
    verified: 'bg-purple-500/10 text-purple-400 border border-purple-500/20',
  }
  return classes[status] || 'bg-slate-500/10 text-base-content/60 border border-slate-500/20'
}

const loadIssue = async () => {
  loading.value = true
  try {
    const resp = await axios.get(`/api/issues/${routeParams.value.id}`)
    issue.value = resp.data.issue
    status.value = issue.value.status
    if (issue.value?.department_id) {
      departmentId.value = issue.value.department_id
    }
    if (issue.value.latitude && issue.value.longitude) {
      mapCenter.value = [parseFloat(issue.value.latitude), parseFloat(issue.value.longitude)]
    }
  } catch (e) {
    error.value = e.response?.data?.error || 'Failed to load issue'
  } finally {
    loading.value = false
  }
}

const loadDepartments = async () => {
  try {
    const resp = await axios.get('/api/admin/departments')
    departments.value = resp.data.departments
  } catch (e) {
    console.error(e)
  }
}

const loadUpdates = async () => {
  try {
    const resp = await axios.get(`/api/issues/${routeParams.value.id}/updates`)
    updates.value = resp.data.updates
  } catch (e) {
    console.error(e)
  }
}

const saveStatus = async () => {
  try {
    const resp = await axios.put(`/api/admin/issues/${routeParams.value.id}/status`, {
      status: status.value,
    })
    issue.value = resp.data.issue
  } catch (e) {
    alert(e.response?.data?.error || 'Failed to update status')
  }
}

const assignDepartment = async () => {
  if (!departmentId.value) return
  try {
    const resp = await axios.put(`/api/admin/issues/${routeParams.value.id}/department`, {
      department_id: departmentId.value,
    })
    issue.value = resp.data.issue
  } catch (e) {
    alert(e.response?.data?.error || 'Failed to assign department')
  }
}

const runVerification = async () => {
  verifying.value = true
  verification.value = null
  detections.value = []
  try {
    const resp = await axios.post(`/api/admin/issues/${routeParams.value.id}/verify`)
    verification.value = resp.data.verification
    detections.value = resp.data.detections || []
  } catch (e) {
    alert(e.response?.data?.error || 'Verification failed')
  } finally {
    verifying.value = false
  }
}

const postUpdate = async () => {
  if (!updateTitle.value) return alert('Title is required')

  const formData = new FormData()
  formData.append('title', updateTitle.value)
  formData.append('body', updateBody.value)
  formData.append('progress', progress.value.toString())

  updateFiles.value.forEach((file) => {
    formData.append('images', file)
  })

  try {
    await axios.post(`/api/admin/issues/${routeParams.value.id}/updates`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    updateTitle.value = ''
    updateBody.value = ''
    progress.value = 0
    updateFiles.value = []
    await loadUpdates()
  } catch (e) {
    alert(e.response?.data?.error || 'Failed to post update')
  }
}

const onUpdateFileChange = (event) => {
  updateFiles.value = Array.from(event.target.files)
}

const openImageModal = (url) => {
  const index = issue.value.image_urls.indexOf(url)
  lightboxImages.value = issue.value.image_urls
  lightboxIndex.value = index
}

onMounted(() => {
  console.log('IssueDetail component mounted, route params:', routeParams.value)
  loadIssue()
  Promise.all([loadDepartments(), loadUpdates()])
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

import { onUnmounted } from 'vue'
onUnmounted(() => {
  window.removeEventListener('theme-changed', handleThemeChange)
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

/* Fix popup styling inside dark leaflet map */
::v-deep(.leaflet-popup-content-wrapper) {
  background-color: var(--color-base-200) !important;
  color: var(--color-base-content) !important;
  border: 1px solid var(--color-base-300) !important;
  border-radius: 12px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
}

::v-deep(.leaflet-popup-tip) {
  background-color: var(--color-base-200) !important;
  border: 1px solid var(--color-base-300) !important;
}

::v-deep(.leaflet-container a.leaflet-popup-close-button) {
  color: var(--color-base-content) !important;
  opacity: 0.6;
}
</style>
