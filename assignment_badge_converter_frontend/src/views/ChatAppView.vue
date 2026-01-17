<script setup lang="ts">
import { nextTick, ref, watch } from "vue";
import { chatStream } from "../api/http";

type ChatMessage = { id: number; role: "user" | "assistant"; content: string };

const messages = ref<ChatMessage[]>([]);
const input = ref("");
const isSending = ref(false);
const result = ref<string>("");
const showToast = ref(false);
const listRef = ref<HTMLDivElement | null>(null);
let toastTimer: number | null = null;
let seq = 0;

watch(result, (value) => {
  if (!value) return;
  showToast.value = true;
  if (toastTimer) window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => {
    showToast.value = false;
    toastTimer = null;
  }, 5000);
});

async function scrollToBottom() {
  await nextTick();
  if (!listRef.value) return;
  listRef.value.scrollTop = listRef.value.scrollHeight;
}

async function sendMessage() {
  const content = input.value.trim();
  if (!content || isSending.value) return;

  const userMessage: ChatMessage = { id: seq++, role: "user", content };
  const assistantMessage: ChatMessage = { id: seq++, role: "assistant", content: "" };

  messages.value = [...messages.value, userMessage, assistantMessage];
  input.value = "";
  isSending.value = true;
  await scrollToBottom();

  try {
    await chatStream(content, (chunk) => {
      assistantMessage.content += chunk;
      messages.value = messages.value.map((m) => (m.id === assistantMessage.id ? assistantMessage : m));
      scrollToBottom();
    });
  } catch (e: any) {
    result.value = `NG: ${e?.message ?? e}`;
  } finally {
    isSending.value = false;
  }
}

function handleKeydown(event: KeyboardEvent) {
  if (event.key !== "Enter" || event.shiftKey) return;
  event.preventDefault();
  sendMessage();
}
</script>

<template>
  <section class="shell">
    <header class="header">
      <div>
        <p class="eyebrow">LLM Chat</p>
        <h2>Badge Assistant</h2>
      </div>
      <p class="muted">Streaming replies powered by gpt-4o-mini.</p>
    </header>

    <div ref="listRef" class="chat">
      <div v-if="messages.length === 0" class="empty">
        Start a conversation by asking a question.
      </div>
      <div v-for="message in messages" :key="message.id" class="bubble" :class="`bubble--${message.role}`">
        <p>{{ message.content }}</p>
      </div>
    </div>

    <form class="composer" @submit.prevent="sendMessage">
      <textarea
        v-model="input"
        class="composer__input"
        rows="3"
        placeholder="Ask anything about badges..."
        @keydown="handleKeydown"
      />
      <button class="primary" type="submit" :disabled="isSending || !input.trim()">
        {{ isSending ? "Sending..." : "Send" }}
      </button>
    </form>

    <transition name="toast">
      <div v-if="showToast && result" class="toast" role="status">{{ result }}</div>
    </transition>
  </section>
</template>

<style scoped>
.shell {
  width: min(960px, 100%);
  background: #ffffff;
  border-radius: 24px;
  padding: 28px;
  box-shadow: 0 18px 50px rgba(15, 23, 42, 0.1);
  display: grid;
  gap: 18px;
}

.header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.header h2 {
  margin: 0;
  font-size: 28px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 12px;
  color: #1e3a8a;
  margin: 0 0 4px;
}

.muted {
  margin: 0;
  color: #6b7280;
}

.chat {
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  padding: 16px;
  min-height: 320px;
  max-height: 420px;
  overflow-y: auto;
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
  display: grid;
  gap: 12px;
}

.empty {
  color: #6b7280;
}

.bubble {
  padding: 12px 14px;
  border-radius: 16px;
  max-width: 75%;
  line-height: 1.5;
}

.bubble p {
  margin: 0;
  white-space: pre-wrap;
}

.bubble--user {
  background: #1e3a8a;
  color: #ffffff;
  justify-self: end;
}

.bubble--assistant {
  background: #eef2ff;
  color: #111827;
  justify-self: start;
}

.composer {
  display: grid;
  gap: 12px;
}

.composer__input {
  border: 1px solid #d1d5db;
  border-radius: 16px;
  padding: 12px;
  font-size: 15px;
  resize: vertical;
  min-height: 80px;
}

.primary {
  border: none;
  border-radius: 999px;
  padding: 12px 18px;
  background: #1e3a8a;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  width: fit-content;
}

.primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.toast {
  position: fixed;
  left: 50%;
  bottom: 20px;
  transform: translateX(-50%);
  background: #0f172a;
  color: #fff;
  padding: 12px 18px;
  border-radius: 999px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.2);
  max-width: min(520px, 90vw);
  text-align: center;
}

.toast-enter-active,
.toast-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translate(-50%, 8px);
}

@media (max-width: 720px) {
  .bubble {
    max-width: 100%;
  }
}
</style>
