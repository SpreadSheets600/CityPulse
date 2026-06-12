<template>
  <div class="min-h-screen flex items-center justify-center bg-base-200 p-6">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold">Reset Your Password</h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Enter your email and we'll send you a reset link.
        </p>
      </div>

      <div v-if="sent" class="alert alert-success">
        <span>If an account exists with that email, a reset link has been sent.</span>
      </div>

      <form v-else class="mt-8 space-y-6" @submit.prevent="handleForgotPassword">
        <div>
          <label for="email" class="label"><span class="label-text">Email</span></label>
          <input id="email" type="email" required class="input input-bordered w-full"
            placeholder="your@email.com" v-model="email" />
        </div>

        <button type="submit" :disabled="loading" class="btn btn-primary w-full">
          {{ loading ? 'Sending...' : 'Send Reset Link' }}
        </button>

        <div v-if="error" class="alert alert-error">
          <span>{{ error }}</span>
        </div>

        <div class="text-center">
          <router-link to="/login" class="link link-primary text-sm">Back to Sign In</router-link>
        </div>
      </form>
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
