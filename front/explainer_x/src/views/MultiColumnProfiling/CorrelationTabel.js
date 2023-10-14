import { MaterialReactTable } from 'material-react-table';
import React  from 'react';

//nested data is ok, see accessorKeys in ColumnDef below

import TotalIncomeCard from 'ui-component/cards/Skeleton/TotalIncomeCard';

const CorrelationTbael = ({isLoading,data,columns}) => {

    const val = data.map( (row,index )=> {
      
        const newRow = {};
      
        const columnName = columns[index +1] ? columns[index+1] : ''; // Get the corresponding column name
       
          newRow[columns[0].accessorKey] =columnName.header;
          const combin={...newRow,...row}
        
        return combin;
      });
     
     
  return (
    <>
    {isLoading ? (
      <TotalIncomeCard />
    ) : (
      <MaterialReactTable data={val} columns={columns} />)}
   
</>  
)

  }

export default CorrelationTbael