import React, { useState, useEffect } from 'react';
import { Select, MenuItem, Typography, Grid } from '@mui/material';
import axios from 'axios';
import MissingValuesCard from './MissingValuesCard';
import OutliersCard from './OutliersCard';
import DataTypesCard from './DataTypesCard';
import UniqueValuesCard from './UniqueValuesCard';
import NegativeValuesCard from './NegativeValuesCard';
import ZeroValuesCard from './ZeroValuesCard';
import BoxPlot from './BoxPlot';
import LinePlot from './LinePlot';
import Histogram from './Histogram';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import { StepLabel } from '@mui/material';
import { updateVersion, updateUpdated } from 'actions/actions';
import { useSelector, useDispatch } from 'react-redux';
import SkeletonEarningCard from 'ui-component/cards/Skeleton/EarningCard';
import MainCard from 'ui-component/cards/MainCard';
import { gridSpacing } from 'store/constant';

const columns = [
  {
    accessorKey: 'Electricity',
    header: 'Electricity',
    size: 150
  },
  {
    accessorKey: 'Gas_01', //normal accessorKey
    header: 'Gas_01',
    size: 150
  },
  {
    accessorKey: 'Gas_02', //normal accessorKey
    header: 'Gas_02',
    size: 150
  },
  {
    accessorKey: 'Gas_03', //normal accessorKey
    header: 'Gas_03',
    size: 150
  },
  {
    accessorKey: 'Day_Degree_Cold', //normal accessorKey
    header: 'Day_Degree_Cold',
    size: 150
  },
  {
    accessorKey: 'Day_Degree_Hot',
    header: 'Day_Degree_Hot',
    size: 150
  },
  {
    accessorKey: 'Min_OutdoorTemp',
    header: 'Min_OutdoorTemp',
    size: 150
  },
  {
    accessorKey: 'Average_OutdoorTemp',
    header: 'Average_OutdoorTemp',
    size: 150
  },
  {
    accessorKey: 'Max_OutdoorTemp',
    header: 'Max_OutdoorTemp',
    size: 150
  },
  {
    accessorKey: 'Maximum_Humidity',
    header: 'Maximum_Humidity',
    size: 150
  },
  {
    accessorKey: 'Average_Humidity',
    header: 'Average_Humidity',
    size: 150
  },
  {
    accessorKey: 'Solar_Radiation',
    header: 'Solar_Radiation',
    size: 150
  },
  {
    accessorKey: 'Hour',
    header: 'Hour',
    size: 150
  },
  {
    accessorKey: 'Day',
    header: 'Day',
    size: 150
  },
  {
    accessorKey: 'Week',
    header: 'Week',
    size: 150
  },
  {
    accessorKey: 'Month',
    header: 'Month',
    size: 150
  },
  {
    accessorKey: 'Year',
    header: 'Year',
    size: 150
  }
];

const SingleColumnProfiling = () => {
  const handleUpdateUpdated = (newValue) => {
    return new Promise((resolve) => {
      dispatch(updateUpdated(newValue));

      resolve();
    });
  };
  const updated = useSelector((state) => state.updated);
  const dispatch = useDispatch();
  const version = useSelector((state) => state.version);
  const handleUpdateVersion = (newValue) => {
    return new Promise((resolve) => {
      dispatch(updateVersion(newValue));
      setVal(newValue);
      resolve();
    });
  };

  const [version_number, setVersionNumber] = useState(0);
  const [val, setVal] = useState(version.version ? version.version : 0);
  const [selectedColumn, setSelectedColumn] = useState('');
  const [activeStep, setActiveStep] = useState(val == -1 ? 2 : val);
  const [missingValues, setMissingValues] = useState(null);
  const [outliers, setOutliers] = useState(null);
  const [dataTypes, setDataTypes] = useState(null);
  const [uniqueValues, setUniqueValues] = useState(null);
  const [negativeValues, setNegativeValues] = useState(null);
  const [zeroValues, setZeroValues] = useState(null);
  const [isLoadingVersion, setIsLoadingVersion] = useState(true);
  const [isLoadingData, setIsLoadingData] = useState(false);
  const [updatedVersions, setUpdatedVersion] = useState([]);
  const [previousPercentageMissingValues, setPreviousPercentageMissingValues] = useState(null);
  const [previousPercentageOutliers, setPreviousPercentageOutliers] = useState(null);
  const [previousPercentageUniqueValues, setPreviousPercentageUniqueValues] = useState(null);
  const [previousPercentageNegativeValues, setPreviousPercentageNegativeValues] = useState(null);
  const [previousPercentageZeroValues, setPreviousPercentageZeroValues] = useState(null);
  const [plotData, setPlotData] = useState(null);
  const baseURL = `http://localhost:8000/api/single_column_profiling/${val}/${updated.updated}/`;
  const handleChangeColumn = (event) => {
    setSelectedColumn(event.target.value);
  };

  const handleStepClick = (step, all) => {
    handleUpdateUpdated('False');
    setActiveStep(step);
    if (version !== step) {
      handleUpdateVersion(all === 1 ? -1 : step);
    }
  };
  const handleStepClick2 = (step, all) => {
    handleUpdateUpdated('True');
    setActiveStep(step);
    if (version !== step) {
      handleUpdateVersion(all === 1 ? -1 : step);
    }
  };

  const fetchPreviousPercentage = async () => {
    console.log(val);
    const previousVersion = parseInt(val) - 1;
    const url = `http://localhost:8000/api/single_column_profiling/${previousVersion}/${updated.updated}/`;

    axios.get(`${url}${selectedColumn}`).then((response) => {
      const result = JSON.parse(response.data);
      console.log(result);
      setPreviousPercentageMissingValues(result.missing_values ? result.missing_values : 0);
      setPreviousPercentageOutliers(result.outlires ? result.outlires : 0);
      setPreviousPercentageUniqueValues(result.unique ? result.unique : 0);
      setPreviousPercentageNegativeValues(result.negativeValues ? result.negativeValues : 0);
      setPreviousPercentageZeroValues(result.zero_values ? result.zero_values : 0);
    });
  };

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/initial_profiling').then((response) => {
      const result = JSON.parse(response.data);
      setVersionNumber(result.versions_number ? result.versions_number : 0);
      setUpdatedVersion(result.updated_version ? JSON.parse(result.updated_version) : []);
      setIsLoadingVersion(false);
    });
  }, []);
  useEffect(() => {
    console.log(val);
    const fetchColumnData = async () => {
      if (!selectedColumn) {
        return;
      }

      setIsLoadingData(true);

      if (parseInt(val) !== 0 && parseInt(val) !== -1) {
        fetchPreviousPercentage();
      } else {
        setPreviousPercentageMissingValues(null);
        setPreviousPercentageOutliers(null);
        setPreviousPercentageUniqueValues(null);
        setPreviousPercentageNegativeValues(null);
        setPreviousPercentageZeroValues(null);
      }

      const url = `${baseURL}${selectedColumn}`;

      axios.get(`${url}`).then((response) => {
        const result = JSON.parse(response.data);
        console.log(result);
        setVersionNumber(result.versions_number ? result.versions_number : 0);
        setUpdatedVersion(result.updated_version ? JSON.parse(result.updated_version) : []);
        setMissingValues(result.missing_values ? result.missing_values : 0);
        setOutliers(result.outlires ? result.outlires : 0);
        setDataTypes(result.type ? result.type : 0);
        setUniqueValues(result.unique ? result.unique : 0);
        setNegativeValues(result.negative_values ? result.negative_values : 0);
        setZeroValues(result.zero_values ? result.zero_values : 0);
        setPlotData(result.column_data ? result.column_data : 0);
        setIsLoadingData(false);
        setIsLoadingVersion(false);
      });
    };
    fetchColumnData();
  }, [selectedColumn, val, updated]);
  console.log(previousPercentageMissingValues)
  console.log(previousPercentageOutliers)
  return (
   
    <>
      <Grid container spacing={gridSpacing}>
        <Grid item lg={12} md={12} sm={12} xs={12}>
          <MainCard>
            <h3>Choose your data version </h3>
            {isLoadingVersion ? (
              <SkeletonEarningCard className="loading" />
            ) : (
              <>
                <Stepper nonLinear activeStep={updated.updated == 'False' ? activeStep : -1}>
                  {Array.from({ length: version_number }, (_, index) => (
                    <Step key={index}>
                      <StepLabel onClick={() => handleStepClick(index, 0)}>Version {index + 1}</StepLabel>
                    </Step>
                  ))}
                  {version_number >= 2 && (
                    <Step>
                      <StepLabel onClick={() => handleStepClick(parseInt(version_number), 1)}>All versions</StepLabel>
                    </Step>
                  )}
                </Stepper>
                {updatedVersions.length > 0 && (
                  <div>
                    <h3>Updated versions</h3>
                    <Stepper nonLinear activeStep={updated.updated == 'True' ? activeStep : -1} style={{ marginTop: '10px' }}>
                      {updatedVersions.map((vers, index) => (
                        <Step key={index}>
                          <StepLabel onClick={() => handleStepClick2(index, 0)}>Version {vers + 1}</StepLabel>
                        </Step>
                      ))}
                      {updatedVersions.length >= 2 && (
                        <Step>
                          <StepLabel onClick={() => handleStepClick2(parseInt(version_number), 1)}>All versions</StepLabel>
                        </Step>
                      )}
                    </Stepper>
                  </div>
                )}{' '}
              </>
            )}
          </MainCard>
        </Grid>
        <Grid item lg={12} md={12} sm={12} xs={12}>
          <MainCard>
            <Typography variant="h4" sx={{ marginBottom: '10px' }}>
              Please select a column
            </Typography>
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
          </MainCard>
        </Grid>
        <Grid item lg={12} md={12} sm={12} xs={12}>
          {isLoadingData ? ( 
            <>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6} md={4}>
                  <SkeletonEarningCard />
                </Grid>
                <Grid item xs={12} sm={6} md={4}>
                  <SkeletonEarningCard />
                </Grid>
                <Grid item xs={12} sm={6} md={4}>
                  <SkeletonEarningCard />
                </Grid>
                <Grid item xs={12} sm={6} md={4}>
                  <SkeletonEarningCard />
                </Grid>
                <Grid item xs={12} sm={6} md={4}>
                  <SkeletonEarningCard />
                </Grid>
                <Grid item xs={12} sm={6} md={4}>
                  <SkeletonEarningCard />
                </Grid>
              </Grid>
            </>
          ) : (
            // If isLoadingData is false, render the actual cards with data
            <>
              <Grid item lg={12} md={12} sm={12} xs={12}>
                {selectedColumn && (missingValues || outliers || dataTypes || uniqueValues || negativeValues || zeroValues || plotData) && (
                  <Grid container spacing={2}>
                    {selectedColumn && missingValues && (
                      <Grid item xs={12} sm={6} md={4}>
                        <MissingValuesCard missingValues={missingValues} previousPercentage={previousPercentageMissingValues} />
                      </Grid>
                    )}

                    {selectedColumn && outliers && (
                      <Grid item xs={12} sm={6} md={4}>
                        <OutliersCard outliers={outliers} previousPercentage={previousPercentageOutliers} />
                      </Grid>
                    )}

                    {selectedColumn && dataTypes && (
                      <Grid item xs={12} sm={6} md={4}>
                        <DataTypesCard dataTypes={dataTypes} />
                      </Grid>
                    )}

                    {selectedColumn && uniqueValues && (
                      <Grid item xs={12} sm={6} md={4}>
                        <UniqueValuesCard uniqueValues={uniqueValues} uniqueValuesPercentage={previousPercentageUniqueValues} />
                      </Grid>
                    )}

                    {selectedColumn && negativeValues && (
                      <Grid item xs={12} sm={6} md={4}>
                        <NegativeValuesCard negativeValues={negativeValues} negativeValuesPercentage={previousPercentageNegativeValues} />
                      </Grid>
                    )}

                    {selectedColumn && zeroValues && (
                      <Grid item xs={12} sm={6} md={4}>
                        <ZeroValuesCard zeroValues={zeroValues} zeroValuesPercentage={previousPercentageZeroValues} />
                      </Grid>
                    )}

                    {selectedColumn && plotData && (
                      <Grid item xs={12}>
                        <BoxPlot plotData={plotData} column={selectedColumn} />
                      </Grid>
                    )}

                    {selectedColumn && plotData && (
                      <Grid item xs={12}>
                        <LinePlot plotData={plotData} column={selectedColumn} />
                      </Grid>
                    )}

                    {selectedColumn && plotData && (
                      <Grid item xs={12}>
                        <Histogram plotData={plotData} column={selectedColumn} />
                      </Grid>
                    )}
                  </Grid>
                )}
              </Grid>
            </>
          )}
        </Grid>
      </Grid>
    </>
  );
};

export default SingleColumnProfiling;
