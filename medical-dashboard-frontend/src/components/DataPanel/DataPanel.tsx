import React, { useState, useEffect } from 'react';
import { useAppStore } from '../stores/appStore';
import { useOrganData } from '../hooks/useOrganData';
import { LoadingSpinner } from './UI/LoadingSpinner';
import { ErrorMessage } from './UI/ErrorMessage';
import { Button } from './UI/Button';
import { AlertTriangle, Activity, Heart, Brain, Liver, Shield } from 'lucide-react';
import { Organ, OrganData } from '../types/medical';

const organs: Organ[] = [
  { id: 'cardiac', name: 'Cœur', icon: '❤️', color: '#ef4444', apiPort: 5003, group: 'vital', critical: true },
  { id: 'respiratory', name: 'Poumons', icon: '🫁', color: '#3b82f6', apiPort: 5003, group: 'vital', critical: true },
  { id: 'neural', name: 'Cerveau', icon: '🧠', color: '#8b5cf6', apiPort: 5003, group: 'vital', critical: true },
  { id: 'hepatic', name: 'Foie', icon: '🟤', color: '#92400e', apiPort: 5003, group: 'vital', critical: false },
  { id: 'renal', name: 'Reins', icon: '🫘', color: '#f97316', apiPort: 5002, group: 'support', critical: false },
  { id: 'digestive', name: 'Système Digestif', icon: '🫃', color: '#10b981', apiPort: 5002, group: 'support', critical: false },
  { id: 'dermal', name: 'Peau', icon: '🤚', color: '#6b7280', apiPort: 5002, group: 'support', critical: false },
  { id: 'endocrine', name: 'Système Endocrinien', icon: '⚗️', color: '#8b5cf6', apiPort: 5002, group: 'support', critical: false },
  { id: 'immune', name: 'Système Immunitaire', icon: '🛡️', color: '#6366f1', apiPort: 5004, group: 'specialized', critical: false },
  { id: 'musculoskeletal', name: 'Système Musculosquelettique', icon: '💪', color: '#ec4899', apiPort: 5004, group: 'specialized', critical: false },
  { id: 'hematological', name: 'Système Sanguin', icon: '🩸', color: '#dc2626', apiPort: 5004, group: 'specialized', critical: true },
  { id: 'reproductive', name: 'Système Reproductif', icon: '👶', color: '#f59e0b', apiPort: 5004, group: 'specialized', critical: false },
];

export const DataPanel: React.FC = () => {
  const { selectedOrgan } = useAppStore();
  const organ = organs.find(o => o.id === selectedOrgan);
  const { data, loading, error, refresh } = useOrganData(organ || null, true);
  const [simulationLoading, setSimulationLoading] = useState(false);

  const handleSimulate = async (condition: string) => {
    if (!organ) return;
    
    setSimulationLoading(true);
    try {
      // Ici, vous implémenteriez l'appel API pour simuler une condition
      // await apiClient.simulateCondition(organ.group, organ.id, condition);
      setTimeout(() => {
        alert(`Simulation ${condition} activée pour ${organ.name}`);
        setSimulationLoading(false);
        refresh();
      }, 1000);
    } catch (error) {
      console.error('Simulation error:', error);
      setSimulationLoading(false);
    }
  };

  if (!selectedOrgan) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-8 flex flex-col items-center justify-center h-full">
        <Activity size={64} className="text-gray-300 mb-4" />
        <h3 className="text-xl font-semibold text-gray-600 mb-2">Aucun organe sélectionné</h3>
        <p className="text-gray-500 text-center">
          Cliquez sur un organe dans la carte corporelle pour voir ses données détaillées
        </p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-8 flex items-center justify-center h-full">
        <LoadingSpinner size="lg" text={`Chargement des données de ${organ?.name}...`} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-8 h-full">
        <ErrorMessage
          title="Erreur de chargement"
          message={error}
          onRetry={refresh}
        />
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 h-full overflow-y-auto">
      {data && (
        <>
          {/* En-tête */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center">
              <span className="text-3xl mr-3">{organ?.icon}</span>
              <div>
                <h2 className="text-2xl font-bold text-gray-800">{organ?.name}</h2>
                <div className="flex items-center mt-1">
                  <div className={`w-3 h-3 rounded-full mr-2 ${
                    data.status === 'online' ? 'bg-green-500' : 'bg-red-500'
                  }`} />
                  <span className="text-sm text-gray-600">
                    {data.status === 'online' ? 'En ligne' : 'Hors ligne'} • 
                    Santé: <span className={`font-medium ${
                      data.health_status === 'normal' ? 'text-green-600' :
                      data.health_status === 'elevated' ? 'text-yellow-600' :
                      data.health_status === 'low' ? 'text-red-600' : 'text-gray-600'
                    }`}>{data.health_status}</span>
                  </span>
                </div>
              </div>
            </div>
            <Button variant="secondary" size="sm" onClick={refresh}>
              Rafraîchir
            </Button>
          </div>

          {/* Statut */}
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-700 mb-3 flex items-center">
              <Activity size={20} className="mr-2" />
              Statut du Système
            </h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-500">Condition actuelle</p>
                <p className="text-lg font-medium">{data.current_condition || 'Normal'}</p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-sm text-gray-500">Dernière mise à jour</p>
                <p className="text-lg font-medium">
                  {new Date(data.timestamp).toLocaleTimeString()}
                </p>
              </div>
            </div>
          </div>

          {/* Métriques */}
          <div className="mb-8">
            <h3 className="text-lg font-semibold text-gray-700 mb-3 flex items-center">
              <Heart size={20} className="mr-2" />
              Métriques
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {Object.entries(data.metrics || {}).map(([key, value]) => (
                <div key={key} className="bg-blue-50 p-4 rounded-lg">
                  <p className="text-sm text-blue-600 font-medium capitalize">
                    {key.replace(/_/g, ' ')}
                  </p>
                  <p className="text-2xl font-bold text-gray-800">
                    {typeof value === 'number' ? value.toFixed(2) : String(value)}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Paramètres */}
          {data.parameters && (
            <div className="mb-8">
              <h3 className="text-lg font-semibold text-gray-700 mb-3 flex items-center">
                <Brain size={20} className="mr-2" />
                Paramètres
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {Object.entries(data.parameters).map(([key, value]) => (
                  <div key={key} className="bg-green-50 p-4 rounded-lg">
                    <p className="text-sm text-green-600 font-medium">{key}</p>
                    <p className="text-xl font-bold text-gray-800">{value}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Simulation */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <h3 className="text-lg font-semibold text-gray-700 mb-4 flex items-center">
              <Shield size={20} className="mr-2" />
              Simulation Médicale
            </h3>
            <div className="flex flex-wrap gap-3">
              {getConditionsForOrgan(organ!.id).map((condition) => (
                <Button
                  key={condition}
                  variant="danger"
                  size="sm"
                  loading={simulationLoading}
                  onClick={() => handleSimulate(condition)}
                  className="capitalize"
                >
                  Simuler {condition}
                </Button>
              ))}
              <Button
                variant="success"
                size="sm"
                loading={simulationLoading}
                onClick={() => handleSimulate('normal')}
              >
                Retour à la normale
              </Button>
            </div>
            <p className="text-sm text-gray-500 mt-3">
              Attention: Les simulations modifient temporairement les données de l'organe
            </p>
          </div>
        </>
      )}
    </div>
  );
};

function getConditionsForOrgan(organId: string): string[] {
  const conditions: Record<string, string[]> = {
    cardiac: ['tachycardie', 'bradycardie', 'arythmie', 'hypertension'],
    respiratory: ['asthme', 'bpco', 'apnee', 'hyperventilation'],
    neural: ['epilepsie', 'migraine', 'trouble_sommeil', 'stress'],
    hepatic: ['hepatite', 'cirrhose'],
    renal: ['insuffisance', 'infection'],
    digestive: ['ulcere', 'diarrhee'],
    dermal: ['brulure', 'eczema'],
    endocrine: ['diabete', 'stress'],
    immune: ['infection', 'autoimmune', 'immunodeficiency'],
    musculoskeletal: ['arthritis', 'osteoporosis', 'muscle_strain'],
    hematological: ['anemia', 'leukemia', 'thrombocytopenia'],
    reproductive: ['infertility', 'hormonal_imbalance'],
  };
  
  return conditions[organId] || [];
}