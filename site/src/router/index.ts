import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import TaskView from "@/views/TaskView.vue";
import SlidesView from "@/views/SlidesView.vue";
import SettingsView from "@/views/SettingsView.vue";

// GitHub Pages SPA fallback: 404.html rewrites deep links to /?/<route>
// Restore the real route before creating the router.
const ghPagesRoute = (() => {
  const search = window.location.search.slice(1);
  if (!search.startsWith("/")) return window.location.pathname;
  return search.split("~and~").join("&");
})();

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", name: "home", component: HomeView },
    { path: "/task/:taskId", name: "task", component: TaskView, props: true },
    { path: "/slides", name: "slides", component: SlidesView },
    { path: "/settings", name: "settings", component: SettingsView },
    { path: "/:pathMatch(.*)*", redirect: "/" },
  ],
});

// If we were redirected by 404.html, replace the ?/... URL with the clean route
if (window.location.search.startsWith("/=") || window.location.search.startsWith("/")) {
  router.isReady().then(() => {
    const target = ghPagesRoute.replace(import.meta.env.BASE_URL, "/");
    if (target && target !== window.location.pathname) {
      router.replace(target + window.location.hash).catch(() => {});
    }
  });
}

