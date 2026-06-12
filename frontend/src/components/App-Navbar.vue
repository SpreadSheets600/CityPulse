<template>
  <nav class="navbar sticky top-0 z-50 glass-strong px-4 md:px-6 transition-all duration-300">
    <div class="navbar-start">
      <router-link
        @click="closeDropdown"
        :to="
          authStore.isAuthenticated ? (authStore.isAdmin ? '/admin-dashboard' : '/dashboard') : '/'
        "
        class="flex items-center gap-2.5 group"
      >
        <div
          class="w-8 h-8 rounded-lg gradient-primary flex items-center justify-center shadow-lg shadow-primary/20 group-hover:shadow-primary/40 transition-shadow"
        >
          <Zap class="w-4.5 h-4.5 text-white" :stroke-width="2.5" />
        </div>
        <span class="text-lg font-bold tracking-tight text-base-content"
          >City<span class="text-primary">Pulse</span></span
        >
      </router-link>
    </div>

    <div class="navbar-center hidden lg:flex">
      <ul class="menu menu-horizontal gap-1">
        <li>
          <router-link
            to="/"
            class="text-sm font-medium text-base-content/70 hover:text-base-content hover:bg-base-300/50 rounded-lg px-3 py-2 transition-colors"
          >
            Home
          </router-link>
        </li>
        <li v-if="authStore.isAuthenticated">
          <router-link
            :to="authStore.isAdmin ? '/admin-dashboard' : '/dashboard'"
            class="text-sm font-medium text-base-content/70 hover:text-base-content hover:bg-base-300/50 rounded-lg px-3 py-2 transition-colors"
          >
            Dashboard
          </router-link>
        </li>
        <li v-if="authStore.isAuthenticated">
          <router-link
            to="/issues"
            class="text-sm font-medium text-base-content/70 hover:text-base-content hover:bg-base-300/50 rounded-lg px-3 py-2 transition-colors"
          >
            Issues
          </router-link>
        </li>
      </ul>
    </div>

    <div class="navbar-end gap-2">
      <!-- Theme Switcher Toggle -->
      <button
        @click="toggleTheme"
        class="btn btn-ghost btn-circle hover:bg-base-300/50 text-base-content/70 hover:text-base-content"
        aria-label="Toggle light/dark theme"
      >
        <Sun v-if="currentTheme === 'dark'" class="w-5 h-5 animate-fade-in" :stroke-width="2" />
        <Moon v-else class="w-5 h-5 animate-fade-in" :stroke-width="2" />
      </button>

      <div
        v-if="authStore.isAuthenticated"
        class="dropdown dropdown-end"
        :class="{ 'dropdown-open': dropdownOpen }"
      >
        <div
          tabindex="0"
          role="button"
          id="user-menu-button"
          :aria-expanded="dropdownOpen"
          class="btn btn-ghost btn-circle avatar ring-2 ring-base-300 hover:ring-primary/40 transition-all duration-300"
          @click="toggleDropdown"
        >
          <div class="w-9 rounded-full">
            <img
              v-if="profilePictureUrl"
              :src="profilePictureUrl"
              alt="Profile"
              class="object-cover"
            />
            <div
              v-else
              class="w-9 h-9 rounded-full flex items-center justify-center gradient-primary text-white text-sm font-semibold"
            >
              {{ userInitials }}
            </div>
          </div>
        </div>
        <ul
          tabindex="0"
          id="user-dropdown"
          class="menu menu-sm dropdown-content bg-base-200 border border-base-300/60 rounded-xl z-[100] mt-3 w-52 p-2 shadow-2xl shadow-black/30"
        >
          <div class="px-3 py-2 border-b border-base-300/60 mb-1">
            <p class="text-xs text-base-content/50 font-medium">Signed in as</p>
            <p class="text-sm font-semibold text-base-content truncate">
              {{ user?.firstname }} {{ user?.lastname }}
            </p>
          </div>
          <li>
            <router-link
              @click="closeDropdown"
              :to="authStore.isAdmin ? '/admin-dashboard' : '/dashboard'"
              class="py-2.5 rounded-lg gap-3"
            >
              <LayoutDashboard class="w-4 h-4 text-primary" :stroke-width="2" />
              {{ authStore.isAdmin ? 'Admin Dashboard' : 'Dashboard' }}
            </router-link>
          </li>
          <li>
            <router-link @click="closeDropdown" to="/issues" class="py-2.5 rounded-lg gap-3">
              <FileText class="w-4 h-4 text-secondary" :stroke-width="2" />
              Issues
            </router-link>
          </li>
          <li>
            <router-link @click="closeDropdown" to="/profile" class="py-2.5 rounded-lg gap-3">
              <User class="w-4 h-4 text-accent" :stroke-width="2" />
              Profile
            </router-link>
          </li>
          <li class="border-t border-base-300/60 mt-1 pt-1">
            <button @click="handleLogout" class="py-2.5 rounded-lg text-error gap-3">
              <LogOut class="w-4 h-4" :stroke-width="2" />
              Log Out
            </button>
          </li>
        </ul>
      </div>

      <template v-else>
        <router-link
          to="/login"
          class="btn btn-ghost btn-sm rounded-lg text-base-content/70 hover:text-base-content"
        >
          Sign in
        </router-link>
        <router-link
          to="/register"
          class="btn btn-primary btn-sm rounded-lg shadow-lg shadow-primary/20"
        >
          Get Started
        </router-link>
      </template>

      <button class="btn btn-ghost btn-circle lg:hidden" @click="mobileMenuOpen = !mobileMenuOpen">
        <Menu class="w-5 h-5" :stroke-width="2" />
      </button>
    </div>
  </nav>

  <!-- Mobile menu -->
  <div v-if="mobileMenuOpen" class="fixed inset-0 z-40 lg:hidden">
    <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="mobileMenuOpen = false" />
    <div
      class="absolute right-0 top-0 h-full w-72 bg-base-200 border-l border-base-300/60 shadow-2xl p-6 pt-20 animate-slide-in"
    >
      <ul class="menu gap-1">
        <li>
          <router-link
            to="/"
            @click="mobileMenuOpen = false"
            class="py-3 rounded-lg gap-3 text-base font-medium"
          >
            <Home class="w-5 h-5" :stroke-width="2" />
            Home
          </router-link>
        </li>
        <template v-if="authStore.isAuthenticated">
          <li>
            <router-link
              :to="authStore.isAdmin ? '/admin-dashboard' : '/dashboard'"
              @click="mobileMenuOpen = false"
              class="py-3 rounded-lg gap-3 text-base font-medium"
            >
              <LayoutDashboard class="w-5 h-5" :stroke-width="2" />
              Dashboard
            </router-link>
          </li>
          <li>
            <router-link
              to="/issues"
              @click="mobileMenuOpen = false"
              class="py-3 rounded-lg gap-3 text-base font-medium"
            >
              <FileText class="w-5 h-5" :stroke-width="2" />
              Issues
            </router-link>
          </li>
          <li>
            <router-link
              to="/profile"
              @click="mobileMenuOpen = false"
              class="py-3 rounded-lg gap-3 text-base font-medium"
            >
              <User class="w-5 h-5" :stroke-width="2" />
              Profile
            </router-link>
          </li>
          <li class="border-t border-base-300/60 mt-2 pt-2">
            <button @click="handleLogout" class="py-3 rounded-lg text-error gap-3">
              <LogOut class="w-5 h-5" :stroke-width="2" />
              Log Out
            </button>
          </li>
        </template>
        <template v-else>
          <li>
            <router-link
              to="/login"
              @click="mobileMenuOpen = false"
              class="py-3 rounded-lg gap-3 text-base font-medium"
            >
              <LogIn class="w-5 h-5" :stroke-width="2" />
              Sign in
            </router-link>
          </li>
          <li>
            <router-link
              to="/register"
              @click="mobileMenuOpen = false"
              class="py-3 rounded-lg gap-3 text-base font-medium"
            >
              <UserPlus class="w-5 h-5" :stroke-width="2" />
              Get Started
            </router-link>
          </li>
        </template>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import {
  Zap,
  Menu,
  Home,
  LayoutDashboard,
  FileText,
  User,
  LogOut,
  LogIn,
  UserPlus,
  Sun,
  Moon,
} from '@lucide/vue'

const currentTheme = ref(localStorage.getItem('theme') || 'light')

const toggleTheme = () => {
  const newTheme = currentTheme.value === 'light' ? 'dark' : 'light'
  currentTheme.value = newTheme
  document.documentElement.setAttribute('data-theme', newTheme)
  localStorage.setItem('theme', newTheme)
  window.dispatchEvent(new CustomEvent('theme-changed', { detail: newTheme }))
}

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
  return (
    user.value.profile_picture ||
    `https://api.dicebear.com/9.x/notionists-neutral/svg?seed=${user.value.firstname}${user.value.lastname}`
  )
})

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
  mobileMenuOpen.value = false
}

const closeDropdown = () => {
  dropdownOpen.value = false
  mobileMenuOpen.value = false
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
  closeDropdown()
}

const handleClickOutside = (event) => {
  const userMenuButton = document.getElementById('user-menu-button')
  const userDropdown = document.getElementById('user-dropdown')

  if (
    userMenuButton &&
    userDropdown &&
    !userMenuButton.contains(event.target) &&
    !userDropdown.contains(event.target)
  ) {
    dropdownOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
