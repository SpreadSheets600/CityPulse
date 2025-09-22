<template>
  <nav class="bg-white border-gray-200 shadow-sm">
    <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
      <router-link to="/" class="flex items-center space-x-3 rtl:space-x-reverse">
        <span class="self-center text-2xl font-semibold whitespace-nowrap text-gray-900">CityPulse</span>
      </router-link>

      <!-- Profile dropdown and mobile menu button -->
      <!-- Desktop menu and profile dropdown -->
      <div class="flex items-center md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse relative">
        <!-- Profile dropdown button -->
        <button type="button" @click="toggleDropdown"
          class="flex border border-gray-200 text-sm rounded-full md:me-0 focus:ring-4 focus:ring-gray-300"
          id="user-menu-button" aria-expanded="dropdownOpen" data-dropdown-toggle="user-dropdown">
          <span class="sr-only">Open user menu</span>
          <img v-if="profilePictureUrl" :src="profilePictureUrl" alt="Profile"
            class="w-8 h-8 rounded-full object-cover" />
          <div v-else class="w-8 h-8 rounded-full avatar-placeholder">
            {{ userInitials }}
          </div>
        </button>

        <!-- Dropdown menu -->
        <div :class="['z-50 my-4 text-base list-none bg-white divide-y divide-gray-100 rounded-lg shadow-sm absolute top-full right-0 min-w-48',
          dropdownOpen ? 'block' : 'hidden']" id="user-dropdown">
          <div class="px-4 py-3">
            <span class="block text-sm text-gray-900">{{ user?.firstname }} {{ user?.lastname }}</span>
            <span class="block text-sm text-gray-500 truncate">{{ user?.email }}</span>
          </div>
          <ul class="py-2" aria-labelledby="user-menu-button">
            <li>
              <router-link @click="closeDropdown" :to="authStore.isAdmin ? '/admin-dashboard' : '/'"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                {{ authStore.isAdmin ? 'Admin Dashboard' : 'Dashboard' }}
              </router-link>
            </li>
            <li>
              <router-link @click="closeDropdown" to="/issues"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                Issues
              </router-link>
            </li>
            <li>
              <router-link @click="closeDropdown" to="/profile"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                Profile
              </router-link>
            </li>
            <li>
              <button @click="handleLogout"
                class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100">
                Sign out
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const dropdownOpen = ref(false)
const mobileMenuOpen = ref(false)

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
  mobileMenuOpen.value = false // Close mobile menu when opening dropdown
}

const closeDropdown = () => {
  dropdownOpen.value = false
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
  closeDropdown()
}

// Close dropdowns when clicking outside
const handleClickOutside = (event) => {
  const userMenuButton = document.getElementById('user-menu-button')
  const userDropdown = document.getElementById('user-dropdown')
  const mobileMenuButton = document.querySelector('[aria-controls="navbar-user"]')
  const mobileMenu = document.getElementById('navbar-user')

  // Close dropdown if clicking outside
  if (userMenuButton && userDropdown &&
    !userMenuButton.contains(event.target) &&
    !userDropdown.contains(event.target)) {
    dropdownOpen.value = false
  }

  // Close mobile menu if clicking outside (only on mobile)
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
/* Ensure dropdown appears above other content */
#user-dropdown {
  z-index: 50;
}

/* Smooth transitions for dropdown */
#user-dropdown {
  transition: opacity 0.15s ease-out, transform 0.15s ease-out;
}

/* Mobile menu improvements */
@media (max-width: 767px) {
  #navbar-user {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    z-index: 40;
  }
}

/* Avatar styling */
.avatar-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
}
</style>
