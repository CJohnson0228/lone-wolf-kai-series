import { Link } from "react-router";
import { motion } from "motion/react";

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-4xl mx-auto text-center"
      >
        <h1 className="text-5xl font-display font-bold mb-6 text-kai-700 dark:text-kai-400">
          Lone Wolf: Kai Series
        </h1>
        <p className="text-xl mb-8 text-gray-600 dark:text-gray-300">
          Begin your journey as the last of the Kai Lords
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-2xl mx-auto">
          <Link to="/character/new" className="card hover:shadow-lg transition-shadow">
            <h2 className="text-2xl font-bold mb-2 text-kai-600 dark:text-kai-400">
              New Game
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Create a new character and begin your adventure
            </p>
          </Link>

          <Link to="/characters" className="card hover:shadow-lg transition-shadow">
            <h2 className="text-2xl font-bold mb-2 text-kai-600 dark:text-kai-400">
              Continue
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Load an existing character
            </p>
          </Link>
        </div>

        <div className="mt-12">
          <Link to="/settings" className="text-kai-600 dark:text-kai-400 hover:underline">
            Settings
          </Link>
        </div>
      </motion.div>
    </div>
  );
}
