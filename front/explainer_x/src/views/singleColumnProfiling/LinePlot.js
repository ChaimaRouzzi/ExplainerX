import React from 'react';
import { Card, Box } from '@mui/material';
import Plot from 'react-plotly.js';

const LinePlot = ({ plotData,column}) => {
  return (
    <Card>
      <Box p={2}>
        <h3 style={{ marginBottom: '10px' }}>  Tracing the Path: Visualizing Data Trends</h3>
        <div className="heatmap-container">
        <Plot
          data={[
            {
              x: plotData.date_values,
              y: plotData.column_values,
              type: 'scatter',
              mode: 'lines+markers',
              showlegend: true,
              name: column,
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
          layout={{ title: 'Line Plot', width: 950, height: 400 }}
          config={{
            displayModeBar: false, 
            displaylogo: false, 
            responsive: true,
          }}
        />
        </div>
      </Box>
    </Card>
  );
};

export default LinePlot;
