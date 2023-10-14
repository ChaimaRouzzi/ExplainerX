// actions.js
export const LOGIN_SUCCESS = 'LOGIN_SUCCESS';
export const LOGIN_FAILURE = 'LOGIN_FAILURE';

export function loginSuccess(userData) {
    console.log("login action")
    console.log(userData)
  return { type: LOGIN_SUCCESS, payload: userData };
}

export function loginFailure() {
  return { type: LOGIN_FAILURE };
}
