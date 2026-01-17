<script setup lang="ts">
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import { login } from "../api/http";

const router = useRouter();
const email = ref("");
const password = ref("");
const result = ref<string>("");
const showToast = ref(false);
let toastTimer: number | null = null;

watch(result, (value) => {
  if (!value) return;
  showToast.value = true;
  if (toastTimer) window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => {
    showToast.value = false;
    toastTimer = null;
  }, 5000);
});

async function runLogin() {
  result.value = "running...";
  try {
    await login(email.value, password.value);
    result.value = "OK: logged in";
    await router.push("/tenant");
  } catch (e: any) {
    result.value = `NG: ${e?.message ?? e}`;
  }
}

</script>

<template>
  <section class="card">
    <header class="card__header">
      <p class="eyebrow">Welcome back</p>
      <h2>Login to continue</h2>
      <p class="muted">Use your email and password.</p>
    </header>

    <form class="form" @submit.prevent="runLogin">
      <label class="field">
        <span>Email</span>
        <input v-model="email" placeholder="you@example.com" autocomplete="email" />
      </label>
      <label class="field">
        <span>Password</span>
        <input v-model="password" type="password" placeholder="••••••••" autocomplete="current-password" />
      </label>
      <button class="primary" type="submit">Login</button>
    </form>

    <p class="switch">
      New to Badge Converter?
      <RouterLink to="/signup">Sign up.</RouterLink>
    </p>

    <transition name="toast">
      <div v-if="showToast && result" class="toast" role="status">{{ result }}</div>
    </transition>
  </section>
</template>

<style scoped>
.card {
  width: min(480px, 100%);
  background: #0d0f12;
  color: #f8fafc;
  border-radius: 24px;
  padding: 28px;
  box-shadow: 0 28px 80px rgba(15, 23, 42, 0.22);
}

.card__header h2 {
  margin: 4px 0 8px;
  font-size: 28px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 12px;
  color: #f8d477;
  margin: 0;
}

.muted {
  margin: 0;
  color: #cbd5f5;
}

.form {
  display: grid;
  gap: 12px;
  margin-top: 20px;
}

.field {
  display: grid;
  gap: 6px;
  font-weight: 600;
  color: #f8fafc;
}

.field input {
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 10px 12px;
  font-size: 15px;
  background: #111827;
  color: #f8fafc;
}

.primary {
  margin-top: 8px;
  border: none;
  border-radius: 999px;
  padding: 12px 18px;
  background: #f8d477;
  color: #0d0f12;
  font-weight: 700;
  cursor: pointer;
}

.switch {
  margin: 8px 0 0;
  color: #cbd5f5;
}

.switch a {
  color: #f8d477;
  font-weight: 600;
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
</style>
