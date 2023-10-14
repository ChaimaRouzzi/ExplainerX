import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import SkeletonEarningCard from 'ui-component/cards/Skeleton/EarningCard';



const ElectricityCorelation = ({ data, isLoading }) =>{
    console.log(data)
  return (
    <>
    {isLoading?<SkeletonEarningCard/>:
    (<TableContainer component={Paper}>
      <Table  aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell style={{width:"300"}} >Column</TableCell>
            <TableCell >Correlation</TableCell>
            
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((row,index) => (
            <TableRow
              key={index}
             style={{textAlign:'center'}}
            >
             
              <TableCell align="left">{row.column}</TableCell>
              <TableCell align="left">{row.correlation}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>)}
    
    </>
  );
}
export default ElectricityCorelation