import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import { StepLabel } from '@mui/material';
import { updateVersion, updateUpdated } from 'actions/actions';
import { useSelector, useDispatch } from 'react-redux';
import MainCard from 'ui-component/cards/MainCard';
import SkeletonEarningCard from 'ui-component/cards/Skeleton/EarningCard';
import axios from 'axios';
import { Grid, Box } from '@mui/material';
import { gridSpacing } from 'store/constant';
import React, { useState, useEffect } from 'react';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import InfoIcon from '@mui/icons-material/Info';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';

import { Select, MenuItem, Tooltip, IconButton } from '@mui/material';

const methods = [
  {
    value: 'Standard_Scaler',
    label: 'Standard Scaler',
    description:
      'In standard scaling, a feature is scaled by subtracting the mean from all the data points and dividing the resultant values by the standard deviation of the data.'
  },
  {
    value: 'Min-Max_Scaler',
    label: 'Min-Max Scaler ',
    description:
      'In this approach, the data is scaled to a fixed range - usually 0 to 1. The cost of having this bounded range - in contrast to standardization - is that we will end up with smaller standard deviations, which can suppress the effect of outliers.'
  },
  {
    value: 'Robust_Scaler',
    label: 'Robust Scaler ',
    description:
      'This Scaler removes the median and scales the data according to the quantile range (defaults to IQR: Interquartile Range). The IQR is the range between the 1st quartile (25th quantile) and the 3rd quartile (75th quantile).'
  }
];

const Deleting = () => {
  const [state, setState] = React.useState({
    open: false,
    vertical: 'top',
    horizontal: 'center'
  });
  const { vertical, horizontal, open } = state;

  const handleClick = (newState) => () => {
    setLoading2(true);
    const url = `http://127.0.0.1:8000/api/scaling/${val}/${updated.updated}/${selectedMethod}/${selectedColumn}`;

    axios.get(url).then((response) => {
      console.log(response);
      const url2 = `http://127.0.0.1:8000/api/check_duplecate/${val}/${updated.updated}`;
      axios.get(url2).then((response) => {
        const result = JSON.parse(response.data);
        setTthresholdColumns(result);
        console.log(result);
        setSelectedValue('');
        setState({ ...newState, open: true });
        setLoading2(false);
      });
    });
  };

  const handleClose = () => {
    setState({ ...state, open: false });
  };
  const updated = useSelector((state) => state.updated);
  const handleUpdateUpdated = (newValue) => {
    return new Promise((resolve) => {
      dispatch(updateUpdated(newValue));

      resolve();
    });
  };

  const dispatch = useDispatch();
  const version = useSelector((state) => state.version);
  const handleUpdateVersion = (newValue) => {
    return new Promise((resolve) => {
      dispatch(updateVersion(newValue));
      setVal(newValue);
      resolve();
    });
  };

  const [updatedVersions, setUpdatedVersion] = useState([]);
  const [val, setVal] = useState(version.version ? version.version : 0);
  const BaseURL = `http://127.0.0.1:8000/api/initial_profiling`;
  const [isLoading, setLoading] = useState(true);
  const [isLoading2, setLoading2] = useState(true);
  const [version_number, setVersionNumber] = useState(0);
  const [activeStep, setActiveStep] = useState(val == -1 ? 2 : val);
  const [selectedValue, setSelectedValue] = React.useState('');
  const [thresholdColumns, setTthresholdColumns] = React.useState([]);
  const [selectedMethod, setSelectedMethod] = useState('');
  const [isTooltipHovered, setIsTooltipHovered] = useState(false);
  const [selectedColumn, setSelectedColumn] = useState('');

  const handleTooltipHover = (isHovered) => {
    setIsTooltipHovered(isHovered);
  };

  const handleChangeMethod = (event) => {
    setSelectedMethod(event.target.value);
    console.log(event.target.value);
  };

  const handleStepClick = (step, all) => {
    handleUpdateUpdated('False');
    setActiveStep(step);
    if (version !== step) {
      handleUpdateVersion(all === 1 ? -1 : step).then(() => {
        setLoading(true);
        setLoading2(true);

        axios
          .get(BaseURL)
          .then((response) => {
            const result = JSON.parse(response.data);
            console.log(result);

            setVersionNumber(result.versions_number ? result.versions_number : 0);
            const url2 = `http://127.0.0.1:8000/api/check_duplecate/${val}/False`;
            axios.get(url2).then((response) => {
              const result = JSON.parse(response.data);
              setTthresholdColumns(result);
              console.log(result);
              setSelectedValue('');
              setLoading2(false);
            });
            setLoading(false);
          })
          .catch((error) => {
            console.log(error);
            setLoading(false);
          });
      });
    } else {
      // Handle logic when version is already equal to step
    }
  };
  const handleStepClick2 = (step, all) => {
    handleUpdateUpdated('True');
    setActiveStep(step);
    if (version !== step) {
      handleUpdateVersion(all === 1 ? -1 : step).then(() => {
        setLoading(true);
        setLoading2(true);

        axios
          .get(BaseURL)
          .then((response) => {
            const result = JSON.parse(response.data);
            console.log(result);

            setVersionNumber(result.versions_number ? result.versions_number : 0);
            setUpdatedVersion(result.updated_version ? JSON.parse(result.updated_version) : []);
            const url2 = `http://127.0.0.1:8000/api/check_duplecate/${val}/True`;
            axios.get(url2).then((response) => {
              const result = JSON.parse(response.data);
              setTthresholdColumns(result);
              setSelectedValue('');
              setLoading2(false);
            });
            setLoading(false);
          })
          .catch((error) => {
            console.log(error);
            setLoading(false);
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
      setVersionNumber(result.versions_number ? result.versions_number : 0);
      setUpdatedVersion(result.updated_version ? JSON.parse(result.updated_version) : []);
    });

    const url = `http://127.0.0.1:8000/api/check_duplecate/${val}/${updated.updated}`;

    axios.get(url).then((response) => {
      const result = JSON.parse(response.data);
      setTthresholdColumns(result);
      console.log(result);
      console.log(thresholdColumns);
      setLoading(false);
      setLoading2(false);
    });
  }, []);

  return (
    <>
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
            {isLoading2 ? (
              <SkeletonEarningCard />
            ) : (
              <div>
                {thresholdColumns.length > 0 ? (
                  <Grid container spacing={2} style={{ alignItems: 'center' }}>
                    <Grid item lg={4} md={4} sm={12} xs={12} style={{ margin: '30px' }}>
                      <Autocomplete
                        disablePortal
                        id="combo-box-demo-1"
                        options={thresholdColumns}
                        value={selectedValue}
                        sx={{ flex: 1, marginRight: '20px' }}
                        renderInput={(params) => <TextField {...params} label="Choose the column " />}
                        onChange={(event, newValue) => {
                          setSelectedValue(newValue);
                          setSelectedColumn(newValue);
                        }}
                      />
                    </Grid>
                    <Grid item lg={4} md={4} sm={12} xs={12} style={{ margin: '30px' }}>
                      <Box sx={{ position: 'relative' }}>
                        <Select
                          value={selectedMethod}
                          onChange={handleChangeMethod}
                          displayEmpty
                          renderValue={(value) =>
                            value ? methods.find((method) => method.value === value).label : 'Select scaling method '
                          }
                          sx={{ width: '95%' }}
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
                    <Grid item lg={2} md={2} sm={12} xs={12} style={{ margin: '30px', textAlign: 'center' }}>
                      <Button
                        disabled={selectedMethod !== '' ? false : true}
                        onClick={handleClick({ vertical: 'bottom', horizontal: 'right' })}
                        style={{ width: '100px', padding: '10px', height: '50px' }}
                        variant="outlined"
                      >
                        Submit
                      </Button>
                    </Grid>
                  </Grid>
                ) : (
                  <Alert severity="warning">No duplicates rows was found !</Alert>
                )}{' '}
              </div>
            )}
          </MainCard>
        </Grid>

        <Box sx={{ width: 500 }}>
          <Snackbar anchorOrigin={{ vertical, horizontal }} open={open} onClose={handleClose} key={vertical + horizontal}>
            <Alert onClose={handleClose} severity="success" sx={{ width: '100%' }}>
              Operation successfully executed!
            </Alert>
          </Snackbar>
        </Box>
      </Grid>
    </>
  );
};

export default Deleting;
