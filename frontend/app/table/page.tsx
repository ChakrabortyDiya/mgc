"use client";

import React, { useEffect } from "react";
import CustomTable from "../../components/CustomTable";
import { useGlobalContext } from "@/components/GlobalContext";
import { useRouter } from "next/navigation";

export function parseColumns(records: Record<string, any>[]): string[] {
  if (!records || records.length === 0) return [];
  const columnSet = new Set<string>();
  records.forEach((record) => {
    Object.keys(record).forEach((key) => columnSet.add(key));
  });
  return Array.from(columnSet);
}

export function parseData(
  records: Record<string, any>[]
): Record<string, any>[] {
  return records;
}

const TablePage: React.FC = () => {
  const router = useRouter();
  const { comparisonRecords } = useGlobalContext();
  const [columns, setColumns] = React.useState<string[]>([]);
  const [data, setData] = React.useState<Record<string, any>[]>([]);

  useEffect(() => {
    // Wait for comparisonRecords to load
    if (comparisonRecords === undefined) return;

    // Detect page refresh
    const navigationEntries = performance.getEntriesByType("navigation");
    const isReload =
      navigationEntries.length > 0 &&
      (navigationEntries[0] as PerformanceNavigationTiming).type === "reload";

    // If refresh AND there's no data, redirect to "/"
    if (isReload && (!comparisonRecords || comparisonRecords.length === 0)) {
      router.replace("/");
      return;
    }

    if (comparisonRecords.length > 0) {
      const parsedColumns = parseColumns(comparisonRecords);
      const parsedData = parseData(comparisonRecords);
      setColumns(parsedColumns);
      setData(parsedData);
    }
  }, [comparisonRecords, router]);

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Dynamic Table</h1>
      <CustomTable columns={columns} data={data} />
    </div>
  );
};

export default TablePage;
