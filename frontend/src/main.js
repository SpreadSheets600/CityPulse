import 'leaflet/dist/leaflet.css'
import './assets/base.css'
import './api/client'

import { createPinia } from 'pinia'
import { createApp } from 'vue'

import router from './router'
import App from './App.vue'

import ImageLightbox from './components/ImageLightbox.vue'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

app.component('ImageLightbox', ImageLightbox)

import { useAuthStore } from './stores/auth'
const authStore = useAuthStore(pinia)
await authStore.initializeAuth()

app.mount('#app')
