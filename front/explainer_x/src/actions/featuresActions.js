// featureActions.js

export const SET_SELECTED_FEATURES = 'SET_SELECTED_FEATURES';

export const setSelectedFeatures = (features) => ({
  type: SET_SELECTED_FEATURES,
  payload: features,
});
