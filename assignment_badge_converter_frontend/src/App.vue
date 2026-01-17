<script setup lang="ts">
import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { clearTokens } from "./api/auth";

const router = useRouter();
const route = useRoute();
const menuOpen = ref(false);

const section = computed(() => {
  if (route.path.startsWith("/signup") || route.path.startsWith("/login")) return "auth";
  if (route.path.startsWith("/tenant")) return "tenant";
  if (route.path.startsWith("/app") || route.path.startsWith("/user-management")) return "app";
  return "auth";
});

function logout() {
  clearTokens();
  router.push("/login");
}

function toggleMenu() {
  menuOpen.value = !menuOpen.value;
}

function closeMenu() {
  menuOpen.value = false;
}
</script>

<template>
  <div class="page">
    <header class="nav">
      <h1 class="brand">Badge Converter</h1>
      <div v-if="section !== 'auth'" class="menu">
        <button class="menu__toggle" type="button" @click="toggleMenu" aria-haspopup="true" :aria-expanded="menuOpen">
          Menu
        </button>
        <nav v-if="menuOpen" class="menu__panel">
          <template v-if="section === 'tenant'">
            <RouterLink to="/tenant" class="menu__item" active-class="menu__item--active" @click="closeMenu">
              Tenant selection
            </RouterLink>
            <button class="menu__item menu__item--danger" type="button" @click="logout">Logout</button>
          </template>
        <template v-else-if="section === 'app'">
          <RouterLink to="/app" class="menu__item" active-class="menu__item--active" @click="closeMenu">
            Chat
          </RouterLink>
          <RouterLink to="/user-management" class="menu__item" active-class="menu__item--active" @click="closeMenu">
            User management
          </RouterLink>
          <RouterLink to="/tenant" class="menu__item" @click="closeMenu">
            Switch tenant
          </RouterLink>
          <button class="menu__item menu__item--danger" type="button" @click="logout">Logout</button>
        </template>
      </nav>
      </div>
    </header>

    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
:global(body) {
  margin: 0;
  font-family: "Space Grotesk", "Helvetica Neue", Arial, sans-serif;
  color: #0d0f12;
  background: radial-gradient(1200px 800px at 10% 10%, #ffe7d1, transparent),
    radial-gradient(900px 600px at 90% 20%, #d2f1ff, transparent),
    linear-gradient(135deg, #f6f2ea, #f3f7fb);
}

.page {
  min-height: 100vh;
  display: grid;
  grid-template-rows: auto 1fr;
  gap: 24px;
  padding: 24px;
}

.nav {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.brand {
  margin: 0;
  font-size: 22px;
  letter-spacing: 0.04em;
}

.menu {
  position: relative;
  display: flex;
  justify-content: flex-end;
}

.menu__toggle {
  border: 1px solid #0d0f12;
  border-radius: 999px;
  padding: 8px 16px;
  background: #0d0f12;
  color: #f7f7f7;
  font-weight: 600;
  cursor: pointer;
}

.menu__panel {
  position: absolute;
  right: 0;
  top: calc(100% + 8px);
  display: grid;
  min-width: 220px;
  background: #ffffff;
  border-radius: 16px;
  padding: 8px;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.18);
  z-index: 10;
}

.menu__item {
  display: block;
  padding: 10px 12px;
  border-radius: 12px;
  color: #0d0f12;
  text-decoration: none;
  font-weight: 600;
  text-align: left;
  background: transparent;
}

.menu__item:hover {
  background: #f1f5f9;
}

.menu__item--active {
  background: #eef2ff;
  color: #1e28b8;
}

.menu__item--danger {
  color: #d72638;
}

.content {
  display: grid;
  place-items: center;
}

@media (max-width: 640px) {
  .page {
    padding: 16px;
  }
}
</style>
