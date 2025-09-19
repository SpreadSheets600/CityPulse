import './assets/base.css'
import 'leaflet/dist/leaflet.css'
import './api/client'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

import { useAuthStore } from './stores/auth'
const authStore = useAuthStore(pinia)
authStore.initializeAuth()

app.mount('#app')
