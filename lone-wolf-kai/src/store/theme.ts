import { atomWithStorage } from "jotai/utils";

// Theme atom with localStorage persistence
export const themeAtom = atomWithStorage<"light" | "dark">(
  "lone-wolf-theme",
  "light"
);

// Effect to apply theme to document
if (typeof window !== "undefined") {
  const storedTheme = localStorage.getItem("lone-wolf-theme");
  if (storedTheme === "dark" || storedTheme === '"dark"') {
    document.documentElement.classList.add("dark");
  }
}
