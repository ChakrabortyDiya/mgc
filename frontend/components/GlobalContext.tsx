"use client";
import React, {
  createContext,
  useState,
  ReactNode,
  useContext,
  useEffect,
} from "react";
import Loader from "./ui/loader";

interface GlobalContextProps {
  count: number;
  setCount: React.Dispatch<React.SetStateAction<number>>;
  comparisonRecords: any[];
  setComparisonRecords: React.Dispatch<React.SetStateAction<any[]>>;
  setGlobalLoading: React.Dispatch<React.SetStateAction<boolean>>;
}
export const GlobalContext = createContext<GlobalContextProps>({
  count: 0,
  setCount: () => {},
  comparisonRecords: [],
  setComparisonRecords: () => {},
  setGlobalLoading: () => {},
});

export const useGlobalContext = () => {
  return useContext(GlobalContext);
};

export const GlobalProvider = ({ children }: { children: ReactNode }) => {
  const [count, setCount] = useState(0);
  const [comparisonRecords, setComparisonRecords] = useState<any[]>([]);
  const [globalLoading, setGlobalLoading] = useState(false);

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
      }}
    >
      {globalLoading ? <Loader /> : children}
    </GlobalContext.Provider>
  );
};
