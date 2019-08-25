import {
  MARK_OPS_SOLVED,
  DELETE_OP,
  DELETE_ALL_OPS,
  TOGGLE_FAVORITE,
  DELETE_ALL_FAVORITES,
} from '../actions/actionTypes';

const initialState = [];

const opReducer = (state = initialState, action) => {
  console.log(action.type);
  const existentOps = state;
  switch (action.type) {
    case MARK_OPS_SOLVED:
      action.ops.forEach(e => {
        const found = existentOps.find(x => x.id === e.id);
        if (found) {
          found.timeStamps.push(...e.timeStamps);
          found.timesTaken.push(...e.timesTaken);
          found.favorite = e.favorite;
        } else {
          existentOps.push(e);
        }
      });
      // console.log(`${new Date().toISOString()} - op.reducer: opReducer: action.ops`);
      // console.log(action.ops);
      // console.log(existentOps);
      // console.log(newOps);
      return [...existentOps];
    case DELETE_OP:
      return state.filter(x => x.id !== action.id);
    case DELETE_ALL_OPS:
      return initialState;

    // FAVORITES
    case TOGGLE_FAVORITE:
      const found = existentOps.find(x => x.id === action.id);
      found.favorite = !found.favorite;
      return [...existentOps];
    case DELETE_ALL_FAVORITES:
      existentOps.forEach(e => {
        e.favorite = false;
      });
      return [...existentOps];
    // DEFAULT
    default:
      return state;
  }
};

export default opReducer;
