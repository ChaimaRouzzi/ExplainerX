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
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import InfoIcon from '@mui/icons-material/Info';
import Snackbar from '@mui/material/Snackbar';
import InputAdornment from '@mui/material/InputAdornment';
import Alert from '@mui/material/Alert';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import { Select, MenuItem, Tooltip, IconButton } from '@mui/material';
import CircularProgress from '@mui/material/CircularProgress';

const methods = [
  {
    value: 'IQR_capping',
    label: 'IQR capping',
    description:
      'IQR is used to measure variability by dividing a data set into quartiles. The data is sorted in ascending order and split into 4 equal parts. Q1, Q2, Q3 called first, second and third quartiles are the values which separate the 4 equal parts. Q1 represents the 25th percentile of the data.IQR capping is replacing all the values that exist outside the limits with the nearest limit value.'
  },
  {
    value: 'IQR_Trimming',
    label: 'IQR Trimming',
    description: 'IQR trimming is deleting all the rows that contains values outside the limits which are calculated using IQR method.'
  },
  {
    value: 'Mean_Imputation ',
    label: 'Mean Imputation',
    description: 'Replace the outliers with the mean value.'
  },
  {
    value: 'Median_Imputation',
    label: 'Median Imputation',
    description: 'Replace the outliers with the median value.'
  }
];

const Outlires = () => {
  const [state, setState] = React.useState({
    open: false,
    vertical: 'top',
    horizontal: 'center'
  });
  const { vertical, horizontal, open } = state;

  const handleClick = (newState) => () => {
    setLoading2(true);
    const url = `http://127.0.0.1:8000/api/outlires/${val}/${updated.updated}/${selectedMethod}/${selectedColumn}`;

    axios.get(url).then((response) => {
      console.log(response);
      const url2 = `http://127.0.0.1:8000/api/check_outlires/${val}/${updated.updated}/${threshold}`;
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
  const [isLoading2, setLoading2] = useState(false);
  const [version_number, setVersionNumber] = useState(0);
  const [activeStep, setActiveStep] = useState(val == -1 ? 2 : val);
  const [selectedValue, setSelectedValue] = React.useState('');
  const [threshold, setThreshold] = React.useState(0);
  const [thresholdColumns, setTthresholdColumns] = React.useState([]);
  const [selectedMethod, setSelectedMethod] = useState('');
  const [isTooltipHovered, setIsTooltipHovered] = useState(false);
  const [selectedColumn, setSelectedColumn] = useState('');
  const [isNoOutliersColumns, setIsNoOutliersColumns] = useState(false);

  const handleTooltipHover = (isHovered) => {
    setIsTooltipHovered(isHovered);
  };

  const handleThresholdChange = (event) => {
    const newValue = parseInt(event.target.value);
    if (newValue) {
      setLoading2(true);
      setThreshold(newValue);
      const url = `http://127.0.0.1:8000/api/check_outlires/${val}/${updated.updated}/${newValue}`;
      axios.get(url).then((response) => {
        const result = JSON.parse(response.data);
        if (result.length === 0) {
          setIsNoOutliersColumns(true);
        } else {
          setIsNoOutliersColumns(false);
        }
        setTthresholdColumns(result);
        console.log(result);
        console.log(thresholdColumns);
        setLoading2(false);
      });
    }
  };

  const handleChangeMethod = (event) => {
    setSelectedMethod(event.target.value);
    console.log(event.target.value);
  };

  const handleStepClick = (step, all) => {
    const updatedVal = all == 1 ? -1 : step;
    handleUpdateUpdated('False');
    setActiveStep(step);
    if (version !== step) {
      handleUpdateVersion(all === 1 ? -1 : step).then(() => {
        axios
          .get(BaseURL)
          .then((response) => {
            const result = JSON.parse(response.data);
            console.log(result);

            setVersionNumber(result.versions_number ? result.versions_number : 0);
            const url2 = `http://127.0.0.1:8000/api/check_outlires/${updatedVal}/False/${threshold}`;
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
    const updatedVal = all == 1 ? -1 : step;
    setActiveStep(step);
    if (version !== step) {
      handleUpdateVersion(all === 1 ? -1 : step).then(() => {
        axios
          .get(BaseURL)
          .then((response) => {
            const result = JSON.parse(response.data);
            console.log(result);

            setVersionNumber(result.versions_number ? result.versions_number : 0);
            setUpdatedVersion(result.updated_version ? JSON.parse(result.updated_version) : []);
            const url2 = `http://127.0.0.1:8000/api/check_outlires/${updatedVal}/True/${threshold}`;
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

  useEffect(
    () => {
      axios.get(BaseURL).then((response) => {
        const result = JSON.parse(response.data);
        console.log(result);
        setVersionNumber(result.versions_number ? result.versions_number : 0);
        setUpdatedVersion(result.updated_version ? JSON.parse(result.updated_version) : []);
      });

      const url = `http://127.0.0.1:8000/api/check_outlires/${val}/${updated.updated}/${threshold}`;

      axios.get(url).then((response) => {
        const result = JSON.parse(response.data);
        setTthresholdColumns(result);
        console.log(result);
        console.log(thresholdColumns);
        setLoading(false);
        setLoading2(false);
      });
    },

    [],
    threshold
  );

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
          {thresholdColumns.length!=0 ?
          <div>
            
       
            <TextField
              sx={{ marginBottom: '20px', width: '100%' }}
              id="outlined-number"
              label="Choose the outliers percentage threshold"
              type="number"
              InputProps={{
                endAdornment: <InputAdornment position="end">%</InputAdornment>,
                inputProps: { min: 0 }
              }}
              value={threshold}
              onChange={(event) => {
                setThreshold(event.target.value);
              }}
              onKeyDown={(event) => {
                if (event.key === 'Enter') {
                  event.preventDefault();
                  handleThresholdChange(event);
                }
              }}
            />
            <Grid container spacing={1}>
              {!isNoOutliersColumns && (
                <Grid item xs={6}>
                  <FormControl fullWidth variant="outlined">
                    <InputLabel>Choose a column</InputLabel>
                    <Select
                      value={selectedValue}
                      onChange={(event) => {
                        setSelectedValue(event.target.value);
                        setSelectedColumn(event.target.value);
                      }}
                      label="Choose a column"
                    >
                      {thresholdColumns.map((column, index) => (
                        <MenuItem key={index} value={column}>
                          {column}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
              )}
              {!isNoOutliersColumns && (
                <Grid item xs={6}>
                  <Box sx={{ position: 'relative' }}>
                    <FormControl fullWidth variant="outlined">
                      <InputLabel>Outliers Handling Method</InputLabel>
                      <Select name="method" value={selectedMethod} onChange={handleChangeMethod} label="Missing Values Imputation Method">
                        {methods.map((method) => (
                          <MenuItem key={method.value} value={method.value}>
                            {method.label}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
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
                          sx={{ position: 'absolute', top: '50%', right: '-33px', transform: 'translateY(-50%)' }}
                          onClick={handleTooltipHover}
                        >
                          <InfoIcon />
                        </IconButton>
                      </Tooltip>
                    )}
                  </Box>
                </Grid>
              )}
            </Grid>
            {thresholdColumns.length > 0 && (
              <Grid container justifyContent="center" style={{ marginTop: '30px' }}>
                <Button
                  disabled={selectedMethod !== '' ? false : true}
                  type="submit"
                  variant="contained"
                  color="primary"
                  style={{ width: '250px' }}
                  sx={{
                    textAlign: 'center',
                    padding: ' 8px 40px',
                    backgroundColor: '#004aad',
                    marginBottom: '30px',
                    '&:hover': {
                      backgroundColor: '#004aad'
                    }
                  }}
                  onClick={handleClick({ vertical: 'bottom', horizontal: 'right' })}
                >
                  Submit
                </Button>
              </Grid>
            )}
            {isNoOutliersColumns && <Alert severity="warning">No columns with outliers were found!</Alert>}
            {isLoading2 && (
              <Grid container justifyContent="center">
                <CircularProgress size={24} color="inherit" />
              </Grid>
            )}
               </div>: <Alert severity="warning">No columns with outliers were found!</Alert>  }
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

export default Outlires;
