<template>
  <div class="min-h-screen bg-base-100 text-base-content antialiased p-6">
    <div class="max-w-7xl mx-auto">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
        <h1 class="text-3xl font-extrabold text-slate-100 font-mono tracking-wider uppercase">
          Admin Dashboard
        </h1>
        <div class="text-xs font-mono text-slate-500">
          SYSTEM STATUS: <span class="text-emerald-400 font-bold">ONLINE</span>
        </div>
      </div>

      <!-- Admin Actions / Navbar Strip -->
      <div class="flex flex-wrap gap-3 mb-8 bg-base-200 border border-base-300 p-4 rounded-3xl">
        <router-link
          to="/admin/analytics"
          class="btn btn-outline border-base-300 hover:border-slate-500 hover:bg-base-300 rounded-xl btn-sm font-mono tracking-wide"
        >
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
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
            />
          </svg>
          Analytics
        </router-link>
        <router-link
          to="/admin/audit-log"
          class="btn btn-outline border-base-300 hover:border-slate-500 hover:bg-base-300 rounded-xl btn-sm font-mono tracking-wide"
        >
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
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
          Audit Log
        </router-link>
        <router-link
          to="/admin/departments"
          class="btn btn-outline border-base-300 hover:border-slate-500 hover:bg-base-300 rounded-xl btn-sm font-mono tracking-wide"
        >
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
          Departments
        </router-link>
        <router-link
          to="/admin/sla"
          class="btn btn-outline border-base-300 hover:border-slate-500 hover:bg-base-300 rounded-xl btn-sm font-mono tracking-wide"
        >
          <svg
            class="w-4 h-4 mr-2 text-warning"
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
          SLA Tracking
        </router-link>
        <router-link
          to="/admin/geofence"
          class="btn btn-outline border-base-300 hover:border-slate-500 hover:bg-base-300 rounded-xl btn-sm font-mono tracking-wide"
        >
          <svg
            class="w-4 h-4 mr-2 text-info"
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
            <circle cx="12" cy="11" r="3" />
          </svg>
          Geofencing
        </router-link>
        <router-link
          to="/admin/export"
          class="btn btn-primary rounded-xl btn-sm font-mono tracking-wide ml-auto"
        >
          <svg
            class="w-4 h-4 mr-2"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
            />
          </svg>
          Export Reports
        </router-link>
      </div>

      <!-- Loading and Error States -->
      <div v-if="loading" class="text-center py-16">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
        <p class="mt-4 text-slate-400 font-mono text-xs">PULLING ADMINISTRATIVE DATA...</p>
      </div>

      <div
        v-if="error"
        class="bg-red-500/10 border border-red-500/20 text-red-400 rounded-2xl p-5 mb-6 font-mono text-sm"
      >
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <div class="ml-3">
            <p>{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- Main Content -->
      <div
        v-else-if="issues.length === 0"
        class="text-center py-16 border border-dashed border-base-300 rounded-3xl bg-base-200/40"
      >
        <svg
          class="mx-auto h-12 w-12 text-slate-600 mb-3"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
        <h3 class="text-lg font-bold text-slate-300">No reported issues found</h3>
        <p class="mt-1.5 text-sm text-slate-500">
          Wait for users in neighborhood geofences to submit reports.
        </p>
      </div>

      <div v-else>
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <!-- Total -->
          <div
            class="bg-base-200 border border-base-300 shadow-lg rounded-2xl p-5 hover:border-primary/40 transition-all duration-300 flex items-center"
          >
            <div
              class="flex-shrink-0 h-10 w-10 rounded-xl bg-slate-500/10 border border-slate-500/20 flex items-center justify-center"
            >
              <svg
                class="h-5 w-5 text-slate-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <div class="ml-4 flex-1">
              <p class="text-xs font-mono text-slate-400 uppercase tracking-wider">Total Reports</p>
              <p class="text-2xl font-extrabold text-slate-100 font-mono mt-0.5">
                {{ issues.length }}
              </p>
            </div>
          </div>

          <!-- Pending -->
          <div
            class="bg-base-200 border border-base-300 shadow-lg rounded-2xl p-5 hover:border-primary/40 transition-all duration-300 flex items-center"
          >
            <div
              class="flex-shrink-0 h-10 w-10 rounded-xl bg-yellow-500/10 border border-yellow-500/20 flex items-center justify-center"
            >
              <svg
                class="h-5 w-5 text-yellow-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <div class="ml-4 flex-1">
              <p class="text-xs font-mono text-slate-400 uppercase tracking-wider">Pending</p>
              <p class="text-2xl font-extrabold text-slate-100 font-mono mt-0.5">
                {{ getStatusCount('pending') }}
              </p>
            </div>
          </div>

          <!-- In Progress -->
          <div
            class="bg-base-200 border border-base-300 shadow-lg rounded-2xl p-5 hover:border-primary/40 transition-all duration-300 flex items-center"
          >
            <div
              class="flex-shrink-0 h-10 w-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center"
            >
              <svg
                class="h-5 w-5 text-blue-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
            </div>
            <div class="ml-4 flex-1">
              <p class="text-xs font-mono text-slate-400 uppercase tracking-wider">In Progress</p>
              <p class="text-2xl font-extrabold text-slate-100 font-mono mt-0.5">
                {{ getStatusCount('in_progress') }}
              </p>
            </div>
          </div>

          <!-- Resolved -->
          <div
            class="bg-base-200 border border-base-300 shadow-lg rounded-2xl p-5 hover:border-primary/40 transition-all duration-300 flex items-center"
          >
            <div
              class="flex-shrink-0 h-10 w-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center"
            >
              <svg
                class="h-5 w-5 text-emerald-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <div class="ml-4 flex-1">
              <p class="text-xs font-mono text-slate-400 uppercase tracking-wider">Resolved</p>
              <p class="text-2xl font-extrabold text-slate-100 font-mono mt-0.5">
                {{ getStatusCount('resolved') }}
              </p>
            </div>
          </div>
        </div>

        <!-- Map Section -->
        <div class="bg-base-200 border border-base-300 shadow-lg rounded-3xl p-6 mb-8">
          <div class="flex items-center gap-2 mb-4">
            <div class="h-2 w-2 rounded-full bg-primary animate-pulse" />
            <h3 class="font-bold text-slate-100 font-mono text-sm tracking-wider uppercase">
              Live Incident Map Preview
            </h3>
          </div>
          <div
            class="map-container h-80 sm:h-[450px] border border-base-300 rounded-2xl overflow-hidden"
          >
            <l-map
              v-model:zoom="zoom"
              :center="center"
              :use-global-leaflet="false"
              style="height: 100%"
            >
              <!-- Dark map tiles -->
              <l-tile-layer
                url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
              ></l-tile-layer>
              <l-marker
                v-for="issue in issues.filter((i) => i.status !== 'rejected')"
                :key="issue.id"
                :lat-lng="[issue.latitude, issue.longitude]"
              >
                <l-popup>
                  <div class="w-48 text-slate-200">
                    <div class="space-y-1.5 text-xs">
                      <p class="font-bold border-b border-slate-700 pb-1 mb-1 text-slate-100">
                        {{ issue.title }}
                      </p>
                      <p><strong>Type:</strong> {{ issue.issue_type }}</p>
                      <p class="truncate"><strong>Address:</strong> {{ issue.address }}</p>
                    </div>
                    <div class="mt-3">
                      <router-link
                        :to="{ name: 'AdminIssueManage', params: { id: issue.id } }"
                        class="btn btn-primary btn-xs rounded-lg font-mono"
                      >
                        Manage Report
                      </router-link>
                    </div>
                  </div>
                </l-popup>
              </l-marker>
            </l-map>
          </div>
        </div>

        <!-- Issues List -->
        <div class="bg-base-200 border border-base-300 shadow-lg rounded-3xl p-6">
          <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-6 gap-4">
            <div>
              <h3 class="text-xl font-bold text-slate-100">All Reported Incidents</h3>
              <p class="text-xs text-slate-400 mt-0.5">Filter and process client files</p>
            </div>

            <!-- Technical Status Tabs -->
            <div class="flex flex-wrap gap-2">
              <button
                @click="selectedStatus = 'all'"
                :class="[
                  selectedStatus === 'all'
                    ? 'bg-primary text-white border-primary'
                    : 'bg-base-100 text-slate-400 border-base-300 hover:text-slate-300',
                  'px-3 py-1.5 text-xs font-mono border rounded-xl transition-all duration-200 cursor-pointer',
                ]"
              >
                ALL
              </button>
              <button
                @click="selectedStatus = 'pending'"
                :class="[
                  selectedStatus === 'pending'
                    ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
                    : 'bg-base-100 text-slate-400 border-base-300 hover:text-slate-300',
                  'px-3 py-1.5 text-xs font-mono border rounded-xl transition-all duration-200 cursor-pointer',
                ]"
              >
                PENDING
              </button>
              <button
                @click="selectedStatus = 'in_progress'"
                :class="[
                  selectedStatus === 'in_progress'
                    ? 'bg-blue-500/20 text-blue-400 border-blue-500/30'
                    : 'bg-base-100 text-slate-400 border-base-300 hover:text-slate-300',
                  'px-3 py-1.5 text-xs font-mono border rounded-xl transition-all duration-200 cursor-pointer',
                ]"
              >
                IN PROGRESS
              </button>
              <button
                @click="selectedStatus = 'resolved'"
                :class="[
                  selectedStatus === 'resolved'
                    ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
                    : 'bg-base-100 text-slate-400 border-base-300 hover:text-slate-300',
                  'px-3 py-1.5 text-xs font-mono border rounded-xl transition-all duration-200 cursor-pointer',
                ]"
              >
                RESOLVED
              </button>
              <button
                @click="selectedStatus = 'rejected'"
                :class="[
                  selectedStatus === 'rejected'
                    ? 'bg-red-500/20 text-red-400 border-red-500/30'
                    : 'bg-base-100 text-slate-400 border-base-300 hover:text-slate-300',
                  'px-3 py-1.5 text-xs font-mono border rounded-xl transition-all duration-200 cursor-pointer',
                ]"
              >
                REJECTED
              </button>
              <button
                @click="selectedStatus = 'verified'"
                :class="[
                  selectedStatus === 'verified'
                    ? 'bg-purple-500/20 text-purple-400 border-purple-500/30'
                    : 'bg-base-100 text-slate-400 border-base-300 hover:text-slate-300',
                  'px-3 py-1.5 text-xs font-mono border rounded-xl transition-all duration-200 cursor-pointer',
                ]"
              >
                VERIFIED
              </button>
            </div>
          </div>

          <div
            v-if="filteredIssues.length === 0"
            class="text-center py-12 border border-dashed border-base-300 rounded-2xl bg-base-100/30"
          >
            <p class="text-slate-500 text-sm">No issues found matching this filter group.</p>
          </div>

          <div v-else class="space-y-4">
            <div
              v-for="issue in filteredIssues"
              :key="issue.id"
              class="border border-base-300 rounded-2xl hover:border-primary/40 hover:shadow-lg transition-all duration-300 bg-base-100/30 overflow-hidden"
            >
              <router-link
                :to="{ name: 'AdminIssueManage', params: { id: issue.id } }"
                class="block p-5 hover:bg-base-300/10"
              >
                <!-- Header -->
                <div class="flex flex-col sm:flex-row sm:justify-between sm:items-start mb-3 gap-2">
                  <div>
                    <p class="text-lg font-bold text-slate-100">{{ issue.title }}</p>
                    <p class="text-xs text-slate-400 mt-1 line-clamp-2 leading-relaxed">
                      {{ issue.description }}
                    </p>
                  </div>
                  <div
                    class="flex items-center text-xs font-mono text-slate-500 mt-1 sm:mt-0 gap-3"
                  >
                    <span
                      :class="getStatusColor(issue.status)"
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
                      {{ new Date(issue.created_at).toLocaleDateString() }}
                    </span>
                  </div>
                </div>

                <!-- Info Row -->
                <div
                  class="flex flex-wrap items-center gap-3 text-xs font-mono text-slate-500 border-b border-base-300/50 pb-3.5 mb-3.5"
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
                </div>

                <!-- Footer -->
                <div
                  class="flex flex-col sm:flex-row sm:items-center sm:justify-between text-xs text-slate-500 font-mono"
                >
                  <div class="flex items-center mb-1 sm:mb-0">
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
                        d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                      />
                    </svg>
                    Reported by:
                    <span class="text-slate-300 ml-1"
                      >{{ issue.user?.firstname }} {{ issue.user?.lastname }}</span
                    >
                  </div>

                  <div v-if="issue.updated_at !== issue.created_at" class="flex items-center">
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
                    Updated: {{ new Date(issue.updated_at).toLocaleDateString() }}
                  </div>
                </div>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import axios from '../api/client'
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'

const authStore = useAuthStore()
const issues = ref([])
const loading = ref(false)
const error = ref('')
const zoom = ref(13)
const center = ref([28.6139, 77.209])
const selectedStatus = ref('all')

const isAdmin = computed(() => authStore.isAdmin)

const filteredIssues = computed(() => {
  if (selectedStatus.value === 'all') {
    return issues.value
  }
  return issues.value.filter((issue) => issue.status === selectedStatus.value)
})

const fetchIssues = async () => {
  if (!isAdmin.value) {
    error.value = 'Access denied. Admin privileges required.'
    return
  }

  loading.value = true
  error.value = ''
  try {
    const response = await axios.get('/api/admin/issues')
    issues.value = response.data.issues
    if (issues.value.length > 0) {
      center.value = [issues.value[0].latitude, issues.value[0].longitude]
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to fetch issues'
  } finally {
    loading.value = false
  }
}

const getStatusCount = (status) => {
  return issues.value.filter((issue) => issue.status === status).length
}

const getStatusColor = (status) => {
  const colors = {
    pending: 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20',
    in_progress: 'bg-blue-500/10 text-blue-400 border border-blue-500/20',
    resolved: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
    rejected: 'bg-red-500/10 text-red-400 border border-red-500/20',
    verified: 'bg-purple-500/10 text-purple-400 border border-purple-500/20',
  }
  return colors[status] || 'bg-slate-500/10 text-slate-400 border border-slate-500/20'
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
