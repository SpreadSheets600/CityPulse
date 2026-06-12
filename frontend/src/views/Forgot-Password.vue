<template>
  <div class="min-h-screen flex items-center justify-center bg-base-100 p-6 relative overflow-hidden text-base-content antialiased">
    <!-- Background mesh blobs -->
    <div aria-hidden="true"
      class="pointer-events-none absolute top-1/4 left-1/4 h-[30rem] w-[30rem] rounded-full blur-3xl opacity-20 animate-pulse-glow"
      style="background: radial-gradient(circle, rgba(59,130,246,0.3) 0%, transparent 70%)" />

    <div class="max-w-md w-full space-y-8 relative z-10">
      <!-- Card Container -->
      <div class="glass-panel shadow-2xl rounded-3xl p-8 md:p-10 border border-base-300 bg-base-200/55 backdrop-blur-lg">
        <div class="text-center mb-8">
          <router-link to="/" class="text-3xl font-extrabold tracking-wider font-mono bg-gradient-to-r from-blue-400 via-indigo-400 to-emerald-400 bg-clip-text text-transparent hover:scale-105 transition-transform duration-200 inline-block mb-3">
            CityPulse
          </router-link>
          <h2 class="text-xl font-bold text-slate-100 font-sans">Reset Your Password</h2>
          <p class="text-xs text-slate-400 mt-1.5 font-mono">REQUEST SECURE RESET TOKEN</p>
        </div>

        <div v-if="sent" class="border border-emerald-500/20 bg-emerald-500/5 text-emerald-400 p-4 rounded-xl text-center text-sm font-mono mb-4">
          If an account exists with that email, a reset link has been sent.
        </div>

        <form v-else class="space-y-6" @submit.prevent="handleForgotPassword">
          <div>
            <label for="email" class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">Email Address</span></label>
            <input id="email" type="email" required class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary focus:ring-1 focus:ring-primary transition-all font-sans"
              placeholder="your@email.com" v-model="email" />
          </div>

          <button type="submit" :disabled="loading" class="btn btn-primary w-full rounded-xl font-bold py-3.5 shadow-lg shadow-blue-500/10">
            {{ loading ? 'SENDING...' : 'SEND RESET LINK' }}
          </button>

          <div v-if="error" class="text-error text-center text-xs font-mono border border-error/20 bg-error/5 p-2.5 rounded-xl">
            {{ error }}
          </div>

          <div class="text-center">
            <router-link to="/login" class="text-xs font-mono text-primary hover:text-blue-400 transition-colors">Back to Sign In</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from '../api/client'

const email = ref('')
const loading = ref(false)
const error = ref('')
const sent = ref(false)

const handleForgotPassword = async () => {
  loading.value = true
  error.value = ''
  try {
    await axios.post('/api/auth/forgot-password', { email: email.value })
    sent.value = true
  } catch (e) {
    error.value = e.response?.data?.error || 'Something went wrong'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Scoped styles */
</style>
