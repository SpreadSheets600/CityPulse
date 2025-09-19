<template>
  <div id="app">
    <AppNavbar v-if="authStore.isAuthenticated && !isAuthRoute" />
    <router-view />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from './stores/auth'
import AppNavbar from './components/App-Navbar.vue'

const route = useRoute()
const authStore = useAuthStore()

const isAuthRoute = computed(() => {
  return route.name === 'Login' || route.name === 'Register'
})
</script>

<style>
/* Global styles */
</style>
