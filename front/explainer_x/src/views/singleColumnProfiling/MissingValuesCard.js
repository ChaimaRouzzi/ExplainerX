import React from 'react';
import ProgressCard from './card';
import RuleIcon from '@mui/icons-material/Rule';

const MissingValuesCard = ({ missingValues, previousPercentage }) => {
  console.log(previousPercentage);
  return (
    <ProgressCard
      icon={<RuleIcon fontSize="large" />}
      title="Missing Values"
      number={missingValues?.missing_values}
      percentage={missingValues?.missing_values_percentage}
      previousPercentage={previousPercentage?.missing_values_percentage}
    />
  );
};

export default MissingValuesCard;
