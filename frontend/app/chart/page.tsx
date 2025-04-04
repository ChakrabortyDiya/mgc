"use client";

import { Header } from "../../components/header";
import CompressionChart from "../../components/CompressionChart";
import { useState, useEffect } from "react";
import rawData from "../../../data/plot_metadata/compression_ratio.json"

function decodeBdata(bdata: string): number[] {
    const binaryString = atob(bdata);
    const byteArray = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      byteArray[i] = binaryString.charCodeAt(i);
    }
    const floatArray = new Float64Array(byteArray.buffer);
    return Array.from(floatArray);
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
  const [data, setData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

useEffect(() => {
    const parsedData = parseData(rawData);
    setData(parsedData);
    setIsLoading(false);
  }, []);

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
              data={data}
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