import React, { useState, useEffect } from 'react';
import { Button, List, ListItem, ListItemText, Paper, Box,Grid } from '@mui/material';
import ChatGPTLogo from '../../assets/images/chatgpt_logo.png';
import Plot from 'react-plotly.js';
import axios from 'axios';
import SkeletonEarningCard from 'ui-component/cards/Skeleton/EarningCard';

const StepTwoForm = ({ handleBack, shapResult, limeResult, anchorsResult, predictionResult, target, horizon }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [isLoading2, setIsLoading2] = useState(false);
  const [isLoading3, setIsLoading3] = useState(false);
  const [isLoading4, setIsLoading4] = useState(false);

  const sortedShapResult = shapResult ? shapResult.slice().sort((a, b) => Math.abs(b.importance) - Math.abs(a.importance)) : [];
  const sortedLimeResult = limeResult ? limeResult.slice().sort((a, b) => Math.abs(b.importance) - Math.abs(a.importance)) : [];

  const shapFeatures = sortedShapResult.map((item) => item.feature);
  const shapImportances = sortedShapResult.map((item) => item.importance);
  const shapColors = sortedShapResult.map((item) => (item.importance < 0 ? 'rgba(255, 0, 0, 0.7)' : 'rgba(0, 128, 0, 0.7)'));

  const limeFeatures = sortedLimeResult.map((item) => item.feature);
  const limeImportances = sortedLimeResult.map((item) => item.importance);
  const limeColors = sortedLimeResult.map((item) => (item.importance < 0 ? 'rgba(255, 0, 0, 0.7)' : 'rgba(0, 128, 0, 0.7)'));
  const dataObject = anchorsResult ? JSON.parse(anchorsResult) : {};

  const explanationNames = dataObject.Anchor;
  const [ShapInterpretation, setShapInterpretation] = useState('');
  const [LimeInterpretation, setLimeInterpretation] = useState('');
  const [AnchorsInterpretation, setAnchorsInterpretation] = useState('');

  const handleExplainClick = async (method, xaiResult) => {
    if (method == 'shap') {
      setIsLoading2(true);
    } else if (method == 'lime') {
      setIsLoading3(true);
    } else if (method == 'anchors') {
      setIsLoading4(true);
    }
    try {
      const response = await axios.post('http://localhost:8000/api/models_prediction/chat/', {
        method: method,
        xaiResult: xaiResult,
        target: target,
        horizon: horizon,
        prediction: predictionResult
      });

      if (response.status === 200) {
        if (method == 'shap') {
          setShapInterpretation(response.data.response);
        } else if (method == 'lime') {
          setLimeInterpretation(response.data.response);
        } else if (method == 'anchors') {
          setAnchorsInterpretation(response.data.response);
        }
      } else {
        console.error('Error:', response.statusText);
      }
      setIsLoading2(false);
      setIsLoading3(false);
      setIsLoading4(false);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  useEffect(() => {
    if (shapResult && limeResult && anchorsResult && predictionResult && target && horizon) {
      setIsLoading(false);
    }
  }, [shapResult, limeResult, anchorsResult, predictionResult, target, horizon]);

  return (
    <div>
      {isLoading ? (
        <SkeletonEarningCard />
      ) : (
        <div style={{ textAlign: 'left' }}>
          <h2 style={{ color: '#004aad' }}>Feature Importance Explainers</h2>
          <h3>SHAP Values</h3>
          <Plot
            data={[
              {
                y: shapFeatures.reverse(),
                x: shapImportances.reverse(),
                type: 'bar',
                orientation: 'h',
                marker: {
                  color: shapColors.reverse(),
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
           <Grid item lg={4} md={4} sm={12} xs={12}>
          <Button
            variant="contained"
            style={{ backgroundColor: '#74AA9C', color: 'white', marginTop: '15px' ,marginLeft:'0px'}}
            startIcon={<img src={ChatGPTLogo} alt="ChatGPT Logo" style={{ width: '30px', height: '30px' }} />}
            onClick={() => handleExplainClick('shap', shapResult)}
          >
            Explain SHAP Result with ChatGPT
          </Button>
          </Grid>
          {isLoading2 ? (
            <SkeletonEarningCard />
          ) : (
            ShapInterpretation && (
              <div style={{ marginTop: '30px' }}>
                <h3>ChatGPT Response:</h3>
                <div className="chat-bubble">
                  <p>{ShapInterpretation}</p>
                </div>
              </div>
            )
          )}
        </div>
      )}

      {isLoading ? (
        <SkeletonEarningCard />
      ) : (
        <div style={{ textAlign: 'left', marginTop: '60px' }}>
          <h3>LIME Values</h3>
          <Plot
            data={[
              {
                y: limeFeatures.reverse(),
                x: limeImportances.reverse(),
                type: 'bar',
                orientation: 'h',
                marker: {
                  color: limeColors.reverse(),
                  colorbar: false
                }
              }
            ]}
            layout={{
              title: 'LIME Feature Importances',
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
            <Grid item lg={4} md={4} sm={12} xs={12}>
          <Button
            variant="contained"
            style={{ backgroundColor: '#74AA9C', color: 'white', marginTop: '15px' }}
            startIcon={<img src={ChatGPTLogo} alt="ChatGPT Logo" style={{ width: '30px', height: '30px' }} />}
            onClick={() => handleExplainClick('lime', limeResult)}
          >
            Explain LIME Result with ChatGPT
          </Button>
          </Grid>
          {isLoading3 ? (
            <SkeletonEarningCard />
          ) : (
            LimeInterpretation && (
              <div style={{ marginTop: '30px' }}>
                <h3>ChatGPT Response:</h3>
                <div className="chat-bubble">
                  <p>{LimeInterpretation}</p>
                </div>
              </div>
            )
          )}
        </div>
      )}
      {isLoading ? (
        <SkeletonEarningCard />
      ) : (
        <Box style={{ textAlign: 'left', marginTop: '60px' }}>
          <h2 style={{ color: '#004aad' }}>Rule Based Explainer</h2>
          <h3>Anchors Values</h3>
          <Paper elevation={3} className="container">
            <List style={{ marginLeft: '25px' }}>
              {explanationNames?.map((anchor, index) => (
                <ListItem style={{ marginTop: '10px' }} key={index} disablePadding>
                  <ListItemText primary={anchor} />
                </ListItem>
              ))}
            </List>
          </Paper>
          <Grid item lg={4} md={4} sm={12} xs={12}>
          <Button
            variant="contained"
            style={{ backgroundColor: '#74AA9C', color: 'white', marginTop: '30px' }}
            startIcon={<img src={ChatGPTLogo} alt="ChatGPT Logo" style={{ width: '30px', height: '30px' }} />}
            onClick={() => handleExplainClick('anchors', anchorsResult)}
          >
            Explain Anchors Result with ChatGPT
          </Button>
          </Grid>
          {isLoading4 ? (
            <SkeletonEarningCard />
          ) : (
            AnchorsInterpretation && (
              <div style={{ marginTop: '30px' }}>
                <h3>ChatGPT Response:</h3>
                <div className="chat-bubble">
                  <p>{AnchorsInterpretation}</p>
                </div>
              </div>
            )
          )}
        </Box>
      )}

      <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'flex-end' }}>
        <Button onClick={handleBack}>Back</Button>
      </div>
    </div>
  );
};

export default StepTwoForm;
