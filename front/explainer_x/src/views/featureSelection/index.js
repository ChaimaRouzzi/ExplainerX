import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  Typography,
  TextField,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Button
} from '@mui/material';
import axios from 'axios';
import { useDispatch } from 'react-redux';
import { setSelectedFeatures as setSelectedFeaturesAction } from 'actions/featuresActions'; // Rename the imported action
import { useSelector } from 'react-redux';

const FeatureSelection = () => {
  const dispatch = useDispatch();
  const [predictionTarget, setPredictionTarget] = useState(null);
  const [horizon, setHorizon] = useState(null);
  const [method, setMethod] = useState(null);
  const [number, setNumber] = useState(null);
  const [fetchingData, setFetchingData] = useState(false);
  const [selectedFeatures, setSelectedFeatures] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (method && predictionTarget && number) {
          setFetchingData(true);
          setSelectedFeatures([]);
          const response = await axios.post(`http://localhost:8000/api/feature_selection/${method}`, null, {
            params: {
              target: predictionTarget,
              horizon: horizon, 
              k: number
            }
          });
          const data = response.data;
          setSelectedFeatures(data.selected_features);
          dispatch(setSelectedFeaturesAction(data.selected_features));
          setFetchingData(false);
        }
      } catch (error) {
        console.error(error);
        setFetchingData(false);
      }
    };

    fetchData();
  }, [method, predictionTarget, number]);
  const selectedFeaturesFromRedux = useSelector((state) => state.feature.selectedFeatures);

  console.log(selectedFeaturesFromRedux);

  return (
    <div>
      <Card style={{ marginBottom: '20px' }}>
        <CardContent>
          <Typography variant="h3" align="left" gutterBottom style={{ marginBottom: '30px' }}>
            Feature Selection
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <FormControl fullWidth variant="outlined">
                <InputLabel>Prediction Target</InputLabel>
                <Select
                  name="target"
                  value={predictionTarget}
                  onChange={(e) => setPredictionTarget(e.target.value)}
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
              <FormControl fullWidth variant="outlined">
                <InputLabel>Horizon</InputLabel>
                <Select name="horizon" value={horizon} onChange={(e) => setHorizon(e.target.value)} label="Horizon">
                  <MenuItem value="Hourly">Hourly</MenuItem>
                  <MenuItem value="Daily">Daily</MenuItem>
                  <MenuItem value="Weekly">Weekly</MenuItem>
                  <MenuItem value="Monthly">Monthly</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={6}>
              <TextField
                name="features_number"
                label="Number of Features"
                variant="outlined"
                type="number"
                value={number}
                onChange={(e) => setNumber(e.target.value)}
                fullWidth
              />
            </Grid>
            <Grid item xs={6}>
              <FormControl fullWidth variant="outlined">
                <InputLabel>Feature Selection Method</InputLabel>
                <Select name="method" value={method} onChange={(e) => setMethod(e.target.value)} label="Feature Selection Method">
                  <MenuItem value="pearson">Pearson Correlation</MenuItem>
                  <MenuItem value="kendall">Kendall Correlation</MenuItem>
                  <MenuItem value="spearman">Spearman Correlation</MenuItem>
                  <MenuItem value="mutual_info">Mutual Information Score</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>

          {fetchingData && (
            <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
              <CircularProgress />
            </div>
          )}

          {selectedFeatures.length > 0 && (
            <div style={{ marginTop: '20px', width: '300px' }}>
              <Typography variant="h4" gutterBottom>
                Selected Features:
              </Typography>
              <List>
                {selectedFeatures.map((feature, index) => (
                  <ListItem key={index} sx={{ borderBottom: '1px solid #e0e0e0' }}>
                    <ListItemText primary={feature} />
                  </ListItem>
                ))}
              </List>
            </div>
          )}

          {selectedFeatures.length > 0 && (
            <Grid container justifyContent="center">
              <Button
                type="submit"
                variant="contained"
                color="primary"
                style={{ width: '300px' }}
                sx={{
                  textAlign: 'center',
                  padding: '8px 40px',
                  backgroundColor: '#004aad',
                  marginBottom: '30px',
                  '&:hover': {
                    backgroundColor: '#004aad'
                  }
                }}
              >
                Use Selected Features For Model Building
              </Button>
            </Grid>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default FeatureSelection;
