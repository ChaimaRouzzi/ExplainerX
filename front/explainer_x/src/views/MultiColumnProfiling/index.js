import React, { useEffect, useState, useMemo } from 'react';
import axios from 'axios';
import { Grid } from '@mui/material';
import { gridSpacing } from 'store/constant';
import MainCard from 'ui-component/cards/MainCard';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import { StepLabel } from '@mui/material';
import { updateVersion, updateUpdated } from 'actions/actions';
import { useSelector, useDispatch } from 'react-redux';
import SkeletonEarningCard from 'ui-component/cards/Skeleton/EarningCard';
import CorrelationTbael from './CorrelationTabel';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import Heatmap from './Heatmap';
import ElectricityCorelation from './ElectricityCorelation';
import InteractionPlot from './IntaeractionPlot';

const MultiColumnsProfiling = () => {
  const dispatch = useDispatch();
  const version = useSelector((state) => state.version);
  const updated = useSelector((state) => state.updated);

  const handleUpdateVersion = (newValue) => {
    return new Promise((resolve) => {
      dispatch(updateVersion(newValue));
      setVal(newValue);
      resolve();
    });
  };
  const handleUpdateUpdated = (newValue) => {
    return new Promise((resolve) => {
      dispatch(updateUpdated(newValue));

      resolve();
    });
  };
  const corelationMethodes = [{ label: 'pearson' }, { label: 'kendall' }, { label: 'spearman' }];
  const forms = [{ label: 'Table' }, { label: 'Heatmap' }];

  const plot = [{ label: 'line' }, { label: 'scatter' }, { label: 'bar' }, { label: 'Bubble' }];
  const features = [
    {
      label: 'date' //access nested data with dot notation
    },
    {
      label: 'Electricity'
    },
    {
      label: 'Gas_01' //normal label :
    },
    {
      label: 'Gas_02' //normal label :
    },
    {
      label: 'Gas_03' //normal label :
    },
    {
      label: 'Day_Degree_Cold' //normal label :
    },
    {
      label: 'Day_Degree_Hot'
    },
    {
      label: 'Min_OutdoorTemp'
    },
    {
      label: 'Average_OutdoorTemp'
    },
    {
      label: 'Max_OutdoorTemp'
    },
    {
      label: 'Maximum_Humidity'
    },
    {
      label: 'Average_Humidity'
    },
    {
      label: 'Solar_Radiation'
    },
    {
      label: 'Hour'
    },
    {
      label: 'Day'
    },
    {
      label: 'Week'
    },
    {
      label: 'Month'
    },
    {
      label: 'Year'
    }
  ];

  const [val, setVal] = useState(version.version ? version.version : 0);
  const BaseURL = `http://127.0.0.1:8000/api/multi_column_profiling/${val}/${updated.updated}/pearson`;
  const [isLoading, setLoading] = useState(true);

  const [version_number, setVersionNumber] = useState(0);
  const [updatedVersions, setUpdatedVersion] = useState([]);
  const [activeStep, setActiveStep] = useState(val == -1 ? 2 : val);
  const [corelation, setCorelation] = useState([]);
  const [selectedValue, setSelectedValue] = React.useState(corelationMethodes[0]);
  const [selectedValue2, setSelectedValue2] = React.useState(forms[0]);
  const [xColumn, setXColumn] = React.useState(features[0]);
  const [yColumn, setYColumn] = React.useState(features[1]);
  const [plotType, setPlotType] = React.useState(plot[0]);

  const [method, setMethod] = React.useState(selectedValue.label);
  const [dataFormat, setDataForma] = React.useState(selectedValue2.label);
  const [topElectricity, setTopElectricity] = React.useState([]);
  const [topGas, setTopGas] = React.useState([]);
  const [dataset, setDataset] = useState([]);
  const [depandancies, setDepandancies] = useState([]);
  const [depandanteVariable, setDepandanteVariable] = useState(features[0]);
  const handleStepClick = (step, all) => {
    handleUpdateUpdated('False');
    setActiveStep(step);
    if (version !== step) {
      handleUpdateVersion(all === 1 ? -1 : step).then(() => {
        setLoading(true);
        const updatedVal = all == 1 ? -1 : step;
        const updatedURL = `http://127.0.0.1:8000/api/multi_column_profiling/${updatedVal}/False/${method}`;
        axios
          .get(updatedURL)
          .then((response) => {
            const result = JSON.parse(response.data);
            console.log(result);
            setDataset(result.data ? JSON.parse(result.data) : []);

            setDepandancies(result.depandancies ? JSON.parse(result.depandancies) : []);
            setVersionNumber(result.versions_number ? result.versions_number : 0);
            setCorelation(result.correlation ? JSON.parse(result.correlation) : []);
            setUpdatedVersion(result.updated_version ? JSON.parse(result.updated_version) : []);
            setLoading(false);
          })
          .catch((error) => {
            console.log(error);
            setLoading(false);
          });
      });
    } else {
      // Handle logic when version is already equal to step
    }
  };

  const handleStepClick2 = (step, all) => {
    handleUpdateUpdated('True');
    setActiveStep(step);
    if (version !== step) {
      handleUpdateVersion(all === 1 ? -1 : step).then(() => {
        setLoading(true);
        const updatedVal = all == 1 ? -1 : step;
        const updatedURL = `http://127.0.0.1:8000/api/multi_column_profiling/${updatedVal}/True/${method}`;
        axios
          .get(updatedURL)
          .then((response) => {
            const result = JSON.parse(response.data);
            console.log(result);
            setDataset(result.data ? JSON.parse(result.data) : []);

            setDepandancies(result.depandancies ? JSON.parse(result.depandancies) : []);
            setVersionNumber(result.versions_number ? result.versions_number : 0);
            setUpdatedVersion(result.updated_version ? JSON.parse(result.updated_version) : []);
            setCorelation(result.correlation ? JSON.parse(result.correlation) : []);
            setLoading(false);
          })
          .catch((error) => {
            console.log(error);
            setLoading(false);
          });
      });
    } else {
      // Handle logic when version is already equal to step
    }
  };
  const handelChange = (event, newValue) => {
    setLoading(true);
    console.log(newValue);
    const updatedURL = `http://127.0.0.1:8000/api/multi_column_profiling/${val}/${updated.updated}/${
      newValue.label ? newValue.label : 'pearson'
    }`;

    setSelectedValue(newValue);
    setMethod(newValue.label ? newValue.label : 'pearson');
    axios
      .get(updatedURL)
      .then((response) => {
        const result = JSON.parse(response.data);
        console.log(result);

        setVersionNumber(result.versions_number ? result.versions_number : 0);
        setCorelation(result.correlation ? JSON.parse(result.correlation) : []);
        setTopElectricity(result.top_elecricity ? JSON.parse(result.top_elecricity) : []);
        setTopGas(result.top_gaz ? JSON.parse(result.top_gaz) : []);
        setLoading(false);
        setDataset(result.data ? JSON.parse(result.data) : []);
        setDepandancies(result.depandancies ? JSON.parse(result.depandancies) : []);
        setUpdatedVersion(result.updated_version ? JSON.parse(result.updated_version) : []);
      })
      .catch((error) => {
        console.log(error);
        setLoading(false);
      });
  };

  const columns = useMemo(
    () => [
      {
        accessorKey: 'id',
        header: '',
        size: 150
      },
      {
        accessorKey: 'Electricity',
        header: 'Electricity',
        size: 150
      },
      {
        accessorKey: 'Gas_Boiler1', //normal accessorKey
        header: 'Gas_Boiler1',
        size: 150
      },
      {
        accessorKey: 'Gas_Boiler2', //normal accessorKey
        header: 'Gas_Boiler2',
        size: 150
      },
      {
        accessorKey: 'Gas_Boiler3', //normal accessorKey
        header: 'Gas_Boiler3',
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

  const updateAxisWithDelay = (newValue, setFunction) => {
    setLoading(true);
    setFunction(newValue);
    setTimeout(() => setLoading(false), 100);
  };

  useEffect(() => {
    axios.get(BaseURL).then((response) => {
      const result = JSON.parse(response.data);
      console.log(result);

      setVersionNumber(result.versions_number ? result.versions_number : 0);
      setCorelation(result.correlation ? JSON.parse(result.correlation) : []);
      setTopElectricity(result.top_elecricity ? JSON.parse(result.top_elecricity) : []);
      setTopGas(result.top_gaz ? JSON.parse(result.top_gaz) : []);
      setDataset(result.data ? JSON.parse(result.data) : []);
      setDepandancies(result.depandancies ? JSON.parse(result.depandancies) : []);
      setUpdatedVersion(result.updated_version ? JSON.parse(result.updated_version) : []);
      console.log(depandancies);
      setLoading(false);
    });
  }, []);

  return (
    <>
      <Grid container spacing={gridSpacing}>
        <Grid item lg={12} md={12} sm={12} xs={12}>
          <MainCard>
            <h3>Choose your data version </h3>
            {isLoading ? (
              <SkeletonEarningCard className="loading" />
            ) : (
              <>
                <Stepper nonLinear activeStep={updated.updated == 'False' ? activeStep : -1}>
                  {Array.from({ length: version_number }, (_, index) => (
                    <Step key={index}>
                      <StepLabel onClick={() => handleStepClick(index, 0)}>Version {index + 1}</StepLabel>
                    </Step>
                  ))}
                  {version_number >= 2 && (
                    <Step>
                      <StepLabel onClick={() => handleStepClick(parseInt(version_number), 1)}>All versions</StepLabel>
                    </Step>
                  )}
                </Stepper>
                {updatedVersions.length > 0 && (
                  <div>
                    <h3>Updated versions</h3>
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
            <h3>Features Correlation </h3>
            {isLoading ? (
              <SkeletonEarningCard />
            ) : (
              <Grid item lg={12} md={12} sm={12} xs={12} sx={{ display: 'flex' }}>
                <Autocomplete
                  style={{ margin: '50px' }}
                  disablePortal
                  id="combo-box-demo-1"
                  options={corelationMethodes}
                  value={selectedValue}
                  sx={{ flex: 1, marginRight: '20px' }}
                  renderInput={(params) => <TextField {...params} label="Correlation Method" />}
                  onChange={(event, newValue) => {
                    handelChange(event, newValue);
                  }}
                />

                <Autocomplete
                  disablePortal
                  style={{ margin: '50px' }}
                  id="combo-box-demo-2"
                  options={forms}
                  sx={{ flex: 1 }}
                  value={selectedValue2}
                  onChange={(event, newValue) => {
                    setSelectedValue2(newValue);
                    setDataForma(newValue.label);
                  }}
                  renderInput={(params) => <TextField {...params} label="Correlation Data Format" />}
                />
              </Grid>
            )}

            <Grid item lg={12} md={12} sm={12} xs={12}>
              {dataFormat == 'Table' ? (
                <CorrelationTbael isLoading={isLoading} data={corelation} columns={columns} />
              ) : (
                <Heatmap data={corelation} isLoading={isLoading} />
              )}
            </Grid>

            <Grid item lg={12} md={12} sm={12} xs={12}></Grid>
          </MainCard>
        </Grid>
        <Grid item lg={6} md={6} sm={12} xs={12}>
          <MainCard>
            <h3> Correlated Features with Electricity</h3>
            <ElectricityCorelation data={topElectricity} isLoading={isLoading} />
          </MainCard>
        </Grid>
        <Grid item lg={6} md={6} sm={12} xs={12}>
          <MainCard>
            <h3> Correlated Features with Gas</h3>
            <ElectricityCorelation data={topGas} isLoading={isLoading} />
          </MainCard>
        </Grid>

        <Grid item lg={12} md={12} sm={12} xs={12}>
          <MainCard>
            <h3> Features Interactions </h3>
            {isLoading ? (
              <SkeletonEarningCard />
            ) : (
              <Grid item lg={12} md={12} sm={12} xs={12} sx={{ display: 'flex' }}>
                <Autocomplete
                  style={{ margin: '50px' }}
                  disablePortal
                  id="combo-box-demo-1"
                  options={features}
                  value={xColumn}
                  sx={{ flex: 1, marginRight: '20px' }}
                  renderInput={(params) => <TextField {...params} label="Choose X column " />}
                  onChange={(event, newValue) => {
                    updateAxisWithDelay(newValue, setXColumn);
                  }}
                />

                <Autocomplete
                  disablePortal
                  style={{ margin: '50px' }}
                  id="combo-box-demo-2"
                  options={features}
                  sx={{ flex: 1 }}
                  value={yColumn}
                  onChange={(event, newValue) => {
                    updateAxisWithDelay(newValue, setYColumn);
                  }}
                  renderInput={(params) => <TextField {...params} label="Choose Y column" />}
                />
                <Autocomplete
                  disablePortal
                  style={{ margin: '50px' }}
                  id="combo-box-demo-2"
                  options={plot}
                  sx={{ flex: 1 }}
                  value={plotType}
                  onChange={(event, newValue) => {
                    updateAxisWithDelay(newValue, setPlotType);
                  }}
                  renderInput={(params) => <TextField {...params} label="Choose Plot type" />}
                />
              </Grid>
            )}

            <InteractionPlot
              data={dataset}
              xCol={xColumn.label ? xColumn.label : ''}
              yCol={yColumn.label ? yColumn.label : ''}
              plotType={plotType.label ? plotType.label : ''}
              isLoading={isLoading}
            />
          </MainCard>
        </Grid>

        <Grid item lg={12} md={12} sm={12} xs={12}>
          <MainCard>
            <h3> Functional Dependancies</h3>
            {isLoading ? (
              <SkeletonEarningCard />
            ) : (
              <>
                <Grid item lg={12} md={12} sm={12} xs={12} sx={{ display: 'flex' }}>
                  <Autocomplete
                    style={{ margin: '50px' }}
                    disablePortal
                    id="combo-box-demo-1"
                    options={features}
                    value={depandanteVariable}
                    sx={{ flex: 1, marginRight: '20px' }}
                    renderInput={(params) => <TextField {...params} label="Choose The Depandante Column " />}
                    onChange={(event, newValue) => {
                      updateAxisWithDelay(newValue, setDepandanteVariable);
                    }}
                  />
                </Grid>
                <Grid item lg={12} md={12} sm={12} xs={12} sx={{ display: 'flex' }}></Grid>

                {depandancies.map((item, index) => {
                  const key = item[0].replace(/'/g, '');
                  const description = item[1];
                  if ((description == 'date') & (description == depandanteVariable.label.toLowerCase()))
                    return (
                      <p style={{ textAlign: 'center' }} key={index}>
                        {key} <span style={{ color: 'red', fontWeight: '600' }}>-&gt;</span>{' '}
                        <span style={{ color: '#004aad' }}>{description}</span>
                      </p>
                    );
                  if (description == depandanteVariable.label)
                    return (
                      <p style={{ textAlign: 'center' }} key={index}>
                        {key} <span style={{ color: 'red', fontWeight: '600' }}>-&gt;</span>{' '}
                        <span style={{ color: '#004aad' }}>{description}</span>
                      </p>
                    );
                })}
              </>
            )}
          </MainCard>
        </Grid>
      </Grid>
    </>
  );
};

export default MultiColumnsProfiling;
