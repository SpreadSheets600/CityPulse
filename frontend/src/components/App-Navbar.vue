<template>
  <nav class="navbar sticky top-0 z-50 glass-panel shadow-lg px-4 md:px-8 transition-all duration-300">
    <div class="flex-1">
      <router-link @click="closeDropdown"
        :to="authStore.isAuthenticated ? (authStore.isAdmin ? '/admin-dashboard' : '/dashboard') : '/'"
        class="btn btn-ghost text-2xl font-extrabold tracking-wider font-mono bg-gradient-to-r from-blue-400 via-indigo-400 to-emerald-400 bg-clip-text text-transparent hover:scale-105 transition-transform duration-200">
        CityPulse<span class="text-xs text-primary font-sans font-medium px-1.5 py-0.5 rounded-md bg-blue-500/10 border border-blue-500/20 ml-2">SaaS</span>
      </router-link>
    </div>
    <div class="flex gap-4">
      <div v-if="authStore.isAuthenticated" class="dropdown dropdown-end" :class="{ 'dropdown-open': dropdownOpen }">
        <div tabindex="0" role="button" id="user-menu-button" :aria-expanded="dropdownOpen"
          class="btn btn-ghost btn-circle avatar ring-2 ring-primary/20 hover:ring-primary/60 transition-all duration-300" @click="toggleDropdown">
          <div class="w-9 rounded-full">
            <img v-if="profilePictureUrl" :src="profilePictureUrl" alt="Profile" class="object-cover" />
            <div v-else class="w-9 h-9 rounded-full flex items-center justify-center bg-gradient-to-br from-blue-600 to-indigo-600 text-white font-mono">
              <span class="text-sm font-semibold">{{ userInitials }}</span>
            </div>
          </div>
        </div>
        <ul tabindex="0" id="user-dropdown"
          class="menu menu-sm dropdown-content bg-base-200 border border-base-300 rounded-2xl z-[100] mt-4 w-56 p-2.5 shadow-2xl backdrop-blur-md">
          <div class="px-3 py-2 border-b border-base-300 mb-2">
            <p class="text-xs text-slate-400">Signed in as</p>
            <p class="text-sm font-semibold text-slate-200 truncate">{{ user?.firstname }} {{ user?.lastname }}</p>
          </div>
          <li>
            <router-link @click="closeDropdown" :to="authStore.isAdmin ? '/admin-dashboard' : '/dashboard'" class="py-2.5 rounded-xl hover:bg-base-300 transition-colors">
              <svg class="w-4 h-4 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
              {{ authStore.isAdmin ? 'Admin Dashboard' : 'Dashboard' }}
            </router-link>
          </li>
          <li>
            <router-link @click="closeDropdown" to="/issues" class="py-2.5 rounded-xl hover:bg-base-300 transition-colors">
              <svg class="w-4 h-4 text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
              </svg>
              Issues
            </router-link>
          </li>
          <li>
            <router-link @click="closeDropdown" to="/profile" class="py-2.5 rounded-xl hover:bg-base-300 transition-colors">
              <svg class="w-4 h-4 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              Profile
            </router-link>
          </li>
          <li class="border-t border-base-300 mt-2 pt-2">
            <button @click="handleLogout" class="py-2.5 rounded-xl text-error hover:bg-error/10 transition-colors">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Log Out
            </button>
          </li>
        </ul>
      </div>
      <div v-else>
        <router-link to="/login" class="btn btn-outline btn-primary btn-sm rounded-xl px-4 flex items-center gap-1.5 transition-all duration-300">
          <svg aria-hidden="true" class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          <span>Sign in</span>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const mobileMenuOpen = ref(false)
const dropdownOpen = ref(false)

const user = computed(() => authStore.user)

const userInitials = computed(() => {
  if (!user.value) return 'U'
  const first = user.value.firstname?.charAt(0) || ''
  const last = user.value.lastname?.charAt(0) || ''
  return (first + last).toUpperCase() || 'U'
})

const profilePictureUrl = computed(() => {
  if (!user.value) return null
  return user.value.profile_picture || `https://api.dicebear.com/9.x/notionists-neutral/svg?seed=${user.value.firstname}${user.value.lastname}`
})

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
  mobileMenuOpen.value = false
}

const closeDropdown = () => {
  dropdownOpen.value = false
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
  closeDropdown()
}

const handleClickOutside = (event) => {
  const mobileMenuButton = document.querySelector('[aria-controls="navbar-user"]')
  const userMenuButton = document.getElementById('user-menu-button')
  const userDropdown = document.getElementById('user-dropdown')
  const mobileMenu = document.getElementById('navbar-user')

  if (userMenuButton && userDropdown &&
    !userMenuButton.contains(event.target) &&
    !userDropdown.contains(event.target)) {
    dropdownOpen.value = false
  }

  if (window.innerWidth < 768 && mobileMenuButton && mobileMenu &&
    !mobileMenuButton.contains(event.target) &&
    !mobileMenu.contains(event.target)) {
    mobileMenuOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* no custom styles needed; DaisyUI handles dropdown/avatars */
</style>
