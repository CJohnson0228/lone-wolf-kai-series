import { Link } from "react-router";
import { useAtom } from "jotai";
import { themeAtom } from "../store/theme";

export default function Navigation() {
  const [theme, setTheme] = useAtom(themeAtom);

  const toggleTheme = () => {
    setTheme(theme === "light" ? "dark" : "light");
  };

  return (
    <nav className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="font-display font-bold text-xl text-kai-700 dark:text-kai-400">
            Lone Wolf: Kai Series
          </Link>

          <div className="flex items-center gap-4">
            <Link
              to="/characters"
              className="text-gray-600 dark:text-gray-300 hover:text-kai-600 dark:hover:text-kai-400 transition-colors"
            >
              Characters
            </Link>
            <Link
              to="/settings"
              className="text-gray-600 dark:text-gray-300 hover:text-kai-600 dark:hover:text-kai-400 transition-colors"
            >
              Settings
            </Link>
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
              aria-label="Toggle theme"
            >
              {theme === "light" ? "🌙" : "☀️"}
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
