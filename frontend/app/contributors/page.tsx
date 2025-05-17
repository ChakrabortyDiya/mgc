"use client";

import React from "react";
import { Header } from "../../components/header";
import { motion } from "framer-motion";
import Link from "next/link";

export default function ContributorsPage() {
  type Contributor = {
    name: string;
    email: string;
  };

  const contributors: Contributor[] = [
    { name: "Arnab Charit", email: "arnabcharit29@gmail.com" },
    { name: "Diya Chakraborty", email: "crs.diya@gmail.com" },
    { name: "Mriganka Patra", email: "mriganka9432@gmail.com" },
    { name: "Ananya Sadhukhan", email: "ananyasadhukhan1803@gmail.com" },
    { name: "Subhankar Roy", email: "subhankar.roy07@gmail.com" },
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
            Contributors
          </motion.h1>

          <motion.div
            className="bg-white shadow-md rounded-xl p-8 border border-[#D1FFD1]"
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.4, delay: 0.2 }}
          >
            <div className="space-y-4">
              {contributors.map((contributor, index) => (
                <motion.div
                  key={contributor.email}
                  className="bg-[#F5FFF5] rounded-lg p-4"
                  initial={{ opacity: 0, y: 5 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 + index * 0.05, duration: 0.3 }}
                >
                  <p className="text-[#4A6EA9] font-medium">
                    {contributor.name}
                  </p>
                  <p className="text-sm text-gray-700">{contributor.email}</p>
                </motion.div>
              ))}
            </div>
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
