import { TOGGLE_SETTING } from '../actions';

/**
 * Settings declared here will be added to new store
 * Old settings will not be deleted as of now (2019-07-21 09:40:38)
 */
const initialState = {
  isAdditionEnabled: true,
  isSubtractionEnabled: true,
  isMultiplicationEnabled: true,
  isDivisionEnabled: true,
  isSynesthesiaEnabled: false,
  operationsPerRound: 5,
  level: 1,
  // exampleNewSetting: "exampleNewDefaultValue",
};

const settingsReducer = (state = initialState, action) => {
  switch (action.type) {
    case TOGGLE_SETTING:
      return {
        ...state,
        [action.setting.id]: action.setting.value,
      };

    // Possible option to pass operations.
    // case 'MARK_OPERATION_PASSED':
    //     return state.map(todo =>
    //         (todo.id === action.id)
    //             ? { ...todo, completed: !todo.completed } :
    //             todo)
    default:
      return state;
  }
};

export default settingsReducer;
