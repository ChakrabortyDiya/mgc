import React from "react";
import { motion } from "framer-motion";

const spinnerVariants = {
  animate: {
    rotate: 360,
    transition: {
      repeat: Infinity,
      duration: 1,
      ease: "linear",
    },
  },
};

const Loader: React.FC = () => {
  return (
    <div className="flex justify-center items-center h-screen bg-gray-100 absolute left-0 top-0 w-full z-50">
      <motion.div
        className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full"
        variants={spinnerVariants}
        animate="animate"
      />
    </div>
  );
};

export default Loader;
