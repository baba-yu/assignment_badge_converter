<script setup lang="ts">
import { ref } from "vue";
import { internalHealth, login } from "../api/http";

const username = ref("");
const password = ref("");
const result = ref<string>("");

async function runLogin() {
  result.value = "running...";
  try {
    await login(username.value, password.value);
    result.value = "OK: logged in";
  } catch (e: any) {
    result.value = `NG: ${e?.message ?? e}`;
  }
}

async function runInternalHealth() {
  result.value = "running...";
  try {
    await internalHealth();
    result.value = "OK: internal health";
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
      <p class="muted">Use your username and password.</p>
    </header>

    <form class="form" @submit.prevent="runLogin">
      <label class="field">
        <span>Username</span>
        <input v-model="username" placeholder="username" autocomplete="username" />
      </label>
      <label class="field">
        <span>Password</span>
        <input v-model="password" type="password" placeholder="••••••••" autocomplete="current-password" />
      </label>
      <button class="primary" type="submit">Login</button>
    </form>

    <div class="actions">
      <button class="ghost" type="button" @click="runInternalHealth">Internal health</button>
    </div>

    <pre class="result">{{ result }}</pre>
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

.actions {
  margin-top: 12px;
}

.ghost {
  border: 1px solid #334155;
  border-radius: 999px;
  padding: 10px 16px;
  background: transparent;
  color: #f8fafc;
  cursor: pointer;
}

.result {
  margin-top: 16px;
  background: #111827;
  padding: 12px;
  border-radius: 12px;
  min-height: 44px;
}
</style>
