import React, { useState } from 'react';
import { Stepper, Step, StepLabel, Card, CardContent } from '@mui/material';
import StepOne from './StepOne';
import StepTow from './StepTow';


const ParentForm = () => {
  const [files, setFiles] = useState([]);
  const [activeStep, setActiveStep] = useState(0);
  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  return (
    <Card>
      <CardContent>
      <Stepper
          activeStep={activeStep}
          alternativeLabel
        >
          <Step>
            <StepLabel>Step 1 (Load your Data)</StepLabel>
          </Step>
          <Step>
            <StepLabel>Step 2 (Detect Drift)</StepLabel>
          </Step>
        </Stepper>
        {activeStep === 0 && (
          <StepOne activeStep={activeStep} handleBack={handleBack} setActiveStep={setActiveStep} files={files}  setFiles={setFiles}/>
        )}

        {activeStep === 1 && 
         <StepTow  handleBack={handleBack}  files={files}/>}
      </CardContent>
    </Card>
  );
};

export default ParentForm;
