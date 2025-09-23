<template>
  <div class="min-h-screen bg-gradient-to-b from-white to-slate-50 text-slate-800 antialiased">
    <!-- Hero Section -->
    <section id="hero" class="hero relative isolate overflow-hidden min-h-screen flex items-center"
      aria-label="City Pulse hero">

      <div aria-hidden="true" class="absolute inset-0 -z-20 bg-cover"
        :style="{ backgroundImage: 'linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url(https://miro.medium.com/v2/1*jA8GG75oUkXovmpSm2XQtA.jpeg)' }" />

      <!-- Mesh blobs for depth -->
      <div aria-hidden="true"
        class="pointer-events-none absolute -top-24 -left-24 h-[28rem] w-[28rem] rounded-full blur-3xl opacity-20"
        style="background: radial-gradient(circle at 35% 35%, #06B6D4 0%, transparent 55%)" />
      <div aria-hidden="true"
        class="pointer-events-none absolute -bottom-24 -right-24 h-[28rem] w-[28rem] rounded-full blur-3xl opacity-20"
        style="background: radial-gradient(circle at 70% 70%, #FB7185 0%, transparent 55%)" />

      <!-- Content container -->
      <div
        class="relative mx-auto max-w-sm sm:max-w-2xl lg:max-w-7xl px-4 sm:px-6 lg:px-8 py-12 sm:py-16 lg:py-24 pb-20 sm:pb-24 w-full">
        <div class="grid gap-8 lg:gap-12 lg:items-center">
          <!-- Centered copy block -->
          <div class="motion-safe:animate-fade-up text-white text-center">
            <!-- Small live badge -->
            <div
              class="inline-flex items-center gap-2 rounded-full bg-white/10 backdrop-blur px-3 py-1 ring-1 ring-white/15 text-xs text-slate-200">
              <span class="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
              Live in your neighborhood
            </div>

            <h1 class="mt-4 text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-tight">
              Pulse your city to action.
            </h1>

            <p class="mt-5 text-lg text-slate-200/90 max-w-2xl mx-auto">
              City Pulse is the fastest way to report issues potholes, outages, safety hazards and
              mobilize verified responders with real time maps and community updates.
            </p>

            <!-- CTAs -->
            <div class="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
              <!-- Primary CTA: gradient glow + ripple + glint -->
              <router-link to="/login"
                class="group relative inline-flex items-center justify-center rounded-xl px-6 py-3 text-base font-semibold text-slate-900 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 transition active:scale-[.98] shadow-[0_0_22px_rgba(6,182,212,.35),0_10px_24px_rgba(0,0,0,.25)]"
                :style="{ background: 'linear-gradient(135deg,#06B6D4,#312E81)' }" @click="ripple">
                <span
                  class="absolute inset-0 rounded-xl bg-white/20 opacity-0 group-hover:opacity-10 transition"></span>
                <span
                  class="glint pointer-events-none absolute inset-0 rounded-xl opacity-0 group-hover:opacity-100"></span>
                <svg aria-hidden="true" class="mr-2 h-5 w-5 text-white motion-safe:animate-bob" viewBox="0 0 24 24"
                  fill="none">
                  <path d="M6 12h4l2-5 2 10 2-5h4" stroke="white" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round" />
                </svg>
                Report an Issue
              </router-link>

              <!-- Secondary CTA -->
              <a href="#reports"
                class="inline-flex items-center justify-center rounded-xl px-6 py-3 text-base font-semibold ring-1 ring-white/25 text-white/90 hover:bg-white/10 transition focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400">
                See Nearby Reports
              </a>
            </div>

            <!-- Trust bar -->
            <div class="mt-8 flex flex-wrap items-center justify-center gap-6 text-sm text-slate-300">
              <div class="inline-flex items-center gap-2">
                <svg class="h-5 w-5 text-cyan-400" viewBox="0 0 24 24" fill="none">
                  <path d="M20 7l-9 9-5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round" />
                </svg>
                <span><strong class="text-white">{{ totalIssuesText }}</strong> reports solved</span>
              </div>
              <div class="inline-flex items-center gap-2">
                <svg class="h-5 w-5 text-rose-400" viewBox="0 0 24 24" fill="none">
                  <path d="M12 11a4 4 0 1 0-4-4 4 4 0 0 0 4 4Zm0 2c-4.418 0-8 2.239-8 5v1h16v-1c0-2.761-3.582-5-8-5Z"
                    fill="currentColor" />
                </svg>
                <span><strong class="text-white">{{ volunteersText }}</strong> active volunteers</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="absolute bottom-0 left-0 right-0">
        <svg viewBox="0 0 1440 320" class="w-full">
          <path fill="white"
            d="M0,256L80,240C160,224,320,192,480,197.3C640,203,800,245,960,245.3C1120,245,1280,203,1360,181.3L1440,160V320H0Z">
          </path>
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
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M6 13.5V3.75m0 9.75a1.5 1.5 0 0 1 0 3m0-3a1.5 1.5 0 0 0 0 3m0 3.75V16.5m12-3V3.75m0 9.75a1.5 1.5 0 0 1 0 3m0-3a1.5 1.5 0 0 0 0 3m0 3.75V16.5m-6-9V3.75m0 3.75a1.5 1.5 0 0 1 0 3m0-3a1.5 1.5 0 0 0 0 3m0 9.75V10.5" />
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
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M9 6.75V15m6-6v8.25m.503 3.498 4.875-2.437c.381-.19.622-.58.622-1.006V4.82c0-.836-.88-1.38-1.628-1.006l-3.869 1.934c-.317.159-.69.159-1.006 0L9.503 3.252a1.125 1.125 0 0 0-1.006 0L3.622 5.689C3.24 5.88 3 6.27 3 6.695V19.18c0 .836.88 1.38 1.628 1.006l3.869-1.934c.317-.159.69-.159 1.006 0l4.994 2.497c.317.158.69.158 1.006 0Z" />
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
              class="flex items-center justify-center h-12 w-12 rounded-xl bg-gradient-to-br from-cyan-500 to-indigo-600 text-white shadow-neo">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round"
                  d="M9 12.75 11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 0 1-1.043 3.296 3.745 3.745 0 0 1-3.296 1.043A3.745 3.745 0 0 1 12 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 0 1-3.296-1.043 3.745 3.745 0 0 1-1.043-3.296A3.745 3.745 0 0 1 3 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 0 1 1.043-3.296 3.746 3.746 0 0 1 3.296-1.043A3.746 3.746 0 0 1 12 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 0 1 3.296 1.043 3.746 3.746 0 0 1 1.043 3.296A3.745 3.745 0 0 1 21 12Z" />
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
        <div class="items-start">
          <!-- Horizontal scrollable cards -->
          <div>
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-2xl font-bold text-slate-900">Live Nearby Reports</h2>
              <router-link to="/login" class="text-sm text-cyan-700 hover:text-cyan-600">View
                all</router-link>
            </div>
            <div class="relative">
              <div class="flex gap-4 overflow-x-auto snap-x snap-mandatory pb-3" role="list"
                aria-label="Scrollable list of recent reports">
                <!-- Report Card Template -->
                <article v-for="issue in issues" :key="issue.id" role="listitem" tabindex="0"
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

          <!-- Map below the issues -->
          <aside class="mt-8" aria-label="Map preview">
            <div class="rounded-3xl border border-slate-200 bg-white shadow-soft p-4">
              <h3 class="mb-3 font-semibold text-slate-900">Map Preview</h3>
              <div class="relative h-72 rounded-2xl overflow-hidden">
                <l-map v-model:zoom="zoom" :center="center" :use-global-leaflet="false" style="height: 100%;">
                  <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'></l-tile-layer>
                  <l-marker v-for="issue in issues" :key="issue.id" :lat-lng="[issue.latitude, issue.longitude]"
                    :class="issue.status">
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

/* Hero visual enhancements */
::v-deep(.hero) {
  position: relative;
}

::v-deep(.hero .relative) {
  backdrop-filter: blur(10px);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}


/* Soft vignette around edges */
::v-deep(.hero::before) {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: radial-gradient(120% 80% at 50% 40%, rgba(0, 0, 0, 0) 40%, rgba(0, 0, 0, 0.35) 100%);
}

/* Decorative curved mask at bottom */
::v-deep(.hero::after) {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  bottom: -1px;
  height: 120px;
  background: radial-gradient(200% 100% at 50% -20%, rgba(255, 255, 255, 0) 60%, rgba(255, 255, 255, 1) 61%);
}

@media (max-width: 640px) {

  /* Slightly stronger overlay on small screens for readability */
  ::v-deep(.hero > .absolute.inset-0) {
    background-image: linear-gradient(to right, rgba(2, 6, 23, 0.85), rgba(2, 6, 23, 0.6));
  }
}

/* Custom marker colors based on status */
::v-deep(.leaflet-marker-icon) {
  filter: hue-rotate(0deg);
}

::v-deep(.leaflet-marker-icon.pending) {
  filter: hue-rotate(45deg);
  /* Yellow tint */
}

::v-deep(.leaflet-marker-icon.in_progress) {
  filter: hue-rotate(200deg);
  /* Blue tint */
}

::v-deep(.leaflet-marker-icon.resolved) {
  filter: hue-rotate(120deg);
  /* Green tint */
}

::v-deep(.leaflet-marker-icon.rejected) {
  filter: hue-rotate(0deg);
  /* Red tint */
}

::v-deep(.leaflet-marker-icon.verified) {
  filter: hue-rotate(270deg);
  /* Purple tint */
}

/* Keyframes */
@keyframes gradient-pan {
  0% {
    background-position: 0% 50%
  }

  50% {
    background-position: 100% 50%
  }

  100% {
    background-position: 0% 50%
  }
}

@keyframes fade-up {
  0% {
    opacity: 0;
    transform: translateY(12px)
  }

  100% {
    opacity: 1;
    transform: translateY(0)
  }
}

@keyframes bob {

  0%,
  100% {
    transform: translateY(0)
  }

  50% {
    transform: translateY(-1.5px)
  }
}

@keyframes scroll-dot {
  0% {
    transform: translateY(2px);
    opacity: .9
  }

  70% {
    transform: translateY(10px);
    opacity: .4
  }

  100% {
    transform: translateY(2px);
    opacity: 0
  }
}

.animate-gradient-pan {
  animation: gradient-pan 16s ease infinite;
}

.motion-safe\:animate-fade-up {
  animation: fade-up .7s ease both;
}

.motion-safe\:animate-bob {
  animation: bob 1.4s ease-in-out infinite;
}

/* CTA ripple */
.cp-ripple {
  position: absolute;
  width: 14px;
  height: 14px;
  pointer-events: none;
  transform: translate(-50%, -50%);
  border-radius: 9999px;
  background: radial-gradient(circle at center,
      rgba(255, 255, 255, 0.55) 0%,
      rgba(255, 255, 255, 0.35) 25%,
      rgba(255, 255, 255, 0.2) 45%,
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
    transform: translate(-50%, -50%) scale(3)
  }
}

/* Button glint on hover */
.glint {
  background: linear-gradient(120deg, transparent 0%, rgba(255, 255, 255, .25) 40%, transparent 80%);
  transform: translateX(-120%);
  transition: transform .6s ease;
}

.group:hover .glint {
  transform: translateX(120%)
}

/* Scroll cue mouse + dot */
.mouse-outline {
  background: linear-gradient(to bottom, rgba(255, 255, 255, .06), transparent)
}


/* Respect reduced motion */
@media (prefers-reduced-motion: reduce) {

  .animate-gradient-pan,
  .motion-safe\:animate-fade-up,
  .motion-safe\:animate-bob,
  .cp-ripple,
  .dot {
    animation: none !important;
  }
}
</style>
