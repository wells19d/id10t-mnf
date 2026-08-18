import clearing from './area1/clearing.js';
import fallenNursery from './area1/fallenNursery.js';
import house1 from './area1/house1.js';
import house2 from './area1/house2.js';
import house3 from './area1/house3.js';
import lakeEast from './area1/lakeEast.js';
import lakeSouth from './area1/lakeSouth.js';
import massiveTree from './area1/massiveTree.js';
import roadAccess from './area1/roadAccess.js';
import sgEast from './area1/sgEast.js';
import sgWest from './area1/sgWest.js';
import sgSouth from './area1/sgSouth.js';
import silentGrove from './area1/silentGrove.js';
import stoneRing from './area1/stoneRing.js';
import outerCompound from './area2/outerCompound.js';

const areaRegistry = {
  clearing,
  fallenNursery,
  house1,
  ...house1.rooms,
  house2,
  ...house2.rooms,
  house3,
  ...house3.rooms,
  lakeEast,
  lakeSouth,
  massiveTree,
  roadAccess,
  sgEast,
  sgWest,
  sgSouth,
  silentGrove,
  stoneRing,
  outerCompound,
};

export function getArea(location) {
  return areaRegistry[location];
}
