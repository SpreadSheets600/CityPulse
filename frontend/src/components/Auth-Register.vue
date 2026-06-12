<template>
  <div class="min-h-screen flex items-center justify-center bg-base-100 p-6 relative overflow-hidden text-base-content antialiased">
    <!-- Background mesh blobs -->
    <div aria-hidden="true"
      class="pointer-events-none absolute top-1/4 right-1/4 h-[30rem] w-[30rem] rounded-full blur-3xl opacity-20 animate-pulse-glow"
      style="background: radial-gradient(circle, rgba(139,92,246,0.3) 0%, transparent 70%)" />
    <div aria-hidden="true"
      class="pointer-events-none absolute bottom-1/4 left-1/4 h-[30rem] w-[30rem] rounded-full blur-3xl opacity-20 animate-pulse-glow"
      style="background: radial-gradient(circle, rgba(59,130,246,0.25) 0%, transparent 70%)" />

    <div class="max-w-lg w-full space-y-8 relative z-10 py-12">
      <!-- Card Container -->
      <div class="glass-panel shadow-2xl rounded-3xl p-8 md:p-10 border border-base-300 bg-base-200/55 backdrop-blur-lg">
        <div class="text-center mb-8">
          <router-link to="/" class="text-3xl font-extrabold tracking-wider font-mono bg-gradient-to-r from-blue-400 via-indigo-400 to-emerald-400 bg-clip-text text-transparent hover:scale-105 transition-transform duration-200 inline-block mb-3">
            CityPulse
          </router-link>
          <h2 class="text-xl font-bold text-slate-100 font-sans">
            Create your account
          </h2>
          <p class="text-xs text-slate-400 mt-1.5 font-mono">JOIN THE COMMUNITY ACTION NETWORK</p>
        </div>

        <form class="space-y-4" @submit.prevent="handleRegister">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label for="firstname" class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">First Name</span></label>
              <input id="firstname" name="firstname" type="text" required class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary focus:ring-1 focus:ring-primary transition-all font-sans"
                placeholder="John" v-model="userData.firstname" />
            </div>
            <div>
              <label for="lastname" class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">Last Name</span></label>
              <input id="lastname" name="lastname" type="text" required class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary focus:ring-1 focus:ring-primary transition-all font-sans"
                placeholder="Doe" v-model="userData.lastname" />
            </div>
          </div>

          <div>
            <label for="email" class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">Email</span></label>
            <input id="email" name="email" type="email" required class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary focus:ring-1 focus:ring-primary transition-all font-sans" 
              placeholder="john@example.com" v-model="userData.email" />
          </div>

          <div>
            <label for="phone" class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">Phone</span></label>
            <input id="phone" name="phone" type="tel" required class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary focus:ring-1 focus:ring-primary transition-all font-sans" 
              placeholder="+1 (555) 000-0000" v-model="userData.phone" />
          </div>

          <div>
            <label for="address" class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">Address</span></label>
            <input id="address" name="address" type="text" required class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary focus:ring-1 focus:ring-primary transition-all font-sans"
              placeholder="123 Main St, City" v-model="userData.address" />
          </div>

          <div>
            <label for="password" class="label"><span class="label-text font-mono text-xs text-slate-400 uppercase tracking-wider">Password</span></label>
            <input id="password" name="password" type="password" required class="input input-bordered w-full rounded-xl border-base-300 focus:border-primary focus:ring-1 focus:ring-primary transition-all font-sans"
              placeholder="Min. 8 characters" v-model="userData.password" />
          </div>

          <div class="pt-4">
            <button type="submit" :disabled="loading" class="btn btn-primary w-full rounded-xl font-bold py-3.5 shadow-lg shadow-blue-500/10">
              <span v-if="loading" class="flex items-center justify-center gap-2">
                <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                CREATING ACCOUNT...
              </span>
              <span v-else>CREATE ACCOUNT</span>
            </button>
          </div>

          <div class="text-center pt-2">
            <router-link to="/login" class="text-xs font-mono text-primary hover:text-blue-400 transition-colors">
              Already have an account? Sign in here
            </router-link>
          </div>

          <div v-if="error" class="text-error text-center text-xs font-mono border border-error/20 bg-error/5 p-2.5 rounded-xl mt-4">
            {{ error }}
          </div>
        </form>
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
