import React from 'react';
import ProgressCard from 'views/dataAnalysis/card';
import RuleIcon from '@mui/icons-material/Rule';

const MissingValuesCard = ({ missingValues, previousPercentage }) => {
  console.log(missingValues)
  return (
    <ProgressCard
      icon={<RuleIcon fontSize="large" />}
      title="Missing Values"
      number={missingValues?.num_missing_values}
      percentage={missingValues?.missing_percentage}
      previousPercentage={previousPercentage?. missing_percentage}
    />
  );
};

export default MissingValuesCard;
