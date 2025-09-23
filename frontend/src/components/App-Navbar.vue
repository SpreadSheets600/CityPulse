<template>
  <nav class="navbar bg-base-100 shadow">
    <div class="max-w-screen-xl w-full mx-auto px-4">
      <div class="flex items-center justify-between w-full">
        <router-link to="/" class="btn btn-ghost text-2xl font-semibold">CityPulse</router-link>

        <div class="flex-none">
          <div class="dropdown dropdown-end" :class="{ 'dropdown-open': dropdownOpen }">
            <div tabindex="0" role="button" id="user-menu-button" aria-expanded="dropdownOpen"
              class="btn btn-ghost btn-circle avatar" @click="toggleDropdown">
              <div class="w-8 rounded-full">
                <img v-if="profilePictureUrl" :src="profilePictureUrl" alt="Profile" class="object-cover" />
                <div v-else
                  class="w-8 h-8 rounded-full flex items-center justify-center bg-primary text-primary-content">
                  <span class="text-xs font-semibold">{{ userInitials }}</span>
                </div>
              </div>
            </div>
            <ul tabindex="0" id="user-dropdown"
              class="menu menu-sm dropdown-content bg-base-100 rounded-box z-50 mt-3 w-52 p-2 shadow">
              <li>
                <router-link @click="closeDropdown" :to="authStore.isAdmin ? '/admin-dashboard' : '/'">
                  {{ authStore.isAdmin ? 'Admin Dashboard' : 'Dashboard' }}
                </router-link>
              </li>
              <li>
                <router-link @click="closeDropdown" to="/issues">Issues</router-link>
              </li>
              <li>
                <router-link @click="closeDropdown" to="/profile">Profile</router-link>
              </li>
              <li>
                <button @click="handleLogout" class="text-error">Log Out</button>
              </li>
            </ul>
          </div>
        </div>
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
