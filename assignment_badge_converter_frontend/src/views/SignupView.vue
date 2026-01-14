<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { signup } from "../api/http";

const router = useRouter();
const username = ref("");
const email = ref("");
const firstName = ref("");
const lastName = ref("");
const password = ref("");
const result = ref<string>("");

async function runSignup() {
  result.value = "running...";
  try {
    const user = await signup({
      username: username.value,
      email: email.value,
      password: password.value,
      first_name: firstName.value || undefined,
      last_name: lastName.value || undefined,
    });
    result.value = `OK: signed up ${user.username}`;
    await router.push("/login");
  } catch (e: any) {
    result.value = `NG: ${e?.message ?? e}`;
  }
}
</script>

<template>
  <section class="card">
    <header class="card__header">
      <p class="eyebrow">New account</p>
      <h2>Create your badge workspace</h2>
      <p class="muted">Sign up once, then jump to login.</p>
    </header>

    <form class="form" @submit.prevent="runSignup">
      <label class="field">
        <span>Username</span>
        <input v-model="username" placeholder="your-handle" autocomplete="username" />
      </label>
      <label class="field">
        <span>Email</span>
        <input v-model="email" placeholder="you@example.com" autocomplete="email" />
      </label>
      <label class="field">
        <span>First name</span>
        <input v-model="firstName" placeholder="first name" autocomplete="given-name" />
      </label>
      <label class="field">
        <span>Last name</span>
        <input v-model="lastName" placeholder="last name" autocomplete="family-name" />
      </label>
      <label class="field">
        <span>Password</span>
        <input v-model="password" type="password" placeholder="••••••••" autocomplete="new-password" />
      </label>
      <button class="primary" type="submit">Create account</button>
    </form>

    <pre class="result">{{ result }}</pre>
  </section>
</template>

<style scoped>
.card {
  width: min(520px, 100%);
  background: #ffffff;
  border-radius: 24px;
  padding: 28px;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.12);
}

.card__header h2 {
  margin: 4px 0 8px;
  font-size: 28px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 12px;
  color: #f05d23;
  margin: 0;
}

.muted {
  margin: 0;
  color: #4b5563;
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
  color: #111827;
}

.field input {
  border: 1px solid #d1d5db;
  border-radius: 12px;
  padding: 10px 12px;
  font-size: 15px;
}

.primary {
  margin-top: 8px;
  border: none;
  border-radius: 999px;
  padding: 12px 18px;
  background: #0d0f12;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
}

.result {
  margin-top: 16px;
  background: #f8fafc;
  padding: 12px;
  border-radius: 12px;
  min-height: 44px;
}
</style>
