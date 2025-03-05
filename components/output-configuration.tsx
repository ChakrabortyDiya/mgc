"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"

export function OutputConfiguration() {
  const [chartSize, setChartSize] = useState({ width: 1500, height: 500 });

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
                "Name",
                "Compression Ratio",
                "Compression Time",
                "Compression Memory",
                "Compression CPU Usage",
                "Decompression Ratio",
                "Decompression Time",
                "Decompression Memory",
              ].map((column) => (
                <label key={column} className="flex items-center space-x-2">
                  <input type="checkbox" className="form-checkbox h-4 w-4" />
                  <span>{column}</span>
                </label>
              ))}
            </div>
          </div>
          <div className="flex flex-col sm:flex-row gap-2">
            <Button variant="outline" className="w-full sm:w-auto">Display table</Button>
            <Button variant="outline" className="w-full sm:w-auto">Download table</Button>
          </div>
        </div>

        {/* Scatterplot Configuration */}
        <div className="space-y-4">
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
        </div>
      </div>

      <footer className="text-center text-sm text-gray-600 pt-8">
        By <a href="#" className="text-blue-600 hover:underline">Contributors</a>, 2023-2026, public domain
      </footer>
    </div>
  );
}

