<template>
  <nav class="navbar-root sticky z-50 transition-all duration-500" :class="navbarClasses">
    <!-- Main Desktop / Mobile Navbar Bar -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div
        class="relative flex items-center justify-between transition-all duration-500"
        :class="isTransparentNavbar ? 'h-[4.5rem]' : 'h-[3.75rem]'"
      >
        <!-- Start Side: Logo -->
        <div class="flex items-center">
          <router-link
            @click="closeAll"
            :to="homeRoute"
            class="flex items-center gap-2.5 no-underline shrink-0 group"
          >
            <div
              class="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-md shadow-primary/20 group-hover:scale-108 group-hover:rotate-[-3deg] transition-all duration-300"
            >
              <Zap class="w-[18px] h-[18px] text-white" :stroke-width="2.5" />
            </div>
            <span
              class="text-lg font-extrabold tracking-tight logo-text-item"
              :class="isTransparentNavbar ? 'text-white' : 'text-base-content'"
            >
              City<span class="text-primary">Pulse</span>
            </span>
            <span
              v-if="authStore.isAuthenticated"
              class="text-[10px] font-bold uppercase tracking-widest px-2 py-0.5 rounded-md ml-1"
              :class="
                authStore.isAdmin
                  ? 'bg-secondary/12 text-secondary border border-secondary/20 shadow-[0_0_10px_rgba(236,72,153,0.1)]'
                  : 'bg-primary/12 text-primary border border-primary/20 shadow-[0_0_10px_rgba(59,130,246,0.1)]'
              "
            >
              {{ authStore.isAdmin ? 'Admin' : 'Citizen' }}
            </span>
          </router-link>
        </div>

        <!-- Desktop Nav Links (Centered) -->
        <div class="hidden lg:flex absolute left-1/2 -translate-x-1/2 items-center z-10">
          <div
            class="flex items-center gap-1 p-1 bg-base-200/40 rounded-xl border border-base-content/5"
          >
            <template v-for="link in navLinks" :key="link.to">
              <router-link
                :to="link.to"
                class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 cursor-pointer"
                :class="[
                  link.isSpecial
                    ? 'font-semibold text-primary hover:bg-primary/10'
                    : isTransparentNavbar
                      ? 'text-white/85 hover:text-white hover:bg-white/10'
                      : 'text-base-content/65 hover:text-base-content hover:bg-base-100/80',
                  isLinkActive(link)
                    ? isTransparentNavbar
                      ? 'bg-white/15 text-white shadow-none font-semibold'
                      : 'text-base-content bg-base-100 shadow-xs ring-1 ring-base-content/5'
                    : '',
                ]"
              >
                <component v-if="link.icon" :is="link.icon" class="w-3.5 h-3.5" />
                {{ link.label }}
              </router-link>
            </template>

            <!-- Manage Dropdown for Admin -->
            <div
              v-if="authStore.isAuthenticated && authStore.isAdmin"
              class="relative dropdown-root"
              @mouseenter="manageOpen = true"
              @mouseleave="manageOpen = false"
            >
              <button
                class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 cursor-pointer"
                :class="[
                  isTransparentNavbar
                    ? 'text-white/85 hover:text-white hover:bg-white/10'
                    : 'text-base-content/65 hover:text-base-content hover:bg-base-100/80',
                  isManageActive
                    ? isTransparentNavbar
                      ? 'bg-white/15 text-white shadow-none font-semibold'
                      : 'text-base-content bg-base-100 shadow-xs ring-1 ring-base-content/5'
                    : '',
                ]"
              >
                <Shield class="w-3.5 h-3.5" />
                Manage
                <ChevronDown
                  class="w-3.5 h-3.5 opacity-40 transition-transform duration-200"
                  :class="{ 'rotate-180 opacity-70': manageOpen }"
                />
              </button>
              <Transition
                enter-active-class="transition duration-200 ease-out"
                enter-from-class="transform -translate-y-1 scale-95 opacity-0"
                enter-to-class="transform translate-y-0 scale-100 opacity-100"
                leave-active-class="transition duration-150 ease-in"
                leave-from-class="transform translate-y-0 scale-100 opacity-100"
                leave-to-class="transform -translate-y-1 scale-95 opacity-0"
              >
                <div
                  v-if="manageOpen"
                  class="absolute top-[calc(100%+0.5rem)] left-0 min-w-[14.5rem] p-1.5 rounded-2xl bg-base-100/90 backdrop-blur-xl border border-base-content/10 shadow-xl z-50"
                >
                  <router-link
                    v-for="sub in adminManageLinks"
                    :key="sub.to"
                    :to="sub.to"
                    class="flex items-center gap-2.5 w-full px-3 py-2 rounded-xl text-xs font-medium text-base-content/75 hover:text-base-content hover:bg-base-200/50 transition-all duration-150 cursor-pointer"
                  >
                    <component :is="sub.icon" class="w-4 h-4" :class="sub.color" />
                    <span>{{ sub.label }}</span>
                  </router-link>
                </div>
              </Transition>
            </div>
          </div>
        </div>

        <!-- End Side: Controls (Theme, User Dropdown, Hamburger toggle) -->
        <div class="flex items-center gap-2">
          <!-- Theme Toggle -->
          <button
            @click="toggleTheme"
            class="w-9 h-9 flex items-center justify-center rounded-xl border border-transparent transition-all duration-200 cursor-pointer"
            :class="
              isTransparentNavbar
                ? 'text-white/80 hover:text-white hover:bg-white/10 hover:border-white/15'
                : 'text-base-content/65 hover:text-base-content hover:bg-base-200/70 hover:border-base-content/5'
            "
            aria-label="Toggle theme"
          >
            <Transition
              enter-active-class="transition duration-250 ease-out"
              enter-from-class="transform -rotate-90 scale-50 opacity-0"
              enter-to-class="transform rotate-0 scale-100 opacity-100"
              leave-active-class="transition duration-250 ease-in"
              leave-from-class="transform rotate-0 scale-100 opacity-100"
              leave-to-class="transform rotate-90 scale-50 opacity-0"
              mode="out-in"
            >
              <Sun v-if="isDark" class="w-[18px] h-[18px]" :stroke-width="2" key="sun" />
              <Moon v-else class="w-[18px] h-[18px]" :stroke-width="2" key="moon" />
            </Transition>
          </button>

          <!-- User Menu (Authenticated) -->
          <div v-if="authStore.isAuthenticated" class="relative dropdown-root">
            <button
              @click="toggleUserMenu"
              class="flex items-center gap-1.5 p-1 rounded-xl border border-transparent hover:border-base-content/5 hover:bg-base-200/50 transition-all duration-200 cursor-pointer"
            >
              <div
                class="w-8 h-8 rounded-lg overflow-hidden border-2 border-base-300/50 hover:border-primary/40 transition-colors duration-200 relative"
              >
                <img
                  v-if="profilePictureUrl && !imageLoadError"
                  :src="profilePictureUrl"
                  alt="Profile"
                  class="w-full h-full object-cover"
                  @error="imageLoadError = true"
                />
                <div
                  v-else
                  class="w-full h-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-white text-[10px] font-bold"
                >
                  {{ userInitials }}
                </div>
              </div>
              <ChevronDown
                class="w-3.5 h-3.5 opacity-40 transition-transform duration-200 hidden sm:block"
                :class="[
                  userMenuOpen ? 'rotate-180 opacity-70' : '',
                  isTransparentNavbar ? 'text-white/80' : 'text-base-content/40',
                ]"
              />
            </button>

            <Transition
              enter-active-class="transition duration-200 ease-out"
              enter-from-class="transform -translate-y-1 scale-95 opacity-0"
              enter-to-class="transform translate-y-0 scale-100 opacity-100"
              leave-active-class="transition duration-150 ease-in"
              leave-from-class="transform translate-y-0 scale-100 opacity-100"
              leave-to-class="transform -translate-y-1 scale-95 opacity-0"
            >
              <div
                v-if="userMenuOpen"
                class="absolute top-[calc(100%+0.5rem)] right-0 left-auto min-w-[14.5rem] p-1.5 rounded-2xl bg-base-100/90 backdrop-blur-xl border border-base-content/10 shadow-xl z-50"
              >
                <div class="px-3 py-2.5 border-b border-base-content/5 mb-1">
                  <div class="flex items-center justify-between gap-2">
                    <p class="text-xs font-bold text-base-content truncate">
                      {{ user?.firstname }} {{ user?.lastname }}
                    </p>
                    <span
                      class="text-[9px] font-extrabold uppercase tracking-wide px-1.5 py-0.5 rounded-md"
                      :class="
                        authStore.isAdmin
                          ? 'bg-error/12 text-error border border-error/20'
                          : 'bg-success/12 text-success border border-success/20'
                      "
                    >
                      {{ authStore.isAdmin ? 'Admin' : 'Citizen' }}
                    </span>
                  </div>
                  <p class="text-[10px] text-base-content/45 mt-0.5 truncate">{{ user?.email }}</p>
                </div>
                
                <router-link
                  v-for="link in userMenuLinks"
                  :key="link.to"
                  @click="closeAll"
                  :to="link.to"
                  class="flex items-center gap-2.5 w-full px-3 py-2 rounded-xl text-xs font-medium text-base-content/75 hover:text-base-content hover:bg-base-200/50 transition-all duration-150 cursor-pointer"
                >
                  <component :is="link.icon" class="w-4 h-4" :class="link.iconColor" />
                  <span>{{ link.label }}</span>
                </router-link>

                <div class="h-px bg-base-content/5 my-1 mx-2" />
                <button
                  @click="handleLogout"
                  class="flex items-center gap-2.5 w-full px-3 py-2 rounded-xl text-xs font-medium text-error hover:bg-error/8 hover:text-error transition-all duration-150 cursor-pointer"
                >
                  <LogOut class="w-4 h-4" />
                  <span>Sign Out</span>
                </button>
              </div>
            </Transition>
          </div>

          <!-- Guest Actions -->
          <template v-else>
            <router-link
              to="/login"
              class="inline-flex items-center px-3 py-2 rounded-lg text-xs font-semibold transition-all duration-200"
              :class="
                isTransparentNavbar
                  ? 'text-white/70 hover:text-white hover:bg-white/10'
                  : 'text-base-content/70 hover:text-base-content hover:bg-base-200/60'
              "
            >
              Sign In
            </router-link>
            <router-link
              to="/register"
              class="inline-flex items-center px-4 py-2 rounded-xl text-xs font-semibold text-white bg-gradient-to-r from-primary to-secondary hover:translate-y-[-1px] hover:shadow-lg hover:shadow-primary/20 transition-all duration-200"
            >
              Get Started
            </router-link>
          </template>

          <!-- Mobile Toggle Button (Sleek CSS Burger Icon) -->
          <button
            @click="mobileOpen = !mobileOpen"
            class="w-9 h-9 hidden max-lg:flex items-center justify-center rounded-xl border border-transparent transition-all duration-200 cursor-pointer"
            :class="
              isTransparentNavbar
                ? 'text-white/80 hover:text-white hover:bg-white/10 hover:border-white/15'
                : 'text-base-content/65 hover:text-base-content hover:bg-base-200/70 hover:border-base-content/5'
            "
            aria-label="Toggle menu"
          >
            <div class="relative w-5 h-4 flex flex-col justify-between cursor-pointer">
              <span :class="[mobileOpen ? 'translate-y-[6px] rotate-45' : '', 'block w-full h-[2px] bg-current rounded transition-all duration-300']"></span>
              <span :class="[mobileOpen ? 'opacity-0' : '', 'block w-full h-[2px] bg-current rounded transition-all duration-300']"></span>
              <span :class="[mobileOpen ? '-translate-y-[6px] -rotate-45' : '', 'block w-full h-[2px] bg-current rounded transition-all duration-300']"></span>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Slide Down Menu Container -->
    <Transition
      enter-active-class="transition-all duration-300 ease-out overflow-hidden"
      enter-from-class="max-h-0 -translate-y-[10px] opacity-0"
      enter-to-class="max-h-[580px] translate-y-0 opacity-100"
      leave-active-class="transition-all duration-300 ease-in overflow-hidden"
      leave-from-class="max-h-[580px] translate-y-0 opacity-100"
      leave-to-class="max-h-0 -translate-y-[10px] opacity-0"
    >
      <div
        v-if="mobileOpen"
        class="w-full bg-base-100/95 backdrop-blur-xl border-b border-base-content/8 shadow-md hidden max-lg:block"
      >
        <!-- User Card inside Mobile Menu -->
        <div
          v-if="authStore.isAuthenticated"
          class="mx-4 my-3 p-4 rounded-xl bg-base-200/50 border border-base-content/5 flex items-center gap-3 shadow-xs"
        >
          <div
            class="w-8 h-8 rounded-lg overflow-hidden border-2 border-base-300/50 relative flex-shrink-0"
          >
            <img
              v-if="profilePictureUrl && !imageLoadError"
              :src="profilePictureUrl"
              alt="Profile"
              class="w-full h-full object-cover"
              @error="imageLoadError = true"
            />
            <div
              v-else
              class="w-full h-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-white text-[10px] font-bold"
            >
              {{ userInitials }}
            </div>
          </div>
          <div class="min-w-0 flex-1">
            <p class="text-sm font-semibold truncate">{{ user?.firstname }} {{ user?.lastname }}</p>
            <div class="flex items-center gap-2 mt-0.5">
              <span
                class="text-[9px] font-extrabold uppercase tracking-wide px-1.5 py-0.5 rounded-md"
                :class="
                  authStore.isAdmin
                    ? 'bg-error/12 text-error border border-error/20'
                    : 'bg-success/12 text-success border border-success/20'
                "
              >
                {{ authStore.isAdmin ? 'Admin' : 'Citizen' }}
              </span>
              <span class="text-3xs text-base-content/40 truncate max-w-[120px]">{{
                user?.email
              }}</span>
            </div>
          </div>
        </div>

        <div class="flex flex-col gap-0.5 px-4 pb-6 pt-2">
          <template v-for="(link, idx) in mobileNavLinks" :key="idx">
            <!-- Divider -->
            <div v-if="link.isDivider" class="h-px bg-base-content/5 my-1 mx-2" />

            <!-- Header -->
            <div
              v-else-if="link.isHeader"
              class="px-3 py-2 text-[10px] font-bold uppercase tracking-wider text-base-content/40 mt-2"
            >
              {{ link.label }}
            </div>

            <!-- Button Action -->
            <button
              v-else-if="link.action"
              @click="link.action"
              class="flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-sm font-semibold transition-all duration-150 cursor-pointer"
              :class="
                link.isError
                  ? 'text-error hover:bg-error/8'
                  : 'text-base-content/75 hover:text-base-content hover:bg-base-200/50'
              "
            >
              <component :is="link.icon" class="w-[18px] h-[18px] flex-shrink-0" />
              {{ link.label }}
            </button>

            <!-- Regular Link -->
            <router-link
              v-else
              :to="link.to"
              @click="mobileOpen = false"
              class="flex items-center gap-3 rounded-xl transition-all duration-150 cursor-pointer"
              :class="[
                link.isSub
                  ? 'w-full pl-9 pr-3 py-2 text-xs font-semibold text-base-content/70 hover:text-base-content hover:bg-base-200/50'
                  : link.isSpecial
                    ? 'w-full px-3 py-2.5 text-sm font-semibold text-primary bg-primary/8 hover:bg-primary/12'
                    : 'w-full px-3 py-2.5 text-sm font-semibold text-base-content/75 hover:text-base-content hover:bg-base-200/50',
              ]"
            >
              <component
                :is="link.icon"
                class="flex-shrink-0"
                :class="[link.isSub ? 'w-4 h-4' : 'w-[18px] h-[18px]', link.iconClass]"
              />
              {{ link.label }}
            </router-link>
          </template>
        </div>
      </div>
    </Transition>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { useRouter, useRoute } from 'vue-router'
import {
  Zap,
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
  Sparkles,
  MapPin,
} from '@lucide/vue'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const scrolled = ref(false)
const mobileOpen = ref(false)
const userMenuOpen = ref(false)
const manageOpen = ref(false)
const imageLoadError = ref(false)

const user = computed(() => authStore.user)

const homeRoute = computed(() =>
  authStore.isAuthenticated ? (authStore.isAdmin ? '/admin-dashboard' : '/dashboard') : '/',
)

const isLandingPage = computed(() => route.path === '/')
const isTransparentNavbar = computed(() => isLandingPage.value && !scrolled.value)

const navbarClasses = computed(() => {
  if (isTransparentNavbar.value) {
    return 'top-0 left-0 right-0 bg-transparent py-3 border-b border-transparent shadow-none'
  } else {
    return 'top-0 lg:top-3 left-0 right-0 lg:left-3 lg:right-3 lg:mx-auto max-w-7xl lg:rounded-2xl bg-base-100/80 backdrop-blur-xl border border-base-content/8 py-1 shadow-lg'
  }
})

// Dynamic configuration of Navigation Links
const navLinks = computed(() => {
  if (!authStore.isAuthenticated) {
    return [
      { to: '/', label: 'Home' },
      { to: '/#features', label: 'Features', hash: '#features' },
      { to: '/#reports', label: 'Public Map', hash: '#reports' },
    ]
  }
  if (!authStore.isAdmin) {
    return [
      { to: '/dashboard', label: 'Dashboard' },
      { to: '/issues', label: 'My Reports' },
      { to: '/issues/create', label: 'Report', icon: PlusCircle, isSpecial: true },
    ]
  }
  return [
    { to: '/admin-dashboard', label: 'Dashboard' },
    { to: '/admin/analytics', label: 'Analytics', icon: BarChart3 },
  ]
})

const adminManageLinks = [
  { to: '/admin/departments', label: 'Departments', icon: Building2, color: 'text-primary' },
  { to: '/admin/geofence', label: 'Geofencing', icon: Layers, color: 'text-secondary' },
  { to: '/admin/sla', label: 'SLA Config', icon: Clock, color: 'text-accent' },
  { to: '/admin/audit-log', label: 'Audit Logs', icon: History, color: 'opacity-45' },
  { to: '/admin/export', label: 'Export Data', icon: Download, color: 'text-info' },
]

const userMenuLinks = computed(() => {
  if (!authStore.isAuthenticated) return []
  const links = [
    {
      to: authStore.isAdmin ? '/admin-dashboard' : '/dashboard',
      label: 'Dashboard',
      icon: LayoutDashboard,
      iconColor: 'text-primary',
    },
  ]
  if (!authStore.isAdmin) {
    links.push({ to: '/issues/create', label: 'Report Issue', icon: PlusCircle, iconColor: 'text-success' })
  }
  links.push({
    to: '/profile',
    label: 'Profile',
    icon: User,
    iconColor: 'text-accent',
  })
  return links
})

const mobileNavLinks = computed(() => {
  if (!authStore.isAuthenticated) {
    return [
      { to: '/', label: 'Home', icon: Home },
      { to: '/#features', label: 'Features', icon: Sparkles, iconClass: 'text-secondary', hash: '#features' },
      { to: '/#reports', label: 'Public Map', icon: MapPin, iconClass: 'text-primary', hash: '#reports' },
      { isDivider: true },
      { to: '/login', label: 'Sign In', icon: LogIn },
      { to: '/register', label: 'Get Started', icon: UserPlus, isSpecial: true },
    ]
  }

  const links = []
  if (!authStore.isAdmin) {
    links.push(
      { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard, iconClass: 'text-primary' },
      { to: '/issues', label: 'My Reports', icon: FileText, iconClass: 'text-secondary' },
      { to: '/issues/create', label: 'Report Issue', icon: PlusCircle, isSpecial: true }
    )
  } else {
    links.push(
      {
        to: '/admin-dashboard',
        label: 'Dashboard',
        icon: LayoutDashboard,
        iconClass: 'text-primary',
      },
      { to: '/admin/analytics', label: 'Analytics', icon: BarChart3, iconClass: 'text-accent' },
      { isHeader: true, label: 'Management' },
      ...adminManageLinks.map((link) => ({
        ...link,
        isSub: true,
        iconClass: link.color,
      }))
    )
  }

  links.push(
    { isDivider: true },
    { to: '/profile', label: 'Profile', icon: User, iconClass: 'text-accent' },
    { label: 'Sign Out', icon: LogOut, action: handleLogout, isError: true }
  )

  return links
})

const isLinkActive = (link) => {
  if (link.hash) {
    return route.hash === link.hash
  }
  return route.path === link.to && !route.hash
}

// Reactive theme tracking
const currentTheme = ref(localStorage.getItem('theme') || 'light')

const isDark = computed(() => {
  return ['dark', 'citypulse-dark', 'sunset', 'dim'].includes(currentTheme.value)
})

const isManageActive = computed(() =>
  ['/admin/departments', '/admin/geofence', '/admin/sla', '/admin/audit-log', '/admin/export'].some(
    (p) => route.path.includes(p),
  ),
)

const userInitials = computed(() => {
  if (!user.value) return 'U'
  return ((user.value.firstname?.[0] || '') + (user.value.lastname?.[0] || '')).toUpperCase() || 'U'
})

const profilePictureUrl = computed(() => {
  if (!user.value) return null
  return (
    user.value.profile_picture ||
    `https://api.dicebear.com/9.x/notionists-neutral/svg?seed=${user.value.firstname}${user.value.lastname}`
  )
})

const toggleTheme = () => {
  const next = currentTheme.value === 'light' ? 'dark' : 'light'
  currentTheme.value = next
  document.documentElement.setAttribute('data-theme', next)
  localStorage.setItem('theme', next)
  window.dispatchEvent(new CustomEvent('theme-changed', { detail: next }))
}

const toggleUserMenu = () => {
  userMenuOpen.value = !userMenuOpen.value
  manageOpen.value = false
}

const closeAll = () => {
  userMenuOpen.value = false
  manageOpen.value = false
  mobileOpen.value = false
}

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
  closeAll()
}

const handleScroll = () => {
  scrolled.value = window.scrollY > 10
}

const handleClickOutside = (e) => {
  if (!e.target.closest('.dropdown-root')) {
    userMenuOpen.value = false
    manageOpen.value = false
  }
}

// Watch for route changes to close menus automatically
watch(
  () => route.fullPath,
  () => {
    closeAll()
  },
)

// Watch for user changes to reset avatar load error status
watch(
  () => user.value,
  () => {
    imageLoadError.value = false
  },
)

const handleThemeChange = (e) => {
  currentTheme.value = e.detail
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  window.addEventListener('theme-changed', handleThemeChange)
  document.addEventListener('click', handleClickOutside)
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('theme-changed', handleThemeChange)
  document.removeEventListener('click', handleClickOutside)
})
</script>

<!-- No custom style scoped blocks allowed, styling is 100% Tailwind CSS -->
