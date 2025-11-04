import { motion } from "motion/react";
import { useAtom } from "jotai";
import { themeAtom } from "../store/theme";

export default function Settings() {
  const [theme, setTheme] = useAtom(themeAtom);

  const toggleTheme = () => {
    setTheme(theme === "light" ? "dark" : "light");
  };

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-2xl mx-auto">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="space-y-6"
        >
          <h1 className="text-3xl font-display font-bold text-kai-700 dark:text-kai-400">
            Settings
          </h1>

          <div className="card space-y-6">
            <div>
              <h2 className="text-xl font-bold mb-4">Display</h2>
              <div className="flex items-center justify-between">
                <span>Dark Mode</span>
                <button
                  onClick={toggleTheme}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    theme === "dark" ? "bg-kai-600" : "bg-gray-300"
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      theme === "dark" ? "translate-x-6" : "translate-x-1"
                    }`}
                  />
                </button>
              </div>
            </div>

            <div>
              <h2 className="text-xl font-bold mb-4">Gameplay</h2>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Gameplay settings will go here (auto-save, animations, etc.)
              </p>
            </div>

            <div>
              <h2 className="text-xl font-bold mb-4">Data</h2>
              <div className="space-y-2">
                <button className="btn btn-secondary w-full">
                  Export Save Data
                </button>
                <button className="btn btn-secondary w-full">
                  Import Save Data
                </button>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
