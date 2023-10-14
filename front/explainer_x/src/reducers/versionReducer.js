import { UPDATE_VERSION } from '../actions/actions';

const initialState = {
  version: 0,
  // other initial state properties
};

const versionReducer = (state = initialState, action) => {
  switch (action.type) {
    case UPDATE_VERSION:
      return {
        ...state,
        version: action.payload,
      };
    // other case statements for different actions
    default:
      console.log(state)
      return state;
  }
};

export default versionReducer;
