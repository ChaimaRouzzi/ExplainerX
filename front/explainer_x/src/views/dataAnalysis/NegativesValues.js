import React from 'react';
import ProgressCard from 'views/dataAnalysis/card';
import RemoveIcon from '@mui/icons-material/Remove';

const NegativeValuesCard = ({ negativeValues, negativeValuesPercentage }) => {
  console.log(negativeValues)
  return (
    <ProgressCard
      icon={<RemoveIcon fontSize="large" />}
      title="Negative Values"
      number={negativeValues?.num_negatives}
      percentage={negativeValues?.negative_percentage}
      previousPercentage={negativeValuesPercentage?.negative_percentage}
    />
  );
};

export default NegativeValuesCard;
