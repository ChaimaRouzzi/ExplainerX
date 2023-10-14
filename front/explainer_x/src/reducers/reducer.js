import { combineReducers } from 'redux';

// reducer import
import customizationReducer from './customizationReducer';
import versionReducer from './versionReducer';
import loginReducer from './loginReducer';
import updateReducer from './updateReducer';
import featureReducer from './featuresReducer';
// ==============================|| COMBINE REDUCER ||============================== //

const reducer = combineReducers({
  customization: customizationReducer,
  version: versionReducer, 
  login: loginReducer, 
  updated:updateReducer, 
  feature: featureReducer
});

export default reducer;
