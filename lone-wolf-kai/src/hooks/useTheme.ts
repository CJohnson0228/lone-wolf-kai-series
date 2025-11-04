import { useEffect } from "react";
import { useAtom } from "jotai";
import { themeAtom } from "../store/theme";
import { applyTheme } from "../lib/theme";

export function useTheme() {
  const [theme, setTheme] = useAtom(themeAtom);

  useEffect(() => {
    applyTheme(theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(theme === "light" ? "dark" : "light");
  };

  return { theme, setTheme, toggleTheme };
}
