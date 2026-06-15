import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/client'

export const useChatbotStore = defineStore('chatbot', () => {
  const messages = ref([])
  const loading = ref(false)
  const error = ref(null)
  const isOpen = ref(false)

  function toggleChatbot() {
    isOpen.value = !isOpen.value
  }

  function openChatbot() {
    isOpen.value = true
  }

  function closeChatbot() {
    isOpen.value = false
  }

  async function sendMessage(text) {
    if (!text.trim()) return

    messages.value.push({
      id: Date.now(),
      role: 'user',
      content: text,
      timestamp: new Date().toISOString(),
    })

    loading.value = true
    error.value = null

    try {
      const res = await api.post('/chatbot', { message: text })
      messages.value.push({
        id: Date.now() + 1,
        role: 'assistant',
        content: res.data.response,
        timestamp: new Date().toISOString(),
      })
    } catch (e) {
      error.value = e.response?.data?.error || 'Failed to get response'
      messages.value.push({
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      })
    } finally {
      loading.value = false
    }
  }

  function clearMessages() {
    messages.value = []
  }

  return {
    messages,
    loading,
    error,
    isOpen,
    toggleChatbot,
    openChatbot,
    closeChatbot,
    sendMessage,
    clearMessages,
  }
})
