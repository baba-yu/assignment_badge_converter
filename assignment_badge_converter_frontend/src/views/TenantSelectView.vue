<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { fetchTenants, tenantSelect, type Tenant } from "../api/http";

const router = useRouter();
const tenantName = ref("");
const selectedTenantId = ref<number | null>(null);
const tenants = ref<Tenant[]>([]);
const result = ref<string>("");
const showCreate = ref(false);
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

async function loadTenants() {
  try {
    const data = await fetchTenants();
    tenants.value = data.tenants;
  } catch (e: any) {
    result.value = `NG: ${e?.message ?? e}`;
  }
}

async function createTenant() {
  result.value = "running...";
  try {
    if (!tenantName.value.trim()) throw new Error("Tenant name is required");
    const tenant = await tenantSelect({ name: tenantName.value });
    result.value = `OK: created ${tenant.name} (#${tenant.id})`;
    tenants.value = [...tenants.value, tenant];
    selectedTenantId.value = tenant.id;
    showCreate.value = false;
    await router.push("/app");
  } catch (e: any) {
    result.value = `NG: ${e?.message ?? e}`;
  }
}

async function selectTenant() {
  result.value = "running...";
  try {
    if (!selectedTenantId.value) throw new Error("Select a tenant");
    const id = selectedTenantId.value;
    const tenant = await tenantSelect({ tenant_id: id });
    result.value = `OK: selected ${tenant.name} (#${tenant.id})`;
    await router.push("/app");
  } catch (e: any) {
    result.value = `NG: ${e?.message ?? e}`;
  }
}

function openCreate() {
  tenantName.value = "";
  showCreate.value = true;
}

function closeCreate() {
  showCreate.value = false;
}

onMounted(loadTenants);
</script>

<template>
  <section class="shell">
    <header class="header">
      <p class="eyebrow">Tenant</p>
      <h2>Create or choose a workspace</h2>
      <p class="muted">After login, select your tenant to continue.</p>
    </header>

    <form class="panel" @submit.prevent="selectTenant">
      <div class="panel__head">
        <h3>Your tenants</h3>
        <button class="primary" type="button" @click="openCreate">Create tenant</button>
      </div>

      <div class="tenant-grid">
        <button
          v-for="tenant in tenants"
          :key="tenant.id"
          type="button"
          class="tenant-card"
          :class="{ 'tenant-card--active': tenant.id === selectedTenantId }"
          @click="selectedTenantId = tenant.id"
        >
          <span class="tenant-card__name">{{ tenant.name }}</span>
        </button>
        <p v-if="tenants.length === 0" class="empty">No tenants yet.</p>
      </div>

      <div class="panel__actions">
        <button class="ghost" type="submit" :disabled="!selectedTenantId">Continue</button>
      </div>
    </form>

    <div v-if="showCreate" class="modal-backdrop" @click.self="closeCreate">
      <div class="modal">
        <h3>Create tenant</h3>
        <label class="field">
          <span>Tenant name</span>
          <input v-model="tenantName" placeholder="Acme Labs" />
        </label>
        <div class="modal__actions">
          <button class="ghost" type="button" @click="closeCreate">Cancel</button>
          <button class="primary" type="button" @click="createTenant">Create</button>
        </div>
      </div>
    </div>

    <transition name="toast">
      <div v-if="showToast && result" class="toast" role="status">{{ result }}</div>
    </transition>
  </section>
</template>

<style scoped>
.shell {
  width: min(760px, 100%);
  display: grid;
  gap: 20px;
}

.header h2 {
  margin: 6px 0 8px;
  font-size: 28px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 12px;
  color: #1e3a8a;
  margin: 0;
}

.muted {
  margin: 0;
  color: #4b5563;
}

.panel {
  background: #ffffff;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 18px 50px rgba(15, 23, 42, 0.12);
  display: grid;
  gap: 16px;
}

.panel__head {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
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
  border: none;
  border-radius: 999px;
  padding: 12px 18px;
  background: #1e3a8a;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
}

.ghost {
  border: 1px solid #1e3a8a;
  border-radius: 999px;
  padding: 12px 18px;
  background: transparent;
  color: #1e3a8a;
  font-weight: 600;
  cursor: pointer;
}

.ghost:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.tenant-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.tenant-card {
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 16px;
  background: #f9fafb;
  text-align: left;
  font-weight: 600;
  color: #111827;
  cursor: pointer;
}

.tenant-card--active {
  border-color: #1e3a8a;
  box-shadow: 0 0 0 2px rgba(30, 58, 138, 0.15);
  background: #eef2ff;
}

.tenant-card__name {
  display: block;
  font-size: 16px;
}

.empty {
  margin: 0;
  color: #6b7280;
}

.panel__actions {
  display: flex;
  justify-content: flex-end;
}

.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.5);
  display: grid;
  place-items: center;
  padding: 16px;
}

.modal {
  width: min(420px, 100%);
  background: #ffffff;
  border-radius: 18px;
  padding: 20px;
  display: grid;
  gap: 12px;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.2);
}

.modal__actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
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
