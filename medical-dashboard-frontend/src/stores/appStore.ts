import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';
import { Organ, OrganData, Alert, SystemStatus } from '../types/medical.ts';

interface AppState {
  // État
  selectedOrgan: string | null;
  organData: Record<string, OrganData>;
  loadingStates: Record<string, boolean>;
  errors: Record<string, string | null>;
  alerts: Alert[];
  allSystemsStatus: SystemStatus[];
  
  // Actions
  selectOrgan: (organId: string | null) => void;
  setOrganData: (organId: string, data: OrganData) => void;
  setLoading: (organId: string, loading: boolean) => void;
  setError: (organId: string, error: string | null) => void;
  addAlert: (alert: Alert) => void;
  clearError: (organId: string) => void;
  setAllSystemsStatus: (statuses: SystemStatus[]) => void;
}

export const useAppStore = create(
  immer<AppState>((set) => ({
    selectedOrgan: null,
    organData: {},
    loadingStates: {},
    errors: {},
    alerts: [],
    allSystemsStatus: [],

    selectOrgan: (organId) =>
      set((state) => {
        state.selectedOrgan = organId;
      }),

    setOrganData: (organId, data) =>
      set((state) => {
        state.organData[organId] = data;
        state.loadingStates[organId] = false;
        state.errors[organId] = null;
      }),

    setLoading: (organId, loading) =>
      set((state) => {
        state.loadingStates[organId] = loading;
      }),

    setError: (organId, error) =>
      set((state) => {
        state.errors[organId] = error;
        state.loadingStates[organId] = false;
      }),

    addAlert: (alert) =>
      set((state) => {
        state.alerts.unshift(alert);
        if (state.alerts.length > 20) {
          state.alerts.pop();
        }
      }),

    clearError: (organId) =>
      set((state) => {
        state.errors[organId] = null;
      }),

    setAllSystemsStatus: (statuses) =>
      set((state) => {
        state.allSystemsStatus = statuses;
      }),
  }))
);