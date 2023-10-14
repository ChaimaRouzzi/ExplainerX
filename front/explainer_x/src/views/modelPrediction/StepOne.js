import React from 'react';
import {
  Button,
  TextField,
  FormControl,
  Select,
  MenuItem,
  Checkbox,
  FormGroup,
  FormControlLabel,
  Grid,
  Slider,
  Typography,
  CircularProgress,
  InputLabel
} from '@mui/material';

const verticalSpacing = { marginBottom: '20px' };

const StepOneForm = ({
  formData,
  handleFormChange,
  showHourSlider,
  handleSliderChange,
  handleSubmit,
  handleBack,
  handleGetExplanations,
  activeStep,
  loading,
  predictionResult
}) => {
  if (!formData.date) {
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, '0');
    const day = String(currentDate.getDate()).padStart(2, '0');
    formData.date = `${year}-${month}-${day}`;
  }
  const showButtons = !!predictionResult;
  let formattedPredictionText = '';
  if (predictionResult !== null) {
    if (formData.energyType === 'Electricity') {
      formattedPredictionText = (
        <span style={{ fontSize: '17px', fontWeight: 'bold' }}>
          Predicted Electricity consumption: <span style={{ color: 'green' }}>{predictionResult} KW/h</span>
        </span>
      );
    } else if (formData.energyType === 'Gas') {
      formattedPredictionText = (
        <span style={{ fontSize: '17px', fontWeight: 'bold' }}>
          Predicted Gas consumption: <span style={{ color: 'green' }}>{predictionResult} MW/h</span>
        </span>
      );
    }
  }

  return (
    <div style={{ marginTop: 20 }}>
      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}>
          <FormControl fullWidth variant="outlined" style={verticalSpacing}>
            <InputLabel>Prediction Target</InputLabel>
            <Select name="energyType" value={formData.energyType} onChange={handleFormChange} label="Prediction Target">
              <MenuItem value="Electricity">Electricity</MenuItem>
              <MenuItem value="Gas">Gas</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} sm={6}>
          <FormControl fullWidth variant="outlined" style={verticalSpacing}>
            <InputLabel>Horizon</InputLabel>
            <Select name="horizon" value={formData.horizon} onChange={handleFormChange} label="Horizon">
              <MenuItem value="Hourly">Hourly</MenuItem>
              <MenuItem value="Daily">Daily</MenuItem>
              <MenuItem value="Weekly">Weekly</MenuItem>
              <MenuItem value="Monthly">Monthly</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            label="Date"
            type="date"
            name="date"
            value={formData.date}
            onChange={handleFormChange}
            InputLabelProps={{
              shrink: true
            }}
          />
        </Grid>
        {showHourSlider && (
          <Grid item xs={12} sm={6}>
            <Typography id="hour-slider" gutterBottom>
              Select Hour:
            </Typography>
            <Slider
              name="selectedHour"
              value={formData.selectedHour}
              onChange={handleSliderChange}
              valueLabelDisplay="auto"
              step={1}
              marks
              min={0}
              max={23}
              sx={{
                color: '#004aad'
              }}
              aria-labelledby="hour-slider"
            />
          </Grid>
        )}
        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            label="Max Outdoor Temperature"
            type="number"
            name="maxOutdoorTemp"
            value={formData.maxOutdoorTemp}
            onChange={handleFormChange}
          />
        </Grid>
        {
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Min Outdoor Temperature"
              type="number"
              name="minOutdoorTemp"
              value={formData.minOutdoorTemp}
              onChange={handleFormChange}
            />
          </Grid>
        }
        {
          <Grid item xs={12} sm={6}>
            <TextField fullWidth label="Average Outdoor Temperature" type="number" name="avgTemp" value={formData.avgTemp} onChange={handleFormChange} />
          </Grid>
        }
        {
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Solar Radiation"
              type="number"
              name="solarRadiation"
              value={formData.solarRadiation}
              onChange={handleFormChange}
            />
          </Grid>
        }
        {
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Max Humidity"
              type="number"
              name="maxHumidity"
              value={formData.maxHumidity}
              onChange={handleFormChange}
            />
          </Grid>
        }
        {
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Average Humidity"
              type="number"
              name="avgHumidity"
              value={formData.avgHumidity}
              onChange={handleFormChange}
            />
          </Grid>
        }
        {
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Day Degree Hot"
              type="number"
              name="dayDegreeHot"
              value={formData.dayDegreeHot}
              onChange={handleFormChange}
            />
          </Grid>
        }
        {
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Day Degree Cold"
              type="number"
              name="dayDegreeCold"
              value={formData.dayDegreeCold}
              onChange={handleFormChange}
            />
          </Grid>
        }
        {
          <Grid item xs={12}>
            <FormControl component="fieldset">
              <FormGroup>
                <FormControlLabel
                  control={<Checkbox checked={formData.isWeekend} onChange={handleFormChange} name="isWeekend" />}
                  label="Weekend"
                />
                <FormControlLabel
                  control={<Checkbox checked={formData.isHoliday} onChange={handleFormChange} name="isHoliday" />}
                  label="Holiday"
                />
              </FormGroup>
            </FormControl>
          </Grid>
        }
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
