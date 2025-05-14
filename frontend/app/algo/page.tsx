"use client";

import React from "react";
import { Header } from "../../components/header";
import { motion } from "framer-motion";

export default function AlgoPage() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <motion.main 
        className="container mx-auto py-10 px-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4 }}
      >
        <div className="max-w-3xl mx-auto">
          <motion.h1 
            className="text-2xl font-bold text-[#4A6EA9] mb-6"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.1 }}
          >
            The NGC Algorithm
          </motion.h1>
          
          <motion.div 
            className="bg-white shadow-md rounded-xl p-8 border border-[#D1FFD1]"
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.4, delay: 0.2 }}
          >
            <div className="space-y-6 text-gray-800 leading-relaxed">
              <div className="bg-blue-50 p-4 rounded-lg border-l-2 border-[#4A6EA9]">
                <p className="text-gray-800">
                  <strong>Input:</strong> A DNA or RNA sequence
                </p>
              </div>

              <div className="relative pl-6 border-l border-[#4A6EA9] ml-2">
                <ol className="space-y-4 list-decimal">
                  <li className="pl-2">
                    Convert FASTA, multi-FASTA or FASTQ sequence to raw data consisting only 
                    <code className="px-1.5 py-0.5 bg-gray-100 rounded text-[#4A6EA9] text-sm font-mono ml-1">{`{A, C, G, T/U, etc}`}</code>
                  </li>
                  <li className="pl-2">
                    Convert lower-case 
                    <code className="px-1.5 py-0.5 bg-gray-100 rounded text-[#4A6EA9] text-sm font-mono mx-1">{`{a, c, g, t/u}`}</code> 
                    to upper-case 
                    <code className="px-1.5 py-0.5 bg-gray-100 rounded text-[#4A6EA9] text-sm font-mono mx-1">{`{A, C, G, T/U}`}</code>
                  </li>
                  <li className="pl-2">
                    Remove all other IUPAC characters (e.g. 
                    <code className="px-1.5 py-0.5 bg-gray-100 rounded text-[#4A6EA9] text-sm font-mono mx-1">N</code>, 
                    <code className="px-1.5 py-0.5 bg-gray-100 rounded text-[#4A6EA9] text-sm font-mono mx-1">K</code>, 
                    <code className="px-1.5 py-0.5 bg-gray-100 rounded text-[#4A6EA9] text-sm font-mono mx-1">B</code>, etc.)
                  </li>
                  <motion.li 
                    className="pl-2"
                    whileHover={{ x: 3 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    The combined sequence is then converted into 2-bit encoding, which stores four nucleotides per byte, for example 
                    <code className="px-1.5 py-0.5 bg-gray-100 rounded text-[#4A6EA9] text-sm font-mono mx-1">ACGTT → 01233</code>
                  </motion.li>
                  <motion.li 
                    className="pl-2"
                    whileHover={{ x: 3 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    Convert four two-bit-coded nucleotides to extended ASCII code
                  </motion.li>
                  <motion.li 
                    className="pl-2"
                    whileHover={{ x: 3 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    Apply general-purpose encoder
                  </motion.li>
                </ol>
              </div>

              <div className="bg-[#F5FFF5] p-4 rounded-lg border-l-2 border-[#008080]">
                <p className="text-gray-800">
                  <strong>Output:</strong> Compressed sequence
                </p>
              </div>
            </div>
          </motion.div>
        </div>
      </motion.main>
    </div>
  );
}

