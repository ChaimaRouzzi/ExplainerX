import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Select, MenuItem, Typography, Box, Tooltip, IconButton, Grid } from '@mui/material';
import MuiAlert from '@mui/material/Alert';
import { gridSpacing } from 'store/constant';
import SkeletonEarningCard from 'ui-component/cards/Skeleton/EarningCard';
import InfoIcon from '@mui/icons-material/Info';
import MainCard from 'ui-component/cards/MainCard';

const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});
const StationarityTest = ({ ver, updated }) => {
  const baseURL = `http://localhost:8000/api/time_series_analysis/${updated.updated}/`;
  console.log(ver);
  const [selectedColumn, setSelectedColumn] = useState('');
  const [selectedMethod, setSelectedMethod] = useState('');
  const [stationarityData, setStationarityData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isTooltipHovered, setIsTooltipHovered] = useState(false);
  const handleChangeColumn = (event) => {
    setSelectedColumn(event.target.value);
  };

  const handleChangeMethod = (event) => {
    setSelectedMethod(event.target.value);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (selectedColumn && selectedMethod) {
          setIsLoading(true);
          const endpoint = `${baseURL}${selectedMethod}/?column_name=${selectedColumn}&version=${ver}`;
          const response = await axios.get(endpoint);
          setStationarityData(response.data);
          console.log(response.data);
          setIsLoading(false);
        }
      } catch (error) {
        console.log('Error fetching stationarity data:', error);
        setIsLoading(false);
      }
    };

    fetchData();
  }, [selectedColumn, selectedMethod, ver]);

  const columns = [
    {
      accessorKey: 'Electricity',
      header: 'Electricity',
      size: 150
    },
    {
      accessorKey: 'Gas_01',
      header: 'Gas_01',
      size: 150
    },
    {
      accessorKey: 'Gas_02',
      header: 'Gas_02',
      size: 150
    },
    {
      accessorKey: 'Gas_03',
      header: 'Gas_03',
      size: 150
    }
  ];

  const methods = [
    {
      value: 'stationarity_adftest',
      label: 'ADF Test',
      description:
        'The Augmented Dickey-Fuller (ADF) test is used to test for stationarity in a time series. It assesses whether the data has a unit root, which indicates non-stationarity. The test returns a test statistic and critical values, along with a p-value for hypothesis testing.',
      statisticKey: 'ADF Statistic',
      pValueKey: 'p-value',
      criticalValuesKey: 'Critical Values'
    },
    {
      value: 'stationarity_kpsstest',
      label: 'KPSS Test',
      description:
        'The Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test is used to test for stationarity in a time series. It tests the null hypothesis of stationarity against the alternative of a unit root. The test returns a test statistic and critical values, along with a p-value for hypothesis testing.',
      statisticKey: 'KPSS Statistic',
      pValueKey: 'p-value',
      criticalValuesKey: 'Critical Values'
    },
    {
      value: 'stationarity_pptest',
      label: 'PP Test',
      description:
        'The Phillips-Perron (PP) test is used to test for stationarity in a time series. It is a modification of the ADF test and accounts for autocorrelation and heteroscedasticity. The test returns a test statistic and critical values, along with a p-value for hypothesis testing.',
      statisticKey: 'PP Statistic',
      pValueKey: 'p-value',
      criticalValuesKey: 'Critical Values'
    }
  ];

  const renderStationarityStatus = () => {
    if (stationarityData && selectedMethod) {
      const { Stationarity } = stationarityData;
      if (Stationarity === 'Stationary') {
        const { Reason } = stationarityData;
        return (
          <>
            <Alert sx={{ color: '#fff', borderRadius: '0px' }} severity="success">
              The {selectedColumn} time series is Stationary!
            </Alert>

            {Reason && (
              <Typography variant="body1" gutterBottom>
                Reason: {Reason}
              </Typography>
            )}
          </>
        );
      } else if (Stationarity === 'Non-Stationary') {
        return (
          <>
            <Alert sx={{ color: '#fff', borderRadius: '0px' }} severity="error">
              The {selectedColumn} time series is Non-Stationary!
            </Alert>
          </>
        );
      }
    }
    return null;
  };

  const handleTooltipHover = (isHovered) => {
    setIsTooltipHovered(isHovered);
  };

  const getStatisticValue = (key) => {
    const value = stationarityData && stationarityData[key];
    return value !== undefined ? value : '-';
  };

  const renderCriticalValues = () => {
    const criticalValues =
      stationarityData && stationarityData[methods.find((method) => method.value === selectedMethod).criticalValuesKey];
    if (criticalValues) {
      return (
        <>
          <h4 style={{ color: '#004aad', textAlign: 'center' }}> Critical Values</h4>
          <ul className="list-itm">
            {Object.entries(criticalValues).map(([key, value]) => (
              <li key={key}>
                {key}: {value}
              </li>
            ))}
          </ul>
        </>
      );
    }
    return null;
  };

  return (
    <>
      <Grid container spacing={gridSpacing}>
        <Grid item lg={12} md={12} sm={12} xs={12}>
          <MainCard>
            <Grid container spacing={2} style={{ alignItems: 'center' }}>
              <Grid item lg={5} md={5} sm={12} xs={12} style={{ marginLeft: '50px' }}>
                <Typography variant="h4"></Typography>
                <h3 style={{ marginBottom: '10px' }}> Please select a column </h3>
                <Select
                  value={selectedColumn}
                  onChange={handleChangeColumn}
                  displayEmpty
                  renderValue={(value) => (value ? value : 'Column')}
                  sx={{ width: '100%' }}
                >
                  <MenuItem value="" disabled>
                    Select Column
                  </MenuItem>
                  {columns.map((column) => (
                    <MenuItem key={column.accessorKey} value={column.accessorKey}>
                      {column.header}
                    </MenuItem>
                  ))}
                </Select>
              </Grid>
              <Grid item lg={5} md={5} sm={12} xs={12} style={{ marginLeft: '50px' }}>
                <h3 style={{ marginBottom: '10px' }}> Please select a stationarity method </h3>
                <Box sx={{ position: 'relative' }}>
                  <Select
                    value={selectedMethod}
                    onChange={handleChangeMethod}
                    displayEmpty
                    renderValue={(value) => (value ? methods.find((method) => method.value === value).label : 'Stationary Method')}
                    sx={{ width: '100%' }}
                  >
                    <MenuItem value="" disabled>
                      Select Method
                    </MenuItem>
                    {methods.map((method) => (
                      <MenuItem key={method.value} value={method.value}>
                        {method.label}
                      </MenuItem>
                    ))}
                  </Select>
                  {selectedMethod && (
                    <Tooltip
                      title={methods.find((method) => method.value === selectedMethod).description}
                      placement="right"
                      arrow
                      open={isTooltipHovered}
                      PopperProps={{
                        disablePortal: true
                      }}
                      enterDelay={500}
                      enterTouchDelay={0}
                      leaveTouchDelay={200}
                      onMouseEnter={() => handleTooltipHover(true)}
                      onMouseLeave={() => handleTooltipHover(false)}
                    >
                      <IconButton
                        sx={{ position: 'absolute', top: '50%', right: 'épx', transform: 'translateY(-50%)' }}
                        onClick={handleTooltipHover}
                      >
                        <InfoIcon />
                      </IconButton>
                    </Tooltip>
                  )}
                </Box>
              </Grid>
            </Grid>

            {isLoading && <SkeletonEarningCard />}

            {selectedColumn && selectedMethod && !isLoading && (
              <Box mt={3}>
                {stationarityData && (
                  <>
                    {renderStationarityStatus()}

                    <Grid container spacing={2} style={{ alignItems: 'center', marginTop: '10px' }}>
                      <Grid item lg={3} md={3} sm={12} xs={12} style={{ marginLeft: '50px' }}>
                        <MainCard className="shadow">
                          <h4 style={{ color: '#004aad', textAlign: 'center' }}>
                            {' '}
                            {methods.find((method) => method.value === selectedMethod).statisticKey}:{' '}
                          </h4>
                          {getStatisticValue(methods.find((method) => method.value === selectedMethod).statisticKey)}
                        </MainCard>
                      </Grid>
                      <Grid item lg={3} md={3} sm={12} xs={12} style={{ marginLeft: '50px' }}>
                        <MainCard className="shadow">
                          <h4 style={{ color: '#004aad', textAlign: 'center' }}>
                            {' '}
                            {methods.find((method) => method.value === selectedMethod).pValueKey}:{' '}
                          </h4>
                          {getStatisticValue(methods.find((method) => method.value === selectedMethod).pValueKey)}
                        </MainCard>
                      </Grid>
                      <Grid item lg={3} md={3} sm={12} xs={12} style={{ marginLeft: '50px' }}>
                        <MainCard className="shadow">{renderCriticalValues()}</MainCard>
                      </Grid>
                    </Grid>
                  </>
                )}
              </Box>
            )}
          </MainCard>
        </Grid>
      </Grid>
    </>
  );
};

export default StationarityTest;
