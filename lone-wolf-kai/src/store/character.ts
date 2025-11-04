import { atom } from "jotai";
import { atomWithStorage } from "jotai/utils";

// Character type - expand this as needed
export interface Character {
  id: string;
  name: string;
  combatSkill: number;
  endurance: number;
  currentEndurance: number;
  disciplines: string[];
  weapons: string[];
  backpack: string[];
  specialItems: string[];
  goldCrowns: number;
  currentBook: number;
  currentSection: number;
  booksCompleted: number;
  createdAt: string;
  lastPlayed: string;
}

// Current active character
export const currentCharacterAtom = atomWithStorage<Character | null>(
  "lone-wolf-current-character",
  null
);

// All saved characters
export const charactersAtom = atomWithStorage<Character[]>(
  "lone-wolf-characters",
  []
);

// Derived atom: Has any characters
export const hasCharactersAtom = atom((get) => {
  const characters = get(charactersAtom);
  return characters.length > 0;
});
