import React from 'react';
import { styled } from '@mui/material/styles';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import SVRModelBuilder from './svrModelBuilder';
import RandomForestModelBuilder from './rfModelBuilder';
import MLRModelBuilder from './mlrModelBuilder';

import { Grid, Card } from '@mui/material';
import { gridSpacing } from 'store/constant';

const StyledTabs = styled((props) => <Tabs {...props} TabIndicatorProps={{ children: <span className="MuiTabs-indicatorSpan" /> }} />)({
  '& .MuiTabs-indicator': {
    display: 'flex',
    justifyContent: 'center',
    backgroundColor: 'transparent'
  },
  '& .MuiTabs-indicatorSpan': {
    maxWidth: 90,
    width: '100%',
    backgroundColor: '#004aad'
  }
});

const StyledTab = styled((props) => <Tab disableRipple {...props} />)(({ theme }) => ({
  textTransform: 'none',
  fontWeight: theme.typography.fontWeightRegular,
  fontSize: theme.typography.pxToRem(15),
  marginRight: theme.spacing(1),
  color: 'rgba(255, 255, 255, 0.7)',
  '&.Mui-selected': {
    color: '#004aad',
    fontWeight: 'bold'
  },
  '&.Mui-focusVisible': {
    backgroundColor: 'rgba(100, 95, 228, 0.32)'
  },
  '&:not(.Mui-selected)': {
    // Styles for non-selected tabs
    color: 'black'
  }
}));

export default function CustomizedTabs() {
  const [value, setValue] = React.useState(0);

  const TabContent = ({ selectedTab }) => {
    if (selectedTab === 0) {
      return <SVRModelBuilder />;
    } else if (selectedTab === 1) {
      return <RandomForestModelBuilder />;
    } else if (selectedTab === 2) {
      return <MLRModelBuilder />;
    } else {
      return null;
    }
  };

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <>
      <Grid item xs={12}>
        <Grid container spacing={gridSpacing}>
          <Grid item lg={12} md={12} sm={12} xs={12}>
            <Card className="cardContainer">
              <StyledTabs value={value} onChange={handleChange} aria-label="styled tabs example" centered>
                <StyledTab label="SVR" />
                <StyledTab label="Random Forest" />
                <StyledTab label="MLR" />
              </StyledTabs>
              <Box sx={{ p: 8 }} />
            </Card>
          </Grid>
          <Grid item lg={12} md={12} sm={12} xs={12}>
            <TabContent selectedTab={value} />
          </Grid>
        </Grid>
      </Grid>
    </>
  );
}
