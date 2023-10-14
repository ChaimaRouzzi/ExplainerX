import React, { useState, useEffect } from 'react';
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
import BookmarkBorderIcon from '@mui/icons-material/BookmarkBorder';
import { useSelector } from 'react-redux';
import Plot from 'react-plotly.js';
import CloseIcon from '@mui/icons-material/Close';

const SVRModelBuilder = () => {
  const [plotData2, setPlotData2] = useState([]);
  const [showAlert, setShowAlert] = useState(false);
  const [showAlert2, setShowAlert2] = useState(false);
  const [savingModel, setSavingModel] = useState(false);
  const [svrParameters, setSvrParameters] = useState({
    model_name: '',
    predictors: [],
    all_predictors: [],
    target: 'Electricity',
    horizon: 'Hourly',
    kernel: 'linear',
    degree: 3,
    gamma: 'scale',
    coef0: 0.0,
    tol: 0.001,
    C: 1.0,
    epsilon: 0.1,
    shrinking: true,
    cache_size: 200,
    verbose: false,
    max_iter: -1,
    random_state: 42,
    test_size: 20
  });
  const [showSnackbar, setShowSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState('success');

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
    setSvrParameters((prevParameters) => ({
      ...prevParameters,
      [name]: value
    }));
  };

  const handleOptionChange = (event, newValue) => {
    setSelectedOptions(newValue);
  };

  const handleCheckboxChange = (event) => {
    const { name, checked } = event.target;
    setSvrParameters((prevParameters) => ({
      ...prevParameters,
      [name]: checked
    }));
  };

  const handleTestSizeChange = (event, newValue) => {
    setSvrParameters((prevParameters) => ({
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
        color: 'rgba(0, 128, 0, 0.5)'
      }
    }
  ];

  const userData = useSelector((state) => state.login.userData);
  const userID = userData.user_id;
  const token = userData.token;
  const allPredictors = options.map((option) => option.value);
  const selectedPredictors = selectedOptions.map((option) => option.value);

  const handleSubmit = async (event) => {
    if (selectedPredictors.length !== 0 && svrParameters.model_name !== '') {
      event.preventDefault();
      setLoading(true);

      const updatedSvrParameters = {
        ...svrParameters,
        predictors: selectedPredictors,
        all_predictors: allPredictors
      };
      console.log(token);

      try {
        const response = await axios.post('http://localhost:8000/api/models_building/build_svr_model/', updatedSvrParameters, {
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
          console.log(plotData2);
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
    const updatedSvrParameters = {
      ...svrParameters,
      predictors: selectedPredictors,
      all_predictors: allPredictors
    };
    const modelToSave = {
      model_name: svrParameters.model_name,
      user_id: userID,
      params: updatedSvrParameters,
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
      const response = await axios.post('http://localhost:8000/api/models_building/save_model_svr/', modelToSave, {
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
    if (selectedPredictors.length === 0 || svrParameters.model_name === '') {
      setShowAlert(selectedPredictors.length === 0);
      setShowAlert2(svrParameters.model_name === '');
    } else {
      setShowAlert(false);
      setShowAlert2(false);
    }
  }, [selectedPredictors, svrParameters.model_name]);
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
            SVR Model Parameters
          </Typography>
          <form onSubmit={handleSubmit}>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <InputLabel>Prediction Target</InputLabel>
                  <Select name="target" value={svrParameters.target} onChange={handleParameterChange} label="Prediction Target">
                    <MenuItem value="Electricity">Electricity</MenuItem>
                    <MenuItem value="Gas_01">Gas_01</MenuItem>
                    <MenuItem value="Gas_02">Gas_02</MenuItem>
                    <MenuItem value="Gas_03">Gas_03</MenuItem>
                  </Select>
                </FormControl>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <InputLabel>Kernel:</InputLabel>
                  <Select name="kernel" value={svrParameters.kernel} onChange={handleParameterChange} label="Kernel">
                    <MenuItem value="linear">Linear</MenuItem>
                    <MenuItem value="poly">Poly</MenuItem>
                    <MenuItem value="rbf">RBF</MenuItem>
                    <MenuItem value="sigmoid">Sigmoid</MenuItem>
                  </Select>
                </FormControl>
                <TextField
                  name="degree"
                  label="Degree"
                  variant="outlined"
                  type="number"
                  value={svrParameters.degree}
                  onChange={handleParameterChange}
                  fullWidth
                  style={verticalSpacing}
                />
                <TextField
                  name="tol"
                  label="Tolerance"
                  variant="outlined"
                  type="number"
                  value={svrParameters.tol}
                  onChange={handleParameterChange}
                  fullWidth
                  style={verticalSpacing}
                />

                <TextField
                  name="coef0"
                  label="Coef0"
                  variant="outlined"
                  type="number"
                  value={svrParameters.coef0}
                  onChange={handleParameterChange}
                  fullWidth
                  style={verticalSpacing}
                />
              </Grid>

              <Grid item xs={6}>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <InputLabel>Horizon</InputLabel>
                  <Select name="horizon" value={svrParameters.horizon} onChange={handleParameterChange} label="Horizon">
                    <MenuItem value="Hourly">Hourly</MenuItem>
                    <MenuItem value="Daily">Daily</MenuItem>
                    <MenuItem value="Weekly">Weekly</MenuItem>
                    <MenuItem value="Monthly">Monthly</MenuItem>
                  </Select>
                </FormControl>
                <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                  <InputLabel>Gamma:</InputLabel>
                  <Select name="gamma" value={svrParameters.gamma} onChange={handleParameterChange} label="Gamma">
                    <MenuItem value="scale">Scale</MenuItem>
                    <MenuItem value="auto">Auto</MenuItem>
                  </Select>
                </FormControl>

                <TextField
                  name="C"
                  label="Regularization parameter (C)"
                  variant="outlined"
                  type="number"
                  value={svrParameters.C}
                  onChange={handleParameterChange}
                  fullWidth
                  style={verticalSpacing}
                />

                <TextField
                  name="epsilon"
                  label="Epsilon"
                  variant="outlined"
                  type="number"
                  value={svrParameters.epsilon}
                  onChange={handleParameterChange}
                  fullWidth
                  style={verticalSpacing}
                />

                <TextField
                  name="cache_size"
                  label="Cache size"
                  variant="outlined"
                  type="number"
                  value={svrParameters.cache_size}
                  onChange={handleParameterChange}
                  fullWidth
                  style={verticalSpacing}
                />
              </Grid>
            </Grid>

            <Grid container spacing={2}>
              <Grid item xs={6}>
                <TextField
                  name="random_state"
                  label="Random State"
                  variant="outlined"
                  type="number"
                  value={svrParameters.random_state}
                  onChange={handleParameterChange}
                  fullWidth
                />
              </Grid>

              <Grid item xs={6}>
                <TextField
                  name="max_iter"
                  label="Max iterations"
                  variant="outlined"
                  type="number"
                  value={svrParameters.max_iter}
                  onChange={handleParameterChange}
                  fullWidth
                />
              </Grid>
            </Grid>

            <Grid container spacing={2} style={verticalSpacing}>
              <Grid item xs={6}>
                <FormControlLabel
                  control={<Checkbox name="shrinking" checked={svrParameters.shrinking} onChange={handleCheckboxChange} />}
                  label="Shrinking"
                />
              </Grid>
              <Grid item xs={6}>
                <FormControlLabel
                  control={<Checkbox name="verbose" checked={svrParameters.verbose} onChange={handleCheckboxChange} />}
                  label="Verbose"
                />
              </Grid>
            </Grid>
            <Grid container spacing={2} style={verticalSpacing}>
              <Grid item xs={12}>
                <TextField
                  name="model_name"
                  label="Model Name"
                  variant="outlined"
                  value={svrParameters.model_name}
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
                    value={svrParameters.test_size}
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
                  {svrParameters.test_size}%
                </InputLabel>
              </Grid>
            </Grid>

            <Grid container justifyContent="center">
              <Button
                disabled={showAlert || showAlert2}
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
              >
                Build SVR Model
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

export default SVRModelBuilder;
