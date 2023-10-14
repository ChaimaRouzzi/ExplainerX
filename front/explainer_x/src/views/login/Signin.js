import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { loginSuccess, loginFailure } from 'actions/loginActions';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Radio from '@mui/material/Radio';
import Container from '@mui/material/Container';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useSelector } from 'react-redux';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';

const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

import logo from '../../assets/images/logo.png'

const defaultTheme = createTheme();

function SignIn() {
  const [open, setOpen] = React.useState(false);

  const handleClick = () => {
    setOpen(true);
  };

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setOpen(false);
  };
  const [role, setValue] = React.useState('Data scientist');

  const handleChange = (event) => {
    setValue(event.target.value);
  };

  const dispatch = useDispatch();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignIn = async (e) => {
    e.preventDefault();

    try {
      console.log(role)
      const response = await fetch('http://localhost:8000/api/login/authenticate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password,role })
      });

      const data = await response.json();
      handleClick()
      console.log(data);
      if (response.ok) {
        console.log('Login successful:', data);
        dispatch(loginSuccess(data));
        window.localStorage.setItem('isLoggedIn', 'true');
  
        // Fetch initial profiling data after successful login
        try {
          const initialProfilingResponse = await fetch('http://localhost:8000/api/initial_profiling', {
            method: 'GET'
          });
  
          const initialProfilingData = await initialProfilingResponse.json();
          console.log('Initial profiling data:', initialProfilingData);
          
         
        } catch (error) {
          handleClick()
          console.error('Error fetching initial profiling data:', error);
        }
      } else {
        dispatch(loginFailure());
        console.error('Login failed');
      }
    } catch (error) {
      console.error('Error during login:', error);
    }
  };

  const isLoggedIn = useSelector((state) => state.login.isLoggedIn);
  const userData = useSelector((state) => state.login.userData);
  console.log(isLoggedIn);
  console.log(userData);

  return (
    <div className='sign-in'>
      
   
    <ThemeProvider theme={defaultTheme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            height: '100vh'
          }}
        >
          <Card
            elevation={0}
            sx={{
              width:1000,
              height:500,
              borderRadius: 6
            }}
          >
            <CardContent>
              <Box
                sx={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center'
                }}
              >
               
                <img width="80px" src={logo} alt=""/>
                <h2  style={{ color:'#004aad',textAlign:'left',marginTop:'40px' }} >Sign in</h2>
                  
                <form onSubmit={handleSignIn}>
                 
                  <TextField
                  
                    margin="normal"
                    required
                    fullWidth
                    id="email"
                    label="Email Address"
                    name="email"
                    autoComplete="email"
                    autoFocus
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                 
                  <TextField
                  style={{ marginTop:"25px",marginBottom:'25px'}}
                    margin="normal"
                    required
                    fullWidth
                    name="password"
                    label="Password"
                    type="password"
                    id="password"
                    autoComplete="current-password"
                    
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
         
  <FormControl >
    <FormLabel id="demo-controlled-radio-buttons-group" style={{ marginRight: '30px',fontWeight:'600',color:"#004aad"}}>Role</FormLabel>
    <RadioGroup 
    style={{display:'inline'}}
      aria-labelledby="demo-controlled-radio-buttons-group"
      name="controlled-radio-buttons-group"
      value={role}
      onChange={handleChange}
    >
      <FormControlLabel style={{fontSize:'10px'}} value="data_scientist" control={<Radio />} label="Data scientist" />
      <FormControlLabel value="decideur" control={<Radio />} label="Decision maker" />
    </RadioGroup>
  </FormControl>
  


                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    sx={{
                      width: '100%',
                      marginTop:"40px",
                      padding: '8px 0',
                      backgroundColor: '#004aad',
                      '&:hover': {
                        backgroundColor: '#004aad'
                      }
                    }}
                  >
                    Sign In
                  </Button>
                </form>
              </Box>
            </CardContent>
          </Card>
        </Box>
      </Container>
    </ThemeProvider>
    <Snackbar open={open} autoHideDuration={6000} onClose={handleClose}  anchorOrigin={{  vertical:'bottom', horizontal:'right' }}>
        <Alert  severity="error" onClose={handleClose}  >
        The login information are not correct
        </Alert>
      </Snackbar>
    </div>
  );
}

export default SignIn;
