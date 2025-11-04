/**
 * Utility functions
 */

// Generate random number 0-9 (for character creation and combat)
export function randomNumber(): number {
  return Math.floor(Math.random() * 10);
}

// Generate Combat Skill (10 + random 0-9)
export function generateCombatSkill(): number {
  return 10 + randomNumber();
}

// Generate Endurance (20 + random 0-9)
export function generateEndurance(): number {
  return 20 + randomNumber();
}

// Generate unique ID
export function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

// Format date for display
export function formatDate(date: string): string {
  return new Date(date).toLocaleDateString(undefined, {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

// Class name merger (like clsx)
export function cn(...classes: (string | boolean | undefined | null)[]): string {
  return classes.filter(Boolean).join(" ");
}
