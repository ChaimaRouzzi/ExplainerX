import React, { useEffect } from 'react';
import { Card, Typography, Box } from '@mui/material';
import { styled } from '@mui/system';

const StyledCard = styled(Card)({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  padding: '16px',
  maxWidth: '400px',
  height:'120px',
  marginTop:'60px',
  marginBottom:'60px',
  boxShadow:'rgba(14, 30, 37, 0.12) 0px 2px 4px 0px, rgba(14, 30, 37, 0.32) 0px 2px 16px 0px;',
});

const ProgressCard = ({ title, number, percentage, previousPercentage }) => {


  useEffect(() => {
    const timer = setInterval(() => {
     
    }, 500); // Adjust the interval duration for desired update speed

    return () => {
      clearInterval(timer);
    };
  }, [percentage]);


  // Color for the remaining percentage (red in this example)
  const percentageDifference = previousPercentage !== null ? (percentage - previousPercentage).toFixed(2) : 0;
  const isIncrement = percentageDifference > 0;

  return (
    <StyledCard>

      <Box flex={1} mx={2}>
        <Typography variant="h4" style={{color:"#004aad"}}>{title}</Typography>
        <Typography variant="subtitle1">{number}</Typography>
        { previousPercentage != null && ( // Check if the title is not 'Data Types'
          <Typography variant="body2" color={isIncrement ? 'red' : 'green'}>
            {isIncrement ? (
              <span>&#9650;</span> // Down arrow symbol
              ) : (
              <span>&#9660;</span> 
            )}
            {Math.abs(percentageDifference)}%
          </Typography>
        )}
      </Box>
      <Box position="relative">
      
        
       
      </Box>
    </StyledCard>
  );
};

export default ProgressCard;
