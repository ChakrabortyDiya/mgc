"use client";

import { Header } from "../components/header"
import { WelcomeBox } from "../components/welcome-box"
import { QuickSelector } from "../components/quick-selector"
import ComparisonPage from "../components/ComparisonPage"
import { motion } from "framer-motion"

export default function Page() {
  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2
      }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { duration: 0.5 } }
  };

  return (
    <motion.div 
      initial="hidden"
      animate="show"
      variants={container}
      className="min-h-screen bg-white"
    >
      <Header />
      <motion.main className="container mx-auto px-4 py-8">
        <motion.h1 
          variants={item}
          className="text-4xl font-semibold text-[#4A6EA9] text-center mb-8"
        >
          NGC: Normalized Genome Compressors
        </motion.h1>
        <motion.div variants={item}>
          <WelcomeBox />
        </motion.div>
        <motion.div variants={item}>
          <QuickSelector />
        </motion.div>
        <motion.div variants={item} className="space-y-8">
          <ComparisonPage />
          {/* <CompressorSelector />
          <OutputConfiguration selectedGenomes={[]} /> */}
        </motion.div>
        <motion.footer 
          variants={item}
          className="text-center text-sm text-gray-600 pt-8"
        >
          By <a href="#" className="text-blue-600 hover:underline">Contributors</a>, 2023-2026, public domain
        </motion.footer>
      </motion.main>
    </motion.div>
  )
}

