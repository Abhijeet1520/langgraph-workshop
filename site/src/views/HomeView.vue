<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useContent } from "@/composables/useContent";
import { useProgressStore } from "@/stores/progress";
import { useSettingsStore } from "@/stores/settings";

const router = useRouter();
const { curriculum, loadCurriculum } = useContent();
const progress = useProgressStore();
const settings = useSettingsStore();
const loading = ref(true);

onMounted(async () => {
  await loadCurriculum();
  loading.value = false;
});

const levelDone = computed(() => (levelId: string) => {
  const lvl = curriculum.value?.levels.find((l) => l.id === levelId);
  if (!lvl) return 0;
  const done = lvl.tasks.filter((t) => progress.isDone(t.id)).length;
  return lvl.tasks.length ? done / lvl.tasks.length : 0;
});

const LEVEL_ICONS = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"];
</script>

<template>
  <div class="home">
    <section class="hero">
      <h1>Zero to <span class="accent">Email Agent</span></h1>
      <p class="sub">
        Learn LangGraph by building a real email processing agent — levelled notebooks,
        follow-along docs, bring your own LLM provider (or use the workshop endpoint).
      </p>
      <div class="hero-actions">
        <button class="primary" @click="router.push({ name: 'task', params: { taskId: 'task0-welcome' } })">
          Start Level 0 →
        </button>
        <button v-if="!settings.isConfigured" class="ghost" @click="router.push('/settings')">
          ⚙️ Configure your provider first
        </button>
      </div>
    </section>

    <div v-if="loading" class="loading">Loading curriculum…</div>

    <section v-else class="levels">
      <div
        v-for="level in curriculum?.levels"
        :key="level.id"
        class="level-card"
        :class="{ 'level-done': levelDone(level.id) === 1 }"
      >
        <div class="level-head">
          <span class="level-icon">{{ LEVEL_ICONS[level.number] }}</span>
          <div>
            <h3>{{ level.title }}</h3>
            <p class="tagline">{{ level.tagline }}</p>
          </div>
          <span class="level-progress">{{ Math.round(levelDone(level.id) * 100) }}%</span>
        </div>
        <div class="level-tasks">
          <div
            v-for="task in level.tasks"
            :key="task.id"
            class="task-row"
            :class="{ done: progress.isDone(task.id) }"
            @click="level.slides ? router.push('/slides') : router.push({ name: 'task', params: { taskId: task.id } })"
          >
            <span class="task-check">{{ progress.isDone(task.id) ? "✅" : "⬜" }}</span>
            <span class="task-title">{{ task.title }}</span>
            <span class="task-concept">{{ task.concept }}</span>
            <span v-if="task.notebooks.length" class="task-nbs">{{ task.notebooks.length }} notebook{{ task.notebooks.length > 1 ? "s" : "" }}</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
