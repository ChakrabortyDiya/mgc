"use client"

/*import { useState } from "react"*/

import { Label } from "@/components/ui/label"
/*import { Checkbox } from "@/components/ui/checkbox"*/

// type OutputConfigurationProps = {
//   selectedGenomes: string[]
// }

export function OutputConfiguration({selectedMetrics, setSelectedMetrics}: {selectedMetrics: string[], setSelectedMetrics: React.Dispatch<React.SetStateAction<string[]>>}) {
  // const handleDisplayTableClick = () => {
  //   console.log("Selected Genomes:", selectedGenomes)
  // }
  /*const [chartSize, setChartSize] = useState({ width: 1500, height: 500 });*/

  return (
    <div className="space-y-8">
      {/* Left-aligned heading */}
      <div>
        <h3 className="text-lg font-medium text-gray-700">Step 3. Output</h3>
      </div>

      {/* Centered content */}
      <div className="w-full grid grid-cols-2 gap-12">
        {/* Table Configuration */}
        <div className="space-y-4">
          <h4 className="text-lg font-medium">Table</h4>
          <div className="space-y-2">
            <Label>Metrics:</Label>
            <div className="flex flex-col space-y-2">
              {[
              "Compression Size",
              "Total Compression Time",
              "Peak Compression Memory",
              // "Compression CPU Usage",
              "Total Decompression Time",
              "Peak Decompression Memory",
              // "Decompression CPU Usage",
              ].map((column) => (
              <label key={column} className="flex items-center space-x-2">
                <input
                type="checkbox"
                className="form-checkbox h-4 w-4"
                value={column}
                checked={selectedMetrics.includes(column)}
                onChange={(e) => {
                  if (e.target.checked) {
                  setSelectedMetrics([...selectedMetrics, column])
                  } else {
                  setSelectedMetrics(selectedMetrics.filter((m) => m !== column))
                  }
                }}
                />
                <span>{column}</span>
              </label>
              ))}
            </div>
          </div>
        </div>

        {/* Scatterplot Configuration */}
        {/* <div className="space-y-4">
          <h4 className="text-lg font-medium">Scatterplot</h4>
          <div className="space-y-4">
            <div>
              <Label>X axis:</Label>
              <select className="w-full border rounded px-2 py-1 mt-1">
                <option>Compression Ratio</option>
              </select>
            </div>

            <div>
              <Label>Y axis:</Label>
              <select className="w-full border rounded px-2 py-1 mt-1">
                <option>Decompression time</option>
              </select>
            </div>

            <Button variant="outline" className="w-full sm:w-auto">Show scatterplot</Button>
          </div>
        </div> */}
      </div> 
    </div>
  );
}

