import React, { useState,useEffect} from 'react';
import { Grid, Button, Alert } from '@mui/material';
import { gridSpacing } from 'store/constant';
import MainCard from 'ui-component/cards/MainCard';
import DriftTypeCard from './DriftTyprCard';
import axios from 'axios';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import InteractionPlot from './Plot';
import { red, green, blue } from '@mui/material/colors';



import {
    Card,
    CardContent,
    Select,
    MenuItem,
    Typography,
    CircularProgress,
   
  } from '@mui/material';
const StepTow = ({ handleBack,files}) => {
  const [open, setOpen] = React.useState(false);

 

 
    

  const [loading, setLoading] = useState(false);
  const [showPlot, setShowPlot] = useState(true);
  const [loading2, setLoading2] = useState(false);
  const [loading3, setLoading3] = useState(false);
  const [loading4, setLoading4] = useState(true);
  const [write, setWrite] = useState(false);
  
  
//   const [models,setModels]=useState(['XGboost','SVR','Random Forest'])
  console.log(loading)
 
  const [selectedModel, setSelectedModel] = useState('');
  const [modelsList, setModelsList] = useState([]);
  const drifts=['Data Drift','Concept Drift']  
  const [driftType,setDriftType]=useState(drifts[0]) 
  const [isDataDrift,setIsDataDrift]=useState(false) 
  const [isCinceptDrift,setIsCinceptDrift]=useState(false) 
  const [DataDriftResult,setDataDriftResult]=useState([]) 
  const [conceptIndex,setConceptIndex]=useState(-1) 
  const [mea,setMea]=useState(0) 
  const [msa,setMse]=useState(0)  
  const [rmse,setRmse]=useState(0) 
  const [mea2,setMea2]=useState(0) 
  const [msa2,setMse2]=useState(0)  
  const [rmse2,setRmse2]=useState(0) 
 
  const [mea3,setMea3]=useState(0) 
  const [msa3,setMse3]=useState(0)  
  const [rmse3,setRmse3]=useState(0) 
  console.log(loading3,mea3,rmse3,msa3)

  const [shap,setSHap]=useState([]) 
  const [data,setData]=useState([]) 
  const [target,setTarget]=useState('')
  
  const Data_methods = [
    {
      value: 'KS',
      label: '	Kolmogorov-Smirnov test',
      description:
        'The Kolmogorov-Smirnov test is a statistical method used for detecting data drift in two sets of continuous or ordinal data distributions. It compares the cumulative distribution functions (CDFs) of the two datasets and computes the maximum vertical distance between them, known as the Kolmogorov-Smirnov statistic. If this statistic exceeds a critical value, it indicates significant drift between the distributions, highlighting potential changes in the data generating process.'
    },
    {
      value: 'KL',
      label: 'Kullback-Leibler divergence',
      description:
        'The Kullback-Leibler (KL) divergence test is a method for detecting data drift. It measures the difference between the probability distributions of two datasets, indicating the extent of divergence between them. By quantifying the information lost when one distribution is used to approximate the other, the KL divergence test serves as a statistical measure for identifying changes in data distribution, which can help detect shifts or drifts between datasets in various applications, such as monitoring model performance or detecting changes in real-time data streams.'
    },
    {
      value: 'EMD',
      label: "Earth Mover's distance",
      description: "Earth Mover's Distance (EMD) is a data drift detection method that quantifies the dissimilarity between two probability distributions by measuring the minimum cost required to transform one distribution into another. It's commonly used to assess changes between datasets or distributions, making it valuable for identifying shifts in data characteristics, such as in machine learning models monitoring and anomaly detection in various fields."
    }
   
  ];
  
  const Concept_methods = [
    {
      value: 'DDM',
      label: 'DDM',
      description:
        'The Drift Detection Method (DDM) is a concept drift detection technique used in machine learning. It operates by monitoring changes in the distribution of incoming data and alerts when a significant shift, or concept drift, occurs. DDM is particularly effective for detecting gradual drifts in data streams and helps maintain model accuracy by enabling timely adaptations to changing data patterns.'
    },
    {
      value: 'EDDM',
      label: 'EDDM',
      description:
        'EDDM (Early Drift Detection Method) is a concept drift detection technique used in machine learning to identify shifts in data distribution. It operates by comparing statistical measures of data chunks, aiming to promptly detect distributional changes. EDDM is particularly effective for early detection of concept drift, making it valuable in adaptive learning systems and real-time data analysis.'
    },
    {
      value: 'ADWIN',
      label: "Adaptive Windowing",
      description: "ADWIN (Adaptive Windowing) is a concept drift detection method used in data streams analysis. It dynamically adjusts the window size while monitoring statistical measures like mean or variance within the window. As the data distribution changes, ADWIN detects when the statistics significantly deviate, indicating potential concept drift, making it effective for adaptive and real-time concept drift detection in evolving data streams."
    }
   
  ];
  const [selectedMeth,setSelectedMeth]=useState('')
  const handleDetect = async()=>{
    setLoading(true)
    setDataDriftResult([])
    console.log(selectedModel)
    console.log(selectedMeth)
    console.log(driftType)
    const formData = new FormData();
    formData.append('file', files[0]);
    formData.append('model_name', selectedModel.model_name);
    formData.append('model_horizon', selectedModel.horizon);
    formData.append('model_target', selectedModel.target);
    formData.append('predictors', selectedModel.predictors);
    formData.append('method', selectedMeth);

    formData.append('driftType', driftType);
    console.log(formData)
   

    try {
   
      const response = await axios.post('http://localhost:8000/api/drift_detection/', formData, {
        headers: {
          'Content-Type':'multipart/form-data'
        }
      });

      const result=JSON.parse(response.data)
      console.log(result)
      setIsDataDrift(result.data_drift_detected)
      setIsCinceptDrift(result.concept_drift_detected)
      setDataDriftResult(result.data_drift_result)
      setConceptIndex(result.index)
      setMea(result.mea)
      console.log(result.mea)
      setMse(result.msae)
      setRmse(result.rmse)
      setSHap(result.shap)
      setData(result.data)
      setWrite(result.write)
      console.log(data)
      setTarget(result.target)
      console.log(isDataDrift,isCinceptDrift,DataDriftResult,conceptIndex,mea,msa,rmse,shap)
      setLoading(false);
    } catch (error) {
      console.error('Error saving model:', error);
      setLoading(false);
    }
  
  }

  const findMatchingRow = feature => {
    return DataDriftResult.find(item => item.Column === feature && item.DriftDetected === 'True');
  };
  
  const filteredRows = DataDriftResult.filter(item => item.DriftDetected === 'True');

// Then, find the index of the row with the maximum shapValue
let maxShapValue = -Infinity;
let maxShapIndex = -1;

filteredRows.forEach((item, index) => {
  const shapValue = shap[index] ?shap[index].MeanAbsSHAP :-Infinity; // Assuming shap array corresponds to DataDriftResult
  if (shapValue > maxShapValue) {
    maxShapValue = shapValue;
    maxShapIndex = index;
  }
});


  useEffect(() => {
    
    getModelsList();
  }, []);
  const getModelsList = async () => {
    try {
      
      const response = await axios.get('http://localhost:8000/api/models_prediction/list_custom_models/');
      setModelsList(response.data);
      console.log(response.data)
     
    } catch (error) {
      console.error('Error fetching model list:', error);
    }
  };  
  

  const retrainContinuis= async()=>{
    setShowPlot(false)
    setLoading3(true)
    console.log(selectedModel)
    const formData = new FormData();
    formData.append('file', files[0]);
    formData.append('model_name', selectedModel.model_name);
    formData.append('model_horizon', selectedModel.horizon);
    formData.append('model_target', selectedModel.target);
    formData.append('predictors', selectedModel.predictors);
    console.log(formData)
   

    try {
   
      const response = await axios.post('http://localhost:8000/api/retrain_incremantale/', formData, {
        headers: {
          'Content-Type':'multipart/form-data'
        }
      });

      const result=JSON.parse(response.data)
      console.log(result)
      setMea3(result.mean)
      setMse3(result.mse)
      setRmse3(result.rmse)

      setLoading3(false)
      setLoading(false);
    } catch (error) {
      console.error('Error saving model:', error);
      setLoading3(false);
    }

  }
const save = async()=>{
  console.log('save')
    setShowPlot(false)
    const formData = new FormData();
    formData.append('file', files[0]);  
    try {
   
        const response = await axios.post('http://localhost:8000/api/save_data/', formData, {
          headers: {
            'Content-Type':'multipart/form-data'
          }
        });
  
        const result=JSON.parse(response.data)
        console.log(result)
        setOpen(true); 
        setLoading4(false)
     
      } catch (error) {
        console.error('Error saving model:', error);
      
      } 
}
  
  const retrainTotale= async()=>{
    setShowPlot(false)
    setLoading2(true)
    console.log(selectedModel)
    const formData = new FormData();
    formData.append('file', files[0]);
    formData.append('model_name', selectedModel.model_name);
    formData.append('model_horizon', selectedModel.horizon);
    formData.append('model_target', selectedModel.target);
    formData.append('predictors', selectedModel.predictors);
    console.log(formData)
   

    try {
   
      const response = await axios.post('http://localhost:8000/api/retrain_totale/', formData, {
        headers: {
          'Content-Type':'multipart/form-data'
        }
      });

      const result=JSON.parse(response.data)
      console.log(result)
      setMea2(result.mean)
      setMse2(result.mse)
      setRmse2(result.rmse)
      setLoading2(false)
      setLoading(false);
    } catch (error) {
      console.error('Error saving model:', error);
      setLoading2(false);
    }

  }
 
  return (
    <>
      <Grid container spacing={gridSpacing}>
      
        <Grid item lg={12} md={12} sm={12} xs={12}>
        
        <MainCard>
            {msa2==0 && msa3==0 && <> <h3>Detect Drift </h3>
            <Grid container spacing={gridSpacing} style={{marginTop:'20px'}}>
            <Grid item lg={3} md={3} sm={12} xs={12}>
            

            <FormControl fullWidth variant="outlined">
                    <InputLabel>Select Model</InputLabel>
                    <Select
                       name="selectedModel"
                       value={selectedModel}
                       onChange={(event) => {
                         setSelectedModel(event.target.value);
                       }}
                      label="Select Model"
                    >
                      {modelsList.map((model) => (
              <MenuItem key={model.model_name} value={model}>
                {model.model_name}
              </MenuItem>
            ))}
                    </Select>
                  </FormControl>
           
         </Grid>
         {msa2==0 &&<Grid item lg={3} md={3} sm={12} xs={12}>
            <FormControl fullWidth variant="outlined">
                    <InputLabel>Select Drift Type</InputLabel>
                    <Select
                      value={driftType}
                      onChange={(event) => {
                        setDriftType(event.target.value);
                        setSelectedMeth('')
                      }}
                      label="Select Drift Type"
                    >
                      {drifts.map((column, index) => (
                        <MenuItem key={index} value={column}>
                          {column}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
         </Grid>}
         <Grid item lg={3} md={3} sm={12} xs={12}>
            <FormControl fullWidth variant="outlined">
                    <InputLabel>Select Drift Detection Method </InputLabel>
                        <Select
                          value={selectedMeth}
                          onChange={(event) => {
                              setSelectedMeth(event.target.value);
                              console.log(event.target.value);
                    }}
                    label="Select Drift Detection Method"
                    >
                    {driftType === 'Data Drift' && (
                        Data_methods.map((column, index) => (
                        <MenuItem key={index} value={column.value}>
                            {column.label}
                        </MenuItem>
                        ))
                    )}
                    
                    {driftType !== 'Data Drift' && (
                        Concept_methods.map((column, index) => (
                        <MenuItem key={index} value={column.value}>
                            {column.label}
                        </MenuItem>
                        ))
                    )}
                    </Select>

                  </FormControl>
         </Grid>
         
      

       
         <Grid item lg={3} md={3} sm={12} xs={12} style={{ margin: 'auto', textAlign: 'center' }}>
                <Button
                  className='bottun-color'
                  disabled={files.length === 0}
                  variant="contained"
                  color="primary"
                  style={{ width: '250px' }}
                  onClick={handleDetect}
                >
                  Submit
                </Button>
              </Grid>
             

         </Grid> </> }
         {loading &&  <div  style={{display:'flex',justifyContent:'center',textAlign:'center',marginTop:'10px'}}>
            <CircularProgress size={40} color="inherit" />
            </div>}
         {driftType=='Data Drift' && isDataDrift==false  && DataDriftResult.length>0 && msa2==0 &&  msa3==0 &&  
         <>
        <Alert severity="success" style={{ marginTop: '20px' }}>No data drift was detected </Alert>
         
          <div>
        { write&&loading4&& (
        
          
       
        <Grid item lg={12} md={12} sm={12} xs={12} style={{ margin: 'auto' }}>
        <h3>Save the new  data</h3>
        
        <p>No drifting was observed. You now have the option to either save the data as a new version or disregard it. </p>
            <Button
             className='bottun-color'
              disabled={files.length === 0}
              variant="contained"
              color="primary"
              style={{ width: '250px' }}
              onClick={save}

             
            >
              Save the data
            </Button>
          </Grid>) }
          {open && 
          <Alert severity="success" style={{ marginTop: '20px' }}>The data has been successfully added,new version has been created  </Alert>}
          </div> 
        </>}
         
    
         {driftType=='Data Drift' && isDataDrift==true  && DataDriftResult.length>0 && msa2==0 &&  msa3==0 && <Alert severity="error" style={{ marginTop: '20px' }}>Data drift was detected </Alert>}
         {driftType=='Data Drift' && isDataDrift==true  && DataDriftResult.length>0 && msa2==0 &&  msa3==0 &&  ( <>
             
            <div>
              
            
            
            {write && loading4 && (
            
            <Grid item lg={12} md={12} sm={12} xs={12} style={{ margin: 'auto' }}>
            <h3>Save the new  data</h3>
            
            <p>An instance of drift has been identified. It is necessary to preserve the data by creating a new version. </p>
                <Button
                  className='bottun-color'
                  disabled={files.length === 0}
                  variant="contained"
                  color="primary"
                  style={{ width: '250px' }}
                  onClick={save}
    
                 
                >
                  Save the data
                </Button>
              </Grid>)}
            
          {open && 
          <Alert severity="success" style={{ marginTop: '20px' }}>The data has been successfully added,new version has been created  </Alert>}  
            </div>   
            <Grid container spacing={gridSpacing}>
             <Grid item lg={4} md={4} sm={12} xs={12}>
                <DriftTypeCard type={'Drift Type'} title={'Data Drift'}/>
             </Grid> 
             

             <Grid item lg={4} md={4} sm={12} xs={12}>
                <DriftTypeCard title={'Totale Column Number'} type={18}/>
             </Grid> 
             <Grid item lg={4} md={4} sm={12} xs={12}>
                <DriftTypeCard title={'Drifted Columns Number'} type={DataDriftResult.filter(row => row.DriftDetected === 'True').length}/>
             </Grid> 
             </Grid> 
             <TableContainer component={Paper}>
      <Table  aria-label="simple table">
        <TableHead>
          <TableRow >
          
                <TableCell style={{fontWeight:"bold"}}>Column </TableCell>
                <TableCell style={{fontWeight:"bold"}}> {selectedMeth=='KS'?  "PValue": "Distance"} </TableCell>
                <TableCell style={{fontWeight:"bold"}}>Threshold </TableCell>
                <TableCell style={{fontWeight:"bold"}}>Drift Detected </TableCell>
         
          </TableRow>
        </TableHead>
        <TableBody>
          {DataDriftResult.map((row,index) => (
            <TableRow
              key={index}
             style={{textAlign:'center', backgroundColor:row.DriftDetected ==='True' ?'#ff5252' : 'inherit' }}
            >
             
              <TableCell align="left">{row.Column}</TableCell>
              <TableCell align="left">{selectedMeth=='KS'?  row.PValue : row.Distance }</TableCell>
              <TableCell align="left">{row.Alpha}</TableCell>
              <TableCell align="left">{row.DriftDetected}</TableCell>
          
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer> 
          
    <Grid item xs={12}>
                   <h3 style={{marginTop:'40px'}}>Performance Metrics</h3>
                   
                  <Grid container spacing={2} justifyContent="center">
                    <Grid item xs={4}>
                      <Card style={{ backgroundColor: red[100] }}>
                        <CardContent>
                          <Typography variant="h6">Mean Squared Error (MSE)</Typography>
                          <Typography variant="body2" color="textSecondary">
                            {msa !== null ? msa : 'N/A'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={4}>
                      <Card style={{ backgroundColor: green[100] }}>
                        <CardContent>
                          <Typography variant="h6">Root Mean Squared Error (RMSE)</Typography>
                          <Typography variant="body2" color="textSecondary">
                            {rmse !== null ? rmse : 'N/A'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={4}>
                      <Card style={{ backgroundColor: blue[100] }}>
                        <CardContent>
                          <Typography variant="h6">Mean Absolute Error (MAE)</Typography>
                          <Typography variant="body2" color="textSecondary">
                            {mea !== null ? mea : 'N/A'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                  </Grid>
                </Grid>

                <Grid item xs={12}>
                <h3>Drifted Colums Importance</h3>


               
             <TableContainer component={Paper}>
      <Table  aria-label="simple table">
        <TableHead>
          <TableRow >
          
                <TableCell style={{fontWeight:"bold"}}>Column </TableCell>
                <TableCell style={{fontWeight:"bold"}}>Shap values </TableCell>
              
         
          </TableRow>
        </TableHead>
        <TableBody>
          {shap.map((row,index) => (
            <TableRow
              key={index}
             style={{textAlign:'center', backgroundColor: findMatchingRow(row.Feature) ? '#ff5252' : 'inherit'}}
            >
             
              <TableCell align="left">{row.Feature}</TableCell>
              <TableCell align="left">{row.MeanAbsSHAP}</TableCell>
            
          
            </TableRow> ))}
        
        </TableBody>
      </Table>
    </TableContainer>  

    <Grid item lg={12} md={12} sm={12} xs={12} style={{ margin: 'auto' }}>
            <h3>Retrain your Model</h3>
            { parseInt(maxShapIndex) <= 5 ? <p>The decrease in your model performance is due to the occurrence of data drift in one of  the 5 top most importante feautures. Therefore, retraining your model is necessary.</p>:
            <p>Data drift occurs due to a column that does not belong to the top 5 most important features. You have the option to disregard these changes and continue utilizing your model, or you can choose to adjust your model using the updated data. </p>}
                <Button
                  className='bottun-color'
                  disabled={files.length === 0}
                  variant="contained"
                  color="primary"
                  style={{ width: '250px' }}
                  onClick={retrainContinuis}

                 
                >
                  Retrain
                </Button>
              </Grid>
    

    </Grid>
   
         
            
       
            </>
            )}
       

       {loading3 && 
            <div  style={{display:'flex',justifyContent:'center',textAlign:'center',marginTop:'10px'}}>
            <CircularProgress size={40} color="inherit" /></div> 
            }
         {msa2==0  &&  msa3!=0 &&  <>  <Alert severity="success" style={{ marginTop: '20px' }}>Your Model have been retrained with seccess </Alert>
         
         <Grid item xs={12} style={{marginTop:'20px'}}>
                   <h3 style={{marginTop:'40px'}}>Performance Metrics</h3>
                   
                  <Grid container spacing={2} justifyContent="center">
                    <Grid item xs={4}>
                      <Card style={{ backgroundColor: red[100] }}>
                        <CardContent>
                          <Typography variant="h6">Mean Squared Error (MSE)</Typography>
                          <Typography variant="body2" color="textSecondary">
                            {msa3 !== null ? msa3 : 'N/A'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={4}>
                      <Card style={{ backgroundColor: green[100] }}>
                        <CardContent>
                          <Typography variant="h6">Root Mean Squared Error (RMSE)</Typography>
                          <Typography variant="body2" color="textSecondary">
                            {rmse3 !== null ? rmse3 : 'N/A'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={4}>
                      <Card style={{ backgroundColor: blue[100] }}>
                        <CardContent>
                          <Typography variant="h6">Mean Absolute Error (MAE)</Typography>
                          <Typography variant="body2" color="textSecondary">
                            {mea3 !== null ? mea3 : 'N/A'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                  </Grid>
                </Grid> </> }
         {driftType=='Concept Drift' && isCinceptDrift==true  && DataDriftResult.length>0 && msa2==0 &&  msa3==0 &&  (
         <>
         <Alert severity="error" style={{ marginTop: '20px' }}> Concept drift was detected </Alert>
         
            <div>
          {write&&loading4&&(
            
              
           
            <Grid item lg={12} md={12} sm={12} xs={12} style={{ margin: 'auto' }}>
            <h3>Save the new  data</h3>
            
            <p>An instance of drift has been identified. It is necessary to preserve the data by creating a new version. </p>
                <Button
                 className='bottun-color'
                  disabled={files.length === 0}
                  variant="contained"
                  color="primary"
                  style={{ width: '250px' }}
                  onClick={save}
    
                 
                >
                  Save the data
                </Button>
                </Grid>)}
             {open && 
          <Alert severity="success" style={{ marginTop: '20px' }}>The data has been successfully added,new version has been created  </Alert>}
           </div>
             
         <Grid container spacing={gridSpacing}>
             <Grid item lg={4} md={4} sm={12} xs={12}>
                <DriftTypeCard type={'Concept Drift '} title={'Data Drift'}/>
             </Grid> 
             

             <Grid item lg={4} md={4} sm={12} xs={12}>
                <DriftTypeCard title={'Drifted Trget '} type={target}/>
             </Grid> 
             <Grid item lg={4} md={4} sm={12} xs={12}>
                <DriftTypeCard title={'Drifted Index'} type={conceptIndex}/>
             </Grid> 
             </Grid> 

              { showPlot && <InteractionPlot data={data} xCol={'date'} yCol={'Electricity'} index={conceptIndex}/>}



             <Grid item xs={12} style={{marginTop:'20px'}}>
                   <h3 style={{marginTop:'40px'}}>Performance Metrics</h3>
                   
                  <Grid container spacing={2} justifyContent="center">
                    <Grid item xs={4}>
                      <Card style={{ backgroundColor: red[100] }}>
                        <CardContent>
                          <Typography variant="h6">Mean Squared Error (MSE)</Typography>
                          <Typography variant="body2" color="textSecondary">
                            {msa !== null ? msa : 'N/A'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={4}>
                      <Card style={{ backgroundColor: green[100] }}>
                        <CardContent>
                          <Typography variant="h6">Root Mean Squared Error (RMSE)</Typography>
                          <Typography variant="body2" color="textSecondary">
                            {rmse !== null ? rmse : 'N/A'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={4}>
                      <Card style={{ backgroundColor: blue[100] }}>
                        <CardContent>
                          <Typography variant="h6">Mean Absolute Error (MAE)</Typography>
                          <Typography variant="body2" color="textSecondary">
                            {mea !== null ? mea : 'N/A'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                  </Grid>
                </Grid>
                <Grid item lg={12} md={12} sm={12} xs={12} style={{ margin: 'auto' }}>
            <h3>Retrain your Model</h3>
             <p>The decrease in your model performance is due to the occurrence of concept drift. Therefore, retraining your model is necessary.</p>
                <Button
                 className='bottun-color'
                  disabled={files.length === 0}
                  variant="contained"
                  color="primary"
                  style={{ width: '250px' }}
                  onClick={retrainTotale}

                 
                >
                  Retrain
                </Button>
              </Grid>

        
         </>)
         
         }
        
         {driftType=='Concept Drift' && isCinceptDrift==false  && DataDriftResult.length>0 && 
         <>   <Alert severity="success" style={{ marginTop: '20px' }}>No concept drift was detected </Alert>
           
            <div>
              
            
            {write&&loading4&&(
            
            <Grid item lg={12} md={12} sm={12} xs={12} style={{ margin: 'auto' }}>
            <h3>Save the new  data</h3>
            
            <p>No drifting was observed. You now have the option to either save the data as a new version or disregard it. </p>
                <Button
                  className='bottun-color'
                  disabled={files.length === 0}
                  variant="contained"
                  color="primary"
                  style={{ width: '250px' }}
                  onClick={save}
    
                 
                >
                  Save the data
                </Button>
                </Grid>)}
          {open && 
          <Alert severity="success" style={{ marginTop: '20px' }}>The data has been successfully added,new version has been created  </Alert>}
             </div>
             </>}
       



         {loading2 && 
            <div  style={{display:'flex',justifyContent:'center',textAlign:'center',marginTop:'10px'}}>
            <CircularProgress size={40} color="inherit" /></div> 
            }
         {msa2!=0 &&  msa3==0 &&  <>  <Alert severity="success" style={{ marginTop: '20px' }}>Your Model have been retrained with seccess </Alert>
         
         <Grid item xs={12} style={{marginTop:'20px'}}>
                   <h3 style={{marginTop:'40px'}}>Performance Metrics</h3>
                   
                  <Grid container spacing={2} justifyContent="center">
                    <Grid item xs={4}>
                      <Card style={{ backgroundColor: red[100] }}>
                        <CardContent>
                          <Typography variant="h6">Mean Squared Error (MSE)</Typography>
                          <Typography variant="body2" color="textSecondary">
                            {msa2 !== null ? msa2 : 'N/A'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={4}>
                      <Card style={{ backgroundColor: green[100] }}>
                        <CardContent>
                          <Typography variant="h6">Root Mean Squared Error (RMSE)</Typography>
                          <Typography variant="body2" color="textSecondary">
                            {rmse2 !== null ? rmse2 : 'N/A'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={4}>
                      <Card style={{ backgroundColor: blue[100] }}>
                        <CardContent>
                          <Typography variant="h6">Mean Absolute Error (MAE)</Typography>
                          <Typography variant="body2" color="textSecondary">
                            {mea2 !== null ? mea2 : 'N/A'}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                  </Grid>
                </Grid>
         
         
         
         
         </>}

        



        </MainCard>
        <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'flex-end' }}>
        <Button  className='bottun-color'  onClick={handleBack}>Back</Button>
      </div>
        </Grid>
        

      </Grid>
    </>
  );
};

export default StepTow;
