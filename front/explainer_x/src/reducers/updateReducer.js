import { UPDATE_UPDATED } from '../actions/actions';

const initialState = {
  updated: 'False',
  // other initial state properties
};

const updateReducer = (state = initialState, action) => {
  switch (action.type) {
    case UPDATE_UPDATED:
      return {
        ...state,
        updated: action.payload,
      };
    // other case statements for different actions
    default:
  
      return state;
  }
};

export default updateReducer;
