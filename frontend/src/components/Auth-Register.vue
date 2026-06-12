<template>
  <div
    class="min-h-screen flex items-center justify-center bg-base-100 p-6 relative overflow-hidden"
  >
    <!-- Background -->
    <div class="absolute inset-0 -z-20 gradient-mesh opacity-60" />
    <div
      aria-hidden="true"
      class="pointer-events-none absolute top-1/4 right-1/4 h-80 w-80 rounded-full blur-3xl opacity-20"
      style="background: oklch(55% 0.22 285 / 0.12)"
    />
    <div
      aria-hidden="true"
      class="pointer-events-none absolute bottom-1/4 left-1/4 h-80 w-80 rounded-full blur-3xl opacity-15"
      style="background: oklch(55% 0.24 255 / 0.1)"
    />

    <div class="w-full max-w-lg relative z-10 py-8">
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
          <h2 class="text-xl font-bold text-base-content">Create your account</h2>
          <p class="text-sm text-base-content/50 mt-1">Join the community action network</p>
        </div>

        <!-- Form -->
        <form class="space-y-4" @submit.prevent="handleRegister">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label for="firstname" class="label pb-1.5">
                <span
                  class="label-text text-xs font-semibold text-base-content/60 uppercase tracking-wider"
                  >First Name</span
                >
              </label>
              <input
                id="firstname"
                name="firstname"
                type="text"
                required
                class="input input-bordered w-full bg-base-300/30 border-base-300/60 focus:border-primary focus:bg-base-300/50 transition-all rounded-xl text-sm"
                placeholder="John"
                v-model="userData.firstname"
              />
            </div>
            <div>
              <label for="lastname" class="label pb-1.5">
                <span
                  class="label-text text-xs font-semibold text-base-content/60 uppercase tracking-wider"
                  >Last Name</span
                >
              </label>
              <input
                id="lastname"
                name="lastname"
                type="text"
                required
                class="input input-bordered w-full bg-base-300/30 border-base-300/60 focus:border-primary focus:bg-base-300/50 transition-all rounded-xl text-sm"
                placeholder="Doe"
                v-model="userData.lastname"
              />
            </div>
          </div>

          <div>
            <label for="email" class="label pb-1.5">
              <span
                class="label-text text-xs font-semibold text-base-content/60 uppercase tracking-wider"
                >Email</span
              >
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <Mail class="h-4 w-4 text-base-content/30" :stroke-width="2" />
              </div>
              <input
                id="email"
                name="email"
                type="email"
                required
                class="input input-bordered w-full pl-10 bg-base-300/30 border-base-300/60 focus:border-primary focus:bg-base-300/50 transition-all rounded-xl text-sm"
                placeholder="john@example.com"
                v-model="userData.email"
              />
            </div>
          </div>

          <div>
            <label for="phone" class="label pb-1.5">
              <span
                class="label-text text-xs font-semibold text-base-content/60 uppercase tracking-wider"
                >Phone</span
              >
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <Phone class="h-4 w-4 text-base-content/30" :stroke-width="2" />
              </div>
              <input
                id="phone"
                name="phone"
                type="tel"
                required
                class="input input-bordered w-full pl-10 bg-base-300/30 border-base-300/60 focus:border-primary focus:bg-base-300/50 transition-all rounded-xl text-sm"
                placeholder="+1 (555) 000-0000"
                v-model="userData.phone"
              />
            </div>
          </div>

          <div>
            <label for="address" class="label pb-1.5">
              <span
                class="label-text text-xs font-semibold text-base-content/60 uppercase tracking-wider"
                >Address</span
              >
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <MapPin class="h-4 w-4 text-base-content/30" :stroke-width="2" />
              </div>
              <input
                id="address"
                name="address"
                type="text"
                required
                class="input input-bordered w-full pl-10 bg-base-300/30 border-base-300/60 focus:border-primary focus:bg-base-300/50 transition-all rounded-xl text-sm"
                placeholder="123 Main St, City"
                v-model="userData.address"
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
                required
                class="input input-bordered w-full pl-10 bg-base-300/30 border-base-300/60 focus:border-primary focus:bg-base-300/50 transition-all rounded-xl text-sm"
                placeholder="Min. 8 characters"
                v-model="userData.password"
              />
            </div>
          </div>

          <div class="pt-3">
            <button
              type="submit"
              :disabled="loading"
              class="btn btn-primary w-full rounded-xl font-semibold shadow-lg shadow-primary/20 hover:shadow-primary/30 transition-all gap-2"
            >
              <template v-if="loading">
                <span class="loading loading-spinner loading-sm"></span>
                Creating account...
              </template>
              <template v-else>
                <UserPlus class="w-4 h-4" :stroke-width="2" />
                Create account
              </template>
            </button>
          </div>

          <div v-if="error" role="alert" class="alert alert-error rounded-xl text-sm">
            <CircleAlert class="w-4 h-4 shrink-0" :stroke-width="2" />
            {{ error }}
          </div>
        </form>

        <!-- Login link -->
        <p class="text-center text-sm text-base-content/50 mt-8">
          Already have an account?
          <router-link
            to="/login"
            class="text-primary hover:text-primary/80 font-semibold transition-colors ml-1"
          >
            Sign in
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
import { Zap, Mail, Phone, MapPin, Lock, UserPlus, CircleAlert } from '@lucide/vue'

const router = useRouter()
const authStore = useAuthStore()

const userData = ref({
  firstname: '',
  lastname: '',
  email: '',
  phone: '',
  address: '',
  password: '',
  role: 'citizen',
})

const loading = ref(false)
const error = ref('')

const handleRegister = async () => {
  loading.value = true
  error.value = ''

  const result = await authStore.register(userData.value)

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
