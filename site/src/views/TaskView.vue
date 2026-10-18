<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useContent } from "@/composables/useContent";
import { useProgressStore } from "@/stores/progress";
import { renderMarkdown } from "@/composables/useMarkdown";

const props = defineProps<{ taskId: string }>();
const router = useRouter();
const { curriculum, loadCurriculum, loadDoc, findTask, allTasks } = useContent();
const progress = useProgressStore();

const html = ref("");
const loading = ref(true);
const error = ref("");

onMounted(async () => {
  await loadCurriculum();
  const found = findTask(props.taskId);
  if (!found) {
    error.value = `Task "${props.taskId}" not found.`;
    loading.value = false;
    return;
  }
  if (found.task.doc) {
    try {
      const md = await loadDoc(found.task.doc);
      html.value = renderMarkdown(md);
    } catch (e: any) {
      error.value = `Failed to load doc: ${e?.message ?? e}`;
    }
  }
  loading.value = false;
});

const found = computed(() => findTask(props.taskId));

const nav = computed(() => {
  const tasks = allTasks(curriculum.value!);
  const idx = tasks.findIndex(({ task }) => task.id === props.taskId);
  return {
    prev: idx > 0 ? tasks[idx - 1] : null,
    next: idx >= 0 && idx < tasks.length - 1 ? tasks[idx + 1] : null,
  };
});
</script>

<template>
  <div class="task-view">
    <div v-if="loading" class="loading">Loading…</div>
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
      <button class="ghost" @click="router.push('/')">← Back to journey</button>
    </div>
    <template v-else-if="found">
      <header class="task-header">
        <div class="task-meta">
          <span class="level-chip">Level {{ found.level.number }} · {{ found.level.title }}</span>
          <h1>{{ found.task.title }}</h1>
          <p class="concept">{{ found.task.concept }}</p>
        </div>
        <button
          class="done-btn"
          :class="{ isDone: progress.isDone(found.task.id) }"
          @click="progress.toggle(found.task.id)"
        >
          {{ progress.isDone(found.task.id) ? "✅ Completed" : "Mark complete" }}
        </button>
      </header>

      <!-- Follow-along panel: notebooks + Colab -->
      <aside class="followalong">
        <h3>🏃 Follow along</h3>
        <p v-if="!found.task.notebooks.length">This task is docs-only — read, then mark complete.</p>
        <ul v-else class="nb-list">
          <li v-for="nb in found.task.notebooks" :key="nb.path">
            <a class="nb-link" :href="nb.colabUrl" target="_blank" rel="noopener">
              <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" />
              <span class="nb-title">{{ nb.title }}</span>
            </a>
          </li>
        </ul>
        <p class="hint">
          Set your provider first: <router-link to="/settings">⚙️ settings</router-link> → “Copy for Colab”.
        </p>
      </aside>

      <!-- Rendered doc -->
      <article class="doc" v-html="html" />

      <!-- Prev / next -->
      <nav class="task-nav">
        <button v-if="nav.prev" class="ghost" @click="router.push({ name: 'task', params: { taskId: nav.prev!.task.id } })">
          ← {{ nav.prev!.task.title }}
        </button>
        <span v-else />
        <button v-if="nav.next" class="primary" @click="router.push({ name: 'task', params: { taskId: nav.next!.task.id } })">
          {{ nav.next!.task.title }} →
        </button>
      </nav>
    </template>
  </div>
</template>
