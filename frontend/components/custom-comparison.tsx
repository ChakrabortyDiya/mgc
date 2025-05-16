"use client";

import { useState } from "react";
import { useGlobalContext } from "./GlobalContext";

type CustomComparisonProps = {
  selectedGenomes?: string[];
  setSelectedGenomes?: React.Dispatch<React.SetStateAction<string[]>>;
  selectedDatasets?: string[];
  setSelectedDatasets?: React.Dispatch<React.SetStateAction<string[]>>;
};

export function CustomComparison({
  selectedGenomes,
  setSelectedGenomes,
  selectedDatasets,
  setSelectedDatasets,
}: CustomComparisonProps) {
  // Use internal state if no external state is provided
  const [internalGenomes, setInternalGenomes] = useState<string[]>([]);
  const effectiveSelectedGenomes =
    selectedGenomes !== undefined ? selectedGenomes : internalGenomes;
  const effectiveSetSelectedGenomes =
    setSelectedGenomes !== undefined ? setSelectedGenomes : setInternalGenomes;
  const { testData } = useGlobalContext();

  // const [selectedDatasets, setSelectedDatasets] = useState<string[]>([]);

  const handleGenomeChange = (genome: string) => {
    effectiveSetSelectedGenomes((prev) => {
      const safePrev = prev || [];
      const isIncluded = safePrev.includes(genome);
      const updated = isIncluded
        ? safePrev.filter((g) => g !== genome)
        : [...safePrev, genome]; // Only keep the first part of the genome name
      // console.log(`Genome ${genome} ${isIncluded ? "deselected" : "selected"}`);
      return updated;
    });
  };

  const handleDatasetChange = (dataset: string) => {
    if (setSelectedDatasets) {
      setSelectedDatasets((prev) => {
        const isIncluded = prev.includes(dataset);
        const updated = isIncluded
          ? prev.filter((d) => d !== dataset)
          : [...prev, dataset];
        // console.log(`Dataset ${dataset} ${isIncluded ? "deselected" : "selected"}`);
        return updated;
      });
    }
  };

  const genomes = [
    "BuEb (19 kB)",
    "AgPh (43 kB)",
    "YeMi (72 kB)",
    "HaHi (3,799 kB)",
    "EsCo (4,533 kB)",
    "PlFa (8,777 kB)",
    "WaMe (8,931 kB)",
    "ScPo (10,403 kB)",
    "EnIn (25,785 kB)",
    "DrMe (31,428 kB)",
    "OrSa (42,249 kB)",
    "DaRe (61,099 kB)",
    "AeCa (1,554 kB)",
    "HePy (1,629 kB)",
    "AnCa (1,38,858 kB)",
    "GaGa (1,45,052 kB)",
    "HoSa (1,85,306 kB)",
  ];

  const datasets = [
    "humdyst (38,770 kB)",
    "humprtb (56,737 kB)",
    "humhdab (58,864 kB)",
    "humghcs (66,495 kB)",
    "humhbb (73,308 kB)",
    "mtpacga (100,314 kB)",
    "chmpxx (121,024 kB)",
    "chntxx (155,844 kB)",
    "mpomtcg (186,608 kB)",
    "vaccg (191,737 kB)",
    "hehcmv (229,354 kB)",
  ];

  return (
    <div className="space-y-8">
      <h2 className="text-2xl font-semibold text-center text-[#4A6EA9]">
        Result Comparison Using Table
      </h2>

      <div className="space-y-6">
        <h3 className="text-lg font-medium text-gray-700">
          Step 1. Select datasets
        </h3>

        <div className="grid grid-cols-2 gap-8">
          {/* DNA Corpus */}
         
            <div>
              <h4 className="text-sm font-medium text-gray-500 mb-2">
                DNA Corpus 1
              </h4>
              <div className={`border rounded-lg p-4 space-y-2 bg-white max-h-60 overflow-y-auto ${testData.genomes.DNA.checked && "blur"}`}>
                {genomes.map((genome) => (
                  <label key={genome} className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      className="form-checkbox text-[#4A6EA9]"
                      checked={effectiveSelectedGenomes.includes(genome)}
                      onChange={() => handleGenomeChange(genome)}
                      disabled={testData.genomes.DNA.checked}
                    />
                    <span className="text-sm text-gray-600">{genome}</span>
                  </label>
                ))}
              </div>
            </div>
         

          {/* DNA Datasets */}
          
            <div>
              <h4 className="text-sm font-medium text-gray-500 mb-2">
                DNA Corpus 2
              </h4>
              <div className={`border rounded-lg p-4 space-y-2 bg-white max-h-60 overflow-y-auto ${testData.genomes.DNA_Corpus.checked && "blur"}`}>
                <div className="space-y-2">
                  {datasets.map((dataset) => (
                    <label
                      key={dataset}
                      className="flex items-center space-x-2"
                    >
                      <input
                        type="checkbox"
                        className="form-checkbox text-[#4A6EA9]"
                        checked={selectedDatasets?.includes(dataset) || false}
                        onChange={() => handleDatasetChange(dataset)}
                        disabled={testData.genomes.DNA_Corpus.checked}
                      />
                      <span className="text-sm text-gray-600">{dataset}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          

          {/* RNA Datasets */}
          {/* <div className="mt-4">
              <h4 className="text-sm font-medium text-gray-500 mb-2">
                RNA datasets (highly repetitive)
              </h4>
              <div className="border rounded-lg p-4 space-y-6 bg-white max-h-36 overflow-y-auto">
                <div className="space-y-2">
                  {datasets.rna.map((dataset) => (
                    <label key={dataset} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        className="form-checkbox text-[#4A6EA9]"
                        checked={selectedDatasets.includes(dataset)}
                        onChange={() => handleDatasetChange(dataset)}
                      />
                      <span className="text-sm text-gray-600">{dataset}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div> */}
        </div>
      </div>
      <div className="h-6" />
    </div>
  );
}
