<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useContent } from "@/composables/useContent";
import { renderMarkdown } from "@/composables/useMarkdown";

const { loadDoc } = useContent();
const slides = ref<string[]>([]);
const idx = ref(0);
const loading = ref(true);

onMounted(async () => {
  const md = await loadDoc("docs/levels/level-5-next-steps/what-next.md");
  // slide split: H2 ("## ") sections; front matter stripped
  const body = md.replace(/^---[\s\S]*?---\n/, "");
  const parts = body.split(/\n(?=## )/).filter((s) => s.trim());
  slides.value = parts.map((s) => renderMarkdown(s));
  loading.value = false;
  window.addEventListener("keydown", onKey);
});

function onKey(e: KeyboardEvent) {
  if (e.key === "ArrowRight" || e.key === " ") next();
  if (e.key === "ArrowLeft") prev();
}
function next() {
  if (idx.value < slides.value.length - 1) idx.value++;
}
function prev() {
  if (idx.value > 0) idx.value--;
}

const hasPrev = computed(() => idx.value > 0);
const hasNext = computed(() => idx.value < slides.value.length - 1);
</script>

<template>
  <div class="slides" @click.self="next()">
    <div v-if="loading" class="loading">Loading slides…</div>
    <template v-else>
      <article class="slide" v-html="slides[idx]" />
      <div class="slide-controls">
        <button class="ghost" :disabled="!hasPrev" @click="prev()">←</button>
        <span class="slide-count">{{ idx + 1 }} / {{ slides.length }}</span>
        <button class="ghost" :disabled="!hasNext" @click="next()">→</button>
      </div>
    </template>
  </div>
</template>
