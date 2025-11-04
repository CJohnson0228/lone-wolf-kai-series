// Book section types
export interface BookSection {
  section: number;
  text: string;
  type: "choice" | "combat" | "narrative" | "ending" | "defeat" | "victory";
  choices: Choice[];
  illustrations?: string[];
  combat?: CombatEncounter;
}

export interface Choice {
  text: string;
  target: number;
  conditional?: boolean;
  requires?: string;
}

export interface CombatEncounter {
  enemy_name: string;
  combat_skill: number;
  endurance: number;
  can_evade: boolean;
  modifiers?: string[];
}

export interface Discipline {
  id: string;
  name: string;
  description: string;
}

export interface BookData {
  series: string;
  book_number: number;
  title: string;
  authors: string;
  version: string;
  disciplines: Discipline[];
  equipment_rules: any;
  sections: Record<string, BookSection>;
}

// Re-export Character type from store
export type { Character } from "../store/character";
