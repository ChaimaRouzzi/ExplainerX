import React from 'react';
import Plot from 'react-plotly.js';


const InteractionPlot = ({ data ,xCol,yCol,color }) => {

  const dates = data.map((row) => row[xCol]);
  console.log(dates)

  const electricityValues = data.map((row) => row[yCol]);
  console.log(electricityValues)
  const chartData = [
    {
      y: electricityValues,
      x: dates,
      type: 'line',
      marker: {
        color: color,
       
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
      
        <div className="heatmap-container">
          <Plot
            data={chartData}
            layout={{
             // Set the width to 100%
             
              width:500,
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
    
     
    </>
  );
};

export default InteractionPlot;
