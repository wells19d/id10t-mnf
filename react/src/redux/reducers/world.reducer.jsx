const initialState = {
  area1: {
    clearing: {
      visited: false,
    },

    fallenNursery: {
      visited: false,
    },

    house1: {
      visited: false,
      doorUnlocked: false,
    },

    house2: {
      visited: false,
      doorUnlocked: false,
    },

    house3: {
      visited: false,
      doorUnlocked: false,
      safeUnlocked: false,
    },

    lakeEast: {
      visited: false,
    },

    lakeSouth: {
      visited: false,
    },

    massiveTree: {
      visited: false,
    },

    roadAccess: {
      visited: false,
    },

    securityGate: {
      visited: false,
      fuseReplaced: false,
      stationPowered: false,
      gateUnlocked: false,
    },

    silentGrove: {
      visited: false,
    },

    stoneRing: {
      visited: false,
      coalsCooled: false,
    },
  },

  area2: {
    outerCompound: {
      visited: false,
    },
  },
};

const worldReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'SET_WORLD':
      return {
        ...state,
        ...action.payload,
      };

    default:
      return state;
  }
};

export default worldReducer;
