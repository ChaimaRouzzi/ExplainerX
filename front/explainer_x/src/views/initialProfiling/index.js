import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import { StepLabel } from '@mui/material';
import { updateVersion, updateUpdated } from 'actions/actions';
import { useSelector, useDispatch } from 'react-redux';
import MainCard from 'ui-component/cards/MainCard';
import SkeletonEarningCard from 'ui-component/cards/Skeleton/EarningCard';
import axios from 'axios';
import { Grid } from '@mui/material';
import { gridSpacing } from 'store/constant';
import React, { useState, useEffect } from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
// ==============================|| SAMPLE PAGE ||============================== //

const InitialProfiling = () => {
  const dispatch = useDispatch();
  const version = useSelector((state) => state.version);
  const handleUpdateVersion = (newValue) => {
    return new Promise((resolve) => {
      dispatch(updateVersion(newValue));
      setVal(newValue);
      resolve();
    });
  };
  const updated = useSelector((state) => state.updated);
  const handleUpdateUpdated = (newValue) => {
    return new Promise((resolve) => {
      dispatch(updateUpdated(newValue));
      resolve();
    });
  };
  const data = [
    { column: 'date', type: 'Date', description: 'the timestamp each record', owner: 'A hospital in Malaga, Spain' },
    { column: 'Gas_02', type: 'Float', description: 'Gas consumption of boiler Number 02', owner: 'A hospital in Malaga, Spain' },
    { column: 'Gas_01', type: 'Float', description: 'Gas consumption of boiler Number 01', owner: 'A hospital in Malaga, Spain' },
    { column: 'Gas_03', type: 'Float', description: 'Gas consumption of boiler Number 03', owner: 'A hospital in Malaga, Spain' },
    { column: 'Electricity', type: 'Float', description: 'Electricity consumption', owner: 'A hospital in Malaga, Spain' },
    { column: 'Average_Humidity', type: 'Float', description: 'Average outdoor humidity', owner: 'A hospital in Malaga, Spain' },
    { column: 'Maximum_Humidity', type: 'Float', description: 'Maximum outdoor humidity', owner: 'A hospital in Malaga, Spain' },
    { column: 'Solar_Radiation', type: 'Float', description: 'Solar radiation', owner: 'A hospital in Malaga, Spain' },
    {
      column: 'Day_Degree_Cold',
      type: 'Float',
      description: 'Difference between the exterior temperature and 18°C',
      owner: 'A hospital in Malaga, Spain'
    },
    {
      column: 'Day_Degree_Hot',
      type: 'Float',
      description: 'Difference between the exterior temperature and 23°C',
      owner: 'A hospital in Malaga, Spain'
    },
    { column: 'Min_OutdoorTemp', type: 'Float', description: 'Minimum outdoor temperature', owner: 'A hospital in Malaga, Spain' },
    { column: 'Average_OutdoorTemp', type: 'Float', description: 'Average outdoor temperature', owner: 'A hospital in Malaga, Spain' },
    { column: 'Max_OutdoorTemp', type: 'Float', description: 'Maximum outdoor temperature', owner: 'A hospital in Malaga, Spain' },
    { column: 'Hour', type: 'Integer', description: 'The hour of each record', owner: 'A hospital in Malaga, Spain' },
    { column: 'Day', type: 'Integer', description: 'The day of each record', owner: 'A hospital in Malaga, Spain' },
    { column: 'Week', type: 'Integer', description: 'The week of each record', owner: 'A hospital in Malaga, Spain' },
    { column: 'Month', type: 'Integer', description: 'The month of each record', owner: 'A hospital in Malaga, Spain' },
    { column: 'Year', type: 'Integer', description: 'The year of each record', owner: 'A hospital in Malaga, Spain' }
  ];
  const [updatedVersions, setUpdatedVersion] = useState([]);
  const [val, setVal] = useState(version.version ? version.version : 0);
  const BaseURL = `http://127.0.0.1:8000/api/initial_profiling`;
  const [isLoading, setLoading] = useState(true);
  const [version_number, setVersionNumber] = useState(0);
  const [activeStep, setActiveStep] = useState(val == -1 ? 2 : val);
  const handleStepClick = (step, all) => {
    handleUpdateUpdated('False');
    setActiveStep(step);
    if (version !== step) {
      handleUpdateVersion(all === 1 ? -1 : step)
    } else {
      // Handle logic when version is already equal to step
    }
  };
  const handleStepClick2 = (step, all) => {
    handleUpdateUpdated('True');
    setActiveStep(step);
    if (version !== step) {
      handleUpdateVersion(all === 1 ? -1 : step)
    } else {
      // Handle logic when version is already equal to step
    }
  };

  useEffect(() => {
    axios.get(BaseURL).then((response) => {
      const result = JSON.parse(response.data);
      console.log(result);
      setVersionNumber(result.versions_number ? result.versions_number : 0);
      setUpdatedVersion(result.updated_version ? JSON.parse(result.updated_version) : []);
      setLoading(false);
    });
  }, []);
  return (
    <>
      <Grid container spacing={gridSpacing}>
        <Grid item xs={12}>
          <Grid container spacing={gridSpacing}>
          <Grid item lg={12} md={12} sm={12} xs={12}>
              <MainCard>
                <h3>Choose your data version </h3>
                {isLoading ? (
                  <SkeletonEarningCard />
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
                    )}
                  </>
                )}
              </MainCard>
            </Grid>
            <Grid item lg={12} md={12} sm={12} xs={12}>
              <MainCard>
                <h3> Dataset Description </h3>
                <p>
                  {' '}
                  The dataset comprises hourly energy consumption values and meteorological data received from a hospital located in Malaga,
                  Spain. It consists of 18 columns, which will be described in the following section.
                </p>
              </MainCard>
            </Grid>
            <Grid item lg={12} md={12} sm={12} xs={12}>
              <MainCard>
                <h3> Dataset Columns Description </h3>
                {isLoading ? (
                  <SkeletonEarningCard />
                ) : (
                  <TableContainer component={Paper}>
                    <Table aria-label="simple table">
                      <TableHead>
                        <TableRow>
                          <TableCell style={{ fontWeight: 'bold' }}>Column Name </TableCell>
                          <TableCell style={{ fontWeight: 'bold' }}>Column Type</TableCell>
                          <TableCell style={{ fontWeight: 'bold' }}>Column Description</TableCell>
                          <TableCell style={{ fontWeight: 'bold' }}>Column Owner</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {data.map((row, index) => (
                          <TableRow key={index} style={{ textAlign: 'center' }}>
                            <TableCell align="left">{row.column}</TableCell>
                            <TableCell align="left">{row.type}</TableCell>
                            <TableCell align="left">{row.description}</TableCell>
                            <TableCell align="left">{row.owner}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                )}
              </MainCard>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </>
  );
};

export default InitialProfiling;
