<template>
  <div id="app">
    <AppNavbar v-if="authStore.isAuthenticated && !isAuthRoute" />
    <ErrorBoundary>
      <router-view />
    </ErrorBoundary>
    <Chatbot />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from './stores/auth'
import AppNavbar from './components/App-Navbar.vue'
import ErrorBoundary from './components/Error-Boundary.vue'
import Chatbot from './components/Chatbot.vue'

const route = useRoute()
const authStore = useAuthStore()

const isAuthRoute = computed(() => {
  return route.name === 'Login' || route.name === 'Register'
})
</script>

<style>
/* Global styles */
</style>
