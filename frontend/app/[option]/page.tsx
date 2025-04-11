"use client";

import { Header } from "../../components/header";
import CompressionChart from "../../components/CompressionChart";
import { useState, useEffect } from "react";
// import rawData from "../../assets/compression_ratio.json"
import { useSearchParams, useParams } from "next/navigation"; // update import
import axios from "axios";

function decodeBdata(bdata: string): number[] {
  const binaryString = atob(bdata);
  const byteArray = new Uint8Array(binaryString.length);
  for (let i = 0; i < binaryString.length; i++) {
      byteArray[i] = binaryString.charCodeAt(i);
  }
  return Array.from(byteArray);
}

function parseData(rawData: any) {
    if (!rawData || !Array.isArray(rawData.data)) return [];
  
    const parsedData: any[] = [];
  
    rawData.data.forEach((item: any) => {
      if (item.y && item.y.bdata) {
        const yValues = decodeBdata(item.y.bdata);
        item.x.forEach((xValue: string, index: number) => {
          parsedData.push({
            legendgroup: item.legendgroup,
            x: xValue,
            y: yValues[index] || 0,
          });
        });
      }
    });
  
    return parsedData;
}
export default function VisualizationPage() {
  // const [data, setData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // const searchParams = useSearchParams();
  // Removed use of useRouter and use useParams instead
  const { option } = useParams(); // using new hook

  const [selectedChartOptions, setSelectedChartOptions] = useState<string[]>([]);
  const [selectedPlotOptions, setSelectedPlotOptions] = useState<string[]>([]);

  // Log unused variables to ensure they are used
  useEffect(() => {
    console.log("selectedChartOptions:", selectedChartOptions);
    console.log("selectedPlotOptions:", selectedPlotOptions);
  }, [selectedChartOptions, selectedPlotOptions]);

  // generate graph data
  const generateGraphData = async (option: string, type: "barchart" | "plot") => {
    const setter = type === "barchart" ? setSelectedChartOptions : setSelectedPlotOptions;
  
    try {
      const response = await axios.post(`http://127.0.0.1:8000/dashboard/chart/${type}`, {
        name: option?.toLowerCase() || "",
      });
  
      if (response.status !== 200) {
        console.error("Server responded with status:", response.status, response.data);
        throw new Error("Failed to fetch data");
      }
  
      setter(response.data);
  
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error("Error sending request:", error.message, "Response:", error.response?.data);
      } else {
        console.error("Unexpected error:", error);
      }
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      console.log("Selected option:", option);
      if (option) {
        await generateGraphData(
          (typeof option === "string" ? option.replace("_", " ") : "") || "",
          "barchart"
        );
        setIsLoading(false);
      }
    };

    fetchData();
  }, [option]);

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-semibold text-[#4A6EA9] text-center mb-8">
          Compression Visualization
        </h1>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          {isLoading ? (
            <div className="flex justify-center items-center h-64">
              <div className="text-gray-500">Loading visualization data...</div>
            </div>
          ) : (
            <CompressionChart 
              data={parseData(selectedChartOptions)}
              title="Compression Performance Comparison"
              xAxisTitle="Datasets"
              yAxisTitle="Compression Ratio"
            />
          )}
        </div>
      </main>
    </div>
  );
}