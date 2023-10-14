import React from 'react';
import ProgressCard from 'views/dataAnalysis/card';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
const UniqueValuesCard = ({ duplicates, uniqueValuesPercentage }) => {
  console.log(duplicates)
  return (
    <ProgressCard
      icon={<ContentCopyIcon fontSize="large" />}
      title="Duplicated Rows"
      number={duplicates?.num_duplicates}
      percentage={duplicates?.duplicate_percentage}
      previousPercentage={uniqueValuesPercentage?.duplicate_percentage}
    />
  );
};

export default UniqueValuesCard;
