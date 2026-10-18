import { defineStore } from "pinia";

const LS_KEY = "lgw.progress.v1";

export const useProgressStore = defineStore("progress", {
  state: (): { done: Record<string, boolean> } => ({ done: load() }),
  getters: {
    count: (s) => Object.values(s.done).filter(Boolean).length,
  },
  actions: {
    isDone(taskId: string) {
      return Boolean(this.done[taskId]);
    },
    toggle(taskId: string) {
      this.done[taskId] = !this.done[taskId];
      save(this.done);
    },
    markDone(taskId: string) {
      if (!this.done[taskId]) {
        this.done[taskId] = true;
        save(this.done);
      }
    },
    reset() {
      this.done = {};
      save(this.done);
    },
  },
});

function load(): Record<string, boolean> {
  try {
    const raw = localStorage.getItem(LS_KEY);
    if (raw) return JSON.parse(raw);
  } catch {
    /* ignore */
  }
  return {};
}

function save(d: Record<string, boolean>) {
  try {
    localStorage.setItem(LS_KEY, JSON.stringify(d));
  } catch {
    /* ignore */
  }
}
