"use client"

import { useEffect} from "react"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"

interface CompressorTypes {
  proposed: boolean;
  standard: boolean;
}

const standardOptions = [
  "S-7zip", "S-paq8px", "S-bsc", "S-gzip", "S-zstd", "S-bzip2", "S-zpaq", "S-cmix"
]

const proposedOptions = [
  "P-7zip", "P-paq8px", "P-bsc", "P-gzip", "P-zstd", "P-bzip2", "P-zpaq", "P-cmix"
]

export function CompressorSelector({
  compressorTypes,
  setCompressorTypes,
  selectedStandard, setSelectedStandard, selectedProposed, setSelectedProposed
}: {
  compressorTypes: CompressorTypes;
  setCompressorTypes: React.Dispatch<React.SetStateAction<CompressorTypes>>;
  selectedStandard: string[];
  setSelectedStandard: React.Dispatch<React.SetStateAction<string[]>>;
  selectedProposed: string[];
  setSelectedProposed: React.Dispatch<React.SetStateAction<string[]>>;
}) {
  /*const [showTop, setShowTop] = useState(false)
  const [showRelative, setShowRelative] = useState(false)*/
  
  /*const [bestSettingsCount, setBestSettingsCount] = useState(1)
  const [linkSpeed, setLinkSpeed] = useState(100)
  const [relativeCompressor, setRelativeCompressor] = useState("gzip-9")*/
    // Removed redundant line causing error
  

  const handleCompressorTypeChange = (type: "standard" | "proposed") => {
    setCompressorTypes((prev) => ({ ...prev, [type]: !prev[type] }))
  }

  const handleStandardCheckbox = (option: string) => {
    setSelectedStandard((prev) =>
      prev.includes(option) ? prev.filter(o => o !== option) : [...prev, option]
    )
  }

  const handleProposedCheckbox = (option: string) => {
    setSelectedProposed((prev) =>
      prev.includes(option) ? prev.filter(o => o !== option) : [...prev, option]
    )
  }

  useEffect(() => {
    if(compressorTypes.standard === false) {
      setSelectedStandard([])
    }
    if(compressorTypes.proposed === false) {
      setSelectedProposed([])
    }
  },[compressorTypes])

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

           <div className={`flex-1 space-y-2 ${!compressorTypes.standard && "opacity-50 pointer-events-none"}`}>
          <Label>Select standard compressors:</Label>
          {standardOptions.map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox
                checked={selectedStandard.includes(option)}
                onCheckedChange={() => handleStandardCheckbox(option)}
              />
              <span>{option}</span>
            </label>
          ))}
        </div>

        <div className={`flex-1 space-y-2 ${!compressorTypes.proposed && "opacity-50 pointer-events-none"}`}>
          <Label>Select proposed compressors:</Label>
          {proposedOptions.map((option) => (
            <label key={option} className="flex items-center space-x-2">
              <Checkbox
                checked={selectedProposed.includes(option)}
                onCheckedChange={() => handleProposedCheckbox(option)}
              />
              <span>{option}</span>
            </label>
          ))}
        </div>
        </div>
      </div>
    </div>
  )
}

