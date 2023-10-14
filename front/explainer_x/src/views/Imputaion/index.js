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
import Slider from '@mui/material/Slider';
import { makeStyles } from '@material-ui/styles';
import Snackbar from '@mui/material/Snackbar';
import InputAdornment from '@mui/material/InputAdornment';
import Alert from '@mui/material/Alert';
import CircularProgress from '@mui/material/CircularProgress';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';

import { Select, MenuItem, Tooltip, IconButton } from '@mui/material';

const methods = [
  {
    value: 'imputation_mean',
    label: 'Mean',
    description:
      'Replace the missing values with the mean value. It is the common method of imputing missing values. However in presence of outliers, this method may lead to erroneous imputations. In such cases, median is an appropriate measure of central tendency. For some reasons, if you have to use mean values for imputation, then treat the outliers before imputations.'
  },
  {
    value: 'imputation_median',
    label: 'Medain',
    description:
      'Replace the missing values with the Median value. It is best to replace the missing data with it’s median value only when the data has more outliers.'
  },
  {
    value: 'imputation_mode',
    label: 'Mode',
    description: 'In this type of imputation, we replace the missing data with the most common value called mode.'
  },
  {
    value: 'imputation_const',
    label: 'Constant',
    description: 'Replace the missing values with a constant value.'
  },
  {
    value: 'imputation_back',
    label: 'Backward Fill',
    description: 'Backward fill uses the next value to fill the missing value.'
  },
  {
    value: 'imputation_knn',
    label: 'KNN',
    description:
      'KNN is an algorithm that is useful for matching a point with its closest k neighbors in a multi-dimensional space. It can be used for data that are continuous, discrete, ordinal and categorical which makes it particularly useful for dealing with all kind of missing data. The assumption behind using KNN for missing values is that a point value can be approximated by the values of the points that are closest to it, based on other variables.'
  },
  {
    value: 'imputation_for',
    label: 'Forward Fill',
    description: 'Forward fill method fills the missing value with the previous value.'
  },
  {
    value: 'imputation_lin',
    label: 'Linear Interpolation',
    description:
      'Interpolation is mostly used while working with time-series data because in time-series data we like to fill missing values with previous one or two values. for example, suppose temperature, now we would always prefer to fill today’s temperature with the mean of the last 2 days, not with the mean of the month. We can also use Interpolation for calculating the moving averages. Linear Interpolation simply means to estimate a missing value by connecting dots in a straight line in increasing order. In short, It estimates the unknown value in the same increasing order from previous values.'
  },
  {
    value: 'imputation_pol',
    label: 'Polynomiale Interpolation',
    description:
      'In Polynomial Interpolation you need to specify an order. It means that polynomial interpolation is filling missing values with the lowest possible degree that passes through available data points. The polynomial Interpolation curve is like the trigonometric sin curve or assumes it like a parabola shape. If you pass an order as 1 then the output will similar to linear because the polynomial of order 1 is linear.'
  }
];

const Imputation = () => {
  const useStyles = makeStyles({
    root: {
      width: 300,
      margin: '0 auto',
      paddingTop: 20
    },
    slider: {
      color: 'red' // Change this to the desired color
    }
  });

  const [state, setState] = React.useState({
    open: false,
    vertical: 'top',
    horizontal: 'center'
  });
  const { vertical, horizontal, open } = state;

  const handleClick = (newState) => () => {
    setLoading2(true);
    const url = `http://127.0.0.1:8000/api/imputation/${val}/${updated.updated}/${selectedMethod}/${selectedColumn}/${constVal}/${knnVal}`;

    axios.get(url).then((response) => {
      console.log(response);
      const url2 = `http://127.0.0.1:8000/api/check_missing_values/${val}/${updated.updated}/${threshold}`;
      axios.get(url2).then((response) => {
        const result = JSON.parse(response.data);
        setTthresholdColumns(result);
        console.log(result);
        setSelectedValue('');
        setState({ ...newState, open: true });
        setLoading2(false);
        axios.get(BaseURL).then((response) => {
          const result = JSON.parse(response.data);
          console.log(result);
          setVersionNumber(result.versions_number ? result.versions_number : 0);
          setUpdatedVersion(result.updated_version ? JSON.parse(result.updated_version) : []);
        });
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
  const classes = useStyles();
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
  const [isConst, setConst] = useState(false);
  const [isKnn, setisKnn] = useState(false);
  const [selectedColumn, setSelectedColumn] = useState('');
  const [constVal, setConstVal] = useState(0);
  const [knnVal, setKnnVal] = useState(0);
  const [isNoMissingColumns, setIsNoMissingColumns] = useState(false);

  const handleTooltipHover = (isHovered) => {
    setIsTooltipHovered(isHovered);
  };

  const handleThresholdChange = (event) => {
    const newValue = parseInt(event.target.value);
    if (newValue) {
      setLoading2(true);
      setThreshold(newValue);
      const url = `http://127.0.0.1:8000/api/check_missing_values/${val}/${updated.updated}/${newValue}`;
      axios.get(url).then((response) => {
        const result = JSON.parse(response.data);
        if (result.length === 0) {
          setIsNoMissingColumns(true);
        } else {
          setIsNoMissingColumns(false);
        }
        setTthresholdColumns(result);
        console.log(result);
        console.log(thresholdColumns);
        setLoading2(false);
      });
    }
  };

  const handleChangeMethod = (event) => {
    setConst(false);
    setisKnn(false);
    setSelectedMethod(event.target.value);
    console.log(event.target.value);
    if (event.target.value === 'imputation_const') setConst(true);
    if (event.target.value === 'imputation_knn') setisKnn(true);
  };
  const [value, setValue] = useState(5); // Default value

  const handleChange = (event, newValue) => {
    setValue(newValue);
    setKnnVal(newValue);
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
            const url2 = `http://127.0.0.1:8000/api/check_missing_values/${updatedVal}/False/${threshold}`;
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
            const url2 = `http://127.0.0.1:8000/api/check_missing_values/${updatedVal}/True/${threshold}`;
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

      const url = `http://127.0.0.1:8000/api/check_missing_values/${val}/${updated.updated}/${threshold}`;

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
              <div>
                
           
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
            )}    </div>
          </MainCard>
        </Grid>
        <Grid item lg={12} md={12} sm={12} xs={12}>
          
           <MainCard>
            {thresholdColumns.length!=0 ?
            <div>
              
           
            <TextField
              sx={{ marginBottom: '20px', width: '100%' }}
              id="outlined-number"
              label="Choose the missing values percentage threshold"
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
              {!isNoMissingColumns && (
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
              {!isNoMissingColumns && (
                <Grid item xs={6}>
                  <Box sx={{ position: 'relative' }}>
                    <FormControl fullWidth variant="outlined">
                      <InputLabel>Missing Values Imputation Method</InputLabel>
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
              {isKnn && (
                <Grid item lg={9} md={9} sm={12} xs={12} style={{ margin: '30px' }}>
                  <p>Slider Value: {value}</p>
                  <Slider
                    lasses={{ thumb: classes.slider, track: classes.slider, rail: classes.slider }}
                    style={{ color: '#004aad', width: '92%' }}
                    value={value}
                    min={1}
                    max={10}
                    step={1}
                    onChange={handleChange}
                    valueLabelDisplay="auto"
                    aria-labelledby="range-slider"
                  />
                </Grid>
              )}
              {isConst && (
                <Grid item lg={9} md={9} sm={12} xs={12} style={{ margin: '30px' }}>
                  <TextField
                  sx={{ width: '92%' }}
                  id="outlined-number"
                  label="Choose constant value"
                  type="number"
                  InputLabelProps={{
                    shrink: true
                  }}
                  onChange={(event) => {
                    const newValue = event.target.value;
                    console.log(newValue);
                    setConstVal(newValue);
                  }}
                />
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
            {isNoMissingColumns && <Alert severity="warning">No columns with missing values were found!</Alert>}
            {isLoading2 && (
              <Grid container justifyContent="center">
                <CircularProgress size={24} color="inherit" />
              </Grid>
            )} 
             </div>: <Alert severity="warning">No columns with missing values were found!</Alert> }
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

export default Imputation;
