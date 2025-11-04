import { atom } from "jotai";

// Game state atoms
export const currentBookAtom = atom<number>(1);
export const currentSectionAtom = atom<number>(1);
export const gameHistoryAtom = atom<number[]>([]);

// Add more game-related atoms as needed:
// - combatState
// - inventoryState
// - dialogState
// etc.
