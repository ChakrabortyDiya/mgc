"use client";

import React from "react";
import { Header } from "../../components/header";
import { motion } from "framer-motion";
import Link from "next/link";

export default function CompressorsPage() {
  const compressorLinks = [
    { name: "Normalized Genome Compressor", url: "https://github.com/Arno2003/NGC" }
  ];

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
            Compressor Tool
          </motion.h1>

          <motion.div
            className="bg-white shadow-md rounded-xl p-8 border border-[#D1FFD1]"
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.4, delay: 0.2 }}
          >
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {compressorLinks.map((link, index) => (
                <motion.div
                  key={link.name}
                  className="bg-[#F5FFF5] rounded-lg p-4"
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 + index * 0.05, duration: 0.3 }}
                >
                  <motion.a
                    href={link.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-[#4A6EA9] font-medium hover:text-[#008080] transition-colors flex items-center"
                    whileHover={{ x: 3 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-5 w-5 mr-2"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                      />
                    </svg>
                    {link.name}
                  </motion.a>
                </motion.div>
              ))}
            </div>

            <p className="mt-6 text-gray-800 text-sm">
              Compressor details can be found here
              
            </p>
          </motion.div>
          <div className="mt-8 text-center">
              <Link href="/" className="text-sm text-[#4A6EA9] hover:underline">
                ← Back to Home
              </Link>
            </div>
        </div>
      </motion.main>
    </div>
  );
}
