import React from 'react';
import ProgressCard from './card';
import PanoramaFishEyeIcon from '@mui/icons-material/PanoramaFishEye';
const ZeroValuesCard = ({ zeroValues, zeroValuesPercentage }) => {
  return (
    <ProgressCard
      icon={<PanoramaFishEyeIcon fontSize="large" />}
      title="Zero Values"
      number={zeroValues?.zero_values}
      percentage={zeroValues?.zero_percentage}
      previousPercentage={zeroValuesPercentage?.zero_percentage}
    />
  );
};

export default ZeroValuesCard;
