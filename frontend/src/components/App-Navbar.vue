<template>
  <nav class="navbar sticky top-0 z-50 glass-strong border-x-0 border-t-0 px-4 md:px-6 transition-all duration-300">
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
        <span class="text-lg font-bold tracking-tight text-base-content flex items-center gap-1.5"
          >City<span class="text-primary">Pulse</span>
          <span
            v-if="authStore.isAuthenticated && authStore.isAdmin"
            class="badge badge-secondary badge-sm font-mono text-2xs uppercase tracking-wider font-bold h-4.5"
            >Admin</span
          >
        </span>
      </router-link>
    </div>

    <div class="navbar-center hidden lg:flex">
      <ul class="menu menu-horizontal gap-1.5">
        <li>
          <router-link
            to="/"
            class="text-sm font-medium text-base-content/70 hover:text-base-content hover:bg-base-300/50 rounded-lg px-3 py-2 transition-colors"
          >
            Home
          </router-link>
        </li>

        <!-- Authenticated Common / Dashboard -->
        <li v-if="authStore.isAuthenticated">
          <router-link
            :to="authStore.isAdmin ? '/admin-dashboard' : '/dashboard'"
            class="text-sm font-medium text-base-content/70 hover:text-base-content hover:bg-base-300/50 rounded-lg px-3 py-2 transition-colors"
          >
            Dashboard
          </router-link>
        </li>

        <!-- Standard User navigation items -->
        <template v-if="authStore.isAuthenticated && !authStore.isAdmin">
          <li>
            <router-link
              to="/issues"
              class="text-sm font-medium text-base-content/70 hover:text-base-content hover:bg-base-300/50 rounded-lg px-3 py-2 transition-colors"
            >
              My Reports
            </router-link>
          </li>
          <li>
            <router-link
              to="/issues/create"
              class="text-sm font-semibold text-primary hover:bg-primary/10 rounded-lg px-3 py-2 transition-colors flex items-center gap-1.5"
            >
              <PlusCircle class="w-4 h-4" />
              Report Issue
            </router-link>
          </li>
        </template>

        <!-- Admin navigation items -->
        <template v-if="authStore.isAuthenticated && authStore.isAdmin">
          <li>
            <router-link
              to="/admin/analytics"
              class="text-sm font-medium text-base-content/70 hover:text-base-content hover:bg-base-300/50 rounded-lg px-3 py-2 transition-colors flex items-center gap-1.5"
            >
              <BarChart3 class="w-4 h-4 text-accent" />
              Analytics
            </router-link>
          </li>

          <!-- System Management Dropdown -->
          <li class="dropdown dropdown-hover">
            <div
              tabindex="0"
              role="button"
              class="text-sm font-medium text-base-content/70 hover:text-base-content hover:bg-base-300/50 rounded-lg px-3 py-2 transition-colors flex items-center gap-1 cursor-pointer"
            >
              <Shield class="w-4 h-4 text-secondary" />
              Manage
              <ChevronDown class="w-3.5 h-3.5 opacity-55" />
            </div>
            <ul
              tabindex="0"
              class="dropdown-content menu bg-base-200 border border-base-300/60 rounded-xl z-[100] mt-1 w-52 p-2 shadow-2xl shadow-black/30 animate-fade-in"
            >
              <li>
                <router-link to="/admin/departments" class="py-2.5 rounded-lg gap-2.5">
                  <Building2 class="w-4 h-4 text-primary" />
                  Departments
                </router-link>
              </li>
              <li>
                <router-link to="/admin/geofence" class="py-2.5 rounded-lg gap-2.5">
                  <Layers class="w-4 h-4 text-secondary" />
                  Geofencing
                </router-link>
              </li>
              <li>
                <router-link to="/admin/sla" class="py-2.5 rounded-lg gap-2.5">
                  <Clock class="w-4 h-4 text-accent" />
                  SLA Config
                </router-link>
              </li>
              <li>
                <router-link to="/admin/audit-log" class="py-2.5 rounded-lg gap-2.5">
                  <History class="w-4 h-4 text-neutral" />
                  Audit Logs
                </router-link>
              </li>
              <li>
                <router-link to="/admin/export" class="py-2.5 rounded-lg gap-2.5">
                  <Download class="w-4 h-4 text-info" />
                  Export Data
                </router-link>
              </li>
            </ul>
          </li>
        </template>
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
          <div class="px-3 py-2 border-b border-base-300/60 mb-1 flex flex-col gap-0.5">
            <span class="flex items-center justify-between">
              <span class="text-2xs text-base-content/50 font-medium uppercase tracking-wider"
                >Signed in as</span
              >
              <span
                v-if="authStore.isAdmin"
                class="badge badge-secondary badge-xs font-mono font-bold uppercase tracking-wider h-3.5"
                >Admin</span
              >
            </span>
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
          <li v-if="!authStore.isAdmin">
            <router-link @click="closeDropdown" to="/issues/create" class="py-2.5 rounded-lg gap-3">
              <PlusCircle class="w-4 h-4 text-success" :stroke-width="2" />
              Report Issue
            </router-link>
          </li>
          <li>
            <router-link
              @click="closeDropdown"
              :to="authStore.isAdmin ? '/admin-profile' : '/profile'"
              class="py-2.5 rounded-lg gap-3"
            >
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
          class="btn btn-ghost btn-sm text-base-content/75 hover:text-base-content hover:bg-base-300/50 rounded-xl px-3 font-semibold transition-colors"
        >
          Sign In
        </router-link>

        <router-link
          to="/register"
          class="btn btn-primary btn-sm rounded-xl px-4 font-semibold shadow-sm hover:shadow transition-all duration-200 ml-1"
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

        <!-- Authenticated Role-based Mobile Menu -->
        <template v-if="authStore.isAuthenticated">
          <!-- Admin Mobile Links -->
          <template v-if="authStore.isAdmin">
            <li>
              <router-link
                to="/admin-dashboard"
                @click="mobileMenuOpen = false"
                class="py-3 rounded-lg gap-3 text-base font-medium"
              >
                <LayoutDashboard class="w-5 h-5 text-primary" :stroke-width="2" />
                Admin Dashboard
              </router-link>
            </li>
            <li>
              <router-link
                to="/admin/analytics"
                @click="mobileMenuOpen = false"
                class="py-3 rounded-lg gap-3 text-base font-medium"
              >
                <BarChart3 class="w-5 h-5 text-accent" :stroke-width="2" />
                Analytics
              </router-link>
            </li>
            <div class="divider font-mono text-2xs uppercase tracking-widest text-base-content/40 my-1">
              System Management
            </div>
            <li>
              <router-link
                to="/admin/departments"
                @click="mobileMenuOpen = false"
                class="py-2.5 rounded-lg gap-3 text-sm font-medium pl-6"
              >
                <Building2 class="w-4 h-4 text-primary" :stroke-width="2" />
                Departments
              </router-link>
            </li>
            <li>
              <router-link
                to="/admin/geofence"
                @click="mobileMenuOpen = false"
                class="py-2.5 rounded-lg gap-3 text-sm font-medium pl-6"
              >
                <Layers class="w-4 h-4 text-secondary" :stroke-width="2" />
                Geofencing
              </router-link>
            </li>
            <li>
              <router-link
                to="/admin/sla"
                @click="mobileMenuOpen = false"
                class="py-2.5 rounded-lg gap-3 text-sm font-medium pl-6"
              >
                <Clock class="w-4 h-4 text-accent" :stroke-width="2" />
                SLA Config
              </router-link>
            </li>
            <li>
              <router-link
                to="/admin/audit-log"
                @click="mobileMenuOpen = false"
                class="py-2.5 rounded-lg gap-3 text-sm font-medium pl-6"
              >
                <History class="w-4 h-4 text-neutral" :stroke-width="2" />
                Audit Logs
              </router-link>
            </li>
            <li>
              <router-link
                to="/admin/export"
                @click="mobileMenuOpen = false"
                class="py-2.5 rounded-lg gap-3 text-sm font-medium pl-6"
              >
                <Download class="w-4 h-4 text-info" :stroke-width="2" />
                Export Data
              </router-link>
            </li>
            <div class="divider my-1"></div>
            <li>
              <router-link
                to="/admin-profile"
                @click="mobileMenuOpen = false"
                class="py-3 rounded-lg gap-3 text-base font-medium"
              >
                <User class="w-5 h-5 text-accent" :stroke-width="2" />
                Profile
              </router-link>
            </li>
          </template>

          <!-- Standard User Mobile Links -->
          <template v-else>
            <li>
              <router-link
                to="/dashboard"
                @click="mobileMenuOpen = false"
                class="py-3 rounded-lg gap-3 text-base font-medium"
              >
                <LayoutDashboard class="w-5 h-5 text-primary" :stroke-width="2" />
                Dashboard
              </router-link>
            </li>
            <li>
              <router-link
                to="/issues"
                @click="mobileMenuOpen = false"
                class="py-3 rounded-lg gap-3 text-base font-medium"
              >
                <FileText class="w-5 h-5 text-secondary" :stroke-width="2" />
                My Reports
              </router-link>
            </li>
            <li>
              <router-link
                to="/issues/create"
                @click="mobileMenuOpen = false"
                class="py-3 rounded-lg gap-3 text-base font-semibold text-primary"
              >
                <PlusCircle class="w-5 h-5" :stroke-width="2" />
                Report Issue
              </router-link>
            </li>
            <li>
              <router-link
                to="/profile"
                @click="mobileMenuOpen = false"
                class="py-3 rounded-lg gap-3 text-base font-medium"
              >
                <User class="w-5 h-5 text-accent" :stroke-width="2" />
                Profile
              </router-link>
            </li>
          </template>

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
  PlusCircle,
  BarChart3,
  Shield,
  Building2,
  Layers,
  Clock,
  History,
  Download,
  ChevronDown,
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
