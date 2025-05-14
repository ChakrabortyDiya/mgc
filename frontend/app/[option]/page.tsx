"use client";

import { useEffect, useRef, useState } from "react";
import { Header } from "../../components/header";
import { useParams } from "next/navigation";
import axios from "axios";
import Loader from "../../components/ui/loader";
import { useGlobalContext } from "../../components/GlobalContext";
import { motion } from "framer-motion";

export default function VisualizationPage() {
  const [isLoading, setIsLoading] = useState(true);
  const { option } = useParams();
  const { selectedGenomeType } = useGlobalContext();

  const [selectedChartOptions, setSelectedChartOptions] = useState<string>("");
  const chartContainerRef = useRef<HTMLDivElement>(null);

  const generateGraphData = async (option: string) => {
    try {
      console.log("Generating graph data for option:", option);
      console.log("Selected genome type:", selectedGenomeType);
      
      const response =
        option === "wacr -vs- total decompression time"
          ? await axios.post(
              `${process.env.NEXT_PUBLIC_SERVER_LINK}/dashboard/chart/scatterplot`
            )
          : await axios.post(
              `${process.env.NEXT_PUBLIC_SERVER_LINK}/dashboard/chart/barchart`,
              { 
                name: option?.toLowerCase() || "",
                genomeType: selectedGenomeType.toLowerCase()

              }
            );
      if (response.status !== 200) throw new Error("Failed to fetch data");
      setSelectedChartOptions(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        if (option) {
            await generateGraphData(
            typeof option === "string" ? option.replace(/_/g, " ") : ""
            );
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, [option]);

  // This effect will execute scripts inside the injected HTML
  useEffect(() => {
    if (chartContainerRef.current) {
      const scripts = chartContainerRef.current.getElementsByTagName("script");
      const externalScripts: HTMLScriptElement[] = [];
      const inlineScripts: HTMLScriptElement[] = [];

      // Separate external and inline scripts
      for (let i = 0; i < scripts.length; i++) {
        const script = scripts[i];
        if (script.src) {
          externalScripts.push(script);
        } else {
          inlineScripts.push(script);
        }
      }

      // Helper to load a script and return a promise
      const loadScript = (script: HTMLScriptElement) => {
        return new Promise<void>((resolve) => {
          const newScript = document.createElement("script");
          newScript.src = script.src;
          newScript.async = false;
          newScript.onload = () => resolve();
          document.body.appendChild(newScript);
        });
      };

      // Load all external scripts, then run inline scripts
      Promise.all(externalScripts.map(loadScript)).then(() => {
        inlineScripts.forEach((script) => {
          const newScript = document.createElement("script");
          if (script.type) newScript.type = script.type;
          if (script.textContent) newScript.textContent = script.textContent;
          document.body.appendChild(newScript);
        });
      });
    }
  }, [selectedChartOptions]);

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen bg-white"
    >
      {isLoading && <Loader />}
      <Header />
      <motion.main 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="container mx-auto px-4 py-8"
      >
        <motion.div
          ref={chartContainerRef}
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.3 }}
          dangerouslySetInnerHTML={{ __html: selectedChartOptions }}
        />
      </motion.main>
    </motion.div>
  );
}
