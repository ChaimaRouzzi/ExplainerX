import React, { useState, useEffect } from 'react';
import { styled } from '@mui/material/styles';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import StationarityTest from './stationarityTest';
import Decomposition from './decomposition';
import TimeSeriesPlot from './Acf';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import { StepLabel } from '@mui/material';
import { updateVersion, updateUpdated } from 'actions/actions';
import { useSelector, useDispatch } from 'react-redux';
import axios from 'axios';
import { Grid, Card } from '@mui/material';
import { gridSpacing } from 'store/constant';
import MainCard from 'ui-component/cards/MainCard';
import SkeletonEarningCard from 'ui-component/cards/Skeleton/EarningCard';
const StyledTabs = styled((props) => <Tabs {...props} TabIndicatorProps={{ children: <span className="MuiTabs-indicatorSpan" /> }} />)({
  '& .MuiTabs-indicator': {
    display: 'flex',
    justifyContent: 'center',
    backgroundColor: 'transparent'
  },
  '& .MuiTabs-indicatorSpan': {
    maxWidth: 90,
    width: '100%',
    backgroundColor: '#004aad'
  }
});

const StyledTab = styled((props) => <Tab disableRipple {...props} />)(({ theme }) => ({
  textTransform: 'none',
  fontWeight: theme.typography.fontWeightRegular,
  fontSize: theme.typography.pxToRem(15),
  marginRight: theme.spacing(1),
  color: 'rgba(255, 255, 255, 0.7)',
  '&.Mui-selected': {
    color: '#004aad',
    fontWeight: 'bold'
  },
  '&.Mui-focusVisible': {
    backgroundColor: 'rgba(100, 95, 228, 0.32)'
  },
  '&:not(.Mui-selected)': {
    // Styles for non-selected tabs
    color: 'black'
  }
}));

export default function CustomizedTabs() {
  const [value, setValue] = React.useState(0);
  const dispatch = useDispatch();
  const version = useSelector((state) => state.version);
  const updated = useSelector((state) => state.updated);
  const handleUpdateUpdated = (newValue) => {
    return new Promise((resolve) => {
      dispatch(updateUpdated(newValue));

      resolve();
    });
  };
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
  const [version_number, setVersionNumber] = useState(0);
  const [activeStep, setActiveStep] = useState(val == -1 ? 2 : val);
  const handleStepClick = (step, all) => {
    handleUpdateUpdated('False');
    setActiveStep(step);
    if (version !== step) {
      handleUpdateVersion(all === 1 ? -1 : step);
    }
  };
  const handleStepClick2 = (step, all) => {
    handleUpdateUpdated('True');
    setActiveStep(step);
    if (version !== step) {
      handleUpdateVersion(all === 1 ? -1 : step);
    }
  };
  const TabContent = ({ selectedTab }) => {
    if (selectedTab === 0) {
      return <StationarityTest ver={val} updated={updated} />;
    } else if (selectedTab === 1) {
      return <Decomposition ver={val} updated={updated} />;
    } else if (selectedTab === 2) {
      return <TimeSeriesPlot ver={val} updated={updated} />;
    } else {
      return null;
    }
  };

  useEffect(() => {
    axios.get(BaseURL).then((response) => {
      const result = JSON.parse(response.data);
      console.log(result);
      setVersionNumber(result.versions_number ? result.versions_number : 0);
      setUpdatedVersion(result.updated_version ? JSON.parse(result.updated_version) : []);
      setLoading(false);
    });
  }, []);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <>
      <Grid item xs={12}>
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
            <Card className="cardContainer">
              <StyledTabs value={value} onChange={handleChange} aria-label="styled tabs example" centered>
                <StyledTab label="Stationarity Test" />
                <StyledTab label="Time Series Decomposition" />
                <StyledTab label="ACF and PACF functions" />
              </StyledTabs>
              <Box sx={{ p: 8 }} />
            </Card>
          </Grid>
          <Grid item lg={12} md={12} sm={12} xs={12}>
            <TabContent selectedTab={value} />
          </Grid>
        </Grid>
      </Grid>
    </>
  );
}
