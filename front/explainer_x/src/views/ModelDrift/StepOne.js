import React, { useState,useMemo} from 'react';
import { Grid, Button, Alert,  CircularProgress } from '@mui/material';
import { gridSpacing } from 'store/constant';
import MainCard from 'ui-component/cards/MainCard';
import FileUpload from 'react-material-file-upload'; // Make sure to import this correctly
import axios from 'axios';
import DisplayData from 'views/dataAnalysis/DisplayData';


const StepOne = ({ activeStep, handleBack, setActiveStep,files,setFiles}) => {
  
  const [errorMessage, setErrorMessage] = useState('');
  const [dataset, setDataset] = useState([]);
  const [loading, setLoading] = useState(false);



  const columns = useMemo(
    () => [
      {
        accessorKey: 'date', //access nested data with dot notation
        header: 'Date',
        size: 150
      },
      {
        accessorKey: 'Electricity',
        header: 'Electricity',
        size: 150
      },
      {
        accessorKey: 'Gas_01', //normal accessorKey
        header: 'Gas_01',
        size: 150
      },
      {
        accessorKey: 'Gas_02', //normal accessorKey
        header: 'Gas_02',
        size: 150
      },
      {
        accessorKey: 'Gas_03', //normal accessorKey
        header: 'Gas_03',
        size: 150
      },
      {
        accessorKey: 'Day_Degree_Cold', //normal accessorKey
        header: 'Day_Degree_Cold',
        size: 150
      },
      {
        accessorKey: 'Day_Degree_Hot',
        header: 'Day_Degree_Hot',
        size: 150
      },
      {
        accessorKey: 'Min_OutdoorTemp',
        header: 'Min_OutdoorTemp',
        size: 150
      },
      {
        accessorKey: 'Average_OutdoorTemp',
        header: 'Average_OutdoorTemp',
        size: 150
      },
      {
        accessorKey: 'Max_OutdoorTemp',
        header: 'Max_OutdoorTemp',
        size: 150
      },
      {
        accessorKey: 'Maximum_Humidity',
        header: 'Maximum_Humidity',
        size: 150
      },
      {
        accessorKey: 'Average_Humidity',
        header: 'Average_Humidity',
        size: 150
      },
      {
        accessorKey: 'Solar_Radiation',
        header: 'Solar_Radiation',
        size: 150
      },
      {
        accessorKey: 'Hour',
        header: 'Hour',
        size: 150
      },
      {
        accessorKey: 'Day',
        header: 'Day',
        size: 150
      },
      {
        accessorKey: 'Week',
        header: 'Week',
        size: 150
      },
      {
        accessorKey: 'Month',
        header: 'Month',
        size: 150
      },
      {
        accessorKey: 'Year',
        header: 'Year',
        size: 150
      }
    ],
    []
  );




  const handleSubmit = async () => {
    setErrorMessage('')
    setLoading(true)
    const formData = new FormData();
    formData.append('file', files[0]);
    console.log(formData)

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/uploud_file', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
 
      // Handle the response from the backend
      setDataset(JSON.parse(response.data))
      setLoading(false)
      
    } catch (error) {
      if (error.response && error.response.status === 400) {
        setErrorMessage(error.response.data.detail);
        setLoading(false)
      }
    }
  };

 
  return (
    <>
      <Grid container spacing={gridSpacing}>
        <Grid item lg={12} md={12} sm={12} xs={12}>
          <MainCard>
            <h3>Upload your new data file</h3>
            <Grid container spacing={gridSpacing} style={{ alignItems: 'center', textAlign: 'center', marginTop: '10px' }}>
              <Grid item lg={8} md={8} sm={12} xs={12}>
                {/* Make sure the FileUpload component is used correctly */}
                <FileUpload value={files} onChange={setFiles} />
              </Grid>
              <Grid item lg={3} md={3} sm={12} xs={12} style={{ margin: 'auto', textAlign: 'center' }}>
                <Button
                  className='bottun-color'
                  disabled={files.length === 0}
                  variant="contained"
                  color="primary"
                  style={{ width: '250px' }}
                  onClick={handleSubmit}
                >
                  Submit
                </Button>
              </Grid>
            </Grid>
            {loading &&  <div  style={{display:'flex',justifyContent:'center',textAlign:'center',marginTop:'10px'}}>
            <CircularProgress size={40} color="inherit" />
            </div>}
            {errorMessage && <Alert severity="error" style={{ marginTop: '20px' }}>{errorMessage}</Alert>}
            {dataset.length>0 &&  
            <div style={{marginTop:'100px'}}>     
             <h3>Display the uplouded data </h3>
             <DisplayData isLoading={false} data={dataset} columns={columns} />  
            </div>}
          </MainCard>
          {dataset.length> 0 && (
            <Grid container justifyContent="flex-end">
              <Button style={{marginRight:'20px'}}  className='bottun-color' disabled={activeStep === 0} onClick={handleBack}>
                Back
              </Button>
              <Button    className='bottun-color'  variant="contained" color="primary" onClick={()=>setActiveStep(1)}>
               Detect Drift
              </Button>
            </Grid>
          )}
        </Grid>

      </Grid>
    </>
  );
};

export default StepOne;
