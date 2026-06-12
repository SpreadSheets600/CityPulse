<template>
  <div class="min-h-screen flex items-center justify-center bg-base-100 p-6 relative overflow-hidden text-base-content antialiased">
    <!-- Background mesh blobs -->
    <div aria-hidden="true"
      class="pointer-events-none absolute top-1/4 left-1/4 h-[30rem] w-[30rem] rounded-full blur-3xl opacity-20 animate-pulse-glow"
      style="background: radial-gradient(circle, rgba(59,130,246,0.35) 0%, transparent 70%)" />
    <div aria-hidden="true"
      class="pointer-events-none absolute bottom-1/4 right-1/4 h-[30rem] w-[30rem] rounded-full blur-3xl opacity-20 animate-pulse-glow"
      style="background: radial-gradient(circle, rgba(139,92,246,0.2) 0%, transparent 70%)" />

    <div class="max-w-md w-full space-y-8 relative z-10">
      <!-- Card Container -->
      <div class="glass-panel shadow-2xl rounded-3xl p-8 md:p-10 border border-base-300 bg-base-200/55 backdrop-blur-lg">
        <div class="text-center mb-8">
          <router-link to="/" class="text-3xl font-extrabold tracking-wider font-mono bg-gradient-to-r from-blue-400 via-indigo-400 to-emerald-400 bg-clip-text text-transparent hover:scale-105 transition-transform duration-200 inline-block mb-3">
            CityPulse
          </router-link>
          <h2 class="text-xl font-bold text-slate-100 font-sans">
            Sign in to your account
          </h2>
          <p class="text-xs text-slate-400 mt-1.5 font-mono">AUTHORIZED PERSONNEL ONLY</p>
        </div>

        <form class="space-y-5" @submit.prevent="handleLogin">
          <div>
            <label for="identifier" class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">Email or Phone</span></label>
            <div class="relative">
              <input id="identifier" name="identifier" type="text" autocomplete="email" required
                class="input input-bordered w-full rounded-xl pl-10 border-base-300 focus:border-primary focus:ring-1 focus:ring-primary transition-all font-sans" placeholder="name@domain.com" v-model="credentials.identifier" />
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <svg class="h-4.5 w-4.5 text-slate-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.206" />
                </svg>
              </div>
            </div>
          </div>

          <div>
            <label for="password" class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">Password</span></label>
            <div class="relative">
              <input id="password" name="password" type="password" autocomplete="current-password" required
                class="input input-bordered w-full rounded-xl pl-10 border-base-300 focus:border-primary focus:ring-1 focus:ring-primary transition-all font-sans" placeholder="••••••••" v-model="credentials.password" />
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <svg class="h-4.5 w-4.5 text-slate-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
            </div>
          </div>

          <div class="pt-2">
            <button type="submit" :disabled="loading" class="btn btn-primary w-full rounded-xl font-bold py-3.5 shadow-lg shadow-blue-500/10">
              <span v-if="loading" class="flex items-center justify-center gap-2">
                <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                VERIFYING...
              </span>
              <span v-else>SIGN IN</span>
            </button>
          </div>

          <div class="flex items-center justify-between text-xs font-mono pt-2">
            <router-link to="/forgot-password" class="text-primary hover:text-blue-400 transition-colors">
              Forgot password?
            </router-link>
            <router-link to="/register" class="text-primary hover:text-blue-400 transition-colors">
              Register account
            </router-link>
          </div>

          <div v-if="error" class="text-error text-center text-xs font-mono border border-error/20 bg-error/5 p-2.5 rounded-xl mt-4">
            {{ error }}
          </div>
        </form>

        <div class="mt-8">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-base-300"></div>
            </div>
            <div class="relative flex justify-center text-xs font-mono">
              <span class="px-3.5 bg-base-200 text-slate-500 uppercase tracking-widest text-3xs">Identity Provider</span>
            </div>
          </div>

          <div class="mt-5 grid grid-cols-2 gap-4">
            <a href="/api/auth/oauth/google" class="btn btn-outline border-base-300 hover:border-slate-500 rounded-xl w-full flex items-center justify-center font-mono text-xs">
              <svg class="w-4 h-4 mr-2" viewBox="0 0 24 24"><path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
              Google
            </a>
            <a href="/api/auth/oauth/github" class="btn btn-outline border-base-300 hover:border-slate-500 rounded-xl w-full flex items-center justify-center font-mono text-xs">
              <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
              GitHub
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const credentials = ref({
  identifier: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  const result = await authStore.login({
    email: credentials.value.identifier.includes('@') ? credentials.value.identifier : undefined,
    phone: !credentials.value.identifier.includes('@') ? credentials.value.identifier : undefined,
    password: credentials.value.password
  })

  loading.value = false

  if (result.success) {
    if (authStore.isAdmin) {
      router.push('/admin-dashboard')
    } else {
      router.push('/')
    }
  } else {
    error.value = result.error
  }
}
</script>

<style scoped>
/* Scoped styles */
</style>
