import React from 'react';
import ProgressCard from 'views/dataAnalysis/card';
import BubbleChartIcon from '@mui/icons-material/BubbleChart';
const OutliersCard = ({ outliers, previousPercentage }) => {
  console.log(outliers)
  return (
    <ProgressCard
    icon={<BubbleChartIcon fontSize="large" />}
    title="Outliers"
      number={outliers?.num_outliers}
      percentage={outliers?.outlier_percentage}
      previousPercentage={previousPercentage?.percent_outliers}
    />
  );
};

export default OutliersCard;
