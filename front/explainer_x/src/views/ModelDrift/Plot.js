import React from 'react';
import Plot from 'react-plotly.js';


const InteractionPlot = ({ data,xCol,yCol,index }) => {
  console.log(data)
  const dates = data.map((row) => row[xCol]);
 

  const electricityValues = data.map((row) => row[yCol]);
  console.log(electricityValues)
  console.log(dates)
  const chartData = [
    {
      y: electricityValues,
      x: dates,
      type: 'line',
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
              annotations : [
                {
                  x: index,
                  y: 45,
                  xref: 'x',
                  yref: 'y',
                  text: 'Concept drift detected ',
                  showarrow: true,
                  align: 'center',
                  arrowhead: 2,
                  arrowsize: 1,
                  arrowwidth: 2,
                  arrowcolor: '',
                  ax: -20, // Adjust this value
                  ay: -100, // Adjust this value
                  bordercolor: '#ff0000',
                  borderwidth: 0,
                  borderpad: 4,
                  bgcolor: '#ff7f0e',
                  opacity: 0.8,
                },
              ],
              shapes: [
                {
                  type: 'line',
                  x0: index,
                  x1: index,
                  y0: 0,
                  y1: 0.2, // Adjust this value to cover the height of the chart
                  xref: 'x',
                  yref: 'paper',
                  line: {
                    color: 'red',
                    width: 2,
                  },
                },
              ],
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
