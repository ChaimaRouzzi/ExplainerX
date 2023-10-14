import React, { useState, useEffect} from 'react';
import axios from 'axios';
import {
  Slider,
  Card,
  CardContent,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  FormControlLabel,
  Grid,
  CircularProgress,
  Typography,
  Autocomplete,
  Alert,
  Snackbar,
  IconButton
} from '@mui/material';
import { red, green, blue } from '@mui/material/colors';
import { useSelector } from 'react-redux';
import CloseIcon from '@mui/icons-material/Close';
import BookmarkBorderIcon from '@mui/icons-material/BookmarkBorder';


import Plot from 'react-plotly.js';

const RandomForestModelBuilder = () => {
  const [plotData2, setPlotData2] = useState([]);
  const [showAlert, setShowAlert] = useState(false);
  const [showAlert2, setShowAlert2] = useState(false);
  const [savingModel, setSavingModel] = useState(false);
  const [showSnackbar, setShowSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState('success');
  const [rfParameters, setRfParameters] = useState({
    model_name: '',
    predictors: [],
    all_predictors: [],
    target: 'Electricity',
    horizon: 'Hourly',
    n_estimators: 100,
    criterion: 'absolute_error',
    max_depth: 1,
    min_samples_split: 2,
    min_samples_leaf: 1,
    min_weight_fraction_leaf: 0.0,
    max_features: 'auto',
    max_leaf_nodes: 1,
    min_impurity_decrease: 0.0,
    bootstrap: true,
    oob_score: false,
    n_jobs: -1,
    random_state: 42,
    verbose: 0,
    warm_start: false,
    ccp_alpha: 0.0,
    max_samples: 1.0,
    test_size: 20
  });
  const selectedFeatures = useSelector((state) => state.feature.selectedFeatures);
  console.log(selectedFeatures);
  const [shapData, setShapData] = useState([]);
  const [pfiData, setPfiData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [mse, setMSE] = useState(null);
  const [rmse, setRMSE] = useState(null);
  const [mae, setMAE] = useState(null);

  const [selectedOptions, setSelectedOptions] = useState(
    selectedFeatures.map((feature) => ({
      label: feature,
      value: feature
    }))
  );

  const options = [
    { label: 'Day_Degree_Cold', value: 'Day_Degree_Cold' },
    { label: 'Day_Degree_Hot', value: 'Day_Degree_Hot' },
    { label: 'Min_OutdoorTemp', value: 'Min_OutdoorTemp' },
    { label: 'Average_OutdoorTemp', value: 'Average_OutdoorTemp' },
    { label: 'Max_OutdoorTemp', value: 'Max_OutdoorTemp' },
    { label: 'Maximum_Humidity', value: 'Maximum_Humidity' },
    { label: 'Average_Humidity', value: 'Average_Humidity' },
    { label: 'Solar_Radiation', value: 'Solar_Radiation' },
    { label: 'Hour', value: 'Hour' },
    { label: 'Day', value: 'Day' },
    { label: 'Week', value: 'Week' },
    { label: 'Month', value: 'Month' },
    { label: 'Year', value: 'Year' }
  ];

  const handleParameterChange = (event) => {
    const { name, value } = event.target;
    setRfParameters((prevParameters) => ({
      ...prevParameters,
      [name]: value
    }));
  };

  const handleOptionChange = (event, newValue) => {
    setSelectedOptions(newValue);
  };

  const handleCheckboxChange = (event) => {
    const { name, checked } = event.target;
    setRfParameters((prevParameters) => ({
      ...prevParameters,
      [name]: checked
    }));
  };

  const handleTestSizeChange = (event, newValue) => {
    setRfParameters((prevParameters) => ({
      ...prevParameters,
      test_size: newValue
    }));
  };

  const [previousMetrics, setPreviousMetrics] = useState({
    mse: null,
    rmse: null,
    mae: null
  });

  const plotData = [
    {
      x: ['MSE', 'RMSE', 'MAE'],
      y: [previousMetrics.mse, previousMetrics.rmse, previousMetrics.mae],
      type: 'bar',
      name: 'Previous Metrics',
      marker: {
        color: 'rgba(255, 0, 0, 0.5)'
      }
    },
    {
      x: ['MSE', 'RMSE', 'MAE'],
      y: [mse, rmse, mae],
      type: 'bar',
      name: 'Current Metrics',
      marker: {
        color: 'rgba(0, 128, 0, 0.5)' // Green color with some transparency
      }
    }
  ];

  const userData = useSelector((state) => state.login.userData);
  const userID = userData.user_id;
  const token = userData.token;
  const allPredictors = options.map((option) => option.value);
  const selectedPredictors = selectedOptions.map((option) => option.value);

  const handleSubmit = async (event) => {
    if (selectedPredictors.length !== 0 && rfParameters.model_name !== '') {
      event.preventDefault();
      setLoading(true);

      const updatedRfParameters = {
        ...rfParameters,
        predictors: selectedPredictors,
        all_predictors: allPredictors
      };
      console.log(token);

      try {
        const response = await axios.post('http://localhost:8000/api/models_building/build_rf_model/', updatedRfParameters, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        console.log(response.data);

        if (mse !== null || rmse !== null || mae !== null) {
          setPreviousMetrics({
            mse,
            rmse,
            mae
          });
        }

        if (response.data && response.data.mae) {
          setMSE(response.data.mse);
          setRMSE(response.data.rmse);
          setMAE(response.data.mae);
          setShapData(response.data.shap);
          setPfiData(response.data.pfi);
          const actualValues = response.data.actual_values;
          const predictedValues = response.data.predicted_values;
          console.log(predictedValues.flat());
          console.log(actualValues);
          const dates = response.data.dates;
          console.log(dates);

          const actualTrace = {
            x: dates,
            y: actualValues.map((valueArray) => valueArray[0]),
            type: 'scatter',
            mode: 'lines',
            name: 'Actual Data',
            marker: {
              color: 'blue'
            }
          };

          const predictedTrace = {
            x: dates,
            y: predictedValues,
            type: 'scatter',
            mode: 'lines',
            name: 'Predicted Data',
            marker: {
              color: 'red'
            }
          };

          const newPlotData = [actualTrace, predictedTrace];

          setPlotData2(newPlotData);
          console.log(plotData2)
        } else {
          console.error('Error: No predictions found in the server response.');
        }

        setLoading(false);
      } catch (error) {
        console.error('Error:', error);
        setLoading(false);
      }
    }
  };

  const handleSaveModel = async () => {
    const updatedRfParameters = {
      ...rfParameters,
      predictors: selectedPredictors,
      all_predictors: allPredictors
    };
    
    const modelToSave = {
      model_name: rfParameters.model_name,
      user_id: userID,
      params: updatedRfParameters,
      performance: {
        mse,
        rmse,
        mae
      },

      shap_data: shapData,
      pfi_data: pfiData
    };

    console.log(modelToSave);
    setSavingModel(true);

    try {
      console.log('hi');
      const response = await axios.post('http://localhost:8000/api/models_building/save_model_rf/', modelToSave, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      console.log('Model saved:', response.data);
      showSnackbarMessage('Model saved successfully!', 'success');
    } catch (error) {
      console.error('Error saving model:', error);
      showSnackbarMessage('Error saving model.', 'error');
    } finally {
      setSavingModel(false);
    }
  };

  const showSnackbarMessage = (message, severity) => {
    setSnackbarMessage(message);
    setSnackbarSeverity(severity);
    setShowSnackbar(true);
  };

  const handleSnackbarClose = () => {
    setShowSnackbar(false);
  };

  const verticalSpacing = { marginBottom: '15px' };
  console.log('plotData:', plotData);
  console.log(selectedOptions);
  useEffect(() => {
    if (selectedPredictors.length === 0 || rfParameters.model_name === '') {
      setShowAlert(selectedPredictors.length === 0);
      setShowAlert2(rfParameters.model_name === '');
    } else {
      setShowAlert(false);
      setShowAlert2(false);
    }
  }, [selectedPredictors, rfParameters.model_name]);

  return (
    <div>
      <Card style={{ marginBottom: '20px' }}>
        <CardContent>
          <Typography variant="h3" align="left" gutterBottom style={{ marginBottom: '15px' }}>
            Selected Features
          </Typography>
          <Autocomplete
            multiple
            id="multi-select"
            options={options}
            getOptionLabel={(option) => option.label}
            value={selectedOptions}
            isOptionEqualToValue={(option, value) => option.value === value.value}
            onChange={handleOptionChange}
            renderInput={(params) => <TextField {...params} variant="outlined" label="Select options" />}
          />
          {showAlert && <Alert severity="warning">Please select at least one feature !</Alert>}
        </CardContent>
      </Card>
      <div style={{ margin: '20px 0' }} />
      <Card style={{ marginBottom: '20px' }}>
        <CardContent>
          <Typography variant="h3" align="left" gutterBottom style={{ marginBottom: '20px' }}>
            RF Model Parameters
          </Typography>
          <form onSubmit={handleSubmit}>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <InputLabel>Prediction Target</InputLabel>
                  <Select name="target" value={rfParameters.target} onChange={handleParameterChange} label="Prediction Target">
                    <MenuItem value="Electricity">Electricity</MenuItem>
                    <MenuItem value="Gas_01">Gas_01</MenuItem>
                    <MenuItem value="Gas_02">Gas_02</MenuItem>
                    <MenuItem value="Gas_03">Gas_03</MenuItem>
                  </Select>
                </FormControl>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <TextField
                    name="n_estimators"
                    label="Number of Estimators"
                    type="number"
                    variant="outlined"
                    value={rfParameters.n_estimators}
                    onChange={handleParameterChange}
                  />
                </FormControl>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <Select name="criterion" value={rfParameters.criterion} onChange={handleParameterChange} label="Criterion">
                    <MenuItem value="absolute_error">absolute_error</MenuItem>
                    <MenuItem value="squared_error">squared_error</MenuItem>
                    <MenuItem value="friedman_mse">friedman_mse</MenuItem>
                    <MenuItem value="poisson">poisson</MenuItem>
                  </Select>
                </FormControl>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <TextField
                    name="max_depth"
                    label="Max Depth"
                    type="number"
                    variant="outlined"
                    value={rfParameters.max_depth}
                    onChange={handleParameterChange}
                  />
                </FormControl>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <TextField
                    name="min_samples_split"
                    label="Min Samples Split"
                    type="number"
                    variant="outlined"
                    value={rfParameters.min_samples_split}
                    onChange={handleParameterChange}
                  />
                </FormControl>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <TextField
                    name="min_samples_leaf"
                    label="Min Samples Leaf"
                    type="number"
                    variant="outlined"
                    value={rfParameters.min_samples_leaf}
                    onChange={handleParameterChange}
                  />
                </FormControl>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <TextField
                    name="max_leaf_nodes"
                    label="Max Leaf Nodes"
                    type="number"
                    variant="outlined"
                    value={rfParameters.max_leaf_nodes}
                    onChange={handleParameterChange}
                  />
                </FormControl>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <TextField
                    name="min_impurity_decrease"
                    label="Min Impurity Decrease"
                    type="number"
                    variant="outlined"
                    value={rfParameters.min_impurity_decrease}
                    onChange={handleParameterChange}
                  />
                </FormControl>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <TextField
                    name="ccp_alpha"
                    label="CCP Alpha"
                    type="number"
                    variant="outlined"
                    value={rfParameters.ccp_alpha}
                    onChange={handleParameterChange}
                  />
                </FormControl>
                <FormControlLabel
                  control={<Checkbox name="oob_score" checked={rfParameters.oob_score} onChange={handleCheckboxChange} />}
                  label="Out-of-bag Score (OOB)"
                />
                <FormControlLabel
                  control={<Checkbox name="warm_start" checked={rfParameters.warm_start} onChange={handleCheckboxChange} />}
                  label="Warm Start"
                />
              </Grid>
              <Grid item xs={6}>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <InputLabel>Horizon</InputLabel>
                  <Select name="horizon" value={rfParameters.horizon} onChange={handleParameterChange} label="Horizon">
                    <MenuItem value="Hourly">Hourly</MenuItem>
                    <MenuItem value="Daily">Daily</MenuItem>
                    <MenuItem value="Weekly">Weekly</MenuItem>
                    <MenuItem value="Monthly">Monthly</MenuItem>
                  </Select>
                </FormControl>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <TextField
                    name="max_features"
                    label="Max Features"
                    variant="outlined"
                    value={rfParameters.max_features}
                    onChange={handleParameterChange}
                  />
                </FormControl>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <TextField
                    name="random_state"
                    label="Random State"
                    type="number"
                    variant="outlined"
                    value={rfParameters.random_state}
                    onChange={handleParameterChange}
                  />
                </FormControl>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <TextField
                    name="n_jobs"
                    label="Number of Jobs"
                    type="number"
                    variant="outlined"
                    value={rfParameters.n_jobs}
                    onChange={handleParameterChange}
                  />
                </FormControl>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <TextField
                    name="verbose"
                    label="Verbose"
                    type="number"
                    variant="outlined"
                    value={rfParameters.verbose}
                    onChange={handleParameterChange}
                  />
                </FormControl>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <TextField
                    name="min_weight_fraction_leaf"
                    label="Min Weight Fraction Leaf"
                    type="number"
                    variant="outlined"
                    value={rfParameters.min_weight_fraction_leaf}
                    onChange={handleParameterChange}
                  />
                </FormControl>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <TextField
                    name="ccp_alpha"
                    label="CCP Alpha"
                    type="number"
                    variant="outlined"
                    value={rfParameters.ccp_alpha}
                    onChange={handleParameterChange}
                  />
                </FormControl>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <TextField
                    name="max_samples"
                    label="Max Samples"
                    type="number"
                    variant="outlined"
                    value={rfParameters.max_samples}
                    onChange={handleParameterChange}
                  />
                </FormControl>
                <FormControlLabel
                  control={<Checkbox name="bootstrap" checked={rfParameters.bootstrap} onChange={handleCheckboxChange} />}
                  label="Bootstrap"
                />
              </Grid>
            </Grid>
            <Grid container spacing={2} style={verticalSpacing}>
              <Grid item xs={12}>
                <TextField
                  name="model_name"
                  label="Model Name"
                  variant="outlined"
                  value={rfParameters.model_name}
                  onChange={handleParameterChange}
                  fullWidth
                  style={verticalSpacing}
                />
                {showAlert2 && <Alert severity="warning">Please enter a model name !</Alert>}
              </Grid>
              <Grid item xs={6}>
                <FormControl fullWidth variant="outlined">
                  <Slider
                    name="test_size"
                    value={rfParameters.test_size}
                    onChange={handleTestSizeChange}
                    valueLabelDisplay="auto"
                    marks
                    min={1}
                    max={100}
                    sx={{
                      color: '#004aad'
                    }}
                  />
                </FormControl>
              </Grid>
              <Grid item xs={6} style={{ display: 'flex', alignItems: 'center' }}>
                <InputLabel
                  style={{
                    fontWeight: 'bold',
                    color: '#000000',
                    marginRight: '8px'
                  }}
                >
                  Test Size Percentage:
                </InputLabel>
                <InputLabel
                  style={{
                    fontWeight: 'bold',
                    color: '#004aad'
                  }}
                >
                  {rfParameters.test_size}%
                </InputLabel>
              </Grid>
            </Grid>

            <Grid container justifyContent="center">
              <Button
                disabled={showAlert || showAlert2}
                type="submit"
                variant="contained"
                color="primary"
                style={{ width: '275px' }}
                sx={{
                  textAlign: 'center',
                  padding: ' 8px 40px',
                  backgroundColor: '#004aad',
                  marginBottom: '30px',
                  '&:hover': {
                    backgroundColor: '#004aad'
                  }
                }}
              >
                Build Random Forest Model
              </Button>
            </Grid>
          </form>
          <Grid container justifyContent="center">
            {loading ? (
              <CircularProgress size={24} color="inherit" />
            ) : (
              (mse !== null || rmse !== null || mae !== null) && (
                <Grid item xs={12}>
                  <Typography variant="h3" align="left" gutterBottom>
                    Performance Metrics
                  </Typography>
                  <Grid container spacing={2} justifyContent="center">
                    <Grid item xs={4}>
                      <Card style={{ backgroundColor: red[100] }}>
                        <CardContent>
                          <Typography variant="h6">Mean Squared Error (MSE)</Typography>
                          <Typography variant="body2" color="textSecondary">
                            {mse !== null ? mse : 'N/A'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={4}>
                      <Card style={{ backgroundColor: green[100] }}>
                        <CardContent>
                          <Typography variant="h6">Root Mean Squared Error (RMSE)</Typography>
                          <Typography variant="body2" color="textSecondary">
                            {rmse !== null ? rmse : 'N/A'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={4}>
                      <Card style={{ backgroundColor: blue[100] }}>
                        <CardContent>
                          <Typography variant="h6">Mean Absolute Error (MAE)</Typography>
                          <Typography variant="body2" color="textSecondary">
                            {mae !== null ? mae : 'N/A'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                  </Grid>
                </Grid>
              )
            )}
          </Grid>
          {!loading && (mse !== null || rmse !== null || mae !== null) && (
            <div style={{ width: '100%', height: '400px' }}>
              <Plot
                data={plotData}
                layout={{ title: 'Performance Improvements' }}
                config={{
                  displayModeBar: false,
                  displaylogo: false,
                  responsive: true
                }}
              />
            </div>
          )}
          {/* {!loading && plotData2.length > 0 && (
            <div style={{ width: '100%', height: '400px' }}>
              <Plot
                data={plotData2}
                layout={{ title: 'Actual vs Predicted Data' }}
                config={{
                  displayModeBar: false,
                  displaylogo: false,
                  responsive: true
                }}
              />
            </div>
          )} */}
          {!loading && shapData.length > 0 && (
            <div style={{ textAlign: 'left' }}>
              <h3>SHAP Values</h3>
              <Plot
                data={[
                  {
                    name: 'Negative Features',
                    y: shapData
                      .filter((item) => item.importance < 0)
                      .sort((a, b) => a.importance - b.importance)
                      .map((item) => item.feature),
                    x: shapData
                      .filter((item) => item.importance < 0)
                      .sort((a, b) => a.importance - b.importance)
                      .map((item) => item.importance),
                    type: 'bar',
                    orientation: 'h',
                    marker: {
                      color: 'rgba(255, 0, 0, 0.7)',
                      colorbar: false
                    }
                  },
                  {
                    name: 'Positive Features',
                    y: shapData
                      .filter((item) => item.importance >= 0)
                      .sort((a, b) => a.importance - b.importance)
                      .map((item) => item.feature),
                    x: shapData
                      .filter((item) => item.importance >= 0)
                      .sort((a, b) => a.importance - b.importance)
                      .map((item) => item.importance),
                    type: 'bar',
                    orientation: 'h',
                    marker: {
                      color: 'rgba(0, 128, 0, 0.7)',
                      colorbar: false
                    }
                  }
                ]}
                layout={{
                  title: 'SHAP Feature Importances',
                  width: 800,
                  barmode: 'stack',
                  margin: {
                    l: 150,
                    r: 20,
                    t: 30,
                    b: 30
                  }
                }}
                config={{ displayModeBar: false }}
              />
            </div>
          )}

          {!loading && pfiData.length > 0 && (
            <div style={{ textAlign: 'left' }}>
              <h3>Permutation Feature Importance (PFI) Values</h3>
              <Plot
                data={[
                  {
                    name: 'Negative Features',
                    y: pfiData
                      .filter((item) => item.importance < 0)
                      .sort((a, b) => a.importance - b.importance)
                      .map((item) => item.feature),
                    x: pfiData
                      .filter((item) => item.importance < 0)
                      .sort((a, b) => a.importance - b.importance)
                      .map((item) => item.importance),
                    type: 'bar',
                    orientation: 'h',
                    marker: {
                      color: 'rgba(255, 0, 0, 0.7)',
                      colorbar: false
                    }
                  },
                  {
                    name: 'Positive Features',
                    y: pfiData
                      .filter((item) => item.importance >= 0)
                      .sort((a, b) => a.importance - b.importance)
                      .map((item) => item.feature),
                    x: pfiData
                      .filter((item) => item.importance >= 0)
                      .sort((a, b) => a.importance - b.importance)
                      .map((item) => item.importance),
                    type: 'bar',
                    orientation: 'h',
                    marker: {
                      color: 'rgba(0, 128, 0, 0.7)',
                      colorbar: false
                    }
                  }
                ]}
                layout={{
                  title: 'PFI Feature Importances',
                  width: 800,
                  barmode: 'stack',
                  margin: {
                    l: 150,
                    r: 20,
                    t: 30,
                    b: 30
                  }
                }}
                config={{ displayModeBar: false }}
              />
            </div>
          )}

          {(mse !== null || rmse !== null || mae !== null) && (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', marginTop: '30px', marginBottom: '30px' }}>
              <Button
                variant="contained"
                color="primary"
                onClick={handleSaveModel}
                startIcon={<BookmarkBorderIcon style={{ color: 'white' }} />}
                style={{ backgroundColor: 'black', color: 'white', width: '220px' }}
              >
                Save your Model
              </Button>
            </div>
          )}
          {savingModel ? (
            <Grid container justifyContent="center">
              <CircularProgress size={24} color="inherit" />
            </Grid>
          ) : (
            <Snackbar anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }} open={showSnackbar} onClose={handleSnackbarClose}>
              <Alert severity={snackbarSeverity} sx={{ width: 300 }}>
                {snackbarMessage}
                <IconButton
                  aria-label="close"
                  color="inherit"
                  size="small"
                  onClick={handleSnackbarClose}
                  style={{ position: 'absolute', right: '8px', top: '8px' }}
                >
                  <CloseIcon fontSize="inherit" />
                </IconButton>
              </Alert>
            </Snackbar>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default RandomForestModelBuilder;
