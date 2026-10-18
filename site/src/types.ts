export interface WorkshopSettings {
  baseUrl: string;
  apiKey: string;
  model: string;
  providerHint: string;
}

export interface CurriculumNotebook {
  path: string;      // notebooks/level-1-basics/01_introduction.ipynb
  title: string;
  colabUrl: string;
}

export interface CurriculumTask {
  id: string;
  title: string;
  concept: string;
  doc: string | null;
  notebooks: CurriculumNotebook[];
}

export interface CurriculumLevel {
  id: string;
  number: number;
  title: string;
  folder: string;
  notebookFolder: string | null;
  tagline: string;
  slides?: boolean;
  tasks: CurriculumTask[];
}

export interface Curriculum {
  repo: string;
  colabBase: string;
  levels: CurriculumLevel[];
}
