import { useSelector } from 'react-redux';

export const usePlayerState = () => useSelector((state) => state.playerState);

export const usePlayerHealth = () =>
  useSelector((state) => state.playerState.health);

export const usePlayerStatus = () =>
  useSelector((state) => state.playerState.status);

export const usePlayerInventory = () =>
  useSelector((state) => state.playerState.inventory);

export const usePlayerEquippedItems = () =>
  useSelector((state) => state.playerState.equipment);

export const usePlayerLocation = () =>
  useSelector((state) => state.playerState.location);

export const useWorldState = () => useSelector((state) => state.worldState);

export const useItemState = () => useSelector((state) => state.itemState);
