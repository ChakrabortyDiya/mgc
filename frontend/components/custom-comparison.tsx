"use client"

import { useState} from "react"

type CustomComparisonProps = {
  selectedGenomes?: string[]
  setSelectedGenomes?: React.Dispatch<React.SetStateAction<string[]>>
}

export function CustomComparison({
  selectedGenomes,
  setSelectedGenomes,
}: CustomComparisonProps) {
  // Use internal state if no external state is provided
  const [internalGenomes, setInternalGenomes] = useState<string[]>([]);
  const effectiveSelectedGenomes =
    selectedGenomes !== undefined ? selectedGenomes : internalGenomes;
  const effectiveSetSelectedGenomes =
    setSelectedGenomes !== undefined ? setSelectedGenomes : setInternalGenomes;

  const [selectedDatasets, setSelectedDatasets] = useState<string[]>([]);

 

  const handleGenomeChange = (genome: string) => {
    effectiveSetSelectedGenomes((prev) => {
      const safePrev = prev || [];
      const isIncluded = safePrev.includes(genome);
      const updated = isIncluded
        ? safePrev.filter((g) => g !== genome)
        : [...safePrev, genome];
      console.log(`Genome ${genome} ${isIncluded ? "deselected" : "selected"}`);
      return updated;
    });
  };

  const handleDatasetChange = (dataset: string) => {
    setSelectedDatasets((prev) => {
      const isIncluded = prev.includes(dataset);
      const updated = isIncluded ? prev.filter((d) => d !== dataset) : [...prev, dataset];
      console.log(`Dataset ${dataset} ${isIncluded ? "deselected" : "selected"}`);
      return updated;
    });
  };

  const genomes = [
    "AeCa (1,554 kB)",
    "AgPh (43 kB)",
    "AnCa (1,38,858 kB)",
    "BuEb (19 kB)",
    "DaRe (61,099 kB)",
    "DrMe (31,428 kB)",
    "EnIn (25,785 kB)",
    "EsCo (4,533 kB)",
    "GaGa (1,45,052 kB)",
    "HaHi (3,799 kB)",
    "HePy (1,629 kB)",
    "HoSa (1,85,306 kB)",
    "OrSa (42,249 kB)",
    "PlFa (8,777 kB)",
    "ScPo (10,403 kB)",
    "WaMe (8,931 kB)",
    "YeMi (72 kB)",
  ];

  const datasets = {
    dna: [
      "GCA 000001405.28 (9,42,286 kB)",
      "GCA 000165345.1 (9,001 kB)",
      "GCA 000188695.1 (54,835 kB)",
      "GCA 000211355.2 (1,673 kB)",
      "GCA 000350225.2 (1,03,894 kB)",
      "GCA 000398605.1 (510 kB)",
      "GCA 000497125.1 (12,835 kB)",
      "GCA 000988165.1 (5,674 kB)",
      "GCA 001606155.1 (23,119 kB)",
      "GCA 002205965.2 (3,33,021 kB)",
      "GCF 000002235.4 (9,84,246 kB)",
      "GCF 000240135.3 (36,051 kB)",
      "GCF 001884535.1 (50 kB)",
    ],
    rna: [
      "SILVA 132 LSURef (5,95,993 kB)",
      "SILVA 132 SSURef Nr99 (10,83,003 kB)",
      "SILVA 132 SSURef (5,85,687 kB)"
    ],
  };

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
              DNA Corpus (less repetitive)
            </h4>
            <div className="border rounded-lg p-4 space-y-2 bg-white max-h-96 overflow-y-auto">
              {genomes.map((genome) => (
                <label key={genome} className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    className="form-checkbox text-[#4A6EA9]"
                    checked={effectiveSelectedGenomes.includes(genome)}
                    onChange={() => handleGenomeChange(genome)}
                  />
                  <span className="text-sm text-gray-600">{genome}</span>
                </label>
              ))}
            </div>
          </div>

          {/* DNA Datasets */}
          <div>
            <h4 className="text-sm font-medium text-gray-500 mb-2">
              DNA datasets (less repetitive)
            </h4>
            <div className="border rounded-lg p-4 space-y-6 bg-white max-h-60 overflow-y-auto">
              <div className="space-y-2">
                {datasets.dna.map((dataset) => (
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

            {/* RNA Datasets */}
            <div className="mt-4">
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
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

