<template>
  <div class="min-h-screen bg-base-100 text-base-content antialiased overflow-x-hidden">
    <!-- Hero Section -->
    <LandingHero
      :bg-image="bgImage"
      :active-word="activeWord"
      :total-issues-text="totalIssuesText"
      :volunteers-text="volunteersText"
    />

    <main>
      <!-- Features Bento Section -->
      <LandingFeatures />

      <!-- Step process Section -->
      <LandingProcess />

      <!-- Live Reports Section -->
      <LandingReports
        :issues="issues"
        :broken-images="brokenImages"
        @image-error="handleIssueImageError"
      />

      <!-- Map Section -->
      <LandingMap
        v-model:zoom="zoom"
        v-model:center="center"
        :issues="issues"
        :map-tile-url="mapTileUrl"
      />

      <!-- Bottom CTA Section -->
      <LandingCTA />

      <!-- Footer Section -->
      <LandingFooter />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from 'vue'
import bgImage from '@/assets/bg-image.jpg'
import axios from '../api/client'

// Landing components
import LandingHero from '../components/landing/LandingHero.vue'
import LandingFeatures from '../components/landing/LandingFeatures.vue'
import LandingProcess from '../components/landing/LandingProcess.vue'
import LandingReports from '../components/landing/LandingReports.vue'
import LandingMap from '../components/landing/LandingMap.vue'
import LandingCTA from '../components/landing/LandingCTA.vue'
import LandingFooter from '../components/landing/LandingFooter.vue'

const issues = ref([])
const stats = ref({ totalIssues: 0, activeVolunteers: 0 })
const zoom = ref(13)
const center = ref([28.6139, 77.209])
const brokenImages = ref([])

const totalIssuesText = computed(() => stats.value.totalIssues.toLocaleString())
const volunteersText = computed(() => stats.value.activeVolunteers.toLocaleString())

// Text Rotate Anim logic
const words = ['pulse', 'future', 'safety', 'voice', 'heartbeat']
const currentWordIndex = ref(0)
const activeWord = computed(() => words[currentWordIndex.value])
let wordInterval = null

const fetchPublicIssues = async () => {
  try {
    const response = await axios.get('/issues/public')
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

const handleIssueImageError = (id) => {
  brokenImages.value.push(id)
}

// Reactive theme tracking
const currentTheme = ref(localStorage.getItem('theme') || 'light')
const isDark = computed(() =>
  ['citypulse-dark', 'dark', 'sunset', 'dim'].includes(currentTheme.value),
)

const mapTileUrl = computed(() =>
  isDark.value
    ? 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
    : 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
)

const handleThemeChange = (e) => {
  currentTheme.value = e.detail
}

onMounted(() => {
  fetchPublicIssues()
  window.addEventListener('theme-changed', handleThemeChange)

  wordInterval = setInterval(() => {
    currentWordIndex.value = (currentWordIndex.value + 1) % words.length
  }, 2500)
})

onUnmounted(() => {
  window.removeEventListener('theme-changed', handleThemeChange)
  if (wordInterval) {
    clearInterval(wordInterval)
  }
})
</script>
