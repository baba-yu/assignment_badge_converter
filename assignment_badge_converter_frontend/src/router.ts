import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/login" },
    { path: "/login", component: () => import("./views/LoginView.vue") },
    { path: "/signup", component: () => import("./views/SignupView.vue") },
    { path: "/tenant", component: () => import("./views/TenantSelectView.vue") },
    { path: "/app", component: () => import("./views/ChatAppView.vue") },
    { path: "/user-management", component: () => import("./views/AppHomeView.vue") },
  ],
});

export default router;
