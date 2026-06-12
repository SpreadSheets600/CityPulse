<template>
  <div class="min-h-screen bg-base-100 text-base-content antialiased">
    <!-- Hero Section -->
    <section class="relative min-h-[90vh] flex items-center justify-center overflow-hidden isolate">
      <!-- Full Cover Background Image -->
      <div class="absolute inset-0 -z-20">
        <img
          :src="bgImage"
          alt="City background"
          class="w-full h-full object-cover filter brightness-[0.35] dark:brightness-[0.20]"
        />
        <div
          class="absolute inset-0 bg-gradient-to-b from-black/40 via-base-100/40 to-base-100"
        />
      </div>

      <!-- Gradient mesh background animation overlay -->
      <div aria-hidden="true" class="absolute inset-0 -z-10 gradient-mesh opacity-50" />

      <!-- Hero Content (Simple text with buttons) -->
      <div class="relative mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-32 w-full flex flex-col items-center text-center motion-safe:animate-fade-up">

        <h1
          class="text-5xl sm:text-6xl lg:text-7xl font-black tracking-tight leading-[1.05] text-white"
        >
          Your city's pulse
          <br />
          <span class="text-gradient">starts here.</span>
        </h1>

        <p class="mt-6 text-base sm:text-lg text-white/85 max-w-lg mx-auto leading-relaxed font-normal">
          Report local issues, coordinate responders, and track civic action in real time.
        </p>

        <div class="mt-10 flex flex-col sm:flex-row gap-4 justify-center w-full sm:w-auto">
          <router-link
            to="/register"
            class="btn btn-primary btn-lg rounded-2xl shadow-xl shadow-primary/25 hover:shadow-primary/40 hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200 gap-2 px-8"
          >
            <ShieldCheck class="w-5.5 h-5.5" :stroke-width="2.5" />
            Report an Issue
          </router-link>
          <a
            href="#reports"
            class="btn btn-outline border-white/30 text-white hover:bg-white/10 hover:border-white/50 btn-lg rounded-2xl hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200 gap-2 px-8"
          >
            <MapPin class="w-5.5 h-5.5 text-accent" :stroke-width="2" />
            See Nearby Reports
          </a>
        </div>

        <!-- Stats strip -->
        <div class="mt-16 pt-8 border-t border-white/10 flex flex-wrap items-center justify-center gap-12 text-white">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-2xl bg-success/25 flex items-center justify-center shadow-inner">
              <CircleCheckBig class="w-6 h-6 text-success" :stroke-width="2.2" />
            </div>
            <div class="text-left">
              <p class="text-2xl font-black tracking-tight text-white">{{ totalIssuesText }}</p>
              <p class="text-xs text-white/60 font-bold uppercase tracking-wider">Issues resolved</p>
            </div>
          </div>
          <div class="hidden sm:block w-px h-12 bg-white/20" />
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-2xl bg-primary/25 flex items-center justify-center shadow-inner">
              <Users class="w-6 h-6 text-primary-content text-white" :stroke-width="2.2" />
            </div>
            <div class="text-left">
              <p class="text-2xl font-black tracking-tight text-white">{{ volunteersText }}</p>
              <p class="text-xs text-white/60 font-bold uppercase tracking-wider">Active responders</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <main>
      <!-- Features Section -->
      <section class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-28 relative">
        <!-- Feature section header -->
        <div class="text-center max-w-3xl mx-auto mb-20">
          <span class="text-xs font-mono font-bold tracking-widest text-primary uppercase bg-primary/8 px-3 py-1.5 rounded-full">Why CityPulse?</span>
          <h2 class="text-4xl sm:text-5xl font-black tracking-tight mt-4">Built for civic action</h2>
          <p class="mt-4 text-base-content/60 text-lg leading-relaxed">
            Empowering residents and admins with intelligent, fast, and transparent tools for issue resolution.
          </p>
        </div>

        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
          <!-- Feature 1 -->
          <div
            class="card bg-base-200/50 glass-strong border-gradient hover:shadow-xl transition-all duration-300 group rounded-3xl"
          >
            <div class="card-body p-8">
              <div
                class="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center mb-6 group-hover:bg-primary/20 transition-all duration-300 shadow-sm"
              >
                <Zap class="w-6 h-6 text-primary group-hover:scale-110 transition-transform" :stroke-width="2" />
              </div>
              <h3 class="card-title text-xl font-bold">Quick Reporting</h3>
              <p class="text-base-content/55 text-sm leading-relaxed mt-2">
                File detailed reports in under 30 seconds. Attach photos, record voice notes, or record videos with automated geo-tagging.
              </p>
            </div>
          </div>

          <!-- Feature 2 -->
          <div
            class="card bg-base-200/50 glass-strong border-gradient hover:shadow-xl transition-all duration-300 group rounded-3xl"
          >
            <div class="card-body p-8">
              <div
                class="w-12 h-12 rounded-2xl bg-secondary/10 flex items-center justify-center mb-6 group-hover:bg-secondary/20 transition-all duration-300 shadow-sm"
              >
                <Map class="w-6 h-6 text-secondary group-hover:scale-110 transition-transform" :stroke-width="2" />
              </div>
              <h3 class="card-title text-xl font-bold">Interactive Maps</h3>
              <p class="text-base-content/55 text-sm leading-relaxed mt-2">
                View verified issues in your neighborhood. Live maps show status updates, and geofencing helps identify issue hotspots.
              </p>
            </div>
          </div>

          <!-- Feature 3 -->
          <div
            class="card bg-base-200/50 glass-strong border-gradient hover:shadow-xl transition-all duration-300 group rounded-3xl"
          >
            <div class="card-body p-8">
              <div
                class="w-12 h-12 rounded-2xl bg-accent/10 flex items-center justify-center mb-6 group-hover:bg-accent/20 transition-all duration-300 shadow-sm"
              >
                <ShieldCheck class="w-6 h-6 text-accent group-hover:scale-110 transition-transform" :stroke-width="2" />
              </div>
              <h3 class="card-title text-xl font-bold">AI Image Verification</h3>
              <p class="text-base-content/55 text-sm leading-relaxed mt-2">
                Advanced multi-modal computer vision verifies reports immediately upon upload to filter out false or misleading submissions.
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Live Reports Section -->
      <section id="reports" class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20 border-t border-base-300/40">
        <div class="flex items-center justify-between mb-10">
          <div>
            <span class="text-xs font-mono font-bold tracking-widest text-secondary uppercase bg-secondary/8 px-3 py-1 rounded-full">Real-time Feed</span>
            <h2 class="text-3xl font-black tracking-tight mt-3">
              Live Nearby Reports
            </h2>
          </div>
          <router-link to="/login" class="btn btn-ghost btn-sm text-primary hover:bg-primary/8 gap-1 font-bold">
            View all reports
            <ChevronRight class="w-4 h-4" :stroke-width="2.5" />
          </router-link>
        </div>

        <!-- Horizontal Scroll Cards -->
        <div class="flex gap-6 overflow-x-auto snap-x snap-mandatory pb-6 -mx-2 px-2 scrollbar-thin scrollbar-thumb-base-300 scrollbar-track-transparent">
          <article
            v-for="issue in issues"
            :key="issue.id"
            class="snap-start min-w-[310px] w-[310px] card bg-base-100 border border-base-300 shadow-md hover:shadow-xl hover:-translate-y-1 transition-all duration-300 overflow-hidden group"
          >
            <!-- Image Figure -->
            <figure class="relative h-44 overflow-hidden shrink-0">
              <img
                v-if="issue.image_urls && issue.image_urls.length > 0"
                :src="issue.image_urls[0]"
                :alt="issue.title"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <div v-else class="w-full h-full bg-base-200 flex items-center justify-center">
                <ImageIcon class="w-10 h-10 text-base-content/25" :stroke-width="1.5" />
              </div>
              <span
                class="badge badge-sm absolute top-3.5 right-3.5 uppercase font-bold tracking-wider py-2 px-2.5 shadow-sm"
                :class="{
                  'badge-warning text-warning-content': issue.status === 'pending',
                  'badge-info text-info-content': issue.status === 'in_progress',
                  'badge-success text-success-content': issue.status === 'resolved' || issue.status === 'verified',
                  'badge-error text-error-content': issue.status === 'rejected',
                }"
              >
                {{ issue.status }}
              </span>
            </figure>

            <!-- Card Body -->
            <div class="card-body p-5">
              <h3 class="font-bold text-base text-base-content line-clamp-1 group-hover:text-primary transition-colors">{{ issue.title }}</h3>
              <p class="text-xs text-base-content/60 line-clamp-2 leading-relaxed mt-1.5 h-8">
                {{ issue.description }}
              </p>
              <div
                class="flex items-center justify-between text-xs text-base-content/40 mt-4 pt-3.5 border-t border-base-200"
              >
                <span class="inline-flex items-center gap-1 font-semibold">
                  <MapPin class="w-3.5 h-3.5 text-primary" :stroke-width="2.5" />
                  {{ issue.address ? (issue.address.split(',')[0] || 'Nearby') : 'Nearby' }}
                </span>
                <span class="font-medium">{{ timeAgo(issue.created_at) }}</span>
              </div>
            </div>
          </article>
        </div>
      </section>

      <!-- Live Map Coverage Section -->
      <section class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12 border-t border-base-300/40">
        <div class="card bg-base-200/50 glass-strong border border-base-300 p-6 shadow-xl rounded-3xl">
          <div class="flex items-center justify-between mb-6 flex-wrap gap-4">
            <div class="flex items-center gap-2.5">
              <div class="w-2.5 h-2.5 rounded-full bg-accent animate-ping" />
              <h3 class="font-black text-lg uppercase tracking-wider text-base-content/90">Interactive City Map</h3>
            </div>
            <p class="text-xs text-base-content/50 leading-relaxed max-w-md">
              Aggregated visualization of active local reports. Click pin markers to inspect specific reported problems.
            </p>
          </div>
          <div class="relative h-[400px] rounded-2xl overflow-hidden border border-base-300 shadow-inner">
            <l-map
              v-model:zoom="zoom"
              :center="center"
              :use-global-leaflet="false"
              style="height: 100%"
            >
              <l-tile-layer
                 :url="mapTileUrl" attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>'
              />
              <l-marker
                v-for="issue in issues"
                :key="issue.id"
                :lat-lng="[issue.latitude, issue.longitude]"
              >
                <l-popup>
                  <div class="w-52 text-base-content/95 p-1">
                    <div class="space-y-1.5 text-xs">
                      <p class="font-black border-b border-base-300 pb-1.5 mb-1.5 text-base-content text-sm">
                        {{ issue.title }}
                      </p>
                      <p><strong>Type:</strong> {{ issue.issue_type }}</p>
                      <p class="truncate"><strong>Loc:</strong> {{ issue.address }}</p>
                      <p>
                        <strong>Status:</strong>
                        <span class="capitalize font-bold text-primary">{{ issue.status }}</span>
                      </p>
                    </div>
                  </div>
                </l-popup>
              </l-marker>
            </l-map>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <section class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20">
        <div class="relative rounded-3xl overflow-hidden gradient-primary p-12 sm:p-20 text-center shadow-3xl">
          <!-- Glow effects -->
          <div aria-hidden="true" class="absolute -top-32 -left-32 h-80 w-80 rounded-full bg-white/10 blur-3xl pointer-events-none"></div>
          <div aria-hidden="true" class="absolute -bottom-32 -right-32 h-80 w-80 rounded-full bg-accent/20 blur-3xl pointer-events-none"></div>
          <div
            class="absolute inset-0 opacity-[0.07] pointer-events-none"
            style="
              background-image: url('data:image/svg+xml,%3Csvg width=&quot;60&quot; height=&quot;60&quot; viewBox=&quot;0 0 60 60&quot; xmlns=&quot;http://www.w3.org/2000/svg&quot;%3E%3Cg fill=&quot;none&quot; fill-rule=&quot;evenodd&quot;%3E%3Cg fill=&quot;%23ffffff&quot; fill-opacity=&quot;0.4&quot;%3E%3Cpath d=&quot;M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z&quot;/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');
            "
          />
          <h2 class="text-4xl sm:text-5xl font-black text-white tracking-tight relative z-10">
            Make your city better
          </h2>
          <p class="mt-5 text-white/80 max-w-xl mx-auto text-lg sm:text-xl leading-relaxed relative z-10 font-normal">
            Join thousands of active residents who are making their neighborhoods cleaner, safer, and better through verified reporting.
          </p>
          <div class="mt-10 flex flex-col sm:flex-row gap-4 justify-center relative z-10">
            <router-link
              to="/register"
              class="btn bg-white text-primary border-none btn-lg rounded-2xl hover:bg-white/95 hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200 shadow-xl gap-2.5 px-8"
            >
              <Rocket class="w-5.5 h-5.5 text-primary" :stroke-width="2.5" />
              Get Started Free
            </router-link>
            <a
              href="#reports"
              class="btn btn-outline border-white/30 text-white hover:bg-white/10 hover:border-white/50 btn-lg rounded-2xl hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200 gap-2.5 px-8"
            >
              <Play class="w-5.5 h-5.5" :stroke-width="2.5" />
              See it in action
            </a>
          </div>
        </div>
      </section>

      <!-- Footer -->
      <footer class="border-t border-base-300/40 bg-base-100">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20">
          <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-10">
            <!-- Brand -->
            <div class="col-span-2">
              <div class="flex items-center gap-2.5 mb-5">
                <div class="w-9 h-9 rounded-xl gradient-primary flex items-center justify-center shadow-md">
                  <Zap class="w-5 h-5 text-white" :stroke-width="2.5" />
                </div>
                <span class="text-xl font-black tracking-tight"
                  >City<span class="text-primary">Pulse</span></span
                >
              </div>
              <p class="text-sm text-base-content/50 leading-relaxed max-w-xs">
                Empowering municipal teams and neighborhoods with real-time civic analytics and verified issue resolution.
              </p>
            </div>

            <!-- Product -->
            <nav class="col-span-1">
              <h4 class="font-bold text-xs uppercase tracking-widest text-base-content/80 mb-5">Product</h4>
              <ul class="space-y-3.5 text-sm text-base-content/50">
                <li>
                  <a href="#reports" class="hover:text-primary transition-colors"
                    >Live Reports</a
                  >
                </li>
                <li>
                  <a href="#" class="hover:text-primary transition-colors">Interactive Maps</a>
                </li>
                <li>
                  <a href="#" class="hover:text-primary transition-colors">AI Verification</a>
                </li>
                <li><a href="#" class="hover:text-primary transition-colors">API Portal</a></li>
              </ul>
            </nav>

            <!-- Company -->
            <nav class="col-span-1">
              <h4 class="font-bold text-xs uppercase tracking-widest text-base-content/80 mb-5">Company</h4>
              <ul class="space-y-3.5 text-sm text-base-content/50">
                <li><a href="#" class="hover:text-primary transition-colors">About Us</a></li>
                <li><a href="#" class="hover:text-primary transition-colors">Community Blog</a></li>
                <li><a href="#" class="hover:text-primary transition-colors">Careers</a></li>
                <li><a href="#" class="hover:text-primary transition-colors">Contact</a></li>
              </ul>
            </nav>

            <!-- Legal -->
            <nav class="col-span-1">
              <h4 class="font-bold text-xs uppercase tracking-widest text-base-content/80 mb-5">Legal</h4>
              <ul class="space-y-3.5 text-sm text-base-content/50">
                <li>
                  <a href="#" class="hover:text-primary transition-colors">Privacy Policy</a>
                </li>
                <li>
                  <a href="#" class="hover:text-primary transition-colors">Terms of Service</a>
                </li>
                <li>
                  <a href="#" class="hover:text-primary transition-colors">Cookie Policy</a>
                </li>
              </ul>
            </nav>
          </div>

          <!-- Footer bottom -->
          <div
            class="mt-16 pt-8 border-t border-base-300/40 flex flex-col sm:flex-row items-center justify-between gap-6"
          >
            <p class="text-xs text-base-content/40">
              &copy; {{ new Date().getFullYear() }} CityPulse. All rights reserved.
            </p>
            <div class="flex items-center gap-5">
              <a href="#" class="text-base-content/40 hover:text-primary transition-colors">
                <Globe class="w-4.5 h-4.5" :stroke-width="2" />
              </a>
              <a href="#" class="text-base-content/40 hover:text-primary transition-colors">
                <MessageCircle class="w-4.5 h-4.5" :stroke-width="2" />
              </a>
              <a href="#" class="text-base-content/40 hover:text-primary transition-colors">
                <Briefcase class="w-4.5 h-4.5" :stroke-width="2" />
              </a>
            </div>
          </div>
        </div>
      </footer>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import bgImage from '@/assets/bg-image.jpg'
import axios from '../api/client'
import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'
import {
  Zap,
  ShieldCheck,
  MapPin,
  CircleCheckBig,
  Users,
  Map,
  ChevronRight,
  ImageIcon,
  Rocket,
  Play,
  Globe,
  MessageCircle,
  Briefcase,
} from '@lucide/vue'

const issues = ref([])
const stats = ref({ totalIssues: 0, activeVolunteers: 0 })
const zoom = ref(13)
const center = ref([28.6139, 77.209])

const totalIssuesText = computed(() => stats.value.totalIssues.toLocaleString())
const volunteersText = computed(() => stats.value.activeVolunteers.toLocaleString())

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

::v-deep(.leaflet-popup-content-wrapper) {
  background-color: var(--color-base-200) !important;
  color: var(--color-base-content) !important;
  border: 1px solid var(--color-base-300) !important;
  border-radius: 12px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
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
