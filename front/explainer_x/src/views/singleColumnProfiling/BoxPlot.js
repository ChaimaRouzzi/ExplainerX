import React from 'react';
import { Card, Box } from '@mui/material';
import Plot from 'react-plotly.js';

const BoxPlot = ({ plotData ,column}) => {
  return (
    <Card>
      <Box p={2}>
       
          <h3 style={{ marginBottom: '10px' }} >   Outliers Unveiled: Exploring Data Anomalies </h3>
      
          <div className="heatmap-container">
        <Plot
          data={[
            {
              y: plotData.column_values,
              type: 'box',
              showlegend: true,
              name:column,
              marker: {
                color: '#004aad',
               
              },
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
          layout={{ title: 'Box Plot',  width:950, height: 500 }}
          config={{
            displayModeBar: false, // Display the mode bar (including zoom, pan, etc.)
            displaylogo: false, // Display the Plotly logo
            responsive: true, // Enable responsiveness to adjust the chart size with window resize
          }}
        /> 
        </div>
      </Box>
     
    </Card>
  );
};

export default BoxPlot;
