import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/login" },
    { path: "/login", component: () => import("./views/LoginView.vue") },
    { path: "/signup", component: () => import("./views/SignupView.vue") },
  ],
});

export default router;
