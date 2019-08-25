import { combineReducers } from 'redux';
import opReducer from './op.reducer';
import settingsReducer from './settings.reducer';

export default combineReducers({
  operations: opReducer,
  settings: settingsReducer,
});
