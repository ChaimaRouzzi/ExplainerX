import React, { useState, useEffect } from 'react';
import { Button, TextField, Select, MenuItem, Grid, Typography, CircularProgress, InputLabel } from '@mui/material';
import axios from 'axios';

const StepOneForm = ({
  activeStep,
  handleBack,
  setActiveStep,
  setShapResult,
  setLimeResult,
  setAnchorsResult,
  predictionResult,
  setPredictionResult,
  target,
  setTarget,
  horizon,
  setHorizon
}) => {
  const [modelsList, setModelsList] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({});

  const selectedModelObject = modelsList.find((model) => model.model_name === selectedModel);
  console.log(selectedModelObject);
  const modelPredictors = selectedModelObject ? selectedModelObject.predictors : [];
  const [isAnyPredictorEmpty, setIsAnyPredictorEmpty] = useState(true);

  const showButtons = !!predictionResult;
  let formattedPredictionText = '';
  if (predictionResult !== null) {
    if (target === 'Electricity') {
      formattedPredictionText = (
        <span style={{ fontSize: '17px', fontWeight: 'bold' }}>
          Predicted Electricity consumption: <span style={{ color: 'green' }}>{predictionResult} KW/h</span>
        </span>
      );
    } else {
      formattedPredictionText = (
        <span style={{ fontSize: '17px', fontWeight: 'bold' }}>
          Predicted Gas consumption: <span style={{ color: 'green' }}>{predictionResult} MW/h</span>
        </span>
      );
    }
  }

  const getModelsList = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:8000/api/models_prediction/list_custom_models/');
      setModelsList(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching model list:', error);
    }
  };

  const resetForm = () => {
    setFormData({});
    setPredictionResult(null);
  };
  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };
  useEffect(() => {
    const isAnyEmpty = modelPredictors.some((predictor) => !formData[`predictor_${predictor}`]);
    setIsAnyPredictorEmpty(isAnyEmpty);
  }, [formData, modelPredictors]);

  useEffect(() => {
    if (selectedModelObject) {
      setTarget(selectedModelObject.target);
      setHorizon(selectedModelObject.horizon);
    }
  }, [selectedModelObject]);

  const handleSubmit = async () => {
    const valuesList = [];
    setLoading(true);

    for (const key in formData) {
      if (Object.prototype.hasOwnProperty.call(formData, key)) {
        valuesList.push(formData[key]);
      }
    }

    const endpointURL = `http://localhost:8000/api/models_prediction/predict/custom/${selectedModel}`;

    try {
      const response = await axios.post(
        endpointURL,
        {
          data: valuesList,
          target: target,
          horizon: horizon
        },
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );

      setPredictionResult(response.data.prediction);
      console.log(response.data.prediction);
    } catch (error) {
      // Handle errors
    } finally {
      setLoading(false);
    }
    console.log('Form Data Values:', valuesList);
  };

  const handleSubmitXAI = async (explanationType, setExplainResult) => {
    const valuesList = [];
    setLoading(true);

    for (const key in formData) {
      if (Object.prototype.hasOwnProperty.call(formData, key)) {
        valuesList.push(formData[key]);
      }
    }
    const endpointURL = `http://localhost:8000/api/models_prediction/xai_custom/${explanationType}/${selectedModel}`;
    axios
      .post(endpointURL, {
        data: valuesList,
        feature_names: modelPredictors
      })
      .then((response) => {
        setExplainResult(response.data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  const handleGetExplanations = async () => {
    await handleSubmitXAI('shap', setShapResult);
    await handleSubmitXAI('lime', setLimeResult);
    await handleSubmitXAI('anchors', setAnchorsResult);

    setActiveStep(1);
  };

  useEffect(() => {
    getModelsList();
  }, []);

  useEffect(() => {
    resetForm();
  }, [selectedModel]);

  return (
    <div style={{ marginTop: 20 }}>
      <Grid container spacing={2} style={{ marginBottom: '20px' }}>
        <Grid item xs={12}>
          <InputLabel>Select Model</InputLabel>
          <Select
            fullWidth
            name="selectedModel"
            value={selectedModel}
            onChange={(event) => {
              setSelectedModel(event.target.value);
            }}
          >
            {modelsList.map((model) => (
              <MenuItem key={model.model_name} value={model.model_name}>
                {model.model_name}
              </MenuItem>
            ))}
          </Select>
        </Grid>

        {modelPredictors.map((predictor) => (
          <Grid key={predictor} item xs={12} sm={6}>
            <TextField
              fullWidth
              label={predictor}
              type="number"
              name={`predictor_${predictor}`} // Make name unique
              value={formData[`predictor_${predictor}`] || ''}
              onChange={handleInputChange}
            />
          </Grid>
        ))}
      </Grid>

      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: '20px' }}>
          <CircularProgress />
        </div>
      ) : (
        <Grid>
          <Grid container justifyContent="center">
            <Button
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
              onClick={handleSubmit}
              disabled={!selectedModel || isAnyPredictorEmpty}
            >
              Get Prediction
            </Button>
          </Grid>
          <Typography>{formattedPredictionText}</Typography>
          {showButtons && (
            <Grid container justifyContent="flex-end">
              <Button disabled={activeStep === 0} onClick={handleBack}>
                Back
              </Button>
              <Button variant="contained" color="primary" onClick={handleGetExplanations}>
                Get Explanations
              </Button>
            </Grid>
          )}
        </Grid>
      )}
    </div>
  );
};

export default StepOneForm;
