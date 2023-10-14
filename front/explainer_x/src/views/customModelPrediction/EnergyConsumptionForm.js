import React, { useState } from 'react';
import { Stepper, Step, StepLabel, Card, CardContent } from '@mui/material';
import StepOneForm from './StepOne';
import StepTwoForm from './StepTwo';

const ParentForm = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [shapResult, setShapResult] = useState(null);
  const [limeResult, setLimeResult] = useState(null);
  const [anchorsResult, setAnchorsResult] = useState(null);
  const [predictionResult, setPredictionResult] = useState(null);
  const [target, setTarget] = useState('');
  const [horizon, setHorizon] = useState('');


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
            activeStep={activeStep}
            handleBack={handleBack}
            setActiveStep={setActiveStep}
            setShapResult={setShapResult}
            n
            setLimeResult={setLimeResult}
            setAnchorsResult={setAnchorsResult}
            predictionResult={predictionResult}
            setPredictionResult={setPredictionResult}
            target={target}
            setTarget={setTarget}
            horizon={horizon}
            setHorizon={setHorizon}
          />
        )}
        {activeStep === 1 && (
          <StepTwoForm
            handleBack={handleBack}
            shapResult={shapResult}
            limeResult={limeResult}
            anchorsResult={anchorsResult}
            predictionResult={predictionResult}
            target={target}
            horizon={horizon}
          />
        )}
      </CardContent>
    </Card>
  );
};

export default ParentForm;
