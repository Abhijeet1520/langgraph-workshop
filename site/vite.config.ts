import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";
import { cpSync, existsSync, mkdirSync, readdirSync, statSync } from "fs";

// Copy ../docs into public/content at build time (single source of truth).
// Recursively copies markdown + curriculum.json, excluding nothing else.
function copyDocs() {
  return {
    name: "copy-docs",
    apply: "build" as const,
    buildStart() {
      const src = resolve(__dirname, "../docs");
      const dest = resolve(__dirname, "public/content");
      if (!existsSync(dest)) mkdirSync(dest, { recursive: true });
      const copy = (from: string, to: string) => {
        for (const entry of readdirSync(from)) {
          const f = `${from}/${entry}`;
          const t = `${to}/${entry}`;
          if (statSync(f).isDirectory()) {
            if (!existsSync(t)) mkdirSync(t, { recursive: true });
            copy(f, t);
          } else {
            cpSync(f, t);
          }
        }
      };
      copy(src, dest);
      console.log("[copy-docs] docs/ -> public/content/");
    },
  };
}

export default defineConfig({
  plugins: [vue(), copyDocs()],
  base: "/langgraph-workshop/",
  resolve: {
    alias: { "@": resolve(__dirname, "src") },
  },
});
