"use client";

import { useState, useEffect} from "react";
import { CustomComparison } from "./custom-comparison";
import { CompressorSelector } from "./compressor-selector";
import { OutputConfiguration } from "./output-configuration";
import { Button } from "@/components/ui/button";
import axios from "axios";
import { useGlobalContext } from "./GlobalContext";
import { useRouter } from "next/navigation";
interface CompressorTypes {
  proposed: boolean;
  standard: boolean;
}

export default function ComparisonPage() {
  const [selectedGenomes, setSelectedGenomes] = useState<string[]>([]);
  const [selectedDatasets, setSelectedDatasets] = useState<string[]>([]);
  const [compressorTypes, setCompressorTypes] = useState<CompressorTypes>({
    proposed: true,
    standard: true,
  });
  const [selectedStandard, setSelectedStandard] = useState<string[]>([]);
  const [selectedProposed, setSelectedProposed] = useState<string[]>([]);

    const [selectedMetrics, setSelectedMetrics] = useState<string[]>([]);  const { setComparisonRecords, comparisonRecords, setGlobalLoading, testData } =    useGlobalContext();  const [downloadClicked, setDownloadClicked] = useState(false);  const router = useRouter();

    const displayTable = async () => {    try {      const response = await axios.post(        process.env.NEXT_PUBLIC_SERVER_LINK+"/dashboard/data",        {          id: testData.genomes.DNA_Corpus.checked ? selectedGenomes.map((name) => name.split(" ")[0]) : selectedDatasets.map((name) => name.split(" ")[0]),          comp_type: [            compressorTypes.proposed ? 1 : 0,            compressorTypes.standard ? 1 : 0,          ].reverse(),          standard_comp_name: selectedStandard.map(name => name.split("-")[1]),          proposed_comp_name: selectedProposed.map(name => name.split("-")[1]),          metric: selectedMetrics,        }      );      setComparisonRecords(response.data);    } catch (error) {      console.error("Error fetching data:", error);    }  };

    const handleDisplayTable = async () => {    console.log(      "Selected Genomes:",      selectedGenomes.map((name) => name.split(" ")[0])    );    console.log(      "Selected Datasets:",      selectedDatasets.map((name) => name.split(" ")[0])    );    console.log(      "Compressor Types:",      [        compressorTypes.proposed ? 1 : 0,        compressorTypes.standard ? 1 : 0,      ].reverse()    );    console.log("Selected Standard Compressors:", selectedStandard.map(name => name.split("-")[1]));    console.log("Selected Proposed Compressors:", selectedProposed.map(name => name.split("-")[1]));    console.log("Selected Metrics:", selectedMetrics);    setGlobalLoading(true);    await displayTable();    setGlobalLoading(false);    router.push("/table");  };

  const handleDownloadTable: () => void = () => {
    const headers =
      comparisonRecords.length > 0
        ? Object.keys(comparisonRecords[0]).join(",")
        : "";
    const rows = comparisonRecords
      .map((row) => Object.values(row).join(","))
      .join("\n");
    const csvContent = `data:text/csv;charset=utf-8,${headers}\n${rows}`;
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "comparison_records.csv");
    document.body.appendChild(link); // Required for FF
    link.click();
  };

  useEffect(() => {
    if (downloadClicked && comparisonRecords.length > 0) {
      console.log("Clicked");
      console.log("Comparison Records:", comparisonRecords);
      handleDownloadTable();
      setDownloadClicked(false); // Reset the downloadClicked state
    }
  }, [downloadClicked, comparisonRecords]);

  return (
    <div>
      <CustomComparison
        selectedGenomes={selectedGenomes}
        setSelectedGenomes={setSelectedGenomes}
        selectedDatasets={selectedDatasets}
        setSelectedDatasets={setSelectedDatasets}
      />
      <CompressorSelector
        compressorTypes={compressorTypes}
        setCompressorTypes={setCompressorTypes}
        selectedStandard={selectedStandard}
        setSelectedStandard={setSelectedStandard}
        selectedProposed={selectedProposed}
        setSelectedProposed={setSelectedProposed}
      />
      <OutputConfiguration
        selectedMetrics={selectedMetrics}
        setSelectedMetrics={setSelectedMetrics}
      />

      <div className="flex flex-col sm:flex-row gap-2 px-4 mt-4">
        <Button
          variant="outline"
          className="w-full sm:w-auto"
          onClick={handleDisplayTable}
        >
          Display table
        </Button>
        
        <Button
          variant="outline"
          className="w-full sm:w-auto"
          onClick={()=>setDownloadClicked(true)}
          >
          Download table
        </Button>
         
      </div>
    </div>
  );
}
