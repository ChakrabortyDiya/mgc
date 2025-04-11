"use client"

import { useState } from "react"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"

interface CompressorTypes {
  proposed: boolean;
  standard: boolean;
}

export function CompressorSelector({
  compressorTypes,
  setCompressorTypes,
}: {
  compressorTypes: CompressorTypes;
  setCompressorTypes: React.Dispatch<React.SetStateAction<CompressorTypes>>;
}) {
  /*const [showTop, setShowTop] = useState(false)
  const [showRelative, setShowRelative] = useState(false)*/
  
  /*const [bestSettingsCount, setBestSettingsCount] = useState(1)
  const [linkSpeed, setLinkSpeed] = useState(100)
  const [relativeCompressor, setRelativeCompressor] = useState("gzip-9")*/
    // Removed redundant line causing error
  const [selectedStandard, setSelectedStandard] = useState<string[]>([])
  const [selectedProposed, setSelectedProposed] = useState<string[]>([])

  const handleCompressorTypeChange = (type: "standard" | "proposed") => {
    setCompressorTypes((prev) => ({ ...prev, [type]: !prev[type] }))
   
  }

  /*const handleShowTopChange = (checked: boolean) => {
    setShowTop(checked)
    console.log(`Show only top ${checked ? "checked" : "unchecked"}`)
  }

  const handleShowRelativeChange = (checked: boolean) => {
    setShowRelative(checked)
    console.log(`Show all values relative to ${checked ? "checked" : "unchecked"}`)
  }*/

  /*const handleProposedChange = (compressor: string) => {
    setSelectedProposed((prev) =>
      prev.includes(compressor) ? prev.filter((c) => c !== compressor) : [...prev, compressor],
    )
    console.log(
      `Proposed compressor ${compressor} ${selectedProposed.includes(compressor) ? "deselected" : "selected"}`,
    )
  }

  const handleStandardChange = (compressor: string) => {
    setSelectedStandard((prev) =>
      prev.includes(compressor) ? prev.filter((c) => c !== compressor) : [...prev, compressor],
    )
    console.log(
      `Standard compressor ${compressor} ${selectedStandard.includes(compressor) ? "deselected" : "selected"}`,
    )
  }

  const handleSettingsChange = (setting: string) => {
    setSelectedSettings((prev) => (prev.includes(setting) ? prev.filter((s) => s !== setting) : [...prev, setting]))
    console.log(`Compressor setting ${setting} ${selectedSettings.includes(setting) ? "deselected" : "selected"}`)
  }*/

  return (
    <div className="space-y-6">
      <h3 className="text-lg font-medium text-gray-700">Step 2. Select compressors</h3>

      <div className="space-y-4">
        <div className="flex items-start space-x-8">
          <div className="flex-1 space-y-2">
            <div className="space-y-2">
              <label className="flex items-center space-x-2">
                <Checkbox
                  checked={compressorTypes.standard}
                  onCheckedChange={() => handleCompressorTypeChange("standard")}
                />
                <span>Standard compressors</span>
              </label>
              <label className="flex items-center space-x-2">
                <Checkbox
                  checked={compressorTypes.proposed}
                  onCheckedChange={() => handleCompressorTypeChange("proposed")}
                />
                <span>Proposed compressors</span>
              </label>
            </div>
          </div>

          <div className="flex-1">
            <Label>Select standard compressor setting:</Label>
            <select
              multiple
              className="w-full h-64 border rounded mt-2"
              value={selectedProposed}
              onChange={(e) => setSelectedProposed(Array.from(e.target.selectedOptions, (option) => option.value))}
            >
              <option>s-7zip</option>
              <option>s-paq8</option>
              <option>s-bsc</option>
              <option>s-gzip</option>
              <option>s-zstd</option>
              <option>s-bzip2</option>
              <option>s-zpaq</option>
              <option>s-cmix</option>
            </select>
          </div>

          <div className="flex-1">
            <Label>Select proposed compressor setting:</Label>
            <select
              multiple
              className="w-full h-64 border rounded mt-2"
              value={selectedStandard}
              onChange={(e) => setSelectedStandard(Array.from(e.target.selectedOptions, (option) => option.value))}
            >
              <option>p-7zip</option>
              <option>p-paq8</option>
              <option>p-bsc</option>
              <option>p-gzip</option>
              <option>p-zstd</option>
              <option>p-bzip2</option>
              <option>p-zpaq</option>
              <option>p-cmix</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  )
}

