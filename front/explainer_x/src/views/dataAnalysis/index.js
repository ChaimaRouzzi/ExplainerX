import React, { useEffect, useState, useMemo } from 'react';
import DisplayData from './DisplayData';
import axios from 'axios';
import { Grid } from '@mui/material';
import { gridSpacing } from 'store/constant';
import MainCard from 'ui-component/cards/MainCard';
import RowsNumber from './RowsNumber';
import ColumnsNumber from './ColumnsNumber';
import OutliersCard from './Outlires';
import NegativeValuesCard from './NegativesValues';
import UniqueValuesCard from './DuplicatesValues';

import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import { StepLabel } from '@mui/material';
import { updateVersion, updateUpdated } from 'actions/actions';
import { useSelector, useDispatch } from 'react-redux';
import TimelineComponent from './TimelineComponent';
import VersionsPlot from './VersionsPlot';
import SkeletonEarningCard from 'ui-component/cards/Skeleton/EarningCard';
import ColumnsPlot from './ColumnsPlot';
import ColumnsMemory from './ColumnsMemory';
import MissingValuesCard from './MissingValues';
const DataAnalysis = () => {
  const dispatch = useDispatch();

  const version = useSelector((state) => state.version);
  const updated = useSelector((state) => state.updated);
  const [val, setVal] = useState(version.version ? version.version : 0);


  const handleUpdateVersion = (newValue) => {
    return new Promise((resolve) => {
      dispatch(updateVersion(newValue));
      setVal(newValue);
      resolve();
    });
  };

  const handleUpdateUpdated = (newValue) => {
    return new Promise((resolve) => {
      dispatch(updateUpdated(newValue));

      resolve();
    });
  };
  // Replace with your desired version

  const BaseURL = `http://127.0.0.1:8000/api/data_analysis/${val}/${updated.updated}`;
  const [isLoading, setLoading] = useState(true);
  const [isLoadingVersion, setIsLoadingVersion] = useState(true);
  const [dataset, setDataset] = useState([]);
  const [rowsNumber, setRowsNumber] = useState(0);
  const [columnsNumber, setColumnsNumber] = useState(0);
  const [missingValues, SetMissingValues] = useState(0);
  const [outlires, setOutlires] = useState(0);
  const [negative, setNegative] = useState(0);
  const [duplicates, setDuplicates] = useState(0);
  const [timelineDta, setTimelineData] = useState(0);
  const [activeStep, setActiveStep] = useState(val == -1 ? 2 : val);
  const [version_number, setVersionNumber] = useState(0);
  const [updatedVersions, setUpdatedVersion] = useState([]);
  const [labels, setLabels] = useState([]);
  const [labelsColumns, setLabelsColumns] = useState([]);
  const [labelsOutlires, setLabelsOutlires] = useState([]);
  const [labelsMemory, setLabelsMemory] = useState([]);
  const handleStepClick = (step, all) => {
    console.log(updated);
    handleUpdateUpdated('False');
    setActiveStep(step);
    if (version !== step) {
      handleUpdateVersion(all === 1 ? -1 : step).then(() => {
        setLoading(true);
        const updatedVal = all == 1 ? -1 : step;
        const updatedURL = `http://127.0.0.1:8000/api/data_analysis/${updatedVal}/False`;
        axios
          .get(updatedURL)
          .then((response) => {
            const result = JSON.parse(response.data);
            console.log(result);
            setDataset(result.data ? JSON.parse(result.data) : []);
            setRowsNumber(result.rows ? result.rows : 0);
            setColumnsNumber(result.columns ? result.columns : 0);
            SetMissingValues(result.missing_values ? JSON.parse(result.missing_values) : 0);
            setDuplicates(result.duplicate ? JSON.parse(result.duplicate) : 0);
            setNegative(result.negative ? JSON.parse(result.negative) : 0);
            setOutlires(result.outlires ? JSON.parse(result.outlires) : 0);
            setVersionNumber(result.versions_number ? result.versions_number : 0);
            setTimelineData(result.timeline_data ? JSON.parse(result.timeline_data) : []);
            setLabels(result.version_data ? JSON.parse(result.version_data) : []);
            setLabelsColumns(result.missing_values_columns ? JSON.parse(result.missing_values_columns) : []);
            setLabelsOutlires(result.outlires_columns ? JSON.parse(result.outlires_columns) : []);
            setLabelsMemory(result.column_memory ? JSON.parse(result.column_memory) : []);
            setUpdatedVersion(result.updated_version ? JSON.parse(result.updated_version) : []);
            setLoading(false);
            setIsLoadingVersion(false);
          })
          .catch((error) => {
            console.log(error);
            setLoading(false);
            setIsLoadingVersion(false);
          });
      });
    } else {
      // Handle logic when version is already equal to step
    }
  };

  const handleStepClick2 = (step, all) => {
    handleUpdateUpdated('True');

    setActiveStep(step);
    console.log(updated);
    if (version !== step) {
      handleUpdateVersion(all === 1 ? -1 : step).then(() => {
        setLoading(true);
        const updatedVal = all == 1 ? -1 : step;
        const updatedURL = `http://127.0.0.1:8000/api/data_analysis/${updatedVal}/True`;
        axios
          .get(updatedURL)
          .then((response) => {
            const result = JSON.parse(response.data);
            console.log(result);
            setDataset(result.data ? JSON.parse(result.data) : []);
            setRowsNumber(result.rows ? result.rows : 0);
            setColumnsNumber(result.columns ? result.columns : 0);
            SetMissingValues(result.missing_values ? JSON.parse(result.missing_values) : 0);
            setDuplicates(result.duplicate ? JSON.parse(result.duplicate) : 0);
            setNegative(result.negative ? JSON.parse(result.negative) : 0);
            setOutlires(result.outlires ? JSON.parse(result.outlires) : 0);
            setVersionNumber(result.versions_number ? result.versions_number : 0);
            setTimelineData(result.timeline_data ? JSON.parse(result.timeline_data) : []);
            setLabels(result.version_data ? JSON.parse(result.version_data) : []);
            setLabelsColumns(result.missing_values_columns ? JSON.parse(result.missing_values_columns) : []);
            setLabelsOutlires(result.outlires_columns ? JSON.parse(result.outlires_columns) : []);
            setLabelsMemory(result.column_memory ? JSON.parse(result.column_memory) : []);
            setUpdatedVersion(result.updated_version ? JSON.parse(result.updated_version) : []);
            setLoading(false);
            setIsLoadingVersion(false);
          })
          .catch((error) => {
            console.log(error);
            setLoading(false);
            setIsLoadingVersion(false);
          });
      });
    } else {
      // Handle logic when version is already equal to step
    }
  };

  useEffect(() => {
    axios.get(BaseURL).then((response) => {
      const result = JSON.parse(response.data);
      console.log(result);
      setDataset(result.data ? JSON.parse(result.data) : 0);
      setRowsNumber(result.rows ? result.rows : 0);
      setColumnsNumber(result.columns ? result.columns : 0);
      SetMissingValues(result.missing_values ? JSON.parse(result.missing_values) : 0);
      setDuplicates(result.duplicate ? JSON.parse(result.duplicate) : 0);
      setNegative(result.negative ? JSON.parse(result.negative) : 0);
      setOutlires(result.outlires ? JSON.parse(result.outlires) : 0);
      setVersionNumber(result.versions_number ? result.versions_number : 0);
      setTimelineData(result.timeline_data ? JSON.parse(result.timeline_data) : []);
      setLabels(result.version_data ? JSON.parse(result.version_data) : []);
      setLabelsColumns(result.missing_values_columns ? JSON.parse(result.missing_values_columns) : []);
      setLabelsOutlires(result.outlires_columns ? JSON.parse(result.outlires_columns) : []);
      setLabelsMemory(result.column_memory ? JSON.parse(result.column_memory) : []);
      setUpdatedVersion(result.updated_version ? JSON.parse(result.updated_version) : []);
      console.log(updatedVersions);
      setLoading(false); 
      setIsLoadingVersion(false);
    });
  }, []);

  const columns = useMemo(
    () => [
      {
        accessorKey: 'date', //access nested data with dot notation
        header: 'Date',
        size: 150
      },
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
    ],
    []
  );

  return (
    <>
      <Grid container spacing={gridSpacing}>
        <Grid item xs={12}>
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
              <Grid container spacing={1} justifyContent="space-between">
                <Grid item xs={6}>
                  {isLoading && val != 0 ? <SkeletonEarningCard /> : <RowsNumber isLoading={isLoading} data={rowsNumber} />}
                </Grid>
                <Grid item xs={6}>
                  {isLoading && val != 0 ? <SkeletonEarningCard /> : <ColumnsNumber isLoading={isLoading} data={columnsNumber} />}
                </Grid>
              </Grid>
            </Grid>
            <Grid item lg={12} md={12} sm={12} xs={6}>
              <Grid container spacing={1} justifyContent="space-between">
                <Grid item xs={6}>
                  {isLoading ? <SkeletonEarningCard /> : <MissingValuesCard missingValues={missingValues} previousPercentage={null} />}
                </Grid>
                <Grid item xs={6}>
                  {isLoading ? <SkeletonEarningCard /> : <OutliersCard outliers={outlires} />}
                </Grid>
              </Grid>
            </Grid>
            <Grid item lg={12} md={12} sm={12} xs={6}>
              <Grid container spacing={1} justifyContent="space-between">
                <Grid item xs={6}>
                  {isLoading ? <SkeletonEarningCard /> : <NegativeValuesCard negativeValues={negative} />}
                </Grid>
                <Grid item xs={6}>
                  {isLoading ? <SkeletonEarningCard /> : <UniqueValuesCard duplicates={duplicates} />}
                </Grid>
              </Grid>
            </Grid>
            <Grid item lg={12} md={12} xs={12}>
              <MainCard>
                <h3>Data Versions Timeline: Evolution and Progression of Data Versions</h3>
                {isLoading ? <SkeletonEarningCard /> : <TimelineComponent timelineData={timelineDta} isLoading={isLoading} />}
              </MainCard>
            </Grid>
            <Grid item lg={12} md={12} sm={12} xs={6}>
              <Grid container spacing={1} justifyContent="space-between">
                <Grid item xs={6}>
                  <MainCard>
                    <h3>Data Version Distribution: Proportion of Rows in Each Version</h3>
                    <VersionsPlot data={labels} isLoading={isLoading} />
                  </MainCard>
                </Grid>
                <Grid item xs={6}>
                  <MainCard>
                    <h3> Column Memory Utilization: Percentage Distribution by Column </h3>
                    <ColumnsMemory data={labelsMemory} isLoading={isLoading} />
                  </MainCard>
                </Grid>
              </Grid>
            </Grid>
            <Grid item lg={12} md={12} xs={12}>
              <MainCard>
                <h3> Columns Missing Values and Outliers </h3>
                <ColumnsPlot data={labelsColumns} data2={labelsOutlires} isLoading={isLoading} />
              </MainCard>
            </Grid>
            <Grid item lg={12} md={12} xs={12}>
              <MainCard>
                <h3>Display Your Data </h3>
                <DisplayData isLoading={isLoading} data={dataset} columns={columns} />
              </MainCard>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </>
  );
};

export default DataAnalysis;
