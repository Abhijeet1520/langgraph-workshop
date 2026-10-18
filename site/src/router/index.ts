import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import TaskView from "@/views/TaskView.vue";
import SlidesView from "@/views/SlidesView.vue";
import SettingsView from "@/views/SettingsView.vue";

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
