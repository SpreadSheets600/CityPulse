<template>
  <div
    class="min-h-screen flex items-center justify-center bg-base-100 p-6 relative overflow-hidden isolate"
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
import { useAuthStore } from '../../stores/auth'
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
