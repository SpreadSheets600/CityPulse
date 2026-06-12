<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <div class="fixed bottom-5 right-5 z-[9999] flex flex-col items-end">
    <!-- Chatbot Window -->
    <div
      v-if="isOpen"
      class="card card-bordered bg-base-100 shadow-2xl border border-base-300 w-96 h-[520px] flex flex-col overflow-hidden mb-4 transition-all duration-300 animate-fade-in"
    >
      <!-- Header -->
      <div class="bg-primary text-primary-content p-4 flex items-center justify-between shadow-md shrink-0">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 bg-primary-content/15 rounded-full flex items-center justify-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 text-primary-content"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
              />
            </svg>
          </div>
          <span class="font-semibold text-sm tracking-wide">CityPulse Assistant</span>
        </div>
        <button
          @click="closeChatbot"
          class="btn btn-ghost btn-circle btn-sm text-primary-content hover:bg-primary-content/10"
          aria-label="Close chat"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <!-- Messages Area -->
      <div class="flex-1 overflow-y-auto p-4 space-y-4 bg-base-100" ref="messagesContainer">
        <!-- Welcome Message if empty -->
        <div v-if="messages.length === 0" class="chat chat-start">
          <div class="chat-bubble bg-base-200 text-base-content border border-base-300 shadow-sm text-sm">
            Hello! I'm the CityPulse assistant. How can I help you report issues, understand reputational points, or track reports today?
          </div>
        </div>

        <div
          v-for="msg in messages"
          :key="msg.id"
          :class="['chat', msg.role === 'user' ? 'chat-end' : 'chat-start']"
        >
          <div
            :class="[
              'chat-bubble text-sm',
              msg.role === 'user'
                ? 'chat-bubble-primary shadow-sm'
                : 'bg-base-200 text-base-content border border-base-300 shadow-sm'
            ]"
          >
            {{ msg.content }}
          </div>
        </div>

        <!-- Typing Indicator -->
        <div v-if="loading" class="chat chat-start">
          <div class="chat-bubble bg-base-200 text-base-content border border-base-300 py-3 px-4 flex items-center shadow-sm">
            <span class="loading loading-dots loading-sm opacity-70"></span>
          </div>
        </div>
      </div>

      <!-- Input Form -->
      <form @submit.prevent="handleSend" class="p-3 bg-base-200 border-t border-base-300 flex gap-2 items-center shrink-0">
        <input
          v-model="inputText"
          type="text"
          placeholder="Ask me anything..."
          :disabled="loading"
          class="input input-bordered input-sm flex-1 bg-base-100 text-base-content focus:border-primary focus:outline-none"
        />
        <button
          type="submit"
          :disabled="loading || !inputText.trim()"
          class="btn btn-primary btn-sm shadow-md"
        >
          Send
        </button>
      </form>
    </div>

    <!-- Toggle Button -->
    <button
      v-if="!isOpen"
      @click="openChatbot"
      class="btn btn-circle btn-primary btn-lg shadow-2xl hover:scale-110 active:scale-95 transition-all duration-200 border-none flex items-center justify-center"
      aria-label="Open chat assistant"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-7 w-7 text-primary-content"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
        />
      </svg>
    </button>
  </div>
</template>

<script setup>
 
import { ref, nextTick, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useChatbotStore } from '../stores/chatbot'

const chatbotStore = useChatbotStore()
const { messages, loading, isOpen } = storeToRefs(chatbotStore)
const { openChatbot, closeChatbot, sendMessage } = chatbotStore

const inputText = ref('')
const messagesContainer = ref(null)

async function handleSend() {
  if (!inputText.value.trim() || loading.value) return
  const text = inputText.value
  inputText.value = ''
  await sendMessage(text)
}

watch(
  () => messages.value.length,
  async () => {
    await nextTick()
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  },
)
</script>

<style scoped>
/* No custom styling required since standard DaisyUI & Tailwind utility classes are fully leveraged */
</style>
