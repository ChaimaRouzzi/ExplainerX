import React from 'react';
import Plot from 'react-plotly.js';
import SkeletonEarningCard from 'ui-component/cards/Skeleton/EarningCard';

const VersionsPlot = ({data,isLoading}) => {
    const chartData= 
        [
          {values: data.values?data.values:[version1,version2],
          labels:data.labels?data.labels:[1,2],
          type: 'pie',
          hole: 0.6,
          marker: {
            color: ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
          },
          hovertemplate: '<b>%{label}</b><br>%{value} row <extra></extra>',

          textfont: { color: 'white', weight: 'bold',fontSize:'25px' },
          hoverlabel: {
            bgcolor: 'rgba(0, 0, 0, 0.8)',
            font: { color: 'white' },
            bordercolor: 'transparent',
            fontSize: 14,
            borderRadius: 16,
            width:'20px',
            pointerEvents: 'none',
            whiteSpace: 'nowrap',
            align: 'left',
            padding: {
              l: 1,
              r: 1,
              b: 1,
              t: 1,
            },
            namelength: -1,
          },}
        ]
      

  
     

  return (
    <>
    {isLoading ? (
        <SkeletonEarningCard />
      ) : (
    <div className="chart-container">
      <Plot
        data={chartData}
        layout={{
         width:400,
         height:400,
     
          paper_bgcolor: 'transparent', // transparent background
          plot_bgcolor: 'transparent', // transparent plot background
        }}
        config={{
          displayModeBar: false, // Display the mode bar (including zoom, pan, etc.)
          displaylogo: false, // Display the Plotly logo
          responsive: true, // Enable responsiveness to adjust the chart size with window resize
        }}
      />
    </div>
  )
}</>
  )
};

export default VersionsPlot;
