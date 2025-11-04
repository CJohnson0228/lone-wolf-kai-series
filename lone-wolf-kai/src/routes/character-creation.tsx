import { useState } from "react";
import { useNavigate } from "react-router";
import { motion } from "motion/react";

export default function CharacterCreation() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-2xl mx-auto">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="card"
        >
          <h1 className="text-3xl font-display font-bold mb-6 text-kai-700 dark:text-kai-400">
            Create Your Kai Lord
          </h1>

          <div className="mb-6">
            <div className="flex justify-between mb-2">
              {[1, 2, 3, 4, 5].map((s) => (
                <div
                  key={s}
                  className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    s <= step
                      ? "bg-kai-500 text-white"
                      : "bg-gray-300 dark:bg-gray-600 text-gray-600"
                  }`}
                >
                  {s}
                </div>
              ))}
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">
              Step {step} of 5
            </div>
          </div>

          {/* This is where you'll add your character creation steps */}
          <div className="space-y-4">
            <p className="text-center text-gray-500 dark:text-gray-400">
              Character creation UI goes here
            </p>
            <p className="text-sm text-gray-400">
              You'll implement: stats rolling, discipline selection, equipment, etc.
            </p>
          </div>

          <div className="flex justify-between mt-8">
            <button
              onClick={() => navigate("/")}
              className="btn btn-secondary"
            >
              Cancel
            </button>
            <button
              onClick={() => setStep(step + 1)}
              className="btn btn-primary"
            >
              {step < 5 ? "Next" : "Begin Adventure"}
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
