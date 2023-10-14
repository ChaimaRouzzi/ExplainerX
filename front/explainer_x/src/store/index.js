import { createStore } from 'redux';
import reducer from 'reducers/reducer';
// ==============================|| REDUX - MAIN STORE ||============================== //

const store = createStore(reducer);
const persister = 'Free';

export { store, persister };
