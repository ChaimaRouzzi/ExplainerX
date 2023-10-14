import React from 'react';
import Plot from 'react-plotly.js';
import SkeletonEarningCard from 'ui-component/cards/Skeleton/EarningCard';
const Heatmap = ({data,isLoading}) => {
  // Sample data for the heatmap, you can replace this with your own data
  const customColorscale = [
    [0, 'rgb(255, 255, 255)'], // White (Smallest correlation)
    [0.5, 'rgb(158, 202, 225)'], // Light Blue
    [1, 'rgb(8, 48, 107)'], // Dark Blue (Highest correlation)
  ];
  const columns = (data.length>10?Object.keys(data[0]):[])

  // Create a 2D array to hold the values for the heatmap
  const heatmapData = data.map(row => columns.map(column => row[column]));
  const chart = [
    {
        z: heatmapData,
        x: columns,
        y: columns,
      
      type: 'heatmap',
      colorscale: customColorscale,
      hovertemplate: '(<b>%{x}</b> , <b>%{y} </b> ):%{z}  <extra></extra>', // You can choose other color scales from https://plotly.com/javascript/colorscales/
    },

  ];

  const layout = {
    xaxis: {
        tickvals: columns, 
        ticktext: columns.map(col => col.replace(/_/g, ' ')), 

      },
      yaxis: {
        automargin: true, // This will automatically adjust the margins to fit long row names
      },
      // You can adjust the margin and height properties to fit the entire heatmap without cropping
      margin: {
      
        t: 50,
        b: 150,
      },
      height: 900,
      width:900
  };

  return (
    <>
    {isLoading? (<SkeletonEarningCard/>)
 : (  <div className="heatmap-container">
 <Plot data={chart} layout={layout} 
     config={{
    displayModeBar: false, 
    displaylogo: false, 
    responsive: true, 
  }} /></div>)
    }
  </>)
};

export default Heatmap;
