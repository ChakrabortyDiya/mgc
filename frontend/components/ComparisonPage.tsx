"use client"

import { useState,useEffect } from "react"
import { CustomComparison } from "./custom-comparison" 
import { CompressorSelector } from "./compressor-selector"
import { OutputConfiguration } from "./output-configuration"
import { Button } from "@/components/ui/button"

interface CompressorTypes {
  proposed: boolean;
  standard: boolean;
}


export default function ComparisonPage() {
  const [selectedGenomes, setSelectedGenomes] = useState<string[]>([])
  const [compressorTypes, setCompressorTypes] = useState<CompressorTypes>({
    proposed: true,
    standard: true,
  })
  useEffect(() => {
    console.log("Effective Selected Genomes:", selectedGenomes);
  }, [selectedGenomes]);

  useEffect(() => {
    console.log("Compressor Types:", compressorTypes);
  }, [compressorTypes]);
  
  const handleDisplayTable = () => {
    console.log("Selected Genomes:", selectedGenomes)
  }
  const handleDownloadTable = () => {
    console.log("Humba")
  }
  
  return (
    <div>
      <CustomComparison selectedGenomes={selectedGenomes} setSelectedGenomes={setSelectedGenomes} />
      <CompressorSelector compressorTypes={compressorTypes} setCompressorTypes={setCompressorTypes} />
      <OutputConfiguration />

      <div className="flex flex-col sm:flex-row gap-2 px-4 mt-4">
        <Button variant="outline" className="w-full sm:w-auto" onClick={handleDisplayTable}>
          Display table
        </Button>
        <Button variant="outline" className="w-full sm:w-auto" onClick={handleDownloadTable}>
          Download table
        </Button>
      </div>
      <footer className="text-center text-sm text-gray-600 pt-8">
        By <a href="#" className="text-blue-600 hover:underline">Contributors</a>, 2023-2026, public domain
      </footer>
    </div>
  )

}
