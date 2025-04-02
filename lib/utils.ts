import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function parseCompressionData(jsonData: any) {
  if (!jsonData || !jsonData.data) {
    return [];
  }

  // Flatten the data structure for easier consumption
  const flattenedData = jsonData.data.map((item: any) => {
    const metric = item.legendgroup;
    return item.x.map((id: string, index: number) => {
      let value = 0;
      if (item.y && typeof item.y === 'object' && item.y.bdata) {
        // Handle binary data if present
        // This is a placeholder - you might need a proper binary data parser
        value = Array.isArray(item.y) ? item.y[index] : 0;
      } else if (Array.isArray(item.y)) {
        value = item.y[index];
      }
      
      return {
        legendgroup: metric,
        x: id,
        y: value
      };
    });
  }).flat();

  return flattenedData;
}