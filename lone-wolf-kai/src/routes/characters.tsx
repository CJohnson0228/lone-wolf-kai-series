import { Link } from "react-router";
import { motion } from "motion/react";

export default function Characters() {
  // You'll load saved characters from storage here
  const characters: any[] = [];

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-display font-bold mb-8 text-kai-700 dark:text-kai-400">
          Your Characters
        </h1>

        {characters.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="card text-center"
          >
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              No saved characters yet
            </p>
            <Link to="/character/new" className="btn btn-primary">
              Create Your First Character
            </Link>
          </motion.div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Character cards will go here */}
          </div>
        )}
      </div>
    </div>
  );
}
