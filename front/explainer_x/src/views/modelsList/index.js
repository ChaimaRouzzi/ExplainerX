import React, { useState, useEffect } from 'react';
import { Accordion, AccordionSummary, AccordionDetails, Typography, Grid, Paper, Card, CardContent } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import RemoveCircleOutlineIcon from '@mui/icons-material/RemoveCircleOutline';
import SkeletonEarningCard from 'ui-component/cards/Skeleton/EarningCard';
import axios from 'axios';

const AccordionList = () => {
  const [modelsList, setModelsList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedAccordion, setExpandedAccordion] = useState(null);

  useEffect(() => {
    const getModelsList = async () => {
      try {
        setLoading(true);
        const response = await axios.get('http://localhost:8000/api/models_building/models_list/');
        setModelsList(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching model list:', error);
      }
    };

    getModelsList();
  }, []);

  const handleAccordionChange = (panel) => (event, isExpanded) => {
    setExpandedAccordion(isExpanded ? panel : -1);
  };

  const getModelSummary = (model) => {
    try {
      const modelDetails = JSON.parse(model.model_details);

      return (
        <div>
          <Typography style={{ fontWeight: 'bold' }}>{modelDetails.model_name}</Typography>
        </div>
      );
    } catch (error) {
      console.error('Error parsing model details:', error);
      return <Typography>Error parsing model details</Typography>;
    }
  };

  const getModelDetails = (model) => {
    try {
      const modelDetails = JSON.parse(model.model_details);
      const params = modelDetails.params;
      const performance = modelDetails.performance;
      const target = params.target;
      const horizon = params.horizon;
      const test_size = params.test_size;
      const model_name = params.model_name;
      const predictors = params.predictors;

      delete params.target;
      delete params.horizon;
      delete params.all_predictors;
      delete params.test_size;
      delete params.model_name;
      delete params.predictors;

      return (
        <Grid>
          <div style={{ marginBottom: '20px' }}>
            <Typography variant="h4" style={{ marginBottom: '10px', color: '#004aad' }}>
              Model Information:
            </Typography>
            <Typography variant="body1">
              <span style={{ fontWeight: 'bold' }}>Model name:</span> {model_name}
            </Typography>
            <Typography variant="body1">
              <span style={{ fontWeight: 'bold' }}>Target:</span> {target}
            </Typography>
            <Typography variant="body1">
              <span style={{ fontWeight: 'bold' }}>Horizon:</span> {horizon}
            </Typography>
            <Typography variant="body1">
              <span style={{ fontWeight: 'bold' }}>Selected Features:</span> {predictors.join(', ')} {/* Join with commas and space */}
            </Typography>
            {test_size && (
              <Typography variant="body1">
                <span style={{ fontWeight: 'bold' }}>Test size:</span> {test_size}%
              </Typography>
            )}
          </div>

          <div style={{ marginBottom: '20px' }}>
            <Typography variant="h4" style={{ marginBottom: '10px', color: '#004aad' }}>
              Model Parameters:
            </Typography>
            {Object.entries(params).map(([key, value]) => (
              <div key={key}>
                <Typography variant="body1">
                  <span style={{ fontWeight: 'bold' }}>{key}:</span> {value}
                </Typography>
              </div>
            ))}
          </div>
          {performance && (
            <div>
              <Typography variant="h4" style={{ marginBottom: '10px', color: '#004aad' }}>
                Model Performance:
              </Typography>
              {Object.entries(performance).map(([key, value]) => (
                <div key={key}>
                  <Typography variant="body1">
                    <span style={{ fontWeight: 'bold' }}>{key}:</span> {value}
                  </Typography>
                </div>
              ))}
            </div>
          )}
        </Grid>
      );
    } catch (error) {
      console.error('Error parsing model details:', error);
      return <Typography>Error parsing model details</Typography>;
    }
  };

  return (
    <div>
      {loading ? (
        <SkeletonEarningCard />
      ) : (
        <Card style={{ marginBottom: '20px' }}>
          <CardContent>
            <Typography variant="h4" style={{ marginBottom: '20px', color: '#004aad' }}>
              Built Models Traceability
            </Typography>
            {modelsList.length === 0 ? ( // Check if modelsList is empty
              <Typography variant="body1"> You haven&apos;t built any models yet.</Typography>
            ) : (
              modelsList.map((item, index) => (
                <Accordion key={index} expanded={expandedAccordion === index} onChange={handleAccordionChange(index)}>
                  <AccordionSummary
                    expandIcon={
                      expandedAccordion === index ? (
                        <RemoveCircleOutlineIcon style={{ color: '#004aad' }} />
                      ) : (
                        <AddCircleOutlineIcon style={{ color: '#004aad' }} />
                      )
                    }
                  >
                    {getModelSummary(item)}
                  </AccordionSummary>
                  <AccordionDetails>
                    <Paper elevation={0} style={{ padding: '20px', backgroundColor: '#f5f5f5' }}>
                      {getModelDetails(item)}
                    </Paper>
                  </AccordionDetails>
                </Accordion>
              ))
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default AccordionList;
