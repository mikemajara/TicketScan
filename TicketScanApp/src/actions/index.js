import {
  TOGGLE_SETTING, //
} from './actionTypes';

// SETTINGS
export const changeSetting = setting => {
  return {
    type: TOGGLE_SETTING,
    setting,
  };
};

export {
  TOGGLE_SETTING, //
};
