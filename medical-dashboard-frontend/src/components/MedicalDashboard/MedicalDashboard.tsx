import React, { useState } from 'react';
import { BodyMap } from '../BodyMap/BodyMap';
import { DataPanel } from '../DataPanel/DataPanel';
import { useAppStore } from '../../stores/appStore';
import { LoadingSpinner } from '../UI/LoadingSpinner';
import { ErrorMessage } from '../UI/ErrorMessage';
import { useDashboardData } from '../../hooks/useDashboardData';
import { Alert, Activity, BarChart3, ShieldAlert } from 'lucide-react';

export const MedicalDashboard: React.FC = () => {
  const { alerts } = useAppStore();
  const [autoRefresh, setAutoRefresh] = useState(true);
  const { dashboardData, loading, error } = useDashboardData(autoRefresh);

  if (loading && !dashboardData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 flex items-center justify-center">
        <LoadingSpinner size="lg" text="Chargement du dashboard médical..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 flex items-center justify-center">
        <ErrorMessage message={error} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 p-4 md:p-6">
      {/* En-tête */}
      <header className="mb-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-800 flex items-center">
              <Activity className="mr-3 text-blue-600" size={32} />
              Dashboard Médical Avancé
            </h1>
            <p className="text-gray-600 mt-2">
              Surveillance en temps réel des 12 systèmes corporels
            </p>
          </div>
          
          <div className="flex items-center space-x-4 mt-4 md:mt-0">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
              <span className="text-sm text-gray-600">
                {dashboardData?.overview.online_systems || 0}/{dashboardData?.overview.total_systems || 12} systèmes
              </span>
            </div>
            <button
              onClick={() => setAutoRefresh(!autoRefresh)}
              className={`px-4 py-2 rounded-lg font-medium ${
                autoRefresh ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'
              }`}
            >
              {autoRefresh ? 'Auto-refresh: ON' : 'Auto-refresh: OFF'}
            </button>
          </div>
        </div>
      </header>

      {/* Statistiques globales */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-xl shadow">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg mr-3">
              <Activity className="text-blue-600" size={24} />
            </div>
            <div>
              <p className="text-sm text-gray-500">Systèmes en ligne</p>
              <p className="text-2xl font-bold text-gray-800">
                {dashboardData?.overview.online_systems || 0}
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-xl shadow">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg mr-3">
              <BarChart3 className="text-green-600" size={24} />
            </div>
            <div>
              <p className="text-sm text-gray-500">Santé globale</p>
              <p className="text-2xl font-bold text-gray-800">
                {dashboardData?.overview.health_percentage?.toFixed(1) || 0}%
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-xl shadow">
          <div className="flex items-center">
            <div className="p-2 bg-red-100 rounded-lg mr-3">
              <ShieldAlert className="text-red-600" size={24} />
            </div>
            <div>
              <p className="text-sm text-gray-500">Alertes actives</p>
              <p className="text-2xl font-bold text-gray-800">
                {alerts.filter(a => a.level === 'critical' || a.level === 'error').length}
              </p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-xl shadow">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg mr-3">
              <Alert className="text-purple-600" size={24} />
            </div>
            <div>
              <p className="text-sm text-gray-500">Critiques offline</p>
              <p className="text-2xl font-bold text-gray-800">
                {typeof dashboardData?.overview.critical_offline === 'number' 
                  ? dashboardData.overview.critical_offline 
                  : 0}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Alertes récentes */}
      {alerts.length > 0 && (
        <div className="mb-6">
          <div className="bg-white rounded-xl shadow-lg p-4">
            <h3 className="text-lg font-semibold text-gray-700 mb-3 flex items-center">
              <Alert className="mr-2" size={20} />
              Alertes Récentes
            </h3>
            <div className="space-y-2 max-h-40 overflow-y-auto">
              {alerts.slice(0, 5).map((alert, index) => (
                <div
                  key={index}
                  className={`p-3 rounded-lg border-l-4 ${
                    alert.level === 'critical'
                      ? 'bg-red-50 border-red-500'
                      : alert.level === 'error'
                      ? 'bg-orange-50 border-orange-500'
                      : alert.level === 'warning'
                      ? 'bg-yellow-50 border-yellow-500'
                      : 'bg-blue-50 border-blue-500'
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-medium text-gray-800">{alert.message}</p>
                      <p className="text-sm text-gray-500 mt-1">
                        {new Date(alert.timestamp).toLocaleTimeString()}
                      </p>
                    </div>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      alert.level === 'critical'
                        ? 'bg-red-100 text-red-800'
                        : alert.level === 'error'
                        ? 'bg-orange-100 text-orange-800'
                        : alert.level === 'warning'
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-blue-100 text-blue-800'
                    }`}>
                      {alert.level.toUpperCase()}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Contenu principal */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <BodyMap />
        </div>
        <div className="lg:col-span-1">
          <DataPanel />
        </div>
      </div>

      {/* Pied de page */}
      <footer className="mt-6 pt-6 border-t border-gray-200 text-center text-gray-500 text-sm">
        <p>Dashboard Médical Avancé v1.0 • Surveillance en temps réel des systèmes corporels</p>
        <p className="mt-1">
          Données mises à jour: {dashboardData?.timestamp ? 
          new Date(dashboardData.timestamp).toLocaleTimeString() : '--:--:--'}
        </p>
      </footer>
    </div>
  );
};