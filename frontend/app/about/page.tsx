"use client";

import React from "react";
import { Header } from "../../components/header";
import { motion } from "framer-motion";

export default function AboutPage() {
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
                        About the NGC 
                    </motion.h1>
                    
                    <motion.div 
                        className="bg-white shadow-md rounded-xl p-8 border border-[#D1FFD1]"
                        initial={{ y: 10, opacity: 0 }}
                        animate={{ y: 0, opacity: 1 }}
                        transition={{ duration: 0.4, delay: 0.2 }}
                    >
                        <div className="space-y-6 text-gray-800 leading-relaxed">
                            <p>
                                The proposed compressor (NGC) is a reference-free, lossless, two-phase tool. Initially, it transforms the sequence into the primary domain of the DNA/RNA <code className="px-1.5 py-0.5 bg-gray-100 rounded text-[#4A6EA9] text-sm font-mono">{`{A, C, G, T/U}`}</code>, then proceeds with normalization.
                            </p>
                            
                            <div className="bg-[#F5FFF5] p-6 rounded-lg">
                                <p>
                                    In the subsequent step, based on user specifications, it utilizes one of the eight general-purpose compressors:
                                </p>
                                <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-3">
                                    {["7-zip", "paq8px", "bsc", "gzip", "zstd", "bzip2", "zpaq", "cmix"].map((compressor) => (
                                        <motion.div
                                            key={compressor}
                                            className="bg-white rounded-lg border border-gray-200 p-2 text-center"
                                            whileHover={{ scale: 1.03 }}
                                            transition={{ type: "spring", stiffness: 300 }}
                                        >
                                            <span className="font-mono text-[#008080]">{compressor}</span>
                                        </motion.div>
                                    ))}
                                </div>
                            </div>
                            
                            <div className="bg-blue-50 p-4 rounded-lg border-l-2 border-[#4A6EA9]">
                                <p className="text-[#4A6EA9]">
                                    Key features: reference-free, lossless compression with flexible compressor options.
                                </p>
                            </div>
                        </div>
                    </motion.div>
                </div>
            </motion.main>
        </div>
    );
}
