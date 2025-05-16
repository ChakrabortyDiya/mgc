"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import Loader from "./ui/loader";
import { useGlobalContext } from "./GlobalContext";
import { motion, AnimatePresence } from "framer-motion";

export function QuickSelector() {
  const router = useRouter();
  const { selectedGenomeType, setSelectedGenomeType, testData, setTestData } = useGlobalContext();
  console.log(selectedGenomeType); 

  // const [testData, setTestData] = useState({
  //   genomes: {
  //     DNA_Corpus: {
  //       size: "DNA Corpus 1",
  //       checked: selectedGenomeType === "DNA_Corpus",
  //     },
  //     DNA: {
  //       size: "DNA Corpus 2",
  //       checked: selectedGenomeType === "DNA",
  //     },
  //   },
  // });

  // const [selectedChartOptions] = useState<string[]>([]);
  const [selectedChartOptions, setSelectedChartOptions] = useState<string[]>(
    []
  );
  const [selectedPlotOptions, setSelectedPlotOptions] = useState<string[]>([]);

  // Toggle test data selection
  const handleTestDataChange = (
    category: keyof typeof testData,
    selectedOption: string
  ) => {
    setSelectedGenomeType(selectedOption);

    setTestData((prev: any) => {
      const updatedOptions = Object.entries(prev[category]).reduce(
        (acc, [option, value]) => {
          acc[option as keyof (typeof prev)[typeof category]] = {
            ...(value as object),
            checked: option === selectedOption,
          };
          return acc;
        },
        {} as (typeof prev)[typeof category]
      );

      return {
        ...prev,
        [category]: updatedOptions,
      };
    });
  };
  // Handle option selection and API request
  const generateGraphData = async (
    option: string,
    type: "barchart" | "scatterplot"
  ) => {
    try {
      const setter =
        type === "barchart" ? setSelectedChartOptions : setSelectedPlotOptions;

      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_SERVER_LINK}/dashboard/chart/${type}`,
        {
          name: option?.toLowerCase() || "",
        }
      );

      if (response.status !== 200) {
        console.error(
          "Server responded with status:",
          response.status,
          response.data
        );
        throw new Error("Failed to fetch data");
      }

      setter(Array.isArray(response.data) ? response.data : []);
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error(
          "Error sending request:",
          error.message,
          "Response:",
          error.response?.data
        );
      } else {
        console.error("Unexpected error:", error);
      }
    }
  };
  const [isLoading, setIsLoading] = useState(false);

  const fetchData = async (
    option: string,
    type: "barchart" | "scatterplot"
  ) => {
    try {
      setIsLoading(true);
      if (option) {
        await generateGraphData(
          (typeof option === "string" ? option : "") || "",
          type
        );
        router.push("/" + option.toLowerCase().replace(/\s+/g, "_"));
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setIsLoading(false);
    }
  };
  console.log(fetchData);
  // const handleBarClick = (option: string, type: "barchart" | "scatterplot") => {
  //   fetchData(option, type);
  // };
  const [options, setOptions] = useState<string[]>([]);
  useEffect(() => {
    if (testData.genomes["DNA"].checked) {
      setOptions(["WACR"]);
    } else {
      setOptions(["WACR", "TCT", "PCM", "PCC", "TDT", "PDM", "PDC"]);
    }
  }, [testData]);


  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1,
      transition: { 
        staggerChildren: 0.05 
      }
    }
  };
  
  const itemVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center z-50 bg-gray-100">
          <Loader />
        </div>
      )}
      <motion.div 
        className="bg-[#F5FFF5] border border-[#D1FFD1] rounded-lg p-6 mb-8"
        initial={{ scale: 0.98 }}
        animate={{ scale: 1 }}
        transition={{ duration: 0.3 }}
      >
        <motion.h2 
          className="text-2xl font-semibold text-center text-[#008080] mb-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.1 }}
        >
          Result Comparison Using Graph
        </motion.h2>

        <div className="space-y-6">
          {/* Benchmark Dataset Section */}
          <motion.div 
            className="flex flex-wrap items-center gap-6"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
          >
            <motion.span 
              className="text-[#006400] font-medium"
              variants={itemVariants}
            >
              Benchmark dataset
            </motion.span>
            <div className="flex gap-4">
              {Object.entries(testData.genomes as Record<string, { size: string; checked: boolean }>).map(
                ([size, data]) => (
                  <motion.label 
                    key={size} 
                    className="inline-flex items-center"
                    variants={itemVariants}
                    whileHover={{ scale: 1.05 }}
                    transition={{ type: "spring", stiffness: 400, damping: 10 }}
                  >
                    <input
                      type="checkbox"
                      checked={data.checked}
                      onChange={() => handleTestDataChange("genomes", size)}
                      className="form-checkbox text-[#4A6EA9]"
                    />
                    <span className="ml-1 text-[#006400]">{data.size}</span>
                  </motion.label>
                )
              )}
            </div>
          </motion.div>

          {/* Metrics Section */}
          <motion.div 
            className="flex items-start space-x-4"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
          >
            <motion.span 
              className="text-[#0066CC] font-medium w-24"
              variants={itemVariants}
            >
              Metrics
            </motion.span>
            <div className="flex flex-wrap gap-2">
              <AnimatePresence mode="popLayout">
                {options.map((option, index) => (
                  <motion.button
                    key={option}
                    onClick={() =>
                      router.push(`/${option.toLowerCase().replace(/\s+/g, "_")}`)
                    }
                    className={`px-4 py-1 rounded-full border text-sm ${
                      selectedChartOptions?.includes(option)
                        ? "bg-[#4A6EA9] text-white"
                        : "bg-white text-gray-700"
                    } hover:bg-gray-50`}
                    variants={itemVariants}
                    whileHover={{ scale: 1.05, boxShadow: "0px 3px 8px rgba(0,0,0,0.1)" }}
                    whileTap={{ scale: 0.95 }}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0, transition: { delay: index * 0.05 } }}
                    exit={{ opacity: 0, y: -10 }}
                  >
                    {option}
                  </motion.button>
                ))}
              </AnimatePresence>
            </div>
          </motion.div>

          {/* Scatterplot Section */}
          <AnimatePresence>
            {testData.genomes["DNA_Corpus"].checked && (
              <motion.div 
                className="flex flex-wrap items-center gap-4"
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
              >
                <span className="text-[#8B4513] font-medium">
                  Scatterplot (Space-Time Tradeoff)
                </span>
                <div className="flex flex-wrap gap-2">
                  {["WACR -vs- TCT"].map((option) => (
                    <motion.button
                      key={option}
                      onClick={() =>
                        router.push(
                          "/" + option.toLowerCase().replace(/\s+/g, "_")
                        )
                      }
                      className={`px-4 py-1 rounded-full border text-sm ${
                        selectedPlotOptions.includes(option)
                          ? "bg-[#4A6EA9] text-white"
                          : "bg-[#FFF5EE] text-gray-700"
                      } hover:bg-gray-50`}
                      whileHover={{ scale: 1.05, boxShadow: "0px 3px 8px rgba(0,0,0,0.1)" }}
                      whileTap={{ scale: 0.95 }}
                    >
                      {option}
                    </motion.button>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.div>
    </motion.div>
  );
}
