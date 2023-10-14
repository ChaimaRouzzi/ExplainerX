// featureReducer.js
import { SET_SELECTED_FEATURES } from 'actions/featuresActions';

const initialState = {
  selectedFeatures: [],
};

const featureReducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_SELECTED_FEATURES:
      return {
        ...state,
        selectedFeatures: action.payload,
      };
    default:
      return state;
  }
};

export default featureReducer;
