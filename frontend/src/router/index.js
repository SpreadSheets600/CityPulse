import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import Login from '../components/Auth-Login.vue'
import Register from '../components/Auth-Register.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
    },
    {
      path: '/',
      name: 'PublicLanding',
      component: () => import('../views/Public-Landing.vue'),
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('../views/User-Dashboard.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/issues',
      name: 'Issues',
      component: () => import('../views/User-Issues.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/issues/create',
      name: 'CreateIssue',
      component: () => import('../views/Issue-Create.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/issues/:id',
      name: 'IssueDetail',
      component: () => import('../views/Issue-Detail.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('../views/User-Profile.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/admin-profile',
      name: 'AdminProfile',
      component: () => import('../views/User-Profile.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: '/admin-dashboard',
      name: 'AdminDashboard',
      component: () => import('../views/Admin-Dashboard.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
    {
      path: '/admin/issues/:id/manage',
      name: 'AdminIssueManage',
      component: () => import('../views/Admin-Issue-Manage.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
  ],
})

// Navigation Gaurd
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (authStore.token && !authStore.user) {
    await authStore.initializeAuth()
  }

  const isAuthenticated = authStore.isAuthenticated
  const isAdmin = authStore.user?.role === 'admin'

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if ((to.name === 'Login' || to.name === 'Register') && isAuthenticated) {
    // Redirect authenticated users away from login/register pages
    if (isAdmin) {
      next('/admin-dashboard')
    } else {
      next('/dashboard')
    }
  } else if (to.meta.requiresAdmin && !isAdmin) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
