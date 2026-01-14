<template>
  <div class="page">
    <header class="nav">
      <h1 class="brand">Badge Converter</h1>
      <nav class="tabs">
        <RouterLink to="/login" class="tab" active-class="tab--active">Login</RouterLink>
        <RouterLink to="/signup" class="tab" active-class="tab--active">Sign up</RouterLink>
      </nav>
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

.tabs {
  display: flex;
  gap: 8px;
  background: #0d0f12;
  padding: 6px;
  border-radius: 999px;
}

.tab {
  color: #f7f7f7;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 999px;
  font-weight: 600;
}

.tab--active {
  background: #f7f7f7;
  color: #0d0f12;
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
