import React, { useState } from 'react';
import { Stepper, Step, StepLabel, Card, CardContent } from '@mui/material';
import StepOneForm from './StepOne';
import StepTwoForm from './StepTwo';
import axios from 'axios';

const ParentForm = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [formData, setFormData] = useState({
    date: '',
    energyType: 'Electricity',
    horizon: 'Hourly',
    selectedHour: 12,
    approach: '',
    maxOutdoorTemp: 0,
    minOutdoorTemp: 0,
    avgTemp: 0,
    solarRadiation: 0,
    maxHumidity: 0,
    avgHumidity: 0,
    dayDegreeHot: 0,
    dayDegreeCold: 0,
    isWeekend: false,
    isHoliday: false,
    numberPeriods: 1
  });
  const [loading, setLoading] = useState(false);
  const [predictionResult, setPredictionResult] = useState(null);
  const [shapResult, setShapResult] = useState(null);
  const [limeResult, setLimeResult] = useState(null);
  const [anchorsResult, setAnchorsResult] = useState(null);

  const handleFormChange = (event) => {
    const { name, value, type, checked } = event.target;
    const newValue = type === 'checkbox' ? checked : value;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: newValue
    }));
  };

  const handleSliderChange = (event, value) => {
    setFormData((prevFormData) => ({
      ...prevFormData,
      selectedHour: value
    }));
  };

  const getWeekNumber = (date) => {
    const firstDayOfYear = new Date(date.getFullYear(), 0, 1);
    const daysOffset = 4 - firstDayOfYear.getDay();
    const firstThursday = new Date(firstDayOfYear.getTime());
    firstThursday.setDate(firstDayOfYear.getDate() + daysOffset);
    const weekNumber = Math.floor((date.getTime() - firstThursday.getTime()) / (7 * 24 * 60 * 60 * 1000)) + 1;
    return weekNumber;
  };

  const getQuarter = (month) => {
    return Math.ceil(month / 3);
  };

  const fetaureNamesHourly = [
    'Maximum_Humidity',
    'Solar_Radiation',
    'Day_Degree_Hot',
    'Day_Degree_Cold',
    'Average_Humidity',
    'Max_OutdoorTemp',
    'Average_OutdoorTemp',
    'Min_OutdoorTemp',
    'Year',
    'Quarter',
    'Month',
    'Week',
    'Day',
    'Hour',
    'Is_Holiday',
    'Is_Weekend'
  ];
  const fetaureNames = [
    'Maximum_Humidity',
    'Solar_Radiation',
    'Day_Degree_Hot',
    'Day_Degree_Cold',
    'Average_Humidity',
    'Max_OutdoorTemp',
    'Average_OutdoorTemp',
    'Min_OutdoorTemp',
    'Year',
    'Quarter',
    'Month',
    'Week',
    'Day',
    'Is_Holiday',
    'Is_Weekend'
  ];

  const handleSubmitRegression = async () => {
    const dateParts = formData.date.split('-');
    const isHourly = formData.horizon === 'Hourly';
    const input_data_hourly = [
      parseFloat(formData.maxHumidity),
      parseFloat(formData.solarRadiation),
      parseFloat(formData.dayDegreeHot),
      parseFloat(formData.dayDegreeCold),
      parseFloat(formData.avgHumidity),
      parseFloat(formData.maxOutdoorTemp),
      parseFloat(formData.avgTemp),
      parseFloat(formData.minOutdoorTemp),
      parseInt(dateParts[0]),
      getQuarter(parseInt(dateParts[1])),
      parseInt(dateParts[1]),
      getWeekNumber(new Date(formData.date)),
      parseInt(dateParts[2]),
      parseFloat(formData.selectedHour),
      formData.isWeekend ? 1.0 : 0.0,
      formData.isHoliday ? 1.0 : 0.0
    ];

    const input_data = [
      parseFloat(formData.maxHumidity),
      parseFloat(formData.solarRadiation),
      parseFloat(formData.dayDegreeHot),
      parseFloat(formData.dayDegreeCold),
      parseFloat(formData.avgHumidity),
      parseFloat(formData.maxOutdoorTemp),
      parseFloat(formData.avgTemp),
      parseFloat(formData.minOutdoorTemp),
      parseInt(dateParts[0]),
      getQuarter(parseInt(dateParts[1])),
      parseInt(dateParts[1]),
      getWeekNumber(new Date(formData.date)),
      parseInt(dateParts[2]),
      formData.isWeekend ? 1.0 : 0.0,
      formData.isHoliday ? 1.0 : 0.0
    ];

    setLoading(true);
    setPredictionResult(null);

    const energyTypeURL = formData.energyType.toLowerCase();
    const horizonURL = formData.horizon.toLowerCase();
    const endpointURL = `http://localhost:8000/api/models_prediction/predict/regression/${energyTypeURL}_${horizonURL}_xgboost`;

    try {
      const response = await axios.post(endpointURL, isHourly ? input_data_hourly : input_data, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      setPredictionResult(response.data.prediction);
    } catch (error) {
      // Handle errors
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitXAI = async (explanationType, setExplainResult) => {
    const dateParts = formData.date.split('-');
    const isHourly = formData.horizon === 'Hourly';
    const input_data_hourly = [
      parseFloat(formData.maxHumidity),
      parseFloat(formData.solarRadiation),
      parseFloat(formData.dayDegreeHot),
      parseFloat(formData.dayDegreeCold),
      parseFloat(formData.avgHumidity),
      parseFloat(formData.maxOutdoorTemp),
      parseFloat(formData.avgTemp),
      parseFloat(formData.minOutdoorTemp),
      parseInt(dateParts[0]),
      getQuarter(parseInt(dateParts[1])),
      parseInt(dateParts[1]),
      getWeekNumber(new Date(formData.date)),
      parseInt(dateParts[2]),
      parseFloat(formData.selectedHour),
      formData.isWeekend ? 1.0 : 0.0,
      formData.isHoliday ? 1.0 : 0.0
    ];

    const input_data = [
      parseFloat(formData.maxHumidity),
      parseFloat(formData.solarRadiation),
      parseFloat(formData.dayDegreeHot),
      parseFloat(formData.dayDegreeCold),
      parseFloat(formData.avgHumidity),
      parseFloat(formData.maxOutdoorTemp),
      parseFloat(formData.avgTemp),
      parseFloat(formData.minOutdoorTemp),
      parseInt(dateParts[0]),
      getQuarter(parseInt(dateParts[1])),
      parseInt(dateParts[1]),
      getWeekNumber(new Date(formData.date)),
      parseInt(dateParts[2]),
      formData.isWeekend ? 1.0 : 0.0,
      formData.isHoliday ? 1.0 : 0.0
    ];

    const energyTypeURL = formData.energyType.toLowerCase();
    const horizonURL = formData.horizon.toLowerCase();
    const endpointURL = `http://localhost:8000/api/models_prediction/xai/${explanationType}/${energyTypeURL}_${horizonURL}_xgboost`;
    console.log(fetaureNamesHourly);
    console.log(input_data_hourly);
    axios
      .post(endpointURL, {
        data: isHourly? input_data_hourly : input_data,
        feature_names: isHourly? fetaureNamesHourly : fetaureNames
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

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  return (
    <Card>
      <CardContent>
        <Stepper activeStep={activeStep} alternativeLabel>
          <Step>
            <StepLabel>Step 1 (Predictions)</StepLabel>
          </Step>
          <Step>
            <StepLabel>Step 2 (Explanations)</StepLabel>
          </Step>
        </Stepper>
        {activeStep === 0 && (
          <StepOneForm
            formData={formData}
            handleFormChange={handleFormChange}
            showHourSlider={formData.horizon === 'Hourly'}
            handleSliderChange={handleSliderChange}
            handleSubmit={handleSubmitRegression}
            handleBack={handleBack}
            handleGetExplanations={handleGetExplanations}
            activeStep={activeStep}
            loading={loading}
            predictionResult={predictionResult}
          />
        )}
        {activeStep === 1 && (
          <StepTwoForm handleBack={handleBack} shapResult={shapResult} limeResult={limeResult} anchorsResult={anchorsResult} predictionResult={predictionResult} target={formData.energyType} horizon={formData.horizon}/>
        )}
      </CardContent>
    </Card>
  );
};

export default ParentForm;
