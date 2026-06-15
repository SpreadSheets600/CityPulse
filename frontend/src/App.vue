<template>
  <div id="app">
    <AppNavbar v-if="!isAuthRoute" />
    <ErrorBoundary>
      <router-view />
    </ErrorBoundary>
    <Chatbot />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import router from './router'
import AppNavbar from './components/layout/App-Navbar.vue'
import ErrorBoundary from './components/common/Error-Boundary.vue'
import Chatbot from './components/layout/Chatbot.vue'

const route = useRoute()

const routeName = computed(() => route?.name || router.currentRoute.value?.name)

const isAuthRoute = computed(() => {
  return routeName.value === 'Login' || routeName.value === 'Register'
})
</script>

