<template>
  <div
    class="min-h-screen flex items-center justify-center bg-base-100 p-6 relative overflow-hidden text-base-content antialiased"
  >
    <!-- Background mesh blobs -->
    <div
      aria-hidden="true"
      class="pointer-events-none absolute bottom-1/4 right-1/4 h-[30rem] w-[30rem] rounded-full blur-3xl opacity-20 animate-pulse-glow"
      style="background: radial-gradient(circle, rgba(139, 92, 246, 0.3) 0%, transparent 70%)"
    />

    <div class="max-w-md w-full space-y-8 relative z-10">
      <!-- Card Container -->
      <div
        class="glass-panel shadow-2xl rounded-3xl p-8 md:p-10 border border-base-300 bg-base-200/55 backdrop-blur-lg"
      >
        <div class="text-center mb-8">
          <router-link
            to="/"
            class="text-3xl font-extrabold tracking-wider font-mono bg-gradient-to-r from-blue-400 via-indigo-400 to-emerald-400 bg-clip-text text-transparent hover:scale-105 transition-transform duration-200 inline-block mb-3"
          >
            CityPulse
          </router-link>
          <h2 class="text-xl font-bold text-base-content font-sans">Set New Password</h2>
          <p class="text-xs text-base-content/60 mt-1.5 font-mono">FINALIZE ACCOUNT RESTORATION</p>
        </div>

        <div
          v-if="success"
          class="border border-emerald-500/20 bg-emerald-500/5 text-emerald-400 p-4 rounded-xl text-center text-sm font-mono mb-4"
        >
          Password Reset Successfully.
          <router-link to="/login" class="text-primary hover:text-blue-400 underline ml-1"
            >Sign in</router-link
          >
        </div>

        <form v-else class="space-y-5" @submit.prevent="handleResetPassword">
          <div>
            <label for="token" class="label"
              ><span class="label-text font-mono text-xs text-base-content/60 uppercase tracking-wider"
                >Reset Token</span
              ></label
            >
            <input
              id="token"
              type="text"
              required
              class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary focus:ring-1 focus:ring-primary transition-all font-sans"
              placeholder="Paste your reset token"
              v-model="form.token"
            />
          </div>
          <div>
            <label for="password" class="label"
              ><span class="label-text font-mono text-xs text-base-content/60 uppercase tracking-wider"
                >New Password</span
              ></label
            >
            <input
              id="password"
              type="password"
              required
              minlength="8"
              class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary focus:ring-1 focus:ring-primary transition-all font-sans"
              placeholder="At least 8 characters"
              v-model="form.password"
            />
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="btn btn-primary w-full rounded-xl font-bold py-3.5 shadow-lg shadow-blue-500/10"
          >
            {{ loading ? 'RESETTING...' : 'RESET PASSWORD' }}
          </button>

          <div
            v-if="error"
            class="text-error text-center text-xs font-mono border border-error/20 bg-error/5 p-2.5 rounded-xl"
          >
            {{ error }}
          </div>

          <div class="text-center">
            <router-link
              to="/login"
              class="text-xs font-mono text-primary hover:text-blue-400 transition-colors"
              >Back to Sign In</router-link
            >
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import router from '../router'
import axios from '../api/client'

const route = useRoute()
const form = ref({ token: (route?.query?.token || router.currentRoute.value?.query?.token || ''), password: '' })
const loading = ref(false)
const error = ref('')
const success = ref(false)

const handleResetPassword = async () => {
  loading.value = true
  error.value = ''
  try {
    await axios.post('/auth/reset-password', form.value)
    success.value = true
  } catch (e) {
    error.value = e.response?.data?.error || 'Something went wrong'
  } finally {
    loading.value = false
  }
}
</script>

