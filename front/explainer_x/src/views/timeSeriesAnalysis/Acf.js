import React, { useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { TextField, Button, Tooltip, IconButton, MenuItem, Box, Select, Grid, Card } from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';
import { gridSpacing } from 'store/constant';
import SkeletonEarningCard from 'ui-component/cards/Skeleton/EarningCard';
const TimeSeriesPlot = ({ ver, updated }) => {
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedColumn, setSelectedColumn] = useState('');
  const [selectedFunction, setSelectedFunction] = useState('');
  const [numLags, setNumLags] = useState(10);
  const [showModelDescription, setShowModelDescription] = useState(false);
  const [isTooltipHovered, setIsTooltipHovered] = useState(false);

  const fetchData = async () => {
    try {
      setIsLoading(true); // Show the progress circular
      setData([]); // Reset data to an empty array

      const response = await axios.get(
        `http://localhost:8000/api/time_series_analysis/${
          updated.updated
        }/${selectedFunction.toLowerCase()}?column_name=${selectedColumn}&num_lags=${numLags}&version=${ver}`
      );
      setData(response.data);
      setIsLoading(false); // Hide the progress circular
    } catch (error) {
      console.log(error);
      setIsLoading(false); // Hide the progress circular in case of an error
    }
  };

  const columns = [
    { value: 'Electricity', label: 'Electricity' },
    { value: 'Gas_01', label: 'Gas_01' },
    { value: 'Gas_02', label: 'Gas_02' },
    { value: 'Gas_03', label: 'Gas_03' }
  ];

  const functions = [
    {
      value: 'acf',
      label: 'Autocorrelation Function (ACF)',
      description:
        'The Autocorrelation Function (ACF) measures the correlation between a time series and its lagged values. It helps identify the presence of any correlation between the current value and past values at different lags.'
    },
    {
      value: 'pacf',
      label: 'Partial Autocorrelation Function (PACF)',
      description:
        'The Partial Autocorrelation Function (PACF) measures the correlation between a time series and its lagged values after removing the effects of intermediate lags. It helps identify the direct relationship between the current value and past values at different lags, excluding the influence of other lags.'
    }
  ];

  const handleColumnChange = (event) => {
    setSelectedColumn(event.target.value);
    setData([]); // Reset data when selecting a new column
  };

  const handleFunctionChange = (event) => {
    setSelectedFunction(event.target.value);
    setData([]); // Reset data when selecting a new function
  };

  const handleNumLagsChange = (event) => {
    setNumLags(event.target.value);
    setData([]); // Reset data when changing the number of lags
  };

  const handleFetchData = () => {
    fetchData();
  };

  const handleTooltipHover = (isHovered) => {
    setIsTooltipHovered(isHovered);
  };

  const createPlotData = (data, plot_pacf) => {
    const corrArray = plot_pacf ? data.map((item) => item - data[0]) : data;

    const lowerY = corrArray.map((item) => item - data[0]);
    const upperY = corrArray.map((item) => item - data[0]);

    const lines = [...Array(corrArray.length).keys()].map((index) => {
      const xValues = [index.toString(), index.toString()];
      const yValues = [0, corrArray[index]];
      return { x: xValues, y: yValues, type: 'scatter', mode: 'lines', line: { color: '#3f3f3f' } };
    });

    return [
      ...lines,
      {
        x: [...Array(corrArray.length).keys()].map((item) => item.toString()),
        y: corrArray,
        type: 'scatter',
        mode: 'markers',
        marker: { color: '#004aad', size: 12 }
      },
      {
        x: [...Array(corrArray.length).keys()].map((item) => item.toString()),
        y: upperY,
        type: 'scatter',
        mode: 'lines',
        line: { color: 'rgba(255, 255, 255, 0)' }
      },
      {
        x: [...Array(corrArray.length).keys()].map((item) => item.toString()),
        y: lowerY,
        type: 'scatter',
        mode: 'lines',
        fill: 'tonexty',
        fillcolor: 'rgba(32, 146, 230, 0.3)',
        line: { color: 'rgba(255, 255, 255, 0)' }
      }
    ];
  };

  return (
    <Grid container spacing={gridSpacing}>
      <Grid item lg={12} md={12} sm={12} xs={12}>
        <Card>
          <Grid container spacing={2} style={{ alignItems: 'center' }}>
            <Grid item lg={5} md={5} sm={12} xs={12} style={{ marginLeft: '50px' }}>
              <h3 style={{ marginBottom: '10px' }}> Please select a column </h3>
              <Select value={selectedColumn} onChange={handleColumnChange} displayEmpty sx={{ width: '100%' }}>
                <MenuItem value="" disabled>
                  Select Column
                </MenuItem>
                {columns.map((column) => (
                  <MenuItem key={column.value} value={column.value}>
                    {column.label}
                  </MenuItem>
                ))}
              </Select>
            </Grid>
            <Grid item lg={5} md={5} sm={12} xs={12} style={{ marginLeft: '50px' }}>
              <h3 style={{ marginBottom: '10px' }}> Please select a decomposition model </h3>
              <Box sx={{ position: 'relative' }}>
                <Select value={selectedFunction} onChange={handleFunctionChange} displayEmpty sx={{ width: '100%' }}>
                  <MenuItem value="" disabled>
                    Select Function
                  </MenuItem>
                  {functions.map((model) => (
                    <MenuItem key={model.value} value={model.value}>
                      {model.label}
                    </MenuItem>
                  ))}
                </Select>
                {selectedFunction && (
                  <Tooltip
                    title={functions.find((model) => model.value === selectedFunction).description}
                    placement="right"
                    arrow
                    open={showModelDescription || isTooltipHovered}
                    onOpen={() => setShowModelDescription(true)}
                    onClose={() => setShowModelDescription(false)}
                    PopperProps={{
                      disablePortal: true
                    }}
                    enterDelay={500}
                    enterTouchDelay={0}
                    leaveTouchDelay={200}
                    onMouseEnter={() => handleTooltipHover(true)}
                    onMouseLeave={() => handleTooltipHover(false)}
                  >
                    <IconButton sx={{ position: 'absolute', top: '50%', right: 'épx', transform: 'translateY(-50%)' }}>
                      <InfoIcon />
                    </IconButton>
                  </Tooltip>
                )}
              </Box>
            </Grid>
            <Grid item lg={5} md={5} sm={12} xs={12} style={{ marginLeft: '50px' }}>
              <Box sx={{ marginBottom: '20px' }}>
                <h3 style={{ marginBottom: '10px' }}> Please enter the number of lags </h3>
                <TextField value={numLags} onChange={handleNumLagsChange} type="number" variant="outlined" fullWidth />
              </Box>
            </Grid>
            <Grid item lg={5} md={5} sm={12} xs={12} style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Button
                variant="contained"
                onClick={handleFetchData}
                sx={{
                  textAlign: 'center',
                  padding: ' 8px 40px',
                  backgroundColor: '#004aad',
                  '&:hover': {
                    backgroundColor: '#004aad'
                  }
                }}
              >
                Get Plots
              </Button>
            </Grid>
            <Grid item lg={12} md={12} sm={12} xs={12}>
              {isLoading && <SkeletonEarningCard />}
            </Grid>
            {data.length > 0 && (
              <div className="heatmap-container" style={{ margin: 'auto' }}>
                <Plot
                  data={createPlotData(data, selectedFunction === 'PACF')}
                  layout={{
                    title: `${selectedFunction} function for the column: ${selectedColumn}`,
                    showlegend: false,
                    width: 1000,
                    height: 400
                  }}
                  config={{
                    displayModeBar: false, // Display the mode bar (including zoom, pan, etc.)
                    displaylogo: false, // Display the Plotly logo
                    responsive: true // Enable responsiveness to adjust the chart size with window resize
                  }}
                />
              </div>
            )}
          </Grid>
        </Card>
      </Grid>
    </Grid>
  );
};

export default TimeSeriesPlot;
