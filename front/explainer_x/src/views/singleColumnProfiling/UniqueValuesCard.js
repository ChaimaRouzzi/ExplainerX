import React from 'react';
import ProgressCard from './card';
import LooksOneIcon from '@mui/icons-material/LooksOne';
const UniqueValuesCard = ({ uniqueValues, uniqueValuesPercentage }) => {
  return (
    <ProgressCard
      icon={<LooksOneIcon fontSize="large" />}
      title="Unique Values"
      number={uniqueValues?.unique_values}
      percentage={uniqueValues?.unique_percentage}
      previousPercentage={uniqueValuesPercentage?.unique_percentage}
    />
  );
};

export default UniqueValuesCard;
