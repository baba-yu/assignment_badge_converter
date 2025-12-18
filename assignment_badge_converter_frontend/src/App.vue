<script setup lang="ts">
import { ref } from "vue";
import { smoke } from "./api/smoke";

const username = ref("");
const password = ref("");
const result = ref<string>("");

async function run() {
  result.value = "running...";
  try {
    await smoke(username.value, password.value);
    result.value = "OK: login -> internal health";
  } catch (e: any) {
    result.value = `NG: ${e?.message ?? e}`;
  }
}
</script>

<template>
  <div style="padding: 16px; max-width: 520px;">
    <h2>Smoke Test</h2>

    <div style="display: grid; gap: 8px;">
      <input v-model="username" placeholder="username" />
      <input v-model="password" placeholder="password" type="password" />
      <button @click="run">Run</button>
      <pre>{{ result }}</pre>
    </div>
  </div>
</template>
