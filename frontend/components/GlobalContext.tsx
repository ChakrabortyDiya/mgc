"use client";
import React, {
  createContext,
  useState,
  ReactNode,
  useContext,
  useEffect,
} from "react";
import Loader from "./ui/loader";
import { AnimatePresence, motion } from "framer-motion";

interface GlobalContextProps {
  count: number;
  setCount: React.Dispatch<React.SetStateAction<number>>;
  comparisonRecords: any[];
  setComparisonRecords: React.Dispatch<React.SetStateAction<any[]>>;
  setGlobalLoading: React.Dispatch<React.SetStateAction<boolean>>;
  selectedGenomeType: string;
  setSelectedGenomeType: React.Dispatch<React.SetStateAction<string>>;
}

const GlobalContext = createContext<GlobalContextProps>({
  count: 0,
  setCount: () => {},
  comparisonRecords: [],
  setComparisonRecords: () => {},
  setGlobalLoading: () => {},
  selectedGenomeType: "DNA_Corpus",
  setSelectedGenomeType: () => {},
});

export const GlobalContextProvider = ({ children }: { children: ReactNode }) => {
  const [count, setCount] = useState(0);
  const [comparisonRecords, setComparisonRecords] = useState<any[]>([]);
  const [globalLoading, setGlobalLoading] = useState<boolean>(false);
  const [selectedGenomeType, setSelectedGenomeType] = useState<string>("DNA_Corpus");

  useEffect(() => {
    console.log("Global Loading State:", globalLoading);
  }, [globalLoading]);

  return (
    <GlobalContext.Provider
      value={{
        count,
        setCount,
        comparisonRecords,
        setComparisonRecords,
        setGlobalLoading,
        selectedGenomeType,
        setSelectedGenomeType,
      }}
    >
      <AnimatePresence mode="wait">
        {globalLoading ? (
          <motion.div
            key="loader"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            <Loader />
          </motion.div>
        ) : (
          <motion.div
            key="content"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            {children}
          </motion.div>
        )}
      </AnimatePresence>
    </GlobalContext.Provider>
  );
};

export const useGlobalContext = () => useContext(GlobalContext);
