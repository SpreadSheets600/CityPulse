<template>
  <div class="min-h-screen bg-gradient-to-b from-white to-slate-50 text-slate-800 antialiased">
    <!-- Navbar -->
    <AppNavbar />

    <!-- Hero Section -->
    <section class="relative overflow-hidden">
      <!-- Soft background shapes -->
      <div class="pointer-events-none absolute inset-0 -z-10">
        <div class="absolute -top-20 -left-20 h-64 w-64 rounded-full bg-cyan-200/40 blur-3xl"></div>
        <div class="absolute -bottom-10 -right-16 h-72 w-72 rounded-full bg-indigo-200/40 blur-3xl"></div>
      </div>

      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-10 pb-20">
        <div class="grid lg:grid-cols-2 items-center gap-12">
          <!-- Left: Copy -->
          <div class="animate-fade-up">
            <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-tight text-slate-900">
              Pulse your city to action.
            </h1>
            <p class="mt-5 text-lg text-slate-600 max-w-2xl">
              City Pulse is the fastest way to report issues—potholes, outages, safety hazards—and
              mobilize verified responders with real‑time maps and community updates.
            </p>
            <div class="mt-8 flex flex-col sm:flex-row gap-4">
              <!-- Primary CTA -->
              <router-link to="/login"
                class="relative group inline-flex items-center justify-center rounded-xl px-6 py-3 text-base font-semibold text-white focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 transition transform active:scale-[.98] shadow-lg"
                style="background: linear-gradient(135deg, var(--cp-teal), var(--cp-indigo));">
                <span
                  class="absolute inset-0 rounded-xl bg-white/20 opacity-0 group-hover:opacity-10 transition"></span>
                <svg aria-hidden="true" class="mr-2 h-5 w-5 text-white" viewBox="0 0 24 24" fill="none">
                  <path d="M6 12h4l2-5 2 10 2-5h4" stroke="white" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round" />
                </svg>
                Report an Issue
              </router-link>
              <a href="#reports"
                class="inline-flex items-center justify-center rounded-xl px-6 py-3 text-base font-semibold ring-1 ring-slate-300 text-slate-700 hover:bg-slate-100 transition focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400">
                See Nearby Reports
              </a>
            </div>
            <!-- Trust bar -->
            <div class="mt-8 flex flex-wrap items-center gap-6 text-sm text-slate-600">
              <div class="inline-flex items-center gap-2">
                <svg class="h-5 w-5 text-cyan-600" viewBox="0 0 24 24" fill="none">
                  <path d="M20 7l-9 9-5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round" />
                </svg>
                <span><strong class="text-slate-900">{{ stats.totalIssues }}</strong> reports solved</span>
              </div>
              <div class="inline-flex items-center gap-2">
                <svg class="h-5 w-5 text-rose-500" viewBox="0 0 24 24" fill="none">
                  <path d="M12 11a4 4 0 1 0-4-4 4 4 0 0 0 4 4Zm0 2c-4.418 0-8 2.239-8 5v1h16v-1c0-2.761-3.582-5-8-5Z"
                    fill="currentColor" />
                </svg>
                <span><strong class="text-slate-900">{{ stats.activeVolunteers }}</strong> active
                  volunteers</span>
              </div>
            </div>
          </div>

          <!-- Right: Image Collage -->
          <div class="relative h-[420px] lg:h-[520px] animate-fade-up">
            <div
              class="absolute -inset-6 -z-10 bg-gradient-to-tr from-cyan-200/40 to-indigo-200/40 rounded-[3rem] blur-2xl">
            </div>
            <div class="grid grid-cols-2 gap-4 h-full">
              <div class="flex flex-col gap-4">
                <img src="https://images.unsplash.com/photo-1486308510493-aa64833637b8?auto=format&fit=crop&w=900&q=60"
                  alt="City street" class="h-56 w-full object-cover rounded-2xl shadow-soft">
                <img src="https://images.unsplash.com/photo-1508057198894-247b23fe5ade?auto=format&fit=crop&w=900&q=60"
                  alt="Community" class="h-56 w-full object-cover rounded-2xl shadow-soft">
              </div>
              <div class="flex flex-col gap-4 mt-8">
                <img src="https://images.unsplash.com/photo-1532634896-26909d0d4b6a?auto=format&fit=crop&w=900&q=60"
                  alt="Maintenance" class="h-56 w-full object-cover rounded-2xl shadow-soft">
                <img src="https://images.unsplash.com/photo-1521790361543-f645cf042ec4?auto=format&fit=crop&w=900&q=60"
                  alt="Volunteers" class="h-56 w-full object-cover rounded-2xl shadow-soft">
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Divider -->
      <div aria-hidden="true">
        <svg class="w-full h-16 text-white" preserveAspectRatio="none" viewBox="0 0 1440 100">
          <path fill="currentColor" d="M0,80 C240,20 480,20 720,80 C960,140 1200,140 1440,80 L1440,100 L0,100 Z"></path>
        </svg>
      </div>
    </section>

    <main>
      <!-- Feature strip -->
      <section class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <!-- Card -->
          <article
            class="group rounded-2xl p-6 border border-slate-200 bg-white shadow-soft transition transform hover:-translate-y-1 focus-within:-translate-y-1"
            tabindex="0">
            <div
              class="flex items-center justify-center h-12 w-12 rounded-xl bg-gradient-to-br from-cyan-500 to-indigo-600 text-white shadow-neo">
              <svg aria-hidden="true" viewBox="0 0 24 24" class="h-6 w-6">
                <path d="M3 6h18M3 12h12M3 18h6" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
              </svg>
            </div>
            <h3 class="mt-4 text-lg font-semibold">Quick Report</h3>
            <p class="mt-1 text-slate-600">File a report in under 30 seconds with photo, location, and
              category. No app download required.</p>
          </article>
          <!-- Card -->
          <article
            class="group rounded-2xl p-6 border border-slate-200 bg-white shadow-soft transition transform hover:-translate-y-1 focus-within:-translate-y-1"
            tabindex="0">
            <div
              class="flex items-center justify-center h-12 w-12 rounded-xl bg-gradient-to-br from-indigo-600 to-cyan-500 text-white shadow-neo">
              <svg aria-hidden="true" viewBox="0 0 24 24" class="h-6 w-6">
                <path
                  d="M12 2v4m0 12v4m10-10h-4M6 12H2m15.07 7.07-2.83-2.83M5.76 6.34 2.93 3.51m16.16 0-2.83 2.83M5.76 17.66l-2.83 2.83"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" />
              </svg>
            </div>
            <h3 class="mt-4 text-lg font-semibold">Real-time Map</h3>
            <p class="mt-1 text-slate-600">See issues around you with live updates and smart clustering for
              cleaner navigation.</p>
          </article>
          <!-- Card -->
          <article
            class="group rounded-2xl p-6 border border-slate-200 bg-white shadow-soft transition transform hover:-translate-y-1 focus-within:-translate-y-1"
            tabindex="0">
            <div
              class="flex items-center justify-center h-12 w-12 rounded-xl bg-gradient-to-br from-rose-400 to-cyan-500 text-white shadow-neo">
              <svg aria-hidden="true" viewBox="0 0 24 24" class="h-6 w-6">
                <path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                  stroke-linejoin="round" />
              </svg>
            </div>
            <h3 class="mt-4 text-lg font-semibold">Verified Responders</h3>
            <p class="mt-1 text-slate-600">Partnered municipal teams and trained volunteers ensure fast,
              accountable action.</p>
          </article>
        </div>
      </section>

      <!-- Live reports feed -->
      <section id="reports" class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
        <div class="lg:grid lg:grid-cols-3 lg:gap-8 items-start">
          <!-- Horizontal scrollable cards -->
          <div class="lg:col-span-2">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-2xl font-bold text-slate-900">Live Nearby Reports</h2>
              <router-link to="/login" class="text-sm text-cyan-700 hover:text-cyan-600">View
                all</router-link>
            </div>
            <div class="relative">
              <div class="flex gap-4 overflow-x-auto snap-x snap-mandatory pb-3" role="list"
                aria-label="Scrollable list of recent reports">
                <!-- Report Card Template -->
                <article v-for="issue in issues.slice(0, 6)" :key="issue.id" role="listitem" tabindex="0"
                  class="snap-start min-w-[280px] w-[280px] rounded-2xl border border-slate-200 bg-white shadow-soft transition transform hover:-translate-y-1 focus:-translate-y-1">
                  <div class="p-4">
                    <!-- Thumbnail -->
                    <div class="relative h-36 rounded-xl overflow-hidden bg-gradient-to-br from-cyan-100 to-indigo-100">
                      <img v-if="issue.image_urls && issue.image_urls.length > 0" :src="issue.image_urls[0]"
                        :alt="issue.title" class="w-full h-full object-cover" />
                    </div>
                    <h3 class="mt-3 font-semibold">{{ issue.title }}</h3>
                    <p class="mt-1 text-sm text-slate-600 line-clamp-2">{{ issue.description }}</p>
                    <div class="mt-3 flex flex-wrap items-center gap-2 text-xs text-slate-500">
                      <span
                        class="inline-flex items-center gap-1 rounded-full bg-slate-100 px-2 py-1 ring-1 ring-slate-200">
                        <svg class="h-3 w-3 text-cyan-600" viewBox="0 0 24 24" fill="none">
                          <path d="M12 2l3 7h7l-5.5 4 2 7-6.5-4.5L5 20l2-7L1.5 9H9z" fill="currentColor" opacity=".7" />
                        </svg> {{ Math.round(Math.random() * 2 + 0.5) }} km
                      </span>
                      <span>•</span><span>{{ timeAgo(issue.created_at)
                      }}</span><span>•</span><span>{{ issue.address || 'Unknown' }}</span>
                    </div>
                  </div>
                </article>
              </div>
            </div>
          </div>

          <!-- Static small map placeholder (desktop right) -->
          <aside class="hidden lg:block lg:col-span-1" aria-label="Map preview">
            <div class="sticky top-8 rounded-3xl border border-slate-200 bg-white shadow-soft p-4">
              <h3 class="mb-3 font-semibold text-slate-900">Map Preview</h3>
              <div class="relative h-72 rounded-2xl overflow-hidden">
                <l-map v-model:zoom="zoom" :center="center" :use-global-leaflet="false" style="height: 100%;">
                  <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'></l-tile-layer>
                  <l-marker v-for="issue in issues.slice(0, 10)" :key="issue.id"
                    :lat-lng="[issue.latitude, issue.longitude]">
                    <l-popup>
                      <div class="w-48 sm:w-56">
                        <div class="space-y-1 text-sm">
                          <p><strong>Type:</strong> {{ issue.issue_type }}</p>
                          <p><strong>Address:</strong> {{ issue.address }}</p>
                          <p><strong>Status:</strong> {{ issue.status }}</p>
                        </div>
                      </div>
                    </l-popup>
                  </l-marker>
                </l-map>
              </div>
              <p class="mt-3 text-sm text-slate-600">Zoomed to your neighborhood. Aggregated clusters
                reduce clutter and show activity hotspots.</p>
            </div>
          </aside>
        </div>
      </section>

      <!-- FAQ -->
      <section class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <div class="rounded-3xl border border-slate-200 p-6 bg-white shadow-soft">
          <h2 class="text-xl font-semibold text-slate-900">Quick answers</h2>
          <ul class="mt-4 grid sm:grid-cols-2 gap-4 text-slate-600 text-sm">
            <li class="rounded-lg bg-slate-50 p-4 ring-1 ring-slate-200">How quickly are reports verified?
              Typically within minutes by nearby volunteers or municipal partners.</li>
            <li class="rounded-lg bg-slate-50 p-4 ring-1 ring-slate-200">Do I need an account? No—guest
              reporting works. Accounts enable history and notifications.</li>
            <li class="rounded-lg bg-slate-50 p-4 ring-1 ring-slate-200">Is my location shared? Only
              approximate location is shown to protect privacy.</li>
            <li class="rounded-lg bg-slate-50 p-4 ring-1 ring-slate-200">Is it free? City Pulse is free for
              citizens. Municipal dashboards are offered to cities.</li>
          </ul>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="mt-12 border-t border-slate-200 bg-white/80 backdrop-blur">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <div class="flex flex-col md:flex-row items-center md:items-start justify-between gap-6">
          <div class="flex items-center gap-2">
            <span
              class="inline-flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-cyan-500 to-indigo-600">
              <svg aria-hidden="true" viewBox="0 0 24 24" class="h-4 w-4 text-white">
                <path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                  d="M3 12h3l1.5-3 2.5 6L12 6l2 8 1.5-3H21" />
              </svg>
            </span>
            <span class="text-lg font-semibold text-slate-900">City<span class="text-cyan-600"> Pulse</span></span>
          </div>
          <ul class="flex flex-wrap items-center gap-4 text-sm text-slate-600">
            <li><a href="#how" class="hover:text-slate-900">How it works</a></li>
            <li><a href="#reports" class="hover:text-slate-900">Reports</a></li>
            <li><a href="#map" class="hover:text-slate-900">Map</a></li>
            <li><a href="#faq" class="hover:text-slate-900">FAQ</a></li>
            <li><a href="#" class="hover:text-slate-900">Privacy</a></li>
            <li><a href="#" class="hover:text-slate-900">Terms</a></li>
          </ul>
          <div class="flex items-center gap-3">
            <a href="#" aria-label="Follow on X" class="p-2 rounded-lg hover:bg-slate-100">
              <svg class="h-5 w-5 text-slate-600" viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M18.244 2H21l-6.5 7.43L22 22h-5.9l-4.62-6.01L6 22H3.244l7.09-8.1L2 2h6.06l4.15 5.6L18.244 2Z" />
              </svg>
            </a>
            <a href="#" aria-label="Follow on GitHub" class="p-2 rounded-lg hover:bg-slate-100">
              <svg class="h-5 w-5 text-slate-600" viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M12 .5A11.5 11.5 0 0 0 .5 12.3c0 5.24 3.4 9.68 8.12 11.26.6.12.82-.26.82-.58 0-.28-.01-1.05-.02-2.05-3.3.73-4-1.61-4-1.61-.55-1.42-1.34-1.8-1.34-1.8-1.1-.78.08-.76.08-.76 1.22.09 1.87 1.27 1.87 1.27 1.08 1.88 2.84 1.34 3.53 1.03.11-.8.42-1.34.77-1.65-2.64-.31-5.41-1.37-5.41-6.09 0-1.35.47-2.45 1.24-3.31-.12-.31-.54-1.56.12-3.25 0 0 1-.33 3.3 1.26.96-.27 1.98-.4 3-.41 1.02 0 2.04.14 3 .4 2.3-1.59 3.3-1.26 3.3-1.26.66 1.7.24 2.94.12 3.26.77.86 1.24 1.96 1.24 3.3 0 4.73-2.78 5.77-5.43 6.08.43.37.81 1.1.81 2.22 0 1.6-.01 2.88-.01 3.28 0 .32.22.71.83.58A11.51 11.51 0 0 0 23.5 12.3 11.5 11.5 0 0 0 12 .5Z" />
              </svg>
            </a>
            <a href="#" aria-label="Follow on LinkedIn" class="p-2 rounded-lg hover:bg-slate-100">
              <svg class="h-5 w-5 text-slate-600" viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.13 1.45-2.13 2.94v5.67H9.34V9.75h3.42v1.46h.05c.48-.9 1.66-1.85 3.42-1.85 3.66 0 4.34 2.41 4.34 5.54v5.55ZM5.34 8.29a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12ZM7.12 20.45H3.56V9.75h3.56v10.7Z" />
              </svg>
            </a>
          </div>
        </div>
        <p class="mt-4 text-center text-xs text-slate-500">© {{ new Date().getFullYear() }} City Pulse. All
          rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../api/client'
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'
import AppNavbar from '../components/App-Navbar.vue'

const issues = ref([])
const stats = ref({ totalIssues: 0, activeVolunteers: 0 })
const zoom = ref(13)
const center = ref([28.6139, 77.2090]) // Default to Delhi

const fetchPublicIssues = async () => {
  try {
    const response = await axios.get('/api/issues/public')
    issues.value = response.data.issues
    stats.value.totalIssues = issues.value.length
    stats.value.activeVolunteers = Math.floor(Math.random() * 500) + 200 // Mock data
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
:root {
  --cp-teal: #06B6D4;
  --cp-indigo: #4F46E5;
}

.shadow-soft {
  box-shadow: 0 10px 30px rgba(2, 6, 23, 0.06);
}

.animate-fade-up {
  animation: fade-up 0.7s ease both;
}

@keyframes fade-up {
  0% {
    opacity: 0;
    transform: translateY(12px);
  }

  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-clamp: 2;
  overflow: hidden;
}
</style>
