import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  TextField,
  Button,
  Grid,
  Typography,
  Autocomplete,
  FormControl,
  InputLabel,
  Select,
  IconButton,
  MenuItem,
  Paper,
  Alert, 
  CircularProgress, 
  Snackbar
} from '@mui/material';
import { useSelector } from 'react-redux';
import axios from 'axios';

import { ContentCopy as CopyIcon } from '@mui/icons-material';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { darcula } from 'react-syntax-highlighter/dist/esm/styles/prism';
import copy from 'clipboard-copy';
import BookmarkBorderIcon from '@mui/icons-material/BookmarkBorder';
import CloseIcon from '@mui/icons-material/Close';
const CodeSection = ({ code }) => {
  const [isCopied, setIsCopied] = useState(false);

  const handleCopyToClipboard = async () => {
    try {
      await copy(code);
      setIsCopied(true);
    } catch (error) {
      console.error('Copy to clipboard failed: ', error);
    }
  };

  return (
    <Paper elevation={3} style={{ background: '#000', color: '#fff', padding: '20px', marginBottom: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h6" style={{ color: '#fff' }}>
          Code Example for Gradient Boosting Regressor:
        </Typography>
        <IconButton color="primary" onClick={handleCopyToClipboard} disabled={isCopied}>
          <CopyIcon />
        </IconButton>
      </div>
      <SyntaxHighlighter language="javascript" style={darcula}>
        {code}
      </SyntaxHighlighter>
    </Paper>
  );
};

const ExternalModelBuilder = () => {
  const sampleCode = `
  import pandas as pd
  import joblib
  import numpy as np
  from sklearn.model_selection import train_test_split
  from sklearn.ensemble import GradientBoostingRegressor
  from sklearn.metrics import mean_squared_error, r2_score
  from sklearn.model_selection import train_test_split
  import requests
  from sklearn.preprocessing import MinMaxScaler

  get_url = "http://localhost:8000/api/models_building/get_data/" 
  response = requests.get(get_url)
  response_json = response.json()
  df = pd.read_json(response_json)

  # Select all columns except for the column you want to exclude
  X = df.drop('Gas_01', axis=1).values

  # Select only the column you want to use as the target variable
  y = df['Gas_01'].values
  X_train, X_test, y_train, y_test = train_test_split(X, y)

  gb_regressor = GradientBoostingRegressor(
    n_estimators=100,   
    learning_rate=0.1, 
    max_depth=3,       
    random_state=42)

  # Train the model using the training data
  gb_regressor.fit(X_train, y_train)

  y_pred = gb_regressor.predict(X_test)
  
  # Evaluate the model using mean squared error
  mse = mean_squared_error(y_test, y_pred)
  print(f"Mean Squared Error (MSE): {mse:.2f}")
  joblib.dump(gb_regressor, "external_boosting_model_gas1_weekly.joblib")
  
  upload_url = 'http://localhost:8000/api/models_building/upload_model' 
  with open("external_boosting_model_gas1_weekly.joblib", 'rb') as file:
      files = {'file': file}
      response = requests.post(upload_url, files=files)
      print(response.json())
  `;
  const selectedFeatures = useSelector((state) => state.feature.selectedFeatures);
  const userData = useSelector((state) => state.login.userData);
  const userID = userData.user_id;
  const [savingModel, setSavingModel] = useState(false);
  const [showSnackbar, setShowSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState('success');

  const [selectedOptions, setSelectedOptions] = useState(
    selectedFeatures.map((feature) => ({
      label: feature,
      value: feature
    }))
  );
  const [predictionTarget, setPredictionTarget] = useState('Electricity');
  const [horizon, setHorizon] = useState('Hourly');
  const [modelName, setModelName] = useState('');
  const selectedFeatureValues = [predictionTarget, ...selectedOptions.map((option) => option.value)];
  const [showAlert, setShowAlert] = useState(false);
  const [showAlert2, setShowAlert2] = useState(false);

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
  const showSnackbarMessage = (message, severity) => {
    setSnackbarMessage(message);
    setSnackbarSeverity(severity);
    setShowSnackbar(true);
  };

  const handleSnackbarClose = () => {
    setShowSnackbar(false);
  };

  const handleUploadData = async () => {
    console.log(selectedFeatureValues);
    const requestData = {
      features: selectedFeatureValues,
      horizon: horizon
    };
    const endpointURL = `http://localhost:8000/api/models_building/upload_data/`;
    axios
      .post(endpointURL, requestData)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  const handleSaveExternalModel = async () => {
    const requestData = {
      user_id: userID,
      model_name: modelName,
      features: selectedOptions.map((option) => option.value),
      target: predictionTarget,
      horizon: horizon
    };
    setSavingModel(true);
    try {
      const response = await axios.post('http://localhost:8000/api/models_building/save_external_model/', requestData);
      console.log('Response:', response.data);
      console.log('Model saved:', response.data);
      showSnackbarMessage('Model saved successfully!', 'success');
    } catch (error) {
      console.error('Error saving model:', error);
      showSnackbarMessage('Error saving model.', 'error');
    }
    finally {
      setSavingModel(false);
    }
  };

  const handleOptionChange = (event, newValue) => {
    setSelectedOptions(newValue);
  };
  const verticalSpacing = { marginBottom: '15px' };

  useEffect(() => {
    if (selectedFeatureValues.length === 0 || modelName === '') {
      setShowAlert(selectedFeatureValues.length === 0);
      setShowAlert2(modelName === '');
    } else {
      setShowAlert(false);
      setShowAlert2(false);
    }
  }, [selectedFeatureValues, modelName]);

  return (
    <div>
      <Card style={{ marginBottom: '20px' }}>
        <CardContent>
          <Typography variant="h3" align="left" gutterBottom style={{ marginBottom: '20px' }}>
            Select Target and Horizon
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                <InputLabel>Prediction Target</InputLabel>
                <Select
                  name="target"
                  value={predictionTarget}
                  onChange={(event) => setPredictionTarget(event.target.value)}
                  label="Prediction Target"
                >
                  <MenuItem value="Electricity">Electricity</MenuItem>
                  <MenuItem value="Gas_01">Gas_01</MenuItem>
                  <MenuItem value="Gas_02">Gas_02</MenuItem>
                  <MenuItem value="Gas_03">Gas_03</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={6}>
              <FormControl fullWidth variant="outlined" style={verticalSpacing}>
                <InputLabel>Horizon</InputLabel>
                <Select name="horizon" value={horizon} onChange={(event) => setHorizon(event.target.value)} label="Horizon">
                  <MenuItem value="Hourly">Hourly</MenuItem>
                  <MenuItem value="Daily">Daily</MenuItem>
                  <MenuItem value="Weekly">Weekly</MenuItem>
                  <MenuItem value="Monthly">Monthly</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
          <div style={{ margin: '20px 0' }} />
          <Typography variant="h3" align="left" gutterBottom style={{ marginBottom: '20px' }}>
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

          <Grid container justifyContent="center">
            <Button
              type="submit"
              variant="contained"
              color="primary"
              style={{ width: '350px' }}
              sx={{
                textAlign: 'center',
                padding: ' 8px 40px',
                backgroundColor: '#004aad',
                marginBottom: ' 10px',
                marginTop: '30px',
                '&:hover': {
                  backgroundColor: '#004aad'
                }
              }}
              onClick={handleUploadData}
            >
              Use Selected Features Externally
            </Button>
          </Grid>
        </CardContent>
      </Card>
      <div style={{ margin: '20px 0' }} />
      <div>
        <CodeSection code={sampleCode} />
      </div>
      <div style={{ margin: '20px 0' }} />
      <Card style={{ marginBottom: '20px' }}>
        <CardContent>
          <Typography variant="h3" align="left" gutterBottom style={{ marginBottom: '15px' }}>
            Save your Model
          </Typography>
          <Grid container spacing={2} style={verticalSpacing}>
            <Grid item xs={12}>
              <TextField
                name="model_name"
                label="Model Name"
                variant="outlined"
                value={modelName}
                onChange={(event) => setModelName(event.target.value)}
                fullWidth
                style={verticalSpacing}
              />
              {showAlert2 && (
                <Alert severity="warning">Please enter a model name (the same name of the joblib uploaded using the API) !</Alert>
              )}
            </Grid>
          </Grid>
          <Grid container justifyContent="center">
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', marginTop: '30px', marginBottom: '30px' }}>
              <Button
                disabled={modelName == '' ? true : false}
                variant="contained"
                color="primary"
                onClick={handleSaveExternalModel}
                startIcon={<BookmarkBorderIcon style={{ color: 'white' }} />}
                style={{ backgroundColor: 'black', color: 'white', width: '220px' }}
              >
                Save your Model
              </Button>
            </div>
          </Grid>
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

export default ExternalModelBuilder;
