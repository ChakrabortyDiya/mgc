"use client"

import { useState } from "react"
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export function CompressorSelector() {
  const [showTop, setShowTop] = useState(false)
  const [showRelative, setShowRelative] = useState(false)
  const [compressorTypes, setCompressorTypes] = useState({
    proposed: true,
    standard: true,
  })
  const [bestSettingsCount, setBestSettingsCount] = useState(1)
  const [linkSpeed, setLinkSpeed] = useState(100)
  const [relativeCompressor, setRelativeCompressor] = useState("gzip-9")
  const [selectedProposed, setSelectedProposed] = useState<string[]>([])
  const [selectedStandard, setSelectedStandard] = useState<string[]>([])
  const [selectedSettings, setSelectedSettings] = useState<string[]>([])

  const handleCompressorTypeChange = (type: "proposed" | "standard") => {
    setCompressorTypes((prev) => ({ ...prev, [type]: !prev[type] }))
    console.log(`${type} compressors ${compressorTypes[type] ? "unchecked" : "checked"}`)
  }

  const handleShowTopChange = (checked: boolean) => {
    setShowTop(checked)
    console.log(`Show only top ${checked ? "checked" : "unchecked"}`)
  }

  const handleShowRelativeChange = (checked: boolean) => {
    setShowRelative(checked)
    console.log(`Show all values relative to ${checked ? "checked" : "unchecked"}`)
  }

  const handleProposedChange = (compressor: string) => {
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
  }

  return (
    <div className="space-y-6">
      <h3 className="text-lg font-medium text-gray-700">Step 2. Select compressors</h3>

      <div className="space-y-4">
        <div className="flex items-start space-x-8">
          <div className="flex-1 space-y-2">
            <div className="space-y-2">
              <label className="flex items-center space-x-2">
                <Checkbox
                  checked={compressorTypes.proposed}
                  onCheckedChange={() => handleCompressorTypeChange("proposed")}
                />
                <span>Standard compressors</span>
              </label>
              <label className="flex items-center space-x-2">
                <Checkbox
                  checked={compressorTypes.standard}
                  onCheckedChange={() => handleCompressorTypeChange("standard")}
                />
                <span>Proposed compressors</span>
              </label>
            </div>

            <div className="space-y-4">
              <label className="flex items-center space-x-2">
                <Checkbox defaultChecked />
                <span>Setting Metrics</span>
              </label>

              <select className="w-full border rounded px-2 py-1">
                <option>Compression Ratio</option>
                <option>Compression Time</option>
                <option>Compression Memory</option>
                <option>Compression CPU Usage</option>
                <option>Decompression Time</option>
                <option>Decompression Memory</option>
                <option>Decompression CPU Usage</option>
              </select>
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
              <option>S-7zip</option>
              <option>S-PAQ8</option>
              <option>S-BSC</option>
              <option>S-GZIP</option>
              <option>S-ZSTD</option>
              <option>S-BZIP2</option>
              <option>S-ZPAQ</option>
              <option>S-Cmix</option>
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
              <option>P-7zip</option>
              <option>P-PAQ8</option>
              <option>P-BSC</option>
              <option>P-GZIP</option>
              <option>P-ZSTD</option>
              <option>P-BZIP2</option>
              <option>P-ZPAQ</option>
              <option>P-Cmix</option>
            </select>
          </div>
          <div className="flex-1">
            <Label>Select individual compressor setting:</Label>
            <select
              multiple
              className="w-full h-64 border rounded mt-2"
              value={selectedStandard}
              onChange={(e) => setSelectedStandard(Array.from(e.target.selectedOptions, (option) => option.value))}
            >
              <option></option>
            </select>
          </div>
        </div>
      </div>
    </div>
  )
}

