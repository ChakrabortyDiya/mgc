"use client"

import { useState } from "react"
import { useRouter } from "next/navigation";  
import axios from "axios";

export function QuickSelector() {
  const [testData, setTestData] = useState({
    genomes: {
      DNA: true,
      RNA: false,
    },
    otherDatasets: {
      RawFASTA: false,
      MultiFASTA: false,
      FASTQ: false,
    },
  })

  const [selectedChartOptions, setSelectedChartOptions] = useState<string[]>([])
  const [selectedPlotOptions, setSelectedPlotOptions] = useState<string[]>([])
  const [loadingOption, setLoadingOption] = useState<string | null>(null);
  
  const router = useRouter();  

  const handleTestDataChange = (category: "genomes" | "otherDatasets", option?: string) => {
    setTestData((prev) => ({
      ...prev,
      [category]: {
        ...prev[category],
        [option!]: !prev[category][option as keyof (typeof prev)[typeof category]],
      },
    }))
  }

  // Send selected metric to backend using Axios
  const handleOptionClick = async (option: string, type: "chart" | "plot") => {
    setLoadingOption(option);
    const setter = type === "chart" ? setSelectedChartOptions : setSelectedPlotOptions;

    try {
      const response = await axios.post("http://127.0.0.1:8000/dashboard/plot", {
        name: option.toLowerCase(),
      });

      if (response.status !== 200) throw new Error("Failed to fetch data");

      setter((prev) => (prev.includes(option) ? prev.filter((o) => o !== option) : [...prev, option]));

      if (type === "chart") router.push("/chart");
    } catch (error) {
      console.error("Error sending request:", error);
    } finally {
      setLoadingOption(null);
    }
  };

  /*const handleOptionClick = (option: string, type: "chart" | "plot") => {
    const setter = type === "chart" ? setSelectedChartOptions : setSelectedPlotOptions
    /*const current = type === "chart" ? selectedChartOptions : selectedPlotOptions*/
   /* setter((prev) => (prev.includes(option) ? prev.filter((o) => o !== option) : [...prev, option]))
    if (type === "chart") {
      router.push("/chart");  
    }    
  }*/

  return (
    <div className="bg-[#F5FFF5] border border-[#D1FFD1] rounded-lg p-6 mb-8">
      <h2 className="text-2xl font-semibold text-center text-[#008080] mb-6">Dashboard</h2>

      <div className="space-y-6">
        {/* Test Data Section */}
        <div className="flex flex-wrap items-center gap-6">
          <span className="text-[#006400] font-medium whitespace-nowrap">Benchmark dataset</span>
          <div className="flex items-center gap-4">
            {Object.entries(testData.genomes).map(([size, checked]) => (
              <label key={size} className="inline-flex items-center">
                <input
                  type="checkbox"
                  checked={checked}
                  onChange={() => handleTestDataChange("genomes", size)}
                  className="form-checkbox text-[#4A6EA9]"
                />
                <span className="ml-1 text-[#006400]">{size}</span>
              </label>
            ))}
          </div>

          {/* Types Section (Closer to Options) */}
          <div className="flex items-center gap-2">
            <span className="text-[#800000] font-medium">Types</span>
            <div className="flex gap-3">
              {Object.entries(testData.otherDatasets).map(([type, checked]) => (
                <label key={type} className="inline-flex items-center">
                  <input
                    type="checkbox"
                    checked={checked}
                    onChange={() => handleTestDataChange("otherDatasets", type)}
                    className="form-checkbox text-[#4A6EA9]"
                  />
                  <span className="ml-1 text-[#800000]">{type}</span>
                </label>
              ))}
            </div>
          </div>
        </div>

               {/* Column Chart Section */}
        <div className="flex items-start space-x-4">
          <span className="text-[#0066CC] font-medium whitespace-nowrap w-24">Metrics</span>
          <div className="flex flex-wrap gap-2">
            {[
              "Compression Ratio",
              "Compression Time",
              "Compression Memory",
              "Compression CPU Usage",
              "Decompression Time",
              "Decompression Memory",
              "Decompression CPU Usage",
            ].map((option) => (
              <button
                key={option}
                onClick={() => handleOptionClick(option, "chart")}
                className={`px-4 py-1 rounded-full border ${
                  selectedChartOptions.includes(option) ? "bg-[#4A6EA9] text-white" : "bg-white text-gray-700"
                } hover:bg-gray-50 text-sm`}
              >
                {option}
              </button>
            ))}
          </div>
        </div>


        {/* Scatterplot Section (Same Line as Options) */}
        <div className="flex flex-wrap items-center gap-4">
          <span className="text-[#8B4513] font-medium whitespace-nowrap">Scatterplot (Space-Time Tradeoff)</span>
          <div className="flex flex-wrap gap-2">
            {["Compression Ratio -vs- Decompression Time"].map((option) => (
              <button
                key={option}
                onClick={() => handleOptionClick(option, "plot")}
                className={`px-4 py-1 rounded-full border text-sm ${
                  selectedPlotOptions.includes(option) ? "bg-[#4A6EA9] text-white" : "bg-[#FFF5EE] text-gray-700"
                } hover:bg-gray-50`}
              >
                {option}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

