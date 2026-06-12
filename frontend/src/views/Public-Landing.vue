<template>
  <div class="min-h-screen bg-base-100 text-base-content antialiased">
    <!-- Hero Section -->
    <section class="relative min-h-[100dvh] flex items-center overflow-hidden">
      <!-- Background -->
      <div class="absolute inset-0 -z-20">
        <div
          class="absolute inset-0 bg-cover bg-center opacity-30"
          :style="{
            backgroundImage:
              'url(https://images.unsplash.com/photo-1519501025264-65ba15a82390?q=80&w=1600&auto=format&fit=crop)',
          }"
        />
        <div
          class="absolute inset-0 bg-gradient-to-b from-base-100/60 via-base-100/90 to-base-100"
        />
      </div>

      <!-- Gradient mesh -->
      <div aria-hidden="true" class="absolute inset-0 -z-10 gradient-mesh opacity-60" />

      <!-- Decorative orbs -->
      <div
        aria-hidden="true"
        class="pointer-events-none absolute -top-32 -left-32 h-96 w-96 rounded-full blur-3xl opacity-30 animate-pulse-subtle"
        style="background: oklch(55% 0.24 255 / 0.15)"
      />
      <div
        aria-hidden="true"
        class="pointer-events-none absolute -bottom-32 -right-32 h-96 w-96 rounded-full blur-3xl opacity-25 animate-pulse-subtle"
        style="background: oklch(55% 0.22 285 / 0.12); animation-delay: 1.5s"
      />

      <!-- Content -->
      <div class="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-24 w-full">
        <div class="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
          <!-- Left: Copy -->
          <div class="motion-safe:animate-fade-up">
            <div
              class="inline-flex items-center gap-2 rounded-full bg-primary/10 border border-primary/20 px-3.5 py-1.5 mb-8"
            >
              <span class="h-2 w-2 rounded-full bg-accent animate-pulse-subtle" />
              <span class="text-xs font-mono font-medium text-primary tracking-wide uppercase"
                >Live in your neighborhood</span
              >
            </div>

            <h1
              class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-[1.08]"
            >
              Your city's pulse
              <br />
              <span class="text-gradient">starts here.</span>
            </h1>

            <p class="mt-6 text-lg text-base-content/60 max-w-lg leading-relaxed">
              Report issues, mobilize responders, and track real-time action. CityPulse connects
              communities with verified civic action.
            </p>

            <div class="mt-10 flex flex-col sm:flex-row gap-3">
              <router-link
                to="/register"
                class="btn btn-primary btn-lg rounded-xl shadow-lg shadow-primary/25 hover:shadow-primary/40 transition-all gap-2"
              >
                <ShieldCheck class="w-5 h-5" :stroke-width="2" />
                Report an Issue
              </router-link>
              <a
                href="#reports"
                class="btn btn-ghost btn-lg rounded-xl border border-base-300/60 hover:border-base-300 gap-2"
              >
                <MapPin class="w-5 h-5" :stroke-width="2" />
                See Nearby Reports
              </a>
            </div>

            <!-- Stats strip -->
            <div class="mt-14 flex flex-wrap items-center gap-8">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-success/10 flex items-center justify-center">
                  <CircleCheckBig class="w-5 h-5 text-success" :stroke-width="2" />
                </div>
                <div>
                  <p class="text-lg font-bold text-base-content">{{ totalIssuesText }}</p>
                  <p class="text-xs text-base-content/50 font-medium">Issues resolved</p>
                </div>
              </div>
              <div class="w-px h-10 bg-base-300/60" />
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                  <Users class="w-5 h-5 text-primary" :stroke-width="2" />
                </div>
                <div>
                  <p class="text-lg font-bold text-base-content">{{ volunteersText }}</p>
                  <p class="text-xs text-base-content/50 font-medium">Active responders</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Right: Hero visual -->
          <div class="hidden lg:block relative">
            <div
              class="relative rounded-2xl overflow-hidden border border-base-300/40 shadow-2xl shadow-black/40"
            >
              <img
                src="https://picsum.photos/seed/citypulse-hero/800/600"
                alt="City infrastructure"
                class="w-full h-auto object-cover aspect-[4/3]"
              />
              <div
                class="absolute inset-0 bg-gradient-to-t from-base-100/80 via-transparent to-transparent"
              />
              <div class="absolute bottom-4 left-4 right-4 glass rounded-xl p-4">
                <div class="flex items-center gap-3">
                  <div
                    class="w-10 h-10 rounded-full bg-success/20 flex items-center justify-center"
                  >
                    <CircleCheckBig class="w-5 h-5 text-success" :stroke-width="2" />
                  </div>
                  <div>
                    <p class="text-sm font-semibold text-base-content">
                      Pothole on Main St. resolved
                    </p>
                    <p class="text-xs text-base-content/50">2 hours ago by verified responder</p>
                  </div>
                </div>
              </div>
            </div>
            <!-- Floating stat card -->
            <div class="absolute -top-4 -right-4 glass rounded-xl p-3.5 shadow-xl animate-float">
              <div class="flex items-center gap-2.5">
                <div class="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
                  <Activity class="w-4 h-4 text-primary" :stroke-width="2" />
                </div>
                <div>
                  <p class="text-xs font-bold text-base-content">Live Feed</p>
                  <p class="text-[10px] text-base-content/50">12 reports today</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <main>
      <!-- Features Section -->
      <section class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20">
        <div class="text-center max-w-2xl mx-auto mb-16">
          <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight">Built for civic action</h2>
          <p class="mt-4 text-base-content/50 text-lg">
            Everything you need to report, track, and resolve community issues.
          </p>
        </div>

        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <!-- Feature 1 -->
          <div
            class="card bg-base-200/60 border border-base-300/40 hover:border-primary/30 transition-all duration-300 group"
          >
            <div class="card-body p-7">
              <div
                class="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors"
              >
                <Zap class="w-6 h-6 text-primary" :stroke-width="2" />
              </div>
              <h3 class="card-title text-lg">Quick Report</h3>
              <p class="text-base-content/50 text-sm leading-relaxed">
                File reports in under 30 seconds with photos, voice notes, or videos and instant
                location capture.
              </p>
            </div>
          </div>

          <!-- Feature 2 -->
          <div
            class="card bg-base-200/60 border border-base-300/40 hover:border-secondary/30 transition-all duration-300 group"
          >
            <div class="card-body p-7">
              <div
                class="w-12 h-12 rounded-xl bg-secondary/10 flex items-center justify-center mb-4 group-hover:bg-secondary/20 transition-colors"
              >
                <Map class="w-6 h-6 text-secondary" :stroke-width="2" />
              </div>
              <h3 class="card-title text-lg">Interactive Maps</h3>
              <p class="text-base-content/50 text-sm leading-relaxed">
                Visualize verified issues in your area with real-time geofencing and live
                clustering.
              </p>
            </div>
          </div>

          <!-- Feature 3 -->
          <div
            class="card bg-base-200/60 border border-base-300/40 hover:border-accent/30 transition-all duration-300 group"
          >
            <div class="card-body p-7">
              <div
                class="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center mb-4 group-hover:bg-accent/20 transition-colors"
              >
                <ShieldCheck class="w-6 h-6 text-accent" :stroke-width="2" />
              </div>
              <h3 class="card-title text-lg">AI Verification</h3>
              <p class="text-base-content/50 text-sm leading-relaxed">
                Multi-modal AI analyzes and categorizes reports instantly, filtering false entries
                automatically.
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Live Reports Section -->
      <section id="reports" class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-10 items-start">
          <!-- Feed -->
          <div class="lg:col-span-2">
            <div class="flex items-center justify-between mb-8">
              <div>
                <h2 class="text-2xl sm:text-3xl font-extrabold tracking-tight">
                  Live Nearby Reports
                </h2>
                <p class="text-sm text-base-content/50 mt-1">Real-time reports from residents</p>
              </div>
              <router-link to="/login" class="btn btn-ghost btn-sm gap-1 text-primary">
                View all
                <ChevronRight class="w-4 h-4" :stroke-width="2" />
              </router-link>
            </div>

            <div class="flex gap-5 overflow-x-auto snap-x snap-mandatory pb-4 -mx-1 px-1">
              <article
                v-for="issue in issues"
                :key="issue.id"
                class="snap-start min-w-[280px] w-[280px] card bg-base-200/60 border border-base-300/40 hover:border-primary/30 transition-all duration-300"
              >
                <!-- Thumbnail -->
                <figure class="relative h-36">
                  <img
                    v-if="issue.image_urls && issue.image_urls.length > 0"
                    :src="issue.image_urls[0]"
                    :alt="issue.title"
                    class="w-full h-full object-cover"
                  />
                  <div v-else class="w-full h-full bg-base-300/40 flex items-center justify-center">
                    <ImageIcon class="w-8 h-8 text-base-content/20" :stroke-width="1.5" />
                  </div>
                  <span
                    class="badge badge-sm absolute top-2.5 right-2.5"
                    :class="{
                      'badge-warning': issue.status === 'pending',
                      'badge-info': issue.status === 'in_progress',
                      'badge-success': issue.status === 'resolved' || issue.status === 'verified',
                      'badge-error': issue.status === 'rejected',
                    }"
                  >
                    {{ issue.status }}
                  </span>
                </figure>

                <div class="card-body p-4">
                  <h3 class="card-title text-sm leading-snug">{{ issue.title }}</h3>
                  <p class="text-xs text-base-content/50 line-clamp-2 leading-relaxed">
                    {{ issue.description }}
                  </p>
                  <div
                    class="flex items-center justify-between text-xs text-base-content/40 mt-2 pt-3 border-t border-base-300/40"
                  >
                    <span class="inline-flex items-center gap-1">
                      <MapPin class="w-3 h-3" :stroke-width="2" />
                      {{ Math.round(Math.random() * 2 + 0.5) }} km
                    </span>
                    <span>{{ timeAgo(issue.created_at) }}</span>
                  </div>
                </div>
              </article>
            </div>
          </div>

          <!-- Map Sidebar -->
          <aside class="lg:col-span-1">
            <div class="card bg-base-200/60 border border-base-300/40 p-5">
              <div class="flex items-center gap-2 mb-4">
                <div class="w-2 h-2 rounded-full bg-accent animate-pulse-subtle" />
                <h3 class="font-semibold text-sm">Interactive Map</h3>
              </div>
              <div class="relative h-72 rounded-xl overflow-hidden border border-base-300/40">
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
                      <div class="w-48 text-base-content/90">
                        <div class="space-y-1.5 text-xs">
                          <p class="font-bold border-b border-slate-700 pb-1 mb-1 text-base-content">
                            {{ issue.title }}
                          </p>
                          <p><strong>Type:</strong> {{ issue.issue_type }}</p>
                          <p class="truncate"><strong>Loc:</strong> {{ issue.address }}</p>
                          <p>
                            <strong>Status:</strong>
                            <span class="capitalize text-blue-400">{{ issue.status }}</span>
                          </p>
                        </div>
                      </div>
                    </l-popup>
                  </l-marker>
                </l-map>
              </div>
              <p class="mt-3 text-xs text-base-content/40 leading-relaxed">
                Centered on active reports. Live clustering dynamically counts reports to prevent
                noise.
              </p>
            </div>
          </aside>
        </div>
      </section>

      <!-- CTA Section -->
      <section class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20">
        <div class="relative rounded-2xl overflow-hidden gradient-primary p-12 sm:p-16 text-center">
          <div
            class="absolute inset-0 opacity-10"
            style="
              background-image: url('data:image/svg+xml,%3Csvg width=&quot;60&quot; height=&quot;60&quot; viewBox=&quot;0 0 60 60&quot; xmlns=&quot;http://www.w3.org/2000/svg&quot;%3E%3Cg fill=&quot;none&quot; fill-rule=&quot;evenodd&quot;%3E%3Cg fill=&quot;%23ffffff&quot; fill-opacity=&quot;0.4&quot;%3E%3Cpath d=&quot;M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z&quot;/%3E%3C/g%3E%3C/g%3E%3C/svg%3E');
            "
          />
          <h2 class="text-3xl sm:text-4xl font-extrabold text-white tracking-tight relative z-10">
            Make your city better
          </h2>
          <p class="mt-4 text-white/70 max-w-lg mx-auto text-lg relative z-10">
            Join thousands of citizens actively improving their neighborhoods through verified civic
            action.
          </p>
          <div class="mt-8 flex flex-col sm:flex-row gap-3 justify-center relative z-10">
            <router-link
              to="/register"
              class="btn bg-white text-primary border-none btn-lg rounded-xl hover:bg-white/90 shadow-xl gap-2"
            >
              <Rocket class="w-5 h-5" :stroke-width="2" />
              Get Started Free
            </router-link>
            <a
              href="#reports"
              class="btn btn-outline border-white/30 text-white hover:bg-white/10 btn-lg rounded-xl gap-2"
            >
              <Play class="w-5 h-5" :stroke-width="2" />
              See it in action
            </a>
          </div>
        </div>
      </section>

      <!-- Footer -->
      <footer class="border-t border-base-300/40">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16">
          <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-10">
            <!-- Brand -->
            <div class="lg:col-span-1">
              <div class="flex items-center gap-2.5 mb-4">
                <div class="w-8 h-8 rounded-lg gradient-primary flex items-center justify-center">
                  <Zap class="w-4.5 h-4.5 text-white" :stroke-width="2.5" />
                </div>
                <span class="text-lg font-bold tracking-tight"
                  >City<span class="text-primary">Pulse</span></span
                >
              </div>
              <p class="text-sm text-base-content/50 leading-relaxed max-w-xs">
                Empowering communities with real-time civic action and verified issue resolution.
              </p>
            </div>

            <!-- Product -->
            <nav>
              <h4 class="font-semibold text-sm mb-4">Product</h4>
              <ul class="space-y-2.5 text-sm text-base-content/50">
                <li>
                  <a href="#reports" class="hover:text-base-content transition-colors"
                    >Live Reports</a
                  >
                </li>
                <li>
                  <a href="#" class="hover:text-base-content transition-colors">Interactive Maps</a>
                </li>
                <li>
                  <a href="#" class="hover:text-base-content transition-colors">AI Verification</a>
                </li>
                <li><a href="#" class="hover:text-base-content transition-colors">API</a></li>
              </ul>
            </nav>

            <!-- Company -->
            <nav>
              <h4 class="font-semibold text-sm mb-4">Company</h4>
              <ul class="space-y-2.5 text-sm text-base-content/50">
                <li><a href="#" class="hover:text-base-content transition-colors">About</a></li>
                <li><a href="#" class="hover:text-base-content transition-colors">Blog</a></li>
                <li><a href="#" class="hover:text-base-content transition-colors">Careers</a></li>
                <li><a href="#" class="hover:text-base-content transition-colors">Contact</a></li>
              </ul>
            </nav>

            <!-- Legal -->
            <nav>
              <h4 class="font-semibold text-sm mb-4">Legal</h4>
              <ul class="space-y-2.5 text-sm text-base-content/50">
                <li>
                  <a href="#" class="hover:text-base-content transition-colors">Privacy Policy</a>
                </li>
                <li>
                  <a href="#" class="hover:text-base-content transition-colors">Terms of Service</a>
                </li>
                <li>
                  <a href="#" class="hover:text-base-content transition-colors">Cookie Policy</a>
                </li>
              </ul>
            </nav>
          </div>

          <div
            class="mt-12 pt-8 border-t border-base-300/40 flex flex-col sm:flex-row items-center justify-between gap-4"
          >
            <p class="text-xs text-base-content/40">
              &copy; {{ new Date().getFullYear() }} CityPulse. All rights reserved.
            </p>
            <div class="flex items-center gap-4">
              <a href="#" class="text-base-content/40 hover:text-base-content transition-colors">
                <Globe class="w-4 h-4" :stroke-width="2" />
              </a>
              <a href="#" class="text-base-content/40 hover:text-base-content transition-colors">
                <MessageCircle class="w-4 h-4" :stroke-width="2" />
              </a>
              <a href="#" class="text-base-content/40 hover:text-base-content transition-colors">
                <Briefcase class="w-4 h-4" :stroke-width="2" />
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
  Activity,
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
