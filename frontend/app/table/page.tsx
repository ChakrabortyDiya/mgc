"use client";

import React from "react";
import CustomTable from "../../components/CustomTable";

const TablePage: React.FC = () => {
    const sampleColumns = ["ID", "O.Size", "7-zip", "paq8", "bsc"];
    const sampleData = [
      { ID: "BuEb", "O.Size": 18940, "7-zip": 5544, paq8: 4660, bsc: 4886 },
      { ID: "AgPh", "O.Size": 43970, "7-zip": 12283, paq8: 10671, bsc: 11012 },
      { ID: "CyAl", "O.Size": 31200, "7-zip": 8450, paq8: 7100, bsc: 7600 },
      { ID: "DeXt", "O.Size": 27650, "7-zip": 6780, paq8: 5900, bsc: 6200 },
      { ID: "EnLy", "O.Size": 50000, "7-zip": 15000, paq8: 13500, bsc: 14000 }
    ];
  
    return (
      <div className="container mx-auto p-6">
        <h1 className="text-2xl font-bold mb-4">Dynamic Table</h1>
        <CustomTable columns={sampleColumns} data={sampleData} />
      </div>
    );
  };
  
  export default TablePage;