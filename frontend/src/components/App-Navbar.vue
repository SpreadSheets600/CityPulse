<template>
  <nav class="navbar bg-base-200 shadow-sm">
    <div class="flex-1">
      <router-link @click="closeDropdown"
        :to="authStore.isAuthenticated ? (authStore.isAdmin ? '/admin-dashboard' : '/dashboard') : '/'"
        class="btn btn-ghost text-2xl font-semibold">CityPulse</router-link>
    </div>
    <div class="flex gap-2">
      <div v-if="authStore.isAuthenticated" class="dropdown dropdown-end" :class="{ 'dropdown-open': dropdownOpen }">
        <div tabindex="0" role="button" id="user-menu-button" aria-expanded="dropdownOpen"
          class="btn btn-ghost btn-circle avatar" @click="toggleDropdown">
          <div class="w-8 rounded-full border border-gray-300">
            <img v-if="profilePictureUrl" :src="profilePictureUrl" alt="Profile" class="object-cover" />
            <div v-else class="w-8 h-8 rounded-full flex items-center justify-center bg-primary text-primary-content">
              <span class="text-xs font-semibold">{{ userInitials }}</span>
            </div>
          </div>
        </div>
        <ul tabindex="0" id="user-dropdown"
          class="menu menu-sm dropdown-content bg-base-200 rounded-box z-1 mt-4 w-52 p-2 shadow">
          <li>
            <router-link @click="closeDropdown" :to="authStore.isAdmin ? '/admin-dashboard' : '/dashboard'">
              {{ authStore.isAdmin ? 'Admin Dashboard' : 'Dashboard' }}
            </router-link>
          </li>
          <li>
            <router-link @click="closeDropdown" to="/issues">Issues</router-link>
          </li>
          <li>
            <router-link @click="closeDropdown" to="/profile">Profile</router-link>
          </li>
          <li class="border-t border-base-100 mt-2 pt-2">
            <button @click="handleLogout" class="text-error">Log Out</button>
          </li>
        </ul>
      </div>
      <div v-else>
        <router-link to="/login" class="btn btn-ghost">
          <svg aria-hidden="true" class="h-4 w-4 text-current" viewBox="0 0 24 24" fill="none">
            <path d="M12 12a5 5 0 1 0-5-5 5 5 0 0 0 5 5Zm0 2c-4.418 0-8 2.239-8 5v1h16v-1c0-2.761-3.582-5-8-5Z"
              fill="currentColor" opacity=".9" />
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
