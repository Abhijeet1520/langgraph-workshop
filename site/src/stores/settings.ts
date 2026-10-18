import { defineStore } from "pinia";
import type { WorkshopSettings } from "@/types";

const LS_KEY = "lgw.settings.v1";

const DEFAULTS: WorkshopSettings = {
  baseUrl: "",
  apiKey: "",
  model: "openai/gpt-4.1-mini",
  providerHint: "instructor",
};

export const useSettingsStore = defineStore("settings", {
  state: (): { settings: WorkshopSettings; showKey: boolean; verify: "idle" | "ok" | "fail" | "busy"; verifyMsg: string } => ({
    settings: load(),
    showKey: false,
    verify: "idle",
    verifyMsg: "",
  }),
  getters: {
    isConfigured: (s) => Boolean(s.settings.baseUrl && s.settings.apiKey && s.settings.model),
    maskedKey: (s) =>
      s.settings.apiKey
        ? s.settings.apiKey.slice(0, 6) + "•".repeat(Math.max(0, s.settings.apiKey.length - 6))
        : "",
    envExports(): string {
      const { baseUrl, apiKey, model } = this.settings;
      return [
        `export OPENAI_API_KEY="${apiKey}"`,
        `export OPENAI_API_BASE="${baseUrl}"`,
        `export OPENAI_MODEL="${model}"`,
      ].join("\n");
    },
    colabEnv(): string {
      const { apiKey, baseUrl, model } = this.settings;
      return [
        `%env OPENAI_API_KEY=${apiKey}`,
        `%env OPENAI_API_BASE=${baseUrl}`,
        `%env OPENAI_MODEL=${model}`,
      ].join("\n");
    },
    settingsJson(): string {
      return JSON.stringify(this.settings, null, 2);
    },
  },
  actions: {
    update(patch: Partial<WorkshopSettings>) {
      this.settings = { ...this.settings, ...patch };
      save(this.settings);
    },
    toggleShowKey() {
      this.showKey = !this.showKey;
    },
    importJson(text: string) {
      const parsed = JSON.parse(text);
      this.update({
        baseUrl: String(parsed.baseUrl ?? ""),
        apiKey: String(parsed.apiKey ?? ""),
        model: String(parsed.model ?? ""),
        providerHint: String(parsed.providerHint ?? "custom"),
      });
    },
    downloadJson() {
      const blob = new Blob([this.settingsJson], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "settings.json";
      a.click();
      URL.revokeObjectURL(url);
    },
    async verifyConnection() {
      if (!this.isConfigured) {
        this.verify = "fail";
        this.verifyMsg = "Fill in base URL, API key and model first.";
        return;
      }
      this.verify = "busy";
      this.verifyMsg = "Testing…";
      const { baseUrl, apiKey } = this.settings;
      try {
        const res = await fetch(`${baseUrl.replace(/\/$/, "")}/models`, {
          headers: { Authorization: `Bearer ${apiKey}` },
        });
        if (res.ok) {
          this.verify = "ok";
          this.verifyMsg = "✅ Endpoint reachable — you're set.";
        } else {
          this.verify = "fail";
          this.verifyMsg = `Endpoint responded ${res.status}. Key/model may still be fine (some proxies restrict /models) — if notebooks work, ignore this.`;
        }
      } catch (e: any) {
        this.verify = "fail";
        this.verifyMsg = `Could not reach ${baseUrl} (${e?.name ?? "error"}). Check the URL, your connection, and that key + URL come from the same provider.`;
      }
    },
  },
});

function load(): WorkshopSettings {
  try {
    const raw = localStorage.getItem(LS_KEY);
    if (raw) return { ...DEFAULTS, ...JSON.parse(raw) };
  } catch {
    /* corrupted — fall back to defaults */
  }
  return { ...DEFAULTS };
}

function save(s: WorkshopSettings) {
  try {
    localStorage.setItem(LS_KEY, JSON.stringify(s));
  } catch {
    /* storage full/blocked — session-only then */
  }
}
