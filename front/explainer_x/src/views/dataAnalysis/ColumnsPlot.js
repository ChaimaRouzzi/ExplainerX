import React from 'react';
import Plot from 'react-plotly.js';
import SkeletonEarningCard from 'ui-component/cards/Skeleton/EarningCard';

const ColumnsPlot = ({ data, data2, isLoading }) => {
  const removeFirstAndLastFive = (arr) => {
 
    console.log(arr)
    if (arr.length > 10)
    return [...arr.slice(1, arr.length - 5)];
    }
  const chartData = [
    {
      y: data.values ? removeFirstAndLastFive(data.values) : [],
      x: data.labels ? removeFirstAndLastFive(data.labels) : [],
      type: 'bar',
      marker: {
        color: 'rgb(158, 202, 225)',
        line: {
          color: 'rgb(8, 48, 107)',
          width: 1.5,
        },
      },
      hovertemplate: '<b>%{label}</b><br>missing values:%{value}  <extra></extra>',
      showlegend: true,
      name: 'Missing Values',
      textfont: { color: 'white', weight: 'bold', fontSize: '25px' },
      hoverlabel: {
        bgcolor: 'rgba(0, 0, 0, 0.8)',
        font: { color: 'white' },
        bordercolor: 'transparent',
        fontSize: 14,
        borderRadius: 16,
        width: '17px',
        pointerEvents: 'none',
        whiteSpace: 'nowrap',
        align: 'left',
        padding: {
          l: 12,
          r: 12,
        },
        namelength: -5,
      },
    },
    {
      y: data2.values ? removeFirstAndLastFive(data2.values) : [],
      x: data2.labels ? removeFirstAndLastFive(data2.labels) : [],
      type: 'bar',
      marker: {
        color: 'rgba(58, 200, 225, .5)',
        line: {
          color: 'rgb(8, 48, 107)',
          width: 1.5,
        },
      },
      name: 'Outliers',
      hovertemplate: '<b>%{label}</b><br> outlires:%{value} <extra></extra>',
      showlegend: true,
      textfont: { color: 'white', weight: 'bold', fontSize: '25px' },
      hoverlabel: {
        bgcolor: 'rgba(0, 0, 0, 0.8)',
        font: { color: 'white' },
        bordercolor: 'transparent',
        fontSize: 14,
        borderRadius: 16,
        width: '17px',
        pointerEvents: 'none',
        whiteSpace: 'nowrap',
        align: 'left',
        padding: {
          l: 12,
          r: 12,
          b: 12,
          t: 12,
        },
        namelength: -1,
      },
    },
  ];

  

  return (
    <>
      {isLoading ? (
        <SkeletonEarningCard />
      ) : (
        <div className="heatmap-container">
          <Plot
            data={chartData}
            layout={{
             // Set the width to 100%
             
              width:1000,
              paper_bgcolor: 'transparent',
              plot_bgcolor: 'transparent',
              xaxis: {
                tickangle: 45, // Rotate x-axis labels by -45 degrees
                automargin: true, // Automatically adjust margins to fit the labels
              },
            }}
            config={{
              displayModeBar: false, // Display the mode bar (including zoom, pan, etc.)
              displaylogo: false, // Display the Plotly logo
              responsive: true, // Enable responsiveness to adjust the chart size with window resize
            }}
          />
          </div>
    
      )}
    </>
  );
};

export default ColumnsPlot;
