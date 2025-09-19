<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Create your account
        </h2>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="space-y-4">
          <div>
            <label for="firstname" class="block mb-2 text-sm font-medium text-gray-900">First Name</label>
            <input id="firstname" name="firstname" type="text" required
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
              placeholder="First Name" v-model="userData.firstname" />
          </div>
          <div>
            <label for="lastname" class="block mb-2 text-sm font-medium text-gray-900">Last Name</label>
            <input id="lastname" name="lastname" type="text" required
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
              placeholder="Last Name" v-model="userData.lastname" />
          </div>
          <div>
            <label for="email" class="block mb-2 text-sm font-medium text-gray-900">Email</label>
            <input id="email" name="email" type="email" required
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
              placeholder="Email" v-model="userData.email" />
          </div>
          <div>
            <label for="phone" class="block mb-2 text-sm font-medium text-gray-900">Phone</label>
            <input id="phone" name="phone" type="tel" required
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
              placeholder="Phone" v-model="userData.phone" />
          </div>
          <div>
            <label for="address" class="block mb-2 text-sm font-medium text-gray-900">Address</label>
            <input id="address" name="address" type="text" required
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
              placeholder="Address" v-model="userData.address" />
          </div>
          <div>
            <label for="password" class="block mb-2 text-sm font-medium text-gray-900">Password</label>
            <input id="password" name="password" type="password" required
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
              placeholder="Password" v-model="userData.password" />
          </div>
        </div>

        <div>
          <button type="submit" :disabled="loading"
            class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full px-5 py-2.5 text-center disabled:opacity-50">
            <span v-if="loading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                </path>
              </svg>
              Creating account...
            </span>
            <span v-else>Create account</span>
          </button>
        </div>

        <div class="text-center">
          <router-link to="/login" class="font-medium text-indigo-600 hover:text-indigo-500">
            Already have an account? Sign in here
          </router-link>
        </div>

        <div v-if="error" class="text-red-600 text-center text-sm">
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

const userData = ref({
  firstname: '',
  lastname: '',
  email: '',
  phone: '',
  address: '',
  password: '',
  role: 'citizen'
})

const loading = ref(false)
const error = ref('')

const handleRegister = async () => {
  loading.value = true
  error.value = ''

  const result = await authStore.register(userData.value)

  loading.value = false

  if (result.success) {
    router.push('/login')
  } else {
    error.value = result.error
  }
}
</script>
