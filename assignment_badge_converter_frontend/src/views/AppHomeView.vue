<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import {
  deleteTenant,
  fetchTenantUsers,
  inviteTenantUser,
  updateTenantUserRole,
  type Tenant,
  type TenantUser,
} from "../api/http";

const users = ref<TenantUser[]>([]);
const viewerRole = ref<string>("student");
const result = ref<string>("");
const currentTenant = ref<Tenant | null>(null);
const router = useRouter();
const showToast = ref(false);
let toastTimer: number | null = null;

const inviteEmail = ref("");
const inviteFirstName = ref("");
const inviteLastName = ref("");
const inviteRole = ref("student");

const isAdmin = computed(() => viewerRole.value === "admin");

watch(result, (value) => {
  if (!value) return;
  showToast.value = true;
  if (toastTimer) window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => {
    showToast.value = false;
    toastTimer = null;
  }, 5000);
});

async function loadUsers() {
  result.value = "loading...";
  try {
    const data = await fetchTenantUsers();
    users.value = data.users;
    viewerRole.value = data.viewer_role;
    currentTenant.value = data.tenant;
    result.value = "OK";
  } catch (e: any) {
    result.value = `NG: ${e?.message ?? e}`;
  }
}

async function invite() {
  result.value = "running...";
  try {
    const user = await inviteTenantUser({
      email: inviteEmail.value,
      first_name: inviteFirstName.value || undefined,
      last_name: inviteLastName.value || undefined,
      role: inviteRole.value,
    });
    users.value = [...users.value, user];
    inviteEmail.value = "";
    inviteFirstName.value = "";
    inviteLastName.value = "";
    inviteRole.value = "student";
    result.value = `OK: invited ${user.email}`;
  } catch (e: any) {
    result.value = `NG: ${e?.message ?? e}`;
  }
}

async function changeRole(user: TenantUser, role: string) {
  result.value = "running...";
  try {
    const updated = await updateTenantUserRole(user.id, role);
    users.value = users.value.map((u) => (u.id === user.id ? updated : u));
    result.value = `OK: updated ${updated.email}`;
  } catch (e: any) {
    result.value = `NG: ${e?.message ?? e}`;
  }
}

async function removeTenant() {
  if (!currentTenant.value) {
    result.value = "NG: tenant not found";
    return;
  }
  if (!window.confirm(`Delete tenant "${currentTenant.value.name}"?`)) return;
  result.value = "running...";
  try {
    await deleteTenant(currentTenant.value.id);
    result.value = "OK: tenant deleted";
    currentTenant.value = null;
    users.value = [];
    await router.push("/tenant");
  } catch (e: any) {
    result.value = `NG: ${e?.message ?? e}`;
  }
}

onMounted(loadUsers);
</script>

<template>
  <section class="shell">
    <header class="header">
      <h2>User Management</h2>
      <p>Admin can invite and update roles. Others can view only.</p>
    </header>

    <div class="toolbar">
      <RouterLink class="ghost" to="/tenant">Back to tenant selection</RouterLink>
      <button class="danger" type="button" :disabled="!isAdmin" @click="removeTenant">Delete tenant</button>
    </div>

    <form class="invite" @submit.prevent="invite">
      <h3>Invite</h3>
      <div class="fields">
        <input v-model="inviteEmail" placeholder="email" type="email" :disabled="!isAdmin" />
        <input v-model="inviteFirstName" placeholder="first name" :disabled="!isAdmin" />
        <input v-model="inviteLastName" placeholder="last name" :disabled="!isAdmin" />
        <select v-model="inviteRole" :disabled="!isAdmin">
          <option value="student">Student</option>
          <option value="faculty">Faculty</option>
          <option value="admin">Admin</option>
        </select>
      </div>
      <button class="primary" type="submit" :disabled="!isAdmin">Send invite</button>
    </form>

    <div class="table">
      <div class="row head">
        <span>Name</span>
        <span>Email</span>
        <span>Role</span>
      </div>
      <div v-for="user in users" :key="user.id" class="row">
        <span>{{ user.first_name }} {{ user.last_name }}</span>
        <span>{{ user.email }}</span>
        <span>
          <select v-if="isAdmin" :value="user.role" @change="changeRole(user, ($event.target as HTMLSelectElement).value)">
            <option value="student">Student</option>
            <option value="faculty">Faculty</option>
            <option value="admin">Admin</option>
          </select>
          <span v-else>{{ user.role }}</span>
        </span>
      </div>
    </div>

    <transition name="toast">
      <div v-if="showToast && result" class="toast" role="status">{{ result }}</div>
    </transition>
  </section>
</template>

<style scoped>
.shell {
  width: min(960px, 100%);
  background: #ffffff;
  border-radius: 20px;
  padding: 28px;
  box-shadow: 0 18px 50px rgba(15, 23, 42, 0.1);
  display: grid;
  gap: 20px;
}

.header h2 {
  margin: 0 0 6px;
  font-size: 28px;
}

.invite {
  display: grid;
  gap: 12px;
  padding: 16px;
  border-radius: 16px;
  background: #f8fafc;
}

.fields {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 8px;
}

.fields input,
.fields select {
  border: 1px solid #d1d5db;
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 14px;
}

.primary {
  width: fit-content;
  border: none;
  border-radius: 999px;
  padding: 10px 16px;
  background: #1e3a8a;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
}

.toolbar {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.ghost {
  border: 1px solid #1e3a8a;
  border-radius: 999px;
  padding: 8px 14px;
  color: #1e3a8a;
  text-decoration: none;
  font-weight: 600;
}

.danger {
  border: 1px solid #d72638;
  border-radius: 999px;
  padding: 8px 14px;
  background: #d72638;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
}

.danger:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.table {
  display: grid;
  gap: 8px;
}

.row {
  display: grid;
  grid-template-columns: 1.2fr 1.4fr 0.8fr;
  gap: 12px;
  align-items: center;
  padding: 10px 12px;
  border-radius: 12px;
  background: #f8fafc;
}

.row.head {
  background: transparent;
  font-weight: 700;
}

.row select {
  width: 100%;
  border-radius: 8px;
  padding: 6px 8px;
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
  .row {
    grid-template-columns: 1fr;
  }
}
</style>
