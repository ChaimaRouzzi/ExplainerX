import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';
import { Select, MenuItem, Box, Tooltip, IconButton, Typography,Grid } from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';
import MainCard from 'ui-component/cards/MainCard';
import { gridSpacing } from 'store/constant';
import SkeletonEarningCard from 'ui-component/cards/Skeleton/EarningCard';
const Decomposition = ({ver,updated}) => {
  const [decompositionData, setDecompositionData] = useState(null);
  const [selectedColumn, setSelectedColumn] = useState('');
  const [selectedModelType, setSelectedModelType] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showModelDescription, setShowModelDescription] = useState(false); // Add this state
  const [isTooltipHovered, setIsTooltipHovered] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (selectedColumn && selectedModelType) {
          setIsLoading(true);
          const endpoint = `http://localhost:8000/api/time_series_analysis/${updated.updated}/decomposition?column_name=${selectedColumn}&model_type=${selectedModelType}&version=${ver}`;
          const response = await axios.get(endpoint);
          
          if (selectedModelType === "multiplicative" && response.data.Error) {
            setError(response.data.Error);
            setDecompositionData(null);
          } else {
            setDecompositionData(response.data);
            setError(null);
          }

          setIsLoading(false);
        }
      } catch (error) {
        console.log('Error fetching decomposition data:', error);
        setIsLoading(false);
        setError("An error occurred while fetching the decomposition data.");
        setDecompositionData(null);
      }
    };

    fetchData();
  }, [selectedColumn, selectedModelType,ver]);

  const handleChangeColumn = (event) => {
    setSelectedColumn(event.target.value);
  };

  const handleChangeModelType = (event) => {
    setSelectedModelType(event.target.value);
  };



  const columns = [
    { value: 'Electricity', label: 'Electricity' },
    { value: 'Gas_01', label: 'Gas_01' },
    { value: 'Gas_02', label: 'Gas_02' },
    { value: 'Gas_03', label: 'Gas_03' },
  ];

  const models = [
    {
      value: 'additive',
      label: 'Additive',
      description: 'The additive model assumes that the components (trend, seasonal, and residual) are added together to form the time series.',
    },
    {
      value: 'multiplicative',
      label: 'Multiplicative',
      description: 'The multiplicative model assumes that the components (trend, seasonal, and residual) are multiplied together to form the time series.',
    },
  ];

  const getLineChartData = (dataType) => {
    const labels = decompositionData['Date'];
    const data = decompositionData[dataType];

    return {
      x: labels,
      y: data,
      mode: 'lines',
      line: {
        color: '#004aad',
        width: 1,
      },
    };
  };

  const handleTooltipHover = (isHovered) => {
    setIsTooltipHovered(isHovered);
  };

  return (
    <Grid container spacing={gridSpacing}>
  
        <Grid item lg={12} md={12} sm={12} xs={12} >
  <MainCard>
    <Grid container spacing={2} style={{alignItems:'center'}}>
      <Grid item lg={5} md={5} sm={12} xs={12}  style={{ marginLeft: '50px' }} >
            <Typography variant="h4" sx={{ marginBottom: '10px' }}>
              Please select a column
            </Typography>
            <Select value={selectedColumn} onChange={handleChangeColumn} displayEmpty sx={{ width: '100%' }}>
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

         <Grid item lg={5} md={5} sm={12} xs={12}  style={{ marginLeft: '50px' }} >
            <Typography variant="h4" sx={{ marginBottom: '10px' }}>
              Please select a decomposition model
            </Typography>
            <Box sx={{ position: 'relative' }}>
              <Select value={selectedModelType} onChange={handleChangeModelType} displayEmpty sx={{ width: '100%' }}>
                <MenuItem value="" disabled>
                  Select Model Type
                </MenuItem>
                {models.map((model) => (
                  <MenuItem key={model.value} value={model.value}>
                    {model.label}
                  </MenuItem>
                ))}
              </Select>
              {selectedModelType && (
                <Tooltip
                  title={models.find((model) => model.value === selectedModelType).description}
                  placement="right"
                  arrow
                  open={showModelDescription || isTooltipHovered}
                  onOpen={() => setShowModelDescription(true)}
                  onClose={() => setShowModelDescription(false)}
                  PopperProps={{
                    disablePortal: true,
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
    </Grid>

          {isLoading && (
            
              <SkeletonEarningCard/>
           
          )}

          {error && (
            <Typography variant="body1" color="error" sx={{ marginTop: '10px' }}>
              {error}
            </Typography>
          )}

          {decompositionData && selectedColumn && selectedModelType && !isLoading && !error && (
            <Grid container spacing={gridSpacing}>
  
            <Grid item lg={12} md={12} sm={12} xs={12} >
             
                  <h3>Observed Data</h3>
                  <div className="heatmap-container">
                  <Plot
                    data={[getLineChartData('Observed')]}
                    layout={{
                      title: 'Data Evolution',
                      xaxis: { title: 'Date' },
                      yaxis: { title: 'Value' },
                      width:1000,
                      height:400
                    }}
                    config={{
                      displayModeBar: false, // Display the mode bar (including zoom, pan, etc.)
                      displaylogo: false, // Display the Plotly logo
                      responsive: true, // Enable responsiveness to adjust the chart size with window resize
                    }}
                  />
                  </div>
            
               </Grid>
               <Grid item lg={12} md={12} sm={12} xs={12} >
               
                  
                    <h3> Trend Component</h3>
                    <div className="heatmap-container">
                    <Plot
                      data={[getLineChartData('Trend')]}
                      layout={{
                        title: 'Trend',
                        xaxis: { title: 'Date' },
                        yaxis: { title: 'Value' },
                        width:1000,
                        height:400
                      }}
                      config={{
                        displayModeBar: false, // Display the mode bar (including zoom, pan, etc.)
                        displaylogo: false, // Display the Plotly logo
                        responsive: true, // Enable responsiveness to adjust the chart size with window resize
                      }}
                    />
                 </div>
             </Grid>

             <Grid item lg={12} md={12} sm={12} xs={12} >

                    <h3>Seasonal Component</h3>
                    <div className="heatmap-container">
                    <Plot
                      data={[getLineChartData('Seasonal')]}
                      layout={{
                        title: 'Seasonal',
                        xaxis: { title: 'Date' },
                        yaxis: { title: 'Value' },
                        width:1000,
                        height:400
                      }}
                      config={{
                        displayModeBar: false, // Display the mode bar (including zoom, pan, etc.)
                        displaylogo: false, // Display the Plotly logo
                        responsive: true, // Enable responsiveness to adjust the chart size with window resize
                      }}
                    />
                </div>
              </Grid>

              <Grid item lg={12} md={12} sm={12} xs={12} >
                   
                   
                    <h3>Residual Component </h3>
                    <div className="heatmap-container">
                    <Plot
                      data={[getLineChartData('Residual')]}
                      layout={{
                        title: 'Residual',
                        xaxis: { title: 'Date' },
                        yaxis: { title: 'Value' },
                        width:1000,
                        height:400
                      }}
                      config={{
                        displayModeBar: false, // Display the mode bar (including zoom, pan, etc.)
                        displaylogo: false, // Display the Plotly logo
                        responsive: true, // Enable responsiveness to adjust the chart size with window resize
                      }}
                    />
                   </div>
              </Grid>
           
            </Grid>
          )}
       </MainCard>
</Grid>
        
      </Grid>
  );
};

export default Decomposition;
