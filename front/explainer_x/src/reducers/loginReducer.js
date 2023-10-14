import { LOGIN_FAILURE } from "actions/loginActions";
import { LOGIN_SUCCESS } from "actions/loginActions";

const initialState = {
    isLoggedIn: false,
    userData: null,
  };  

export default function loginReducer(state = initialState, action) {
  switch (action.type) {
    case LOGIN_SUCCESS:
        console.log("login reducer")
      return {
        ...state,
        isLoggedIn: true,
        userData: action.payload,
      };
    case LOGIN_FAILURE:
      return {
        ...state,
        isLoggedIn: false,
        userData: null,
      };
    default: 
      return state;
  }
}
