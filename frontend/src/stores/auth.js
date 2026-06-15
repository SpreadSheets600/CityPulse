import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

import axios from '../api/client'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const isAuthenticated = computed(() => !!token.value)

  const isAdmin = computed(() => user.value?.role === 'admin')

  const setToken = (newToken) => {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
    }
  }

  const setUser = (userData) => {
    user.value = userData
  }

  const login = async (credentials) => {
    try {
      const response = await axios.post('/auth/login', credentials)
      const { access_token, user: userData } = response.data

      setToken(access_token)
      setUser(userData)

      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data?.msg || 'Login Failed' }
    }
  }

  const register = async (userData) => {
    try {
      const response = await axios.post('/auth/register', userData)
      const { access_token, user: userData_res } = response.data
      if (access_token) {
        setToken(access_token)
        setUser(userData_res)
      }
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data?.error || 'Registration Failed' }
    }
  }

  const logout = async () => {
    try {
      await axios.post('/auth/logout')
    } catch (error) {
      console.error('Logout Error :', error)
    } finally {
      setToken(null)
      setUser(null)
    }
  }

  const initializeAuth = async () => {
    if (token.value) {
      try {
        const response = await axios.get('/auth/me')
        setUser(response.data.user)
      } catch (error) {
        console.error('Failed to fetch user data:', error)
        setToken(null)
        setUser(null)
      }
    }
  }

  const updateProfile = async (profileData) => {
    try {
      const response = await axios.put('/auth/profile', profileData)
      setUser(response.data.user)
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data?.error || 'Update Failed' }
    }
  }

  return {
    user,
    token,
    login,
    logout,
    register,
    initializeAuth,
    updateProfile,
    isAuthenticated,
    isAdmin,
  }
})
