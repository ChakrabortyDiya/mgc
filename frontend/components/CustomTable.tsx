import React, { useState } from "react";

interface TableProps {
  columns: string[];
  data: Record<string, any>[];
}

const CustomTable: React.FC<TableProps> = ({ columns, data }) => {
  const [search, setSearch] = useState("");
  const [sortColumn, setSortColumn] = useState<string | null>(null);
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");

  const filteredData = data.filter((row) =>
    columns.some((col) =>
      row[col]?.toString().toLowerCase().includes(search.toLowerCase())
    )
  );

  const sortedData = sortColumn
    ? [...filteredData].sort((a, b) => {
        const valueA = a[sortColumn];
        const valueB = b[sortColumn];

        if (typeof valueA === "number" && typeof valueB === "number") {
          return sortOrder === "asc" ? valueA - valueB : valueB - valueA;
        }

        return sortOrder === "asc"
          ? valueA.toString().localeCompare(valueB.toString())
          : valueB.toString().localeCompare(valueA.toString());
      })
    : filteredData;

  const handleSort = (col: string) => {
    setSortColumn(col);
    setSortOrder(sortColumn === col && sortOrder === "asc" ? "desc" : "asc");
  };

  return (
    <div className="p-4 w-full overflow-x-auto">
      <input
        type="text"
        placeholder="Search..."
        className="mb-4 p-2 border rounded w-full"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <table className="min-w-full bg-white border shadow-md rounded-lg">
        <thead>
          <tr className="bg-gray-200">
            {columns.map((col) => (
              <th
                key={col}
                className="p-3 border cursor-pointer"
                onClick={() => handleSort(col)}
              >
                {col} {sortColumn === col ? (sortOrder === "asc" ? "▲" : "▼") : ""}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sortedData.map((row, index) => (
            <tr key={index} className="border-b hover:bg-gray-100">
              {columns.map((col) => (
                <td key={col} className="p-3 border">
                  {row[col] ?? "-"}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CustomTable;
