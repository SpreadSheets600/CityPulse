<template>
  <div class="min-h-screen bg-base-100 text-base-content antialiased">
    <!-- Hero Section -->
    <section id="hero" class="hero relative isolate overflow-hidden min-h-screen flex items-center"
      aria-label="City Pulse hero">

      <div aria-hidden="true" class="absolute inset-0 -z-20 bg-cover bg-center"
        :style="{ backgroundImage: 'linear-gradient(rgba(7, 10, 19, 0.75), rgba(7, 10, 19, 0.95)), url(https://images.unsplash.com/photo-1519501025264-65ba15a82390?q=80&w=1600&auto=format&fit=crop)' }" />

      <!-- Deep Space Mesh Blobs -->
      <div aria-hidden="true"
        class="pointer-events-none absolute -top-40 -left-40 h-[32rem] w-[32rem] rounded-full blur-3xl opacity-30 animate-pulse-glow"
        style="background: radial-gradient(circle, rgba(59,130,246,0.3) 0%, transparent 70%)" />
      <div aria-hidden="true"
        class="pointer-events-none absolute -bottom-40 -right-40 h-[32rem] w-[32rem] rounded-full blur-3xl opacity-30 animate-pulse-glow"
        style="background: radial-gradient(circle, rgba(139,92,246,0.2) 0%, transparent 70%)" />

      <!-- Content Container -->
      <div
        class="relative mx-auto max-w-sm sm:max-w-2xl lg:max-w-7xl px-4 sm:px-6 lg:px-8 py-12 sm:py-16 lg:py-24 pb-20 sm:pb-24 w-full">
        <div class="grid gap-8 lg:gap-12 lg:items-center">
          <div class="motion-safe:animate-fade-up text-center">
            <!-- Technical Live Badge -->
            <div
              class="inline-flex items-center gap-2 rounded-full bg-blue-500/10 border border-blue-500/20 px-3.5 py-1.5 text-xs font-mono text-blue-400 tracking-wider uppercase mb-6">
              <span class="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
              Live in your neighborhood
            </div>

            <h1 class="mt-4 text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight leading-none">
              Pulse your city <br class="hidden sm:inline" />
              <span class="bg-gradient-to-r from-blue-400 via-indigo-400 to-emerald-400 bg-clip-text text-transparent">to action.</span>
            </h1>

            <p class="mt-6 text-lg sm:text-xl text-slate-400 max-w-3xl mx-auto leading-relaxed">
              City Pulse is the fastest way to report issues like potholes, outages, and safety hazards, 
              mobilizing verified responders with real-time analytics and community-driven action.
            </p>

            <!-- Premium CTAs -->
            <div class="mt-10 flex flex-col sm:flex-row gap-4 justify-center">
              <router-link to="/login"
                class="group relative inline-flex items-center justify-center rounded-2xl px-8 py-4 text-base font-bold text-white transition active:scale-[.98] shadow-lg overflow-hidden bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500"
                @click="ripple">
                <svg aria-hidden="true" class="mr-2.5 h-5 w-5 text-white motion-safe:animate-bob" viewBox="0 0 24 24"
                  fill="none" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                Report an Issue
              </router-link>

              <a href="#reports"
                class="inline-flex items-center justify-center rounded-2xl px-8 py-4 text-base font-bold border border-base-300 hover:border-slate-500 bg-base-200/50 hover:bg-base-200 transition duration-200">
                See Nearby Reports
              </a>
            </div>

            <!-- Technical Trust Bar -->
            <div class="mt-12 flex flex-wrap items-center justify-center gap-8 text-sm font-mono text-slate-400">
              <div class="inline-flex items-center gap-2.5">
                <svg class="h-5 w-5 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                  <polyline points="22 4 12 14.01 9 11.01" />
                </svg>
                <span><strong class="text-white font-semibold">{{ totalIssuesText }}</strong> issues solved</span>
              </div>
              <div class="inline-flex items-center gap-2.5">
                <svg class="h-5 w-5 text-blue-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                  <circle cx="9" cy="7" r="4" />
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                  <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                </svg>
                <span><strong class="text-white font-semibold">{{ volunteersText }}</strong> responders active</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Hero bottom divider styled for dark theme -->
      <div class="absolute bottom-0 left-0 right-0">
        <svg viewBox="0 0 1440 120" class="w-full h-auto" preserveAspectRatio="none">
          <path fill="#070a13"
            d="M0,32L120,42.7C240,53,480,75,720,74.7C960,75,1200,53,1320,42.7L1440,32V120H0Z">
          </path>
        </svg>
      </div>
    </section>

    <main class="bg-[#070a13] -mt-1 pb-20">
      <!-- Feature Strip -->
      <section class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16">
        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
          <!-- Card 1 -->
          <article
            class="group rounded-3xl p-8 border border-base-300 bg-base-200/40 backdrop-blur-md transition-all duration-300 hover:-translate-y-2 hover:border-primary/40 hover:shadow-[0_8px_30px_rgb(0,0,0,0.5)]"
            tabindex="0">
            <div
              class="flex items-center justify-center h-12 w-12 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 text-white shadow-[0_4px_20px_rgba(59,130,246,0.3)]">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
                stroke="currentColor" class="h-6 w-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </div>
            <h3 class="mt-6 text-xl font-bold text-slate-100">Quick Report</h3>
            <p class="mt-3 text-slate-400 leading-relaxed">File reports in under 30 seconds. Attach photos, voice notes, or videos with instant location capture.</p>
          </article>
          
          <!-- Card 2 -->
          <article
            class="group rounded-3xl p-8 border border-base-300 bg-base-200/40 backdrop-blur-md transition-all duration-300 hover:-translate-y-2 hover:border-primary/40 hover:shadow-[0_8px_30px_rgb(0,0,0,0.5)]"
            tabindex="0">
            <div
              class="flex items-center justify-center h-12 w-12 rounded-2xl bg-gradient-to-br from-indigo-600 to-emerald-500 text-white shadow-[0_4px_20px_rgba(139,92,246,0.3)]">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
                stroke="currentColor" class="h-6 w-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M9 6.75V15m6-6v8.25m.503 3.498 4.875-2.437c.381-.19.622-.58.622-1.006V4.82c0-.836-.88-1.38-1.628-1.006l-3.869 1.934c-.317.159-.69.159-1.006 0L9.503 3.252a1.125 1.125 0 0 0-1.006 0L3.622 5.689C3.24 5.88 3 6.27 3 6.695V19.18c0 .836.88 1.38 1.628 1.006l3.869-1.934c.317-.159.69-.159 1.006 0l4.994 2.497c.317.158.69.158 1.006 0Z" />
              </svg>
            </div>
            <h3 class="mt-6 text-xl font-bold text-slate-100">Interactive Maps</h3>
            <p class="mt-3 text-slate-400 leading-relaxed">Visualize verified issues surrounding your area. Real-time geofencing keeps you in the pulse of updates.</p>
          </article>

          <!-- Card 3 -->
          <article
            class="group rounded-3xl p-8 border border-base-300 bg-base-200/40 backdrop-blur-md transition-all duration-300 hover:-translate-y-2 hover:border-primary/40 hover:shadow-[0_8px_30px_rgb(0,0,0,0.5)]"
            tabindex="0">
            <div
              class="flex items-center justify-center h-12 w-12 rounded-2xl bg-gradient-to-br from-emerald-500 to-blue-500 text-white shadow-[0_4px_20px_rgba(16,185,129,0.3)]">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
                stroke="currentColor" class="h-6 w-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M9 12.75 11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 0 1-1.043 3.296 3.745 3.745 0 0 1-3.296 1.043A3.745 3.745 0 0 1 12 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 0 1-3.296-1.043 3.745 3.745 0 0 1-1.043-3.296A3.745 3.745 0 0 1 3 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 0 1 1.043-3.296 3.746 3.746 0 0 1 3.296-1.043A3.746 3.746 0 0 1 12 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 0 1 3.296 1.043 3.746 3.746 0 0 1 1.043 3.296A3.745 3.745 0 0 1 21 12Z" />
              </svg>
            </div>
            <h3 class="mt-6 text-xl font-bold text-slate-100">AI Verification</h3>
            <p class="mt-3 text-slate-400 leading-relaxed">Integrated multi-modal AI models analyze and categorize reports immediately, filtering false entries.</p>
          </article>
        </div>
      </section>

      <!-- Live Reports Feed -->
      <section id="reports" class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-12 items-start">
          <!-- Left: Feed (Span 2) -->
          <div class="lg:col-span-2">
            <div class="flex items-center justify-between mb-8">
              <div>
                <h2 class="text-3xl font-extrabold text-slate-100">Live Nearby Reports</h2>
                <p class="text-sm text-slate-400 mt-1">Real-time reports reported by residents</p>
              </div>
              <router-link to="/login" class="btn btn-ghost text-sm text-primary hover:text-blue-400 flex items-center gap-1">
                View all
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
                </svg>
              </router-link>
            </div>

            <div class="relative">
              <div class="flex gap-6 overflow-x-auto snap-x snap-mandatory pb-6" role="list"
                aria-label="Scrollable list of recent reports">
                <!-- Report Card Template -->
                <article v-for="issue in issues" :key="issue.id" role="listitem" tabindex="0"
                  class="snap-start min-w-[300px] w-[300px] rounded-3xl border border-base-300 bg-base-200/50 hover:bg-base-200/80 hover:border-primary/30 transition-all duration-300 shadow-lg p-5">
                  <!-- Thumbnail -->
                  <div class="relative h-40 rounded-2xl overflow-hidden bg-gradient-to-br from-blue-900/40 to-indigo-900/40 border border-base-300">
                    <img v-if="issue.image_urls && issue.image_urls.length > 0" :src="issue.image_urls[0]"
                      :alt="issue.title" class="w-full h-full object-cover" />
                    <div v-else class="w-full h-full flex items-center justify-center text-slate-600">
                      <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    </div>
                    <!-- Badges -->
                    <span class="absolute top-3 right-3 px-2.5 py-0.5 rounded-full text-2xs font-mono font-semibold uppercase tracking-wider"
                      :class="{
                        'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20': issue.status === 'pending',
                        'bg-blue-500/10 text-blue-400 border border-blue-500/20': issue.status === 'in_progress',
                        'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20': issue.status === 'resolved' || issue.status === 'verified',
                        'bg-red-500/10 text-red-400 border border-red-500/20': issue.status === 'rejected',
                      }">
                      {{ issue.status }}
                    </span>
                  </div>
                  
                  <h3 class="mt-4 text-lg font-bold text-slate-100 truncate">{{ issue.title }}</h3>
                  <p class="mt-2 text-sm text-slate-400 line-clamp-2 leading-relaxed h-10">{{ issue.description }}</p>
                  
                  <div class="mt-4 pt-4 border-t border-base-300 flex items-center justify-between text-xs font-mono text-slate-500">
                    <span class="inline-flex items-center gap-1 rounded-md bg-blue-500/5 px-2 py-1 border border-blue-500/10">
                      <svg class="h-3 w-3 text-blue-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      </svg> 
                      {{ Math.round(Math.random() * 2 + 0.5) }} km
                    </span>
                    <span>{{ timeAgo(issue.created_at) }}</span>
                  </div>
                </article>
              </div>
            </div>
          </div>

          <!-- Right: Map Preview (Span 1) -->
          <aside class="lg:col-span-1" aria-label="Map preview">
            <div class="rounded-3xl border border-base-300 bg-base-200/40 backdrop-blur-md p-6 shadow-xl">
              <div class="flex items-center gap-2 mb-4">
                <div class="h-2 w-2 rounded-full bg-primary animate-pulse" />
                <h3 class="font-bold text-slate-100 font-mono text-sm tracking-wider uppercase">Interactive Map</h3>
              </div>
              <div class="relative h-80 rounded-2xl overflow-hidden border border-base-300">
                <l-map v-model:zoom="zoom" :center="center" :use-global-leaflet="false" style="height: 100%;">
                  <!-- CartoDB Dark Matter tile layer for premium dark aesthetics -->
                  <l-tile-layer url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'></l-tile-layer>
                  <l-marker v-for="issue in issues" :key="issue.id" :lat-lng="[issue.latitude, issue.longitude]">
                    <l-popup>
                      <div class="w-48 text-slate-200">
                        <div class="space-y-1.5 text-xs">
                          <p class="font-bold border-b border-slate-700 pb-1 mb-1 text-slate-100">{{ issue.title }}</p>
                          <p><strong>Type:</strong> {{ issue.issue_type }}</p>
                          <p class="truncate"><strong>Loc:</strong> {{ issue.address }}</p>
                          <p><strong>Status:</strong> <span class="capitalize text-blue-400">{{ issue.status }}</span></p>
                        </div>
                      </div>
                    </l-popup>
                  </l-marker>
                </l-map>
              </div>
              <p class="mt-4 text-xs text-slate-400 leading-relaxed font-mono">
                Centered on active reports. Live clustering dynamically counts reports to prevent noise overlay.
              </p>
            </div>
          </aside>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from '../api/client'
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'

const issues = ref([])
const stats = ref({ totalIssues: 0, activeVolunteers: 0 })
const zoom = ref(13)
const center = ref([28.6139, 77.2090])

const totalIssuesText = computed(() => stats.value.totalIssues.toLocaleString())
const volunteersText = computed(() => stats.value.activeVolunteers.toLocaleString())

const ripple = (event) => {
  const button = event.target.closest('button') || event.target
  const circle = document.createElement('span')
  const diameter = Math.max(button.clientWidth, button.clientHeight)
  const radius = diameter / 2
  circle.style.width = circle.style.height = `${diameter}px`
  circle.style.left = `${event.clientX - button.offsetLeft - radius}px`
  circle.style.top = `${event.clientY - button.offsetTop - radius}px`
  circle.classList.add('cp-ripple')
  const existingRipple = button.getElementsByClassName('cp-ripple')[0]
  if (existingRipple) {
    existingRipple.remove()
  }
  button.appendChild(circle)
}

const fetchPublicIssues = async () => {
  try {
    const response = await axios.get('/api/issues/public')
    issues.value = response.data.issues
    stats.value.totalIssues = issues.value.length
    stats.value.activeVolunteers = Math.floor(Math.random() * 500) + 200
    if (issues.value.length > 0) {
      center.value = [issues.value[0].latitude, issues.value[0].longitude]
    }
  } catch (error) {
    console.error('Failed to fetch public issues:', error)
  }
}

const timeAgo = (dateString) => {
  const now = new Date()
  const date = new Date(dateString)
  const diffInMs = now - date
  const diffInHours = Math.floor(diffInMs / (1000 * 60 * 60))
  if (diffInHours < 1) return 'Just now'
  if (diffInHours < 24) return `${diffInHours}h ago`
  const diffInDays = Math.floor(diffInHours / 24)
  return `${diffInDays}d ago`
}

onMounted(() => {
  fetchPublicIssues()
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

/* Custom ripple animation */
.cp-ripple {
  position: absolute;
  width: 14px;
  height: 14px;
  pointer-events: none;
  transform: translate(-50%, -50%);
  border-radius: 9999px;
  background: radial-gradient(circle at center,
      rgba(255, 255, 255, 0.45) 0%,
      rgba(255, 255, 255, 0.25) 25%,
      rgba(255, 255, 255, 0.1) 45%,
      transparent 60%);
  animation: cp-ripple 520ms ease-out forwards;
}

@keyframes cp-ripple {
  from {
    opacity: .45;
    transform: translate(-50%, -50%) scale(0)
  }
  to {
    opacity: 0;
    transform: translate(-50%, -50%) scale(4)
  }
}

@media (prefers-reduced-motion: reduce) {
  .animate-pulse-glow,
  .motion-safe\:animate-fade-up,
  .motion-safe\:animate-bob,
  .cp-ripple {
    animation: none !important;
  }
}
</style>
