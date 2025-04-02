import React from 'react';
import dynamic from 'next/dynamic';
import { ApexOptions } from 'apexcharts';

// Dynamically import ApexCharts to avoid SSR issues
const ReactApexChart = dynamic(() => import('react-apexcharts'), { ssr: false });

interface DataPoint {
  legendgroup: string;
  x: string;
  y: number | string;
}

interface ChartProps {
  data: DataPoint[];
  title?: string;
  xAxisTitle?: string;
  yAxisTitle?: string;
}

const CompressionChart: React.FC<ChartProps> = ({ 
  data, 
  title = 'Data Visualization',
  xAxisTitle = 'ID',
  yAxisTitle = 'Value'
}) => {
  // Extract unique IDs and metrics
  const ids = Array.from(new Set(data.map((item) => item.x)));
  const metrics = Array.from(new Set(data.map((item) => item.legendgroup)));
  
  // Organize data for ApexCharts with proper typing
  const series = metrics.map(metric => {
    const metricData = data.filter((item) => item.legendgroup === metric);
    return {
      name: metric as string, // Explicitly cast to string
      data: ids.map(id => {
        const matchingItem = metricData.find((item) => item.x === id);
        return matchingItem ? parseFloat(matchingItem.y.toString()) : 0;
      })
    };
  });

   // Calculate dynamic chart width based on the number of data points
   const chartWidth = Math.max(ids.length * 50, 1000); // 50px per bar, minimum width 1000px


  const options: ApexOptions = {
    chart: {
      type: 'bar',
      height: 500,
      stacked: false,
      toolbar: {
        show: true,
      },
      zoom: {
        enabled: true
      }
    },
    responsive: [{
      breakpoint: 480,
      options: {
        legend: {
          position: 'bottom',
          offsetX: -10,
          offsetY: 0
        }
      }
    }],
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: '70%',
      },
    },
    xaxis: {
      type: 'category',
      categories: ids,
      title: {
        text: xAxisTitle
      }
    },
    yaxis: {
      title: {
        text: yAxisTitle
      },
    },
    legend: {
      position: 'right',
      offsetY: 40
    },
    fill: {
      opacity: 1
    },
    title: {
      text: title,
      align: 'center'
    },
    tooltip: {
      y: {
        formatter: function (val) {
          return val.toFixed(2);
        }
      }
    }
  };

  return (
    <div className="chart-container">
      <div className="overflow-x-auto">
        <div style={{ minWidth: `${chartWidth}px` }}>
          {typeof window !== 'undefined' && (
            <ReactApexChart 
              options={options}
              series={series}
              type="bar"
              height={500}
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default CompressionChart;