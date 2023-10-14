import React from 'react';
import ProgressCard from './card';
import DataObjectIcon from '@mui/icons-material/DataObject';const DataTypesCard = ({ dataTypes }) => {
  return (
    <ProgressCard
      icon={<DataObjectIcon fontSize="large" />}
      title="Data Type"
      number={dataTypes?.[0]} // Assuming the data types API returns an array with one element
      percentage={100}
    />
  );
};

export default DataTypesCard;
