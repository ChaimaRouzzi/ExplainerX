import React from 'react';
import ProgressCard from './card';
import BubbleChartIcon from '@mui/icons-material/BubbleChart';
const OutliersCard = ({ outliers, previousPercentage }) => {
  console.log(previousPercentage);
  return (
    <ProgressCard
    icon={<BubbleChartIcon fontSize="large" />}
    title="Outliers"
      number={outliers?.num_outliers}
      percentage={outliers?.percent_outliers}
      previousPercentage={previousPercentage?.percent_outliers}
    />
  );
};

export default OutliersCard;
