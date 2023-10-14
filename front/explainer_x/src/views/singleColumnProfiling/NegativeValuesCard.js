import React from 'react';
import ProgressCard from './card';
import RemoveIcon from '@mui/icons-material/Remove';

const NegativeValuesCard = ({ negativeValues, negativeValuesPercentage }) => {
  return (
    <ProgressCard
      icon={<RemoveIcon fontSize="large" />}
      title="Negative Values"
      number={negativeValues?.negative_values}
      percentage={negativeValues?.negative_percentage}
      previousPercentage={negativeValuesPercentage?.negative_percentage}
    />
  );
};

export default NegativeValuesCard;
