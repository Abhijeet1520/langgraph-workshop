import { ref } from "vue";
import type { Curriculum, CurriculumLevel, CurriculumNotebook, CurriculumTask } from "@/types";

const CONTENT = `${import.meta.env.BASE_URL}content`;

const curriculum = ref<Curriculum | null>(null);
const docCache = new Map<string, string>();

export function useContent() {
  async function loadCurriculum(): Promise<Curriculum> {
    if (curriculum.value) return curriculum.value;
    const res = await fetch(`${CONTENT}/curriculum.json`);
    if (!res.ok) throw new Error(`curriculum.json: ${res.status}`);
    const raw = await res.json();
    // normalize: expand notebook filenames into full objects with colab urls
    for (const level of raw.levels as any[]) {
      level.notebookFolder = level.notebookFolder ?? null;
      for (const task of level.tasks as any[]) {
        task.notebooks = task.notebooks ?? [];
        task.doc = task.doc ?? null;
        task.notebooks = [
          ...(task.notebooks ?? []).map((nb: string) => {
            const path = `${level.notebookFolder}/${nb}`;
            return {
              path,
              title: nb.replace(/^\d+_/, "").replace(/\.ipynb$/, "").replace(/_/g, " "),
              colabUrl: `${raw.colabBase}/${path}`,
            } satisfies CurriculumNotebook;
          }),
          ...(task.notebook
            ? [
                {
                  path: task.notebook,
                  title: task.notebook.split("/").pop()!.replace(/\.ipynb$/, ""),
                  colabUrl: `${raw.colabBase}/${task.notebook}`,
                } satisfies CurriculumNotebook,
              ]
            : []),
        ];
        task.doc = task.doc;
      }
    }
    curriculum.value = raw as Curriculum;
    return curriculum.value;
  }

  async function loadDoc(path: string): Promise<string> {
    if (docCache.has(path)) return docCache.get(path)!;
    const res = await fetch(`${CONTENT}/${path.replace(/^docs\//, "")}`);
    if (!res.ok) throw new Error(`doc ${path}: ${res.status}`);
    const text = await res.text();
    docCache.set(path, text);
    return text;
  }

  function allTasks(c: Curriculum): Array<{ task: CurriculumTask; level: CurriculumLevel }> {
    return c.levels.flatMap((level) => level.tasks.map((task) => ({ task, level })));
  }

  function findTask(taskId: string): { task: CurriculumTask; level: CurriculumLevel } | undefined {
    if (!curriculum.value) return undefined;
    return allTasks(curriculum.value).find(({ task }) => task.id === taskId);
  }

  return { curriculum, loadCurriculum, loadDoc, findTask, allTasks, CONTENT };
}
