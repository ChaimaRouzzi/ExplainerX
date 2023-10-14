import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import { StepLabel } from '@mui/material';
import { updateVersion, updateUpdated } from 'actions/actions';
import { useSelector, useDispatch } from 'react-redux';
import MainCard from 'ui-component/cards/MainCard';
import SkeletonEarningCard from 'ui-component/cards/Skeleton/EarningCard';
import axios from 'axios';
import { Grid } from '@mui/material';
import { gridSpacing } from 'store/constant';
import React, { useState, useEffect } from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Alert from '@mui/material/Alert';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import InteractionPlot from './plot';
// ==============================|| SAMPLE PAGE ||============================== //

const Trace = () => {
  const dispatch = useDispatch();
  const version = 0;
  const handleUpdateVersion = (newValue) => {
    return new Promise((resolve) => {
      dispatch(updateVersion(newValue));
      setVal(newValue);
      resolve();
    });
  };
  const updated = useSelector((state) => state.updated);
  
  const handleUpdateUpdated = (newValue) => {
    return new Promise((resolve) => {
      dispatch(updateUpdated(newValue));

      resolve();
    });
  };

  const [updatedVersions, setUpdatedVersion] = useState([]);
  const [val, setVal] = useState(version.version ? version.version : 0);
  const BaseURL = `http://127.0.0.1:8000/api/initial_profiling`;
  const [isLoading, setLoading] = useState(true);
  const [version_number, setVersionNumber] = useState(0);
  const [status1, setStatus1] = useState([]);
  const [status2, setStatus2] = useState([]);
  const [data1, setData1] = useState([]);
  const [data2, setData2] = useState([]);
  const [columns_status1, setColumnsStatus1] = useState([]);
  const [columns_status2, setColumnsStatus2] = useState([]);
  const [trace, setTrace] = useState([]);
  const [activeStep, setActiveStep] = useState(val == -1 ? 2 : val);

  function doesColumnExistInTrace(trace, column) {
    return trace.some((item) => item.column === column);
  }
  const handleStepClick2 = (step, all) => {
    handleUpdateUpdated('True');
    setActiveStep(step);
    if (version !== step) {
      const updatedVal = all == 1 ? -1 : step;
      handleUpdateVersion(all === 1 ? -1 : step).then(() => {
        setLoading(true);

        axios
          .get(BaseURL)
          .then((response) => {
            const result = JSON.parse(response.data);
            console.log(result);

            setVersionNumber(result.versions_number ? result.versions_number : 0);
            setUpdatedVersion(result.updated_version ? JSON.parse(result.updated_version) : []);
          })
          .catch((error) => {
            console.log(error);
          });
        axios.get(`http://127.0.0.1:8000/api/preprocessing_trace/${updatedVal}/True`).then((response) => {
          const result = JSON.parse(response.data);
          console.log(result);
          setTrace(result.trace ? JSON.parse(result.trace) : []);
          setStatus1(result.status1 ? result.status1[0] : {});
          setStatus2(result.status2 ? result.status2[0] : {});
          setData1(result.columns_status1 ? JSON.parse(result.data1) : []);
          setData2(result.columns_status2 ? JSON.parse(result.data2) : []);
          setColumnsStatus1(result.columns_status1 ? JSON.parse(result.columns_status1) : []);
          setColumnsStatus2(result.columns_status2 ? JSON.parse(result.columns_status2) : []);
          console.log(trace, data1, data2, status1, status2, columns_status1, columns_status2);
          setLoading(false);
        });
      });
    } else {
      // Handle logic when version is already equal to step
    }
  };

  useEffect(() => {
    axios.get(BaseURL).then((response) => {
      const result = JSON.parse(response.data);
      console.log(result);
      setVersionNumber(result.versions_number ? result.versions_number : 0);
      setUpdatedVersion(result.updated_version ? JSON.parse(result.updated_version) : []);
    });

    axios.get(`http://127.0.0.1:8000/api/preprocessing_trace/${val}/${updated.updated}`).then((response) => {
      const result = JSON.parse(response.data);
      console.log(result);
      setTrace(result.trace ? JSON.parse(result.trace) : []);
      setStatus1(result.status1 ? result.status1[0] : {});
      setStatus2(result.status2 ? result.status2[0] : {});
      setData1(result.columns_status1 ? JSON.parse(result.data1) : []);
      setData2(result.columns_status2 ? JSON.parse(result.data2) : []);
      setColumnsStatus1(result.columns_status1 ? JSON.parse(result.columns_status1) : []);
      setColumnsStatus2(result.columns_status2 ? JSON.parse(result.columns_status2) : []);
      console.log(status1);
      setLoading(false);
    });
  }, []);

  console.log(status2.number_of_missing_values);
  return (
    <>
      <Grid container spacing={gridSpacing}>
        <Grid item xs={12}>
          <Grid container spacing={gridSpacing}>
            <Grid item lg={12} md={12} sm={12} xs={12}>
              <MainCard>
                <h3>Choose your updated version </h3>
                {isLoading ? (
                  <SkeletonEarningCard className="loading" />
                ) : (
                  <>

                    {updatedVersions.length > 0 && (
                      <div>
                        <Stepper nonLinear activeStep={updated.updated == 'True' ? activeStep : -1} style={{ marginTop: '10px' }}>
                          {updatedVersions.map((vers, index) => (
                            <Step key={index}>
                              <StepLabel onClick={() => handleStepClick2(index, 0)}>Version {vers + 1}</StepLabel>
                            </Step>
                          ))}
                          {updatedVersions.length >= 2 && (
                            <Step>
                              <StepLabel onClick={() => handleStepClick2(parseInt(version_number), 1)}>All versions</StepLabel>
                            </Step>
                          )}
                        </Stepper>
                      </div>
                    )}{' '}
                  </>
                )}
              </MainCard>
            </Grid>

            <Grid item lg={12} md={12} sm={12} xs={12}>
              <MainCard>
                <h3> Preprocessing traceability </h3>
                {isLoading ? (
                  <SkeletonEarningCard />
                ) : (
                  <div>
                    {trace.length == 0 ? (
                      <Alert severity="warning">No operations have been applied to the data yet</Alert>
                    ) : (
                      <TableContainer component={Paper}>
                        <Table aria-label="simple table">
                          <TableHead>
                            <TableRow>
                              <TableCell style={{ fontWeight: 'bold' }}>Operation </TableCell>
                              <TableCell style={{ fontWeight: 'bold' }}>Column Name</TableCell>
                              <TableCell style={{ fontWeight: 'bold' }}>Method</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {trace.map((row, index) => (
                              <TableRow key={index} style={{ textAlign: 'center' }}>
                                <TableCell align="left">{row.operation}</TableCell>
                                <TableCell align="left">{row.column}</TableCell>
                                <TableCell align="left">{row.method}</TableCell>
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      </TableContainer>
                    )}
                  </div>
                )}
              </MainCard>
            </Grid>

            {trace.length == 0 ? (
              ''
            ) : (
              <Grid item lg={12} md={12} sm={12} xs={12}>
                <MainCard>
                  <h3> Original Data vs Processed Data</h3>
                  {isLoading ? (
                    <SkeletonEarningCard />
                  ) : (
                    <div>
                      <Grid container spacing={gridSpacing}>
                        <Grid item lg={5} md={5} sm={12} xs={12} style={{ margin: '30px' }}>
                          <h4 style={{ textAlign: 'center', color: '#004aad' }}>Original Data</h4>
                          <TableContainer component={Paper}>
                            <Table aria-label="simple table">
                              <TableHead>
                                <TableRow>
                                  <TableCell style={{ fontWeight: 'bold' }}>Mesure </TableCell>
                                  <TableCell style={{ fontWeight: 'bold' }}>Value</TableCell>
                                </TableRow>
                              </TableHead>
                              <TableBody>
                                <TableRow key={1} style={{ textAlign: 'center' }}>
                                  <TableCell align="left">Number of Rows</TableCell>
                                  <TableCell align="left">{status1.number_of_rows ? status1.number_of_rows : ''}</TableCell>
                                </TableRow>
                                <TableRow key={2} style={{ textAlign: 'center' }}>
                                  <TableCell align="left">Number of Columns</TableCell>
                                  <TableCell align="left">{status1.number_of_columns ? status1.number_of_columns : ''}</TableCell>
                                </TableRow>
                                <TableRow key={3} style={{ textAlign: 'center' }}>
                                  <TableCell align="left">Number of Missing Values</TableCell>
                                  <TableCell align="left">
                                    {status1.number_of_missing_values ? status1.number_of_missing_values : ''}
                                  </TableCell>
                                </TableRow>
                                <TableRow key={6} style={{ textAlign: 'center' }}>
                                  <TableCell align="left">Number of Outlires</TableCell>
                                  <TableCell align="left">{status1.number_of_outliers ? status1.number_of_outliers : ''}</TableCell>
                                </TableRow>
                                <TableRow key={4} style={{ textAlign: 'center' }}>
                                  <TableCell align="left">Number of Zero Values</TableCell>
                                  <TableCell align="left">{status1.number_of_zero_values ? status1.number_of_zero_values : ''}</TableCell>
                                </TableRow>
                                <TableRow key={5} style={{ textAlign: 'center' }}>
                                  <TableCell align="left">Number of Duplicates Rows</TableCell>
                                  <TableCell align="left">
                                    {status1.number_of_duplicate_rows ? status1.number_of_duplicate_rows : 0}
                                  </TableCell>
                                </TableRow>
                              </TableBody>
                            </Table>
                          </TableContainer>
                        </Grid>

                        <Grid item lg={5} md={5} sm={12} xs={12} style={{ margin: '30px' }}>
                          <h4 style={{ textAlign: 'center', color: '#004aad' }}>Processed Data</h4>
                          <TableContainer component={Paper}>
                            <Table aria-label="simple table">
                              <TableHead>
                                <TableRow>
                                  <TableCell style={{ fontWeight: 'bold' }}>Mesure </TableCell>
                                  <TableCell style={{ fontWeight: 'bold' }}>Value</TableCell>
                                </TableRow>
                              </TableHead>
                              <TableBody>
                                <TableRow key={1} style={{ textAlign: 'center' }}>
                                  <TableCell align="left">Number of Rows</TableCell>
                                  <TableCell align="left">{status2.number_of_rows ? status2.number_of_rows : ''}</TableCell>
                                </TableRow>
                                <TableRow key={2} style={{ textAlign: 'center' }}>
                                  <TableCell align="left">Number of Columns</TableCell>
                                  <TableCell align="left">{status2.number_of_columns ? status2.number_of_columns : ''}</TableCell>
                                </TableRow>
                                <TableRow key={3} style={{ textAlign: 'center' }}>
                                  <TableCell align="left">Number of Missing Values</TableCell>
                                  {parseInt(status1.number_of_missing_values) > parseInt(status2.number_of_missing_values) && (
                                    <TableCell align="left" sx={{ color: 'green' }}>
                                      {' '}
                                      <ArrowDownwardIcon sx={{ fontSize: 15 }} />{' '}
                                      {status1.number_of_missing_values ? status2.number_of_missing_values : ''}
                                    </TableCell>
                                  )}
                                  {parseInt(status1.number_of_missing_values) < parseInt(status2.number_of_missing_values) && (
                                    <TableCell align="left" sx={{ color: 'red' }}>
                                      <ArrowUpwardIcon sx={{ fontSize: 15 }} />{' '}
                                      {status2.number_of_missing_values ? status2.number_of_missing_values : ''}
                                    </TableCell>
                                  )}
                                  {parseInt(status1.number_of_missing_values) == parseInt(status2.number_of_missing_values) && (
                                    <TableCell align="left">
                                      {status2.number_of_missing_values ? status2.number_of_missing_values : ''}
                                    </TableCell>
                                  )}
                                </TableRow>
                                <TableRow key={6} style={{ textAlign: 'center' }}>
                                  <TableCell align="left">Number Outlires</TableCell>
                                  {parseInt(status1.number_of_outliers) > parseInt(status2.number_of_outliers) && (
                                    <TableCell align="left" sx={{ color: 'green' }}>
                                      {' '}
                                      <ArrowDownwardIcon sx={{ fontSize: 15 }} />{' '}
                                      {status2.number_of_outliers ? status2.number_of_outliers : ''}
                                    </TableCell>
                                  )}
                                  {parseInt(status1.number_of_outliers) < parseInt(status2.number_of_outliers) && (
                                    <TableCell align="left" sx={{ color: 'red' }}>
                                      <ArrowUpwardIcon sx={{ fontSize: 15 }} />{' '}
                                      {status2.number_of_outliers ? status2.number_of_outliers : ''}
                                    </TableCell>
                                  )}
                                  {parseInt(status1.number_of_outliers) == parseInt(status2.number_of_outliers) && (
                                    <TableCell align="left">{status2.number_of_outliers ? status2.number_of_outliers : ''}</TableCell>
                                  )}
                                </TableRow>
                                <TableRow key={4} style={{ textAlign: 'center' }}>
                                  <TableCell align="left">Number of Zero Values</TableCell>
                                  {parseInt(status1.number_of_zero_values) > parseInt(status2.number_of_zero_values) && (
                                    <TableCell align="left" sx={{ color: 'green' }}>
                                      {' '}
                                      <ArrowDownwardIcon sx={{ fontSize: 15 }} />{' '}
                                      {status2.number_of_zero_values ? status2.number_of_zero_values : ''}
                                    </TableCell>
                                  )}
                                  {parseInt(status1.number_of_zero_values) < parseInt(status2.number_of_zero_values) && (
                                    <TableCell align="left" sx={{ color: 'red' }}>
                                      <ArrowUpwardIcon sx={{ fontSize: 15 }} />{' '}
                                      {status2.number_of_zero_values ? status2.number_of_zero_values : ''}
                                    </TableCell>
                                  )}
                                  {parseInt(status1.number_of_zero_values) == parseInt(status2.number_of_zero_values) && (
                                    <TableCell align="left">{status2.number_of_zero_values ? status2.number_of_zero_values : ''}</TableCell>
                                  )}
                                </TableRow>
                                <TableRow key={5} style={{ textAlign: 'center' }}>
                                  <TableCell align="left">Number of Duplicates Rows</TableCell>

                                  {parseInt(status1.number_of_duplicate_rows) > parseInt(status2.number_of_duplicate_rows) && (
                                    <TableCell align="left" sx={{ color: 'green' }}>
                                      {' '}
                                      <ArrowDownwardIcon sx={{ fontSize: 15 }} />{' '}
                                      {status2.number_of_duplicate_rows ? status2.number_of_duplicate_rows : 0}
                                    </TableCell>
                                  )}
                                  {parseInt(status1.number_of_duplicate_rows) < parseInt(status2.number_of_duplicate_rows) && (
                                    <TableCell align="left" sx={{ color: 'red' }}>
                                      <ArrowUpwardIcon sx={{ fontSize: 15 }} />{' '}
                                      {status2.number_of_duplicate_rows ? status2.number_of_duplicate_rows : 0}
                                    </TableCell>
                                  )}
                                  {parseInt(status1.number_of_duplicate_rows) == parseInt(status2.number_of_duplicate_rows) && (
                                    <TableCell align="left">
                                      {status2.number_of_duplicate_rows ? status2.number_of_duplicate_rows : 0}
                                    </TableCell>
                                  )}
                                </TableRow>
                              </TableBody>
                            </Table>
                          </TableContainer>
                        </Grid>
                      </Grid>
                    </div>
                  )}
                </MainCard>
              </Grid>
            )}

            {trace.length == 0 ? (
              ''
            ) : (
              <Grid item lg={12} md={12} sm={12} xs={12}>
                <MainCard>
                  <h3>Detailed Column Comparison</h3>
                  {isLoading ? (
                    <SkeletonEarningCard />
                  ) : (
                    <div>
                      {columns_status1.map((col, index) => (
                        <div key={index}>
                          {doesColumnExistInTrace(trace, col.column) && (
                            <Grid container spacing={gridSpacing}>
                              <>
                                <Grid item lg={5} md={5} sm={12} xs={12} style={{ margin: '30px' }}>
                                  <h4 style={{ textAlign: 'center', color: '#004aad' }}>Original Column {col.column} </h4>

                                  <TableContainer component={Paper}>
                                    <Table aria-label="simple table">
                                      <TableHead>
                                        <TableRow>
                                          <TableCell style={{ fontWeight: 'bold' }}>Mesure </TableCell>
                                          <TableCell style={{ fontWeight: 'bold' }}>Value</TableCell>
                                        </TableRow>
                                      </TableHead>
                                      <TableBody>
                                        <TableRow key={1} style={{ textAlign: 'center' }}>
                                          <TableCell align="left">Min</TableCell>
                                          <TableCell align="left">{col.Min}</TableCell>
                                        </TableRow>
                                        <TableRow key={2} style={{ textAlign: 'center' }}>
                                          <TableCell align="left">Max</TableCell>
                                          <TableCell align="left">{col.Max}</TableCell>
                                        </TableRow>
                                        <TableRow key={3} style={{ textAlign: 'center' }}>
                                          <TableCell align="left">Mean</TableCell>
                                          <TableCell align="left">{col.Mean}</TableCell>
                                        </TableRow>
                                        <TableRow key={6} style={{ textAlign: 'center' }}>
                                          <TableCell align="left">Unique</TableCell>
                                          <TableCell align="left">{col.Unique}</TableCell>
                                        </TableRow>
                                        <TableRow key={4} style={{ textAlign: 'center' }}>
                                          <TableCell align="left">Missing Values </TableCell>
                                          <TableCell align="left">{col.Missing_Values}</TableCell>
                                        </TableRow>
                                        <TableRow key={5} style={{ textAlign: 'center' }}>
                                          <TableCell align="left">Outlires</TableCell>
                                          <TableCell align="left">{col.Outliers}</TableCell>
                                        </TableRow>
                                        <TableRow key={5} style={{ textAlign: 'center' }}>
                                          <TableCell align="left">Negative</TableCell>
                                          <TableCell align="left">{col.Negative}</TableCell>
                                        </TableRow>
                                        <TableRow key={5} style={{ textAlign: 'center' }}>
                                          <TableCell align="left">Zeros</TableCell>
                                          <TableCell align="left">{col.Zeros}</TableCell>
                                        </TableRow>
                                      </TableBody>
                                    </Table>
                                  </TableContainer>
                                </Grid>

                                <Grid item lg={5} md={5} sm={12} xs={12} style={{ margin: '30px' }}>
                                  <h4 style={{ textAlign: 'center', color: '#004aad' }}>Processed column {col.column} </h4>
                                  <TableContainer component={Paper}>
                                    <Table aria-label="simple table">
                                      <TableHead>
                                        <TableRow>
                                          <TableCell style={{ fontWeight: 'bold' }}>Mesure </TableCell>
                                          <TableCell style={{ fontWeight: 'bold' }}>Value</TableCell>
                                        </TableRow>
                                      </TableHead>
                                      <TableBody>
                                        <TableRow key={3} style={{ textAlign: 'center' }}>
                                          <TableCell align="left">Min</TableCell>
                                          {parseFloat(columns_status2[index].Min) < parseFloat(col.Min) && (
                                            <TableCell align="left" sx={{ color: 'green' }}>
                                              {' '}
                                              <ArrowDownwardIcon sx={{ fontSize: 15 }} /> {columns_status2[index].Min}
                                            </TableCell>
                                          )}
                                          {parseFloat(columns_status2[index].Min) > parseFloat(col.Min) && (
                                            <TableCell align="left" sx={{ color: 'red' }}>
                                              <ArrowUpwardIcon sx={{ fontSize: 15 }} /> {columns_status2[index].Min}
                                            </TableCell>
                                          )}
                                          {parseFloat(columns_status2[index].Min) == parseFloat(col.Min) && (
                                            <TableCell align="left">{columns_status2[index].Min}</TableCell>
                                          )}
                                        </TableRow>
                                        <TableRow key={3} style={{ textAlign: 'center' }}>
                                          <TableCell align="left">Max</TableCell>
                                          {parseFloat(columns_status2[index].Max) < parseFloat(col.Max) && (
                                            <TableCell align="left" sx={{ color: 'green' }}>
                                              {' '}
                                              <ArrowDownwardIcon sx={{ fontSize: 15 }} /> {columns_status2[index].Max}
                                            </TableCell>
                                          )}
                                          {parseFloat(columns_status2[index].Max) > parseFloat(col.Max) && (
                                            <TableCell align="left" sx={{ color: 'red' }}>
                                              <ArrowUpwardIcon sx={{ fontSize: 15 }} /> {columns_status2[index].Max}
                                            </TableCell>
                                          )}
                                          {parseFloat(columns_status2[index].Max) == parseFloat(col.Max) && (
                                            <TableCell align="left">{columns_status2[index].Max}</TableCell>
                                          )}
                                        </TableRow>
                                        <TableRow key={3} style={{ textAlign: 'center' }}>
                                          <TableCell align="left">Mean</TableCell>
                                          {parseFloat(columns_status2[index].Mean) < parseFloat(col.Mean) && (
                                            <TableCell align="left" sx={{ color: 'green' }}>
                                              {' '}
                                              <ArrowDownwardIcon sx={{ fontSize: 15 }} /> {columns_status2[index].Mean}
                                            </TableCell>
                                          )}
                                          {parseFloat(columns_status2[index].Mean) > parseFloat(col.Mean) && (
                                            <TableCell align="left" sx={{ color: 'red' }}>
                                              <ArrowUpwardIcon sx={{ fontSize: 15 }} /> {columns_status2[index].Mean}
                                            </TableCell>
                                          )}
                                          {parseFloat(columns_status2[index].Mean) == parseFloat(col.Mean) && (
                                            <TableCell align="left">{columns_status2[index].Mean}</TableCell>
                                          )}
                                        </TableRow>
                                        <TableRow key={3} style={{ textAlign: 'center' }}>
                                          <TableCell align="left">Unique</TableCell>
                                          {parseFloat(columns_status2[index].Unique) < parseFloat(col.Unique) && (
                                            <TableCell align="left" sx={{ color: 'green' }}>
                                              {' '}
                                              <ArrowDownwardIcon sx={{ fontSize: 15 }} /> {columns_status2[index].Unique}
                                            </TableCell>
                                          )}
                                          {parseFloat(columns_status2[index].Unique) > parseFloat(col.Unique) && (
                                            <TableCell align="left" sx={{ color: 'red' }}>
                                              <ArrowUpwardIcon sx={{ fontSize: 15 }} /> {columns_status2[index].Unique}
                                            </TableCell>
                                          )}
                                          {parseFloat(columns_status2[index].Unique) == parseFloat(col.Unique) && (
                                            <TableCell align="left">{columns_status2[index].Unique}</TableCell>
                                          )}
                                        </TableRow>
                                        <TableRow key={3} style={{ textAlign: 'center' }}>
                                          <TableCell align="left">Missing Values</TableCell>
                                          {parseFloat(columns_status2[index].Missing_Values) < parseFloat(col.Missing_Values) && (
                                            <TableCell align="left" sx={{ color: 'green' }}>
                                              {' '}
                                              <ArrowDownwardIcon sx={{ fontSize: 15 }} /> {columns_status2[index].Missing_Values}
                                            </TableCell>
                                          )}
                                          {parseFloat(columns_status2[index].Missing_Values) > parseFloat(col.Missing_Values) && (
                                            <TableCell align="left" sx={{ color: 'red' }}>
                                              <ArrowUpwardIcon sx={{ fontSize: 15 }} /> {columns_status2[index].Missing_Values}
                                            </TableCell>
                                          )}
                                          {parseFloat(columns_status2[index].Missing_Values) == parseFloat(col.Missing_Values) && (
                                            <TableCell align="left">{columns_status2[index].Missing_Values}</TableCell>
                                          )}
                                        </TableRow>

                                        <TableRow key={3} style={{ textAlign: 'center' }}>
                                          <TableCell align="left">Outliers</TableCell>
                                          {parseFloat(columns_status2[index].Outliers) < parseFloat(col.Outliers) && (
                                            <TableCell align="left" sx={{ color: 'green' }}>
                                              {' '}
                                              <ArrowDownwardIcon sx={{ fontSize: 15 }} /> {columns_status2[index].Outliers}
                                            </TableCell>
                                          )}
                                          {parseFloat(columns_status2[index].Outliers) > parseFloat(col.Outliers) && (
                                            <TableCell align="left" sx={{ color: 'red' }}>
                                              <ArrowUpwardIcon sx={{ fontSize: 15 }} /> {columns_status2[index].Outliers}
                                            </TableCell>
                                          )}
                                          {parseFloat(columns_status2[index].Outliers) == parseFloat(col.Outliers) && (
                                            <TableCell align="left">{columns_status2[index].Outliers}</TableCell>
                                          )}
                                        </TableRow>

                                        <TableRow key={3} style={{ textAlign: 'center' }}>
                                          <TableCell align="left">Negative</TableCell>
                                          {parseFloat(columns_status2[index].Negative) < parseFloat(col.Negative) && (
                                            <TableCell align="left" sx={{ color: 'green' }}>
                                              {' '}
                                              <ArrowDownwardIcon sx={{ fontSize: 15 }} /> {columns_status2[index].Negative}
                                            </TableCell>
                                          )}
                                          {parseFloat(columns_status2[index].Negative) > parseFloat(col.Negative) && (
                                            <TableCell align="left" sx={{ color: 'red' }}>
                                              <ArrowUpwardIcon sx={{ fontSize: 15 }} /> {columns_status2[index].Negative}
                                            </TableCell>
                                          )}
                                          {parseFloat(columns_status2[index].Negative) == parseFloat(col.Negative) && (
                                            <TableCell align="left">{columns_status2[index].Negative}</TableCell>
                                          )}
                                        </TableRow>
                                        <TableRow key={3} style={{ textAlign: 'center' }}>
                                          <TableCell align="left">Zeros</TableCell>
                                          {parseFloat(columns_status2[index].Zeros) < parseFloat(col.Zeros) && (
                                            <TableCell align="left" sx={{ color: 'green' }}>
                                              {' '}
                                              <ArrowDownwardIcon sx={{ fontSize: 15 }} /> {columns_status2[index].Zeros}
                                            </TableCell>
                                          )}
                                          {parseFloat(columns_status2[index].Zeros) > parseFloat(col.Zeros) && (
                                            <TableCell align="left" sx={{ color: 'red' }}>
                                              <ArrowUpwardIcon sx={{ fontSize: 15 }} /> {columns_status2[index].Zeros}
                                            </TableCell>
                                          )}
                                          {parseFloat(columns_status2[index].Zeros) == parseFloat(col.Zeros) && (
                                            <TableCell align="left">{columns_status2[index].Zeros}</TableCell>
                                          )}
                                        </TableRow>
                                      </TableBody>
                                    </Table>
                                  </TableContainer>
                                </Grid>

                                <Grid item lg={5} md={5} sm={12} xs={12} style={{ margin: '30px' }}>
                                  <InteractionPlot data={data1} xCol={'date'} yCol={col.column} color={'#004aad'} />
                                </Grid>
                                <Grid item lg={5} md={5} sm={12} xs={12} style={{ margin: '30px' }}>
                                  <InteractionPlot data={data2} xCol={'date'} yCol={col.column} color={'red'} />
                                </Grid>
                              </>
                            </Grid>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </MainCard>
              </Grid>
            )}
          </Grid>
        </Grid>
      </Grid>
    </>
  );
};

export default Trace;
