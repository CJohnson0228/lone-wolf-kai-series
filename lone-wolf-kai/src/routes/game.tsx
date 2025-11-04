import { useParams } from "react-router";
import { motion } from "motion/react";

export default function Game() {
  const { bookId, sectionId } = useParams();

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="space-y-6"
        >
          {/* Character Stats Sidebar - you'll make this responsive */}
          <div className="card">
            <h2 className="text-2xl font-display font-bold mb-4">
              Book {bookId}, Section {sectionId}
            </h2>

            <div className="story-text">
              <p>This is where the story section content will be displayed.</p>
              <p>
                You'll load the content from the extracted JSON based on bookId and
                sectionId.
              </p>
            </div>

            {/* Choices will go here */}
            <div className="mt-6 space-y-3">
              <button className="choice-btn">
                <span className="font-medium">Choice 1</span>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  Turn to section X
                </p>
              </button>
              <button className="choice-btn">
                <span className="font-medium">Choice 2</span>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                  Turn to section Y
                </p>
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
