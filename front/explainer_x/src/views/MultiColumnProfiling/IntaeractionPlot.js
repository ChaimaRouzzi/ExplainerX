import React from 'react';
import Plot from 'react-plotly.js';
import SkeletonEarningCard from 'ui-component/cards/Skeleton/EarningCard';

const InteractionPlot = ({ data, isLoading,xCol,yCol,plotType }) => {

  const dates = data.map((row) => row[xCol]);
  console.log(dates)
  console.log(plotType)

  const electricityValues = data.map((row) => row[yCol]);
  console.log(electricityValues)
  const chartData = [
    {
      y: electricityValues,
      x: dates,
      type: plotType,
      marker: {
        color: '#004aad',
       
      },
      hovertemplate: `<b>${xCol}</b>: %{x}<br><b>${yCol}</b>: %{y} <extra></extra>`,
      showlegend: true,
      name: yCol,
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
    }
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

export default InteractionPlot;
