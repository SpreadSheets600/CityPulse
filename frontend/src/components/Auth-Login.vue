<template>
  <div class="min-h-screen flex items-center justify-center bg-base-200 p-6">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold">
          Sign in to your account
        </h2>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="space-y-4">
          <div>
            <label for="identifier" class="label"><span class="label-text">Email or Phone</span></label>
            <input id="identifier" name="identifier" type="text" autocomplete="email" required
              class="input input-bordered w-full" placeholder="Email or Phone" v-model="credentials.identifier" />
          </div>
          <div>
            <label for="password" class="label"><span class="label-text">Password</span></label>
            <input id="password" name="password" type="password" autocomplete="current-password" required
              class="input input-bordered w-full" placeholder="Password" v-model="credentials.password" />
          </div>
        </div>

        <div>
          <button type="submit" :disabled="loading" class="btn btn-primary w-full">
            <span v-if="loading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                </path>
              </svg>
              Signing in...
            </span>
            <span v-else>Sign in</span>
          </button>
        </div>

        <div class="text-center">
          <router-link to="/register" class="link link-primary">
            Don't have an account? Register here
          </router-link>
        </div>

        <div v-if="error" class="text-error text-center text-sm">
          {{ error }}
        </div>
      </form>
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
    // Redirect admin users to admin dashboard, regular users to home
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
