"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import Loader from "./ui/loader";

export function QuickSelector() {
  const router = useRouter();
  const [testData, setTestData] = useState({
    genomes: {
      DNA_Corpus: {
        size: "DNA Corpus(raw)",
        checked: false,
      },
      DNA: {
        size: "DNA(FASTA)",
        checked: false,
      },
      RNA: {
        size: "RNA(FASTA)",
        checked: false,
      },
    },
  });

  // const [selectedChartOptions] = useState<string[]>([]);
  const [selectedChartOptions, setSelectedChartOptions] = useState<string[]>(
    []
  );
  const [selectedPlotOptions, setSelectedPlotOptions] = useState<string[]>([]);

  // const router = useRouter();

  // Toggle test data selection
  const handleTestDataChange = (
    category: keyof typeof testData,
    option: string
  ) => {
    setTestData((prev) => {
      const currentOption =
        prev[category][option as keyof (typeof prev)[typeof category]];
      return {
        ...prev,
        [category]: {
          ...prev[category],
          [option]: {
            ...currentOption,
            checked: !currentOption.checked,
          },
        },
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
          (typeof option === "string" ? option.replace("_", " ") : "") || "",
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

  const handleBarClick = (option: string, type: "barchart" | "scatterplot") => {
    fetchData(option, type);
  };
  console.log(handleBarClick);
  return (
    <div>
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center z-50 bg-gray-100">
          <Loader />
        </div>
      )}
      <div className="bg-[#F5FFF5] border border-[#D1FFD1] rounded-lg p-6 mb-8">
        <h2 className="text-2xl font-semibold text-center text-[#008080] mb-6">
          Result Comparison Using Graph
        </h2>

        <div className="space-y-6">
          {/* Benchmark Dataset Section */}
          <div className="flex flex-wrap items-center gap-6">
            <span className="text-[#006400] font-medium">
              Benchmark dataset
            </span>
            <div className="flex gap-4">
              {Object.entries(testData.genomes).map(
                ([size, data]: [
                  string,
                  { size: string; checked: boolean }
                ]) => (
                  <label key={size} className="inline-flex items-center">
                    <input
                      type="checkbox"
                      checked={data.checked}
                      onChange={() => handleTestDataChange("genomes", size)}
                      className="form-checkbox text-[#4A6EA9]"
                    />
                    <span className="ml-1 text-[#006400]">{data.size}</span>
                  </label>
                )
              )}
            </div>
          </div>

          {/* Types Section */}
          {/* <div className="flex flex-wrap items-center gap-2">
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
        </div> */}

          {/* Metrics Section */}
          <div className="flex items-start space-x-4">
            <span className="text-[#0066CC] font-medium w-24">Metrics</span>
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
                  onClick={() => router.push(`/${option.toLowerCase().replace(/\s+/g, "_")}`)}
                  // onClick={() => handleBarClick(option, "barchart")}
                  className={`px-4 py-1 rounded-full border text-sm ${
                    selectedChartOptions?.includes(option)
                      ? "bg-[#4A6EA9] text-white"
                      : "bg-white text-gray-700"
                  } hover:bg-gray-50`}
                >
                  {option}
                </button>
              ))}
            </div>
          </div>

          {/* Scatterplot Section */}
          <div className="flex flex-wrap items-center gap-4">
            <span className="text-[#8B4513] font-medium">
              Scatterplot (Space-Time Tradeoff)
            </span>
            <div className="flex flex-wrap gap-2">
              {["Compression Ratio -vs- Decompression Time"].map((option) => (
                <button
                  key={option}
                  onClick={() => router.push("/" + option.toLowerCase().replace(/\s+/g, "_"))}
                  className={`px-4 py-1 rounded-full border text-sm ${
                    selectedPlotOptions.includes(option)
                      ? "bg-[#4A6EA9] text-white"
                      : "bg-[#FFF5EE] text-gray-700"
                  } hover:bg-gray-50`}
                >
                  {option}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
