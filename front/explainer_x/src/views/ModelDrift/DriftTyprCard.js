import React from 'react';
import ProgressCard from './DriftCard';
import RuleIcon from '@mui/icons-material/Rule';

const DriftTypeCard = ({ type , title }) => {
  
  return (
    <ProgressCard
      icon={<RuleIcon fontSize="large" />}
      title={title}
      number={type}
      percentage={null}
      previousPercentage={null}
    />
  );
};

export default DriftTypeCard;
