import React from 'react';
import { Card, Box } from '@mui/material';
import Plot from 'react-plotly.js';

const Histogram = ({ plotData ,column}) => {
  return (
    <Card>
      <Box p={2}>
      
        <h3  style={{ marginBottom: '10px' }} > Understanding Data Distribution: Exploring with Histograms</h3>
        <div className="heatmap-container">
        <Plot
          data={[
            {
              x: plotData.hist_bins,
              y: plotData.hist_counts,
              type: 'bar',
              showlegend: true,
              name: column,
              marker: {
                color: '#004aad',
               
              },
              hovertemplate: `<b> value</b>: %{x}<br><b>count</b>: %{y} <extra></extra>`,
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
          ]}
          layout={{ title: 'Histogram', width: 950, height: 400 }}
          config={{
            displayModeBar: false, // Display the mode bar (including zoom, pan, etc.)
            displaylogo: false, // Display the Plotly logo
            responsive: true, // Enable responsiveness to adjust the chart size with window resize
          }}
        /></div>
      </Box>
    </Card>
  );
};

export default Histogram;
