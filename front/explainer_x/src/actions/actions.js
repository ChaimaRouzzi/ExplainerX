// action - customization reducer
export const SET_MENU = '@customization/SET_MENU';
export const MENU_TOGGLE = '@customization/MENU_TOGGLE';
export const MENU_OPEN = '@customization/MENU_OPEN';
export const SET_FONT_FAMILY = '@customization/SET_FONT_FAMILY';
export const SET_BORDER_RADIUS = '@customization/SET_BORDER_RADIUS';
export const UPDATE_VERSION = 'UPDATE_VERSION';
export const UPDATE_UPDATED = 'UPDATE_UPDATED';

export const updateVersion = (version) => ({
  type: UPDATE_VERSION,
  payload: version,
});


export const updateUpdated = (updated) => ({
  type: UPDATE_UPDATED,
  payload: updated,
});