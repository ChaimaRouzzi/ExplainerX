import React, { useState, useEffect } from 'react';
import { Card, Typography, Box, CircularProgress } from '@mui/material';
import { styled } from '@mui/system';

const StyledCard = styled(Card)({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  padding: '16px',
  maxWidth: '400px',
});

const ProgressCard = ({ icon, title, number, percentage, previousPercentage }) => {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setProgress(percentage);
    }, 500); // Adjust the interval duration for desired update speed

    return () => {
      clearInterval(timer);
    };
  }, [percentage]);

  const progressColor = 'rgba(0, 74, 173, 0.3)'; // Color for the progress percentage (green in this example)
  const remainingColor = '#004aad'; // Color for the remaining percentage (red in this example)
  const percentageDifference = previousPercentage !== null ? (percentage - previousPercentage).toFixed(2) : 0;
  const isIncrement = percentageDifference > 0;

  return (
    <StyledCard>
      <Box>
        {icon}
      </Box>
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
        <CircularProgress
          variant="determinate"
          value={progress}
          size={80}
          thickness={5}
          color="primary" // Set the primary color
          sx={{
            position: 'absolute',
            zIndex: 1,
            color: remainingColor,
            '& .MuiCircularProgress-bar': {
              backgroundColor: remainingColor, // Color for the remaining percentage
            },
          }}
        />
        <CircularProgress
          variant="determinate"
          value={100}
          size={80}
          thickness={5}
          color="primary" // Set the primary color
          sx={{
            color: progressColor, // Color for the progress percentage
            '& .MuiCircularProgress-bar': {
              borderRadius: '50%',
              backgroundColor: 'transparent',
            },
          }}
        />
        <Box
          top={0}
          left={0}
          bottom={0}
          right={0}
          position="absolute"
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <Typography variant="body2" component="div" color="textSecondary">{`${percentage}%`}</Typography>
        </Box>
      </Box>
    </StyledCard>
  );
};

export default ProgressCard;
