import { MaterialReactTable } from 'material-react-table';
import React from 'react';

//nested data is ok, see accessorKeys in ColumnDef below

import TotalIncomeCard from 'ui-component/cards/Skeleton/TotalIncomeCard';

const DisplayData = ({isLoading,data,columns}) => {

 
  return (
    <>
    {isLoading ? (
      <TotalIncomeCard />
    ) : (
      <MaterialReactTable data={data} columns={columns} />)}
   
</>  
)

  }

export default DisplayData