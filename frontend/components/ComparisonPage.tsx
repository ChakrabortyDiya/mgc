"use client"

import { useState,useEffect } from "react"
import { CustomComparison } from "./custom-comparison" 
import { CompressorSelector } from "./compressor-selector"
import { OutputConfiguration } from "./output-configuration"
import { Button } from "@/components/ui/button"
import axios from "axios"

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
  const [selectedStandard, setSelectedStandard] = useState<string[]>([])
  const [selectedProposed, setSelectedProposed] = useState<string[]>([])

  const [selectedCompName, setSelectedCompName] = useState<string[]>([])
  const [selectedMetrics, setSelectedMetrics] = useState<string[]>([])


  useEffect(() => {
    setSelectedCompName([selectedStandard[0]?.length > 0 ? selectedStandard[0] : "", selectedProposed[0]?.length > 0 ? selectedProposed[0] : ""])

  }, [selectedProposed, selectedStandard])


  const displayTable = async () => {
    try{
      const response = await axios.post("http://127.0.0.1:8000/dashboard/data", {
        id: selectedGenomes.map(name => name.split(' ')[0]),
        comp_type: [compressorTypes.proposed ? 1 : 0, compressorTypes.standard ? 1 : 0].reverse(),
        comp_name: selectedCompName.map(name => name.split('-')[1]),
        metric: selectedMetrics,
      })
      console.log("Response:", response.data)
    }
    catch (error) {
      console.error("Error fetching data:", error)
    }
  }

  const handleDisplayTable = () => {
    console.log("Selected Genomes:", selectedGenomes.map(name => name.split(' ')[0]))
    console.log("Compressor Types:", [compressorTypes.proposed ? 1 : 0, compressorTypes.standard ? 1 : 0].reverse());
    const splitSecondElements = selectedCompName.map(name => name.split('-')[1]);
    console.log("Effective Selected Comp Name:", splitSecondElements);
    console.log("Selected Standard:", selectedMetrics);
    displayTable()
    
  }
  const handleDownloadTable = () => {
    console.log("Humbaaa aaaaaaaaaaaaaaaa")
  }

  return (
    <div>
      <CustomComparison selectedGenomes={selectedGenomes} setSelectedGenomes={setSelectedGenomes} />
      <CompressorSelector compressorTypes={compressorTypes} setCompressorTypes={setCompressorTypes} selectedStandard={selectedStandard} setSelectedStandard={setSelectedStandard} selectedProposed={selectedProposed} setSelectedProposed={setSelectedProposed} />
      <OutputConfiguration selectedMetrics={selectedMetrics} setSelectedMetrics={setSelectedMetrics} />

      <div className="flex flex-col sm:flex-row gap-2 px-4 mt-4">
        <Button variant="outline" className="w-full sm:w-auto" onClick={handleDisplayTable} >
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
