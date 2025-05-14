"use client";

import { motion } from "framer-motion";
import React from "react";

// Fade in animation for components with staggered children
export const FadeIn = ({ 
  children, 
  className = "", 
  delay = 0,
  duration = 0.5,
}: { 
  children: React.ReactNode; 
  className?: string;
  delay?: number;
  duration?: number;
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ 
        duration: duration, 
        delay: delay,
        ease: "easeOut" 
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
};

// Scale animation for containers that should grow
export const ScaleIn = ({ 
  children, 
  className = "",
  delay = 0, 
}: { 
  children: React.ReactNode; 
  className?: string;
  delay?: number;
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ 
        duration: 0.4, 
        delay: delay,
        ease: "easeOut" 
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
};

// Staggered list items animation
export const StaggeredList = ({ 
  children, 
  className = "", 
  staggerDelay = 0.05,
  initialDelay = 0
}: { 
  children: React.ReactNode; 
  className?: string;
  staggerDelay?: number;
  initialDelay?: number;
}) => {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1,
      transition: { 
        staggerChildren: staggerDelay,
        delayChildren: initialDelay
      }
    }
  };
  
  return (
    <motion.div
      className={className}
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {children}
    </motion.div>
  );
};

// Item variant to use with StaggeredList
export const ListItem = ({ 
  children, 
  className = "" 
}: { 
  children: React.ReactNode; 
  className?: string;
}) => {
  const itemVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { 
        duration: 0.3
      } 
    }
  };
  
  return (
    <motion.div
      className={className}
      variants={itemVariants}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      {children}
    </motion.div>
  );
};

// Button with hover and tap animation
export const AnimatedButton = ({ 
  children, 
  className = "",
  onClick
}: { 
  children: React.ReactNode; 
  className?: string;
  onClick?: () => void;
}) => {
  return (
    <motion.button
      className={className}
      whileHover={{ 
        scale: 1.05, 
        boxShadow: "0px 3px 8px rgba(0,0,0,0.1)" 
      }}
      whileTap={{ scale: 0.95 }}
      transition={{ type: "spring", stiffness: 400, damping: 17 }}
      onClick={onClick}
    >
      {children}
    </motion.button>
  );
}; 