<template>
  <div
    class="min-h-screen flex items-center justify-center bg-base-100 p-6 relative overflow-hidden"
  >
    <!-- Background -->
    <div class="absolute inset-0 -z-20 gradient-mesh opacity-60" />
    <div
      aria-hidden="true"
      class="pointer-events-none absolute top-1/3 left-1/4 h-80 w-80 rounded-full blur-3xl opacity-20"
      style="background: oklch(55% 0.24 255 / 0.12)"
    />
    <div
      aria-hidden="true"
      class="pointer-events-none absolute bottom-1/3 right-1/4 h-80 w-80 rounded-full blur-3xl opacity-15"
      style="background: oklch(55% 0.22 285 / 0.1)"
    />

    <div class="w-full max-w-md relative z-10">
      <!-- Card -->
      <div class="glass-strong rounded-2xl p-8 md:p-10 shadow-2xl shadow-black/40">
        <!-- Logo -->
        <div class="text-center mb-8">
          <router-link to="/" class="inline-flex items-center gap-2.5 mb-6">
            <div
              class="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center shadow-lg shadow-primary/25"
            >
              <Zap class="w-5 h-5 text-white" :stroke-width="2.5" />
            </div>
            <span class="text-xl font-bold tracking-tight"
              >City<span class="text-primary">Pulse</span></span
            >
          </router-link>
          <h2 class="text-xl font-bold text-base-content">Welcome back</h2>
          <p class="text-sm text-base-content/50 mt-1">Sign in to your account</p>
        </div>

        <!-- Form -->
        <form class="space-y-5" @submit.prevent="handleLogin">
          <div>
            <label for="identifier" class="label pb-1.5">
              <span
                class="label-text text-xs font-semibold text-base-content/60 uppercase tracking-wider"
                >Email or Phone</span
              >
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <Mail class="h-4 w-4 text-base-content/30" :stroke-width="2" />
              </div>
              <input
                id="identifier"
                name="identifier"
                type="text"
                autocomplete="email"
                required
                class="input input-bordered w-full pl-10 bg-base-300/30 border-base-300/60 focus:border-primary focus:bg-base-300/50 transition-all rounded-xl text-sm"
                placeholder="name@domain.com"
                v-model="credentials.identifier"
              />
            </div>
          </div>

          <div>
            <label for="password" class="label pb-1.5">
              <span
                class="label-text text-xs font-semibold text-base-content/60 uppercase tracking-wider"
                >Password</span
              >
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <Lock class="h-4 w-4 text-base-content/30" :stroke-width="2" />
              </div>
              <input
                id="password"
                name="password"
                type="password"
                autocomplete="current-password"
                required
                class="input input-bordered w-full pl-10 bg-base-300/30 border-base-300/60 focus:border-primary focus:bg-base-300/50 transition-all rounded-xl text-sm"
                placeholder="Enter your password"
                v-model="credentials.password"
              />
            </div>
          </div>

          <div class="flex items-center justify-between text-xs pt-1">
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" class="checkbox checkbox-sm checkbox-primary" />
              <span class="text-base-content/50">Remember me</span>
            </label>
            <router-link
              to="/forgot-password"
              class="text-primary hover:text-primary/80 font-medium transition-colors"
            >
              Forgot password?
            </router-link>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="btn btn-primary w-full rounded-xl font-semibold shadow-lg shadow-primary/20 hover:shadow-primary/30 transition-all gap-2"
          >
            <template v-if="loading">
              <span class="loading loading-spinner loading-sm"></span>
              Signing in...
            </template>
            <template v-else>
              <LogIn class="w-4 h-4" :stroke-width="2" />
              Sign in
            </template>
          </button>

          <div v-if="error" role="alert" class="alert alert-error rounded-xl text-sm">
            <CircleAlert class="w-4 h-4 shrink-0" :stroke-width="2" />
            {{ error }}
          </div>
        </form>

        <!-- Divider -->
        <div class="relative my-8">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-base-300/60"></div>
          </div>
          <div class="relative flex justify-center text-xs">
            <span
              class="px-3 bg-base-200/80 text-base-content/40 font-medium uppercase tracking-wider"
              >or continue with</span
            >
          </div>
        </div>

        <!-- Social -->
        <div class="grid grid-cols-2 gap-3">
          <a
            href="/api/auth/oauth/google"
            class="btn btn-outline border-base-300/60 hover:border-base-300 hover:bg-base-300/30 rounded-xl gap-2 text-sm font-medium"
          >
            <svg class="w-4 h-4" viewBox="0 0 24 24">
              <path
                fill="currentColor"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"
              />
              <path
                fill="currentColor"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="currentColor"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
              />
              <path
                fill="currentColor"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
              />
            </svg>
            Google
          </a>
          <a
            href="/api/auth/oauth/github"
            class="btn btn-outline border-base-300/60 hover:border-base-300 hover:bg-base-300/30 rounded-xl gap-2 text-sm font-medium"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path
                d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"
              />
            </svg>
            GitHub
          </a>
        </div>

        <!-- Register link -->
        <p class="text-center text-sm text-base-content/50 mt-8">
          Don't have an account?
          <router-link
            to="/register"
            class="text-primary hover:text-primary/80 font-semibold transition-colors ml-1"
          >
            Create account
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { Zap, Mail, Lock, LogIn, CircleAlert } from '@lucide/vue'

const router = useRouter()
const authStore = useAuthStore()

const credentials = ref({
  identifier: '',
  password: '',
})

const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  const result = await authStore.login({
    email: credentials.value.identifier.includes('@') ? credentials.value.identifier : undefined,
    phone: !credentials.value.identifier.includes('@') ? credentials.value.identifier : undefined,
    password: credentials.value.password,
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
