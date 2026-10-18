<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted } from "vue";
import { useSettingsStore } from "@/stores/settings";
import { useProgressStore } from "@/stores/progress";
import { useContent } from "@/composables/useContent";

const settings = useSettingsStore();
const progress = useProgressStore();
const { curriculum, loadCurriculum, allTasks } = useContent();

const totalCount = computed(() => (curriculum.value ? allTasks(curriculum.value).length : 0));

let onDocClick: ((e: MouseEvent) => void) | null = null;

onMounted(async () => {
  try {
    await loadCurriculum();
  } catch (e) {
    console.error("curriculum failed to load", e);
  }
  onDocClick = (e) => {
    const t = e.target as HTMLElement;
    if (t.classList?.contains("copy-btn")) {
      const code = decodeURIComponent(t.getAttribute("data-code") ?? "");
      navigator.clipboard?.writeText(code);
      const old = t.textContent;
      t.textContent = "✓";
      setTimeout(() => (t.textContent = old ?? "⧉"), 900);
    }
  };
  document.addEventListener("click", onDocClick);
});

onBeforeUnmount(() => {
  if (onDocClick) document.removeEventListener("click", onDocClick);
});
</script>

<template>
  <div class="app-shell">
    <header class="topbar">
      <router-link to="/" class="brand">
        <span class="logo-dot">🕸️</span>
        <span>Lang<span class="l2">Graph</span> Workshop</span>
      </router-link>
      <nav class="topnav">
        <router-link to="/">Journey</router-link>
        <router-link to="/slides">Slides</router-link>
      </nav>
      <div class="topbar-right">
        <div class="progress-ring" :title="`${progress.count}/${totalCount} tasks complete`">
          <span class="ring-num">{{ progress.count }}/{{ totalCount }}</span>
        </div>
        <router-link to="/settings" class="gear" :class="{ configured: settings.isConfigured }" title="Settings">⚙️</router-link>
      </div>
    </header>
    <main class="main">
      <router-view />
    </main>
    <footer class="footer">
      <a :href="curriculum?.repo ?? 'https://github.com/Abhijeet1520/langgraph-workshop'" target="_blank" rel="noopener">GitHub</a>
      <span> · LangGraph Workshop — zero to email agent</span>
    </footer>
  </div>
</template>
