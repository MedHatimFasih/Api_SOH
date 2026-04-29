import { useState, useEffect, useCallback } from 'react';
import { apiClient } from '../utils/apiClient';
import { useAppStore } from '../stores/appStore';
import { DashboardData } from '../types';

export const useDashboardData = (autoRefresh: boolean) => {
  const { addAlert, setAllSystemsStatus } = useAppStore();
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboard = useCallback(async () => {
    try {
      setLoading(true);
      const [dashboard, systemsStatus] = await Promise.all([
        apiClient.getDashboard(),
        apiClient.getAllSystemsStatus(),
      ]);
      
      setDashboardData(dashboard);
      setAllSystemsStatus(systemsStatus.by_group ? 
        Object.values(systemsStatus.by_group).flat() : []);
      
      if (systemsStatus.summary?.critical_offline > 0) {
        addAlert({
          timestamp: new Date().toISOString(),
          level: 'critical',
          message: `${systems.summary.critical_offline} système(s) critique(s) hors ligne`,
        });
      }
      setError(null);
    } catch (error: any) {
      setError(error.message || 'Impossible de charger les données du dashboard');
      addAlert({
        timestamp: new Date().toISOString(),
        level: 'error',
        message: 'Impossible de charger les données du dashboard',
      });
    } finally {
      setLoading(false);
    }
  }, [addAlert, setAllSystemsStatus]);

  useEffect(() => {
    fetchDashboard();
    
    if (autoRefresh) {
      const interval = setInterval(fetchDashboard, 15000);
      return () => clearInterval(interval);
    }
  }, [autoRefresh, fetchDashboard]);

  return { dashboardData, loading, error };
};
