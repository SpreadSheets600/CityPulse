<template>
  <div class="chatbot-container" :class="{ 'chatbot-open': isOpen }">
    <button
      v-if="!isOpen"
      @click="openChatbot"
      class="chatbot-toggle"
      aria-label="Open chat assistant"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6"
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

    <div v-if="isOpen" class="chatbot-window">
      <div class="chatbot-header">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 text-white"
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
          <span class="font-bold text-white">CityPulse Assistant</span>
        </div>
        <button @click="closeChatbot" class="chatbot-close" aria-label="Close chat">
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

      <div class="chatbot-messages" ref="messagesContainer">
        <div v-for="msg in messages" :key="msg.id" :class="['message', msg.role]">
          <div class="message-content">
            {{ msg.content }}
          </div>
        </div>
        <div v-if="loading" class="message assistant">
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>

      <form @submit.prevent="handleSend" class="chatbot-input">
        <input
          v-model="inputText"
          type="text"
          placeholder="Ask me anything..."
          :disabled="loading"
          class="flex-1"
        />
        <button
          type="submit"
          :disabled="loading || !inputText.trim()"
          class="btn btn-primary btn-sm"
        >
          Send
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import { useChatbotStore } from '../stores/chatbot'

const chatbotStore = useChatbotStore()
const { messages, loading, isOpen, openChatbot, closeChatbot, sendMessage } = chatbotStore

const inputText = ref('')
const messagesContainer = ref(null)

async function handleSend() {
  if (!inputText.value.trim() || loading) return
  const text = inputText.value
  inputText.value = ''
  await sendMessage(text)
}

watch(
  () => messages.length,
  async () => {
    await nextTick()
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  },
)
</script>

<style scoped>
.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.chatbot-toggle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: oklch(var(--p));
  color: oklch(var(--pc));
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s;
}

.chatbot-toggle:hover {
  transform: scale(1.1);
}

.chatbot-window {
  width: 380px;
  height: 520px;
  background-color: oklch(var(--b1));
  border-radius: 1rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chatbot-header {
  background-color: oklch(var(--p));
  color: oklch(var(--pc));
  padding: 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.chatbot-close {
  color: oklch(var(--pc));
  opacity: 0.8;
  transition: opacity 0.2s;
}

.chatbot-close:hover {
  opacity: 1;
}

.chatbot-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.message {
  max-width: 85%;
}

.message.user {
  align-self: flex-end;
}

.message.assistant {
  align-self: flex-start;
}

.message-content {
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  line-height: 1.4;
}

.message.user .message-content {
  background-color: oklch(var(--p));
  color: oklch(var(--pc));
  border-bottom-right-radius: 0.25rem;
}

.message.assistant .message-content {
  background-color: oklch(var(--b3));
  color: oklch(var(--bc));
  border-bottom-left-radius: 0.25rem;
}

.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 0.75rem 1rem;
  background-color: oklch(var(--b3));
  border-radius: 1rem;
  border-bottom-left-radius: 0.25rem;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  background-color: oklch(var(--bc));
  border-radius: 50%;
  opacity: 0.5;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%,
  60%,
  100% {
    opacity: 0.5;
    transform: translateY(0);
  }
  30% {
    opacity: 1;
    transform: translateY(-4px);
  }
}

.chatbot-input {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid oklch(var(--b3));
  background-color: oklch(var(--b1));
}

.chatbot-input input {
  flex: 1;
  padding: 0.5rem 1rem;
  border: 1px solid oklch(var(--b3));
  border-radius: 1rem;
  background-color: oklch(var(--b2));
  color: oklch(var(--bc));
  font-size: 0.875rem;
}

.chatbot-input input:focus {
  outline: none;
  border-color: oklch(var(--p));
}

.chatbot-input button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
