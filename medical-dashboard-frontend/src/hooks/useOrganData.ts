import { useEffect, useCallback } from 'react';
import { apiClient } from '../utils/apiClient';
import { useAppStore } from '../stores/appStore';
import { Organ } from '../types/medical';

export const useOrganData = (organ: Organ | null, autoRefresh: boolean = false) => {
  const {
    organData,
    loadingStates,
    errors,
    setOrganData,
    setLoading,
    setError,
    addAlert,
  } = useAppStore();

  const fetchOrganData = useCallback(async () => {
    if (!organ) return;

    const organId = organ.id;
    setLoading(organId, true);

    try {
      const data = await apiClient.getSystemStatus(organ.group, organ.id);
      
      setOrganData(organId, data);
      
      // Ajouter une alerte si le système est hors ligne
      if (data.status?.status === 'offline') {
        addAlert({
          timestamp: new Date().toISOString(),
          level: 'error',
          message: `${organ.name} est hors ligne`,
          group: organ.group,
          system: organ.id,
        });
      }
    } catch (error: any) {
      setError(organId, error.message || 'Erreur de chargement');
      addAlert({
        timestamp: new Date().toISOString(),
        level: 'error',
        message: `Impossible de charger les données de ${organ.name}`,
        group: organ.group,
        system: organ.id,
      });
    }
  }, [organ, setOrganData, setLoading, setError, addAlert]);

  useEffect(() => {
    if (organ && autoRefresh) {
      fetchOrganData();
      const interval = setInterval(fetchOrganData, 30000); // Rafraîchir toutes les 30s
      return () => clearInterval(interval);
    }
  }, [organ, autoRefresh, fetchOrganData]);

  return {
    data: organ ? organData[organ.id] : null,
    loading: organ ? loadingStates[organ.id] || false : false,
    error: organ ? errors[organ.id] : null,
    refresh: fetchOrganData,
  };
};