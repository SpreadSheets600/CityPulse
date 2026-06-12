<template>
  <div class="min-h-screen flex items-center justify-center bg-base-200 p-6">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold">Set New Password</h2>
      </div>

      <div v-if="success" class="alert alert-success">
        <span>Password Reset Successfully. <router-link to="/login" class="link">Sign in</router-link></span>
      </div>

      <form v-else class="mt-8 space-y-6" @submit.prevent="handleResetPassword">
        <div>
          <label for="token" class="label"><span class="label-text">Reset Token</span></label>
          <input id="token" type="text" required class="input input-bordered w-full"
            placeholder="Paste your reset token" v-model="form.token" />
        </div>
        <div>
          <label for="password" class="label"><span class="label-text">New Password</span></label>
          <input id="password" type="password" required minlength="8" class="input input-bordered w-full"
            placeholder="At least 8 characters" v-model="form.password" />
        </div>

        <button type="submit" :disabled="loading" class="btn btn-primary w-full">
          {{ loading ? 'Resetting...' : 'Reset Password' }}
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
import { useRoute } from 'vue-router'
import axios from '../api/client'

const route = useRoute()
const form = ref({ token: route.query.token || '', password: '' })
const loading = ref(false)
const error = ref('')
const success = ref(false)

const handleResetPassword = async () => {
  loading.value = true
  error.value = ''
  try {
    await axios.post('/api/auth/reset-password', form.value)
    success.value = true
  } catch (e) {
    error.value = e.response?.data?.error || 'Something went wrong'
  } finally {
    loading.value = false
  }
}
</script>
