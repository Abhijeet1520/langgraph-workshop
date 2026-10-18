<script setup lang="ts">
import { ref } from "vue";
import { useSettingsStore } from "@/stores/settings";
import type { WorkshopSettings } from "@/types";

const store = useSettingsStore();

const draft = ref<WorkshopSettings>({ ...store.settings });
const copied = ref("");

const PROVIDERS = [
  { hint: "instructor", label: "Instructor endpoint (workshop)", baseUrl: "" },
  { hint: "openrouter", label: "OpenRouter", baseUrl: "https://openrouter.ai/api/v1" },
  { hint: "huggingface", label: "Hugging Face", baseUrl: "https://router.huggingface.co/v1" },
  { hint: "anthropic", label: "Anthropic (OpenAI-compat)", baseUrl: "https://api.anthropic.com/v1" },
  { hint: "custom", label: "Custom / local proxy", baseUrl: "" },
];

async function save() {
  store.update({ ...draft.value });
}

async function copy(text: string, what: string) {
  await navigator.clipboard?.writeText(text);
  copied.value = what;
  setTimeout(() => (copied.value = ""), 1200);
}

function onImport(e: Event) {
  const input = e.target as HTMLInputElement;
  const file = input.files?.[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      store.importJson(String(reader.result));
      draft.value = { ...store.settings };
    } catch (err) {
      alert("Invalid settings.json");
    }
  };
  reader.readAsText(file);
  input.value = "";
}
</script>

<template>
  <div class="settings-view">
    <h1>⚙️ Provider Settings</h1>
    <p class="sub">
      One config, everywhere: notebooks read <code>OPENAI_API_KEY</code>, <code>OPENAI_API_BASE</code>,
      <code>OPENAI_MODEL</code>. Fill these in once, then use the copy buttons. Values are stored only in
      <strong>your browser</strong> (localStorage) — never sent to us.
      All scenarios &amp; where to get values:
      <a href="https://github.com/Abhijeet1520/langgraph-workshop/blob/main/docs/setup/providers.md" target="_blank" rel="noopener">providers.md</a>.
    </p>

    <section class="card">
      <h3>Values</h3>
      <label class="field">
        <span>Provider</span>
        <select v-model="draft.providerHint" @change="draft.baseUrl = PROVIDERS.find((p) => p.hint === draft.providerHint)?.baseUrl || draft.baseUrl">
          <option v-for="p in PROVIDERS" :key="p.hint" :value="p.hint">{{ p.label }}</option>
        </select>
      </label>
      <label class="field">
        <span>Base URL</span>
        <input v-model="draft.baseUrl" placeholder="https://…/v1" spellcheck="false" />
      </label>
      <label class="field">
        <span>API key</span>
        <span class="key-row">
          <input
            v-model="draft.apiKey"
            :type="store.showKey ? 'text' : 'password'"
            placeholder="paste your key"
            spellcheck="false"
            autocomplete="off"
          />
          <button class="ghost mini" @click="store.toggleShowKey()" :title="store.showKey ? 'Hide' : 'Show'">
            {{ store.showKey ? "🙈" : "👁" }}
          </button>
        </span>
      </label>
      <label class="field">
        <span>Model</span>
        <input v-model="draft.model" placeholder="openai/gpt-4.1-mini" spellcheck="false" />
      </label>
      <div class="actions">
        <button class="primary" @click="save()">Save</button>
        <button class="ghost" @click="store.verifyConnection()" :disabled="store.verify === 'busy'">
          {{ store.verify === "busy" ? "Testing…" : "Verify connection" }}
        </button>
        <span v-if="store.verifyMsg" class="verify-msg" :class="store.verify">{{ store.verifyMsg }}</span>
      </div>
    </section>

    <section class="card" v-if="store.isConfigured">
      <h3>Copy into your environment</h3>
      <div class="snippet">
        <div class="snippet-head">
          <span>Terminal (local)</span>
          <button class="ghost mini" @click="copy(store.envExports, 'env')">📋 {{ copied === "env" ? "Copied!" : "Copy" }}</button>
        </div>
        <pre><code>{{ store.envExports }}</code></pre>
      </div>
      <div class="snippet">
        <div class="snippet-head">
          <span>Colab cell</span>
          <button class="ghost mini" @click="copy(store.colabEnv, 'colab')">📋 {{ copied === "colab" ? "Copied!" : "Copy" }}</button>
        </div>
        <pre><code>{{ store.colabEnv }}</code></pre>
      </div>
      <div class="snippet">
        <div class="snippet-head">
          <span>settings.json</span>
          <div class="snippet-btns">
            <button class="ghost mini" @click="copy(store.settingsJson, 'json')">📋 {{ copied === "json" ? "Copied!" : "Copy" }}</button>
            <button class="ghost mini" @click="store.downloadJson()">⬇ Download</button>
          </div>
        </div>
        <pre><code>{{ store.settingsJson }}</code></pre>
      </div>
      <p class="hint">
        If the instructor rotates the endpoint mid-session (e.g. switches to OpenRouter/Hugging Face), just
        update the values here and re-copy.
      </p>
    </section>

    <section class="card">
      <h3>Import / reset</h3>
      <label class="file-label">
        <input type="file" accept="application/json" @change="onImport" />
        ⬆ Import settings.json
      </label>
    </section>
  </div>
</template>
