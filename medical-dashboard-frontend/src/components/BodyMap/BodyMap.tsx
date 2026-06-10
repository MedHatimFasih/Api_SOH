import React from 'react';
import { useAppStore } from '../stores/appStore';
import { Organ } from '../types/medical';
import { Tooltip } from './UI/Tooltip';
import styles from './BodyMap.module.css';

const organs: Organ[] = [
  // Groupe Vital (5003)
  { id: 'cardiac', name: 'Cœur', icon: '❤️', color: '#ef4444', apiPort: 5003, group: 'vital', critical: true },
  { id: 'respiratory', name: 'Poumons', icon: '🫁', color: '#3b82f6', apiPort: 5003, group: 'vital', critical: true },
  { id: 'neural', name: 'Cerveau', icon: '🧠', color: '#8b5cf6', apiPort: 5003, group: 'vital', critical: true },
  { id: 'hepatic', name: 'Foie', icon: '🟤', color: '#92400e', apiPort: 5003, group: 'vital', critical: false },
  
  // Groupe Support (5002)
  { id: 'renal', name: 'Reins', icon: '🫘', color: '#f97316', apiPort: 5002, group: 'support', critical: false },
  { id: 'digestive', name: 'Système Digestif', icon: '🫃', color: '#10b981', apiPort: 5002, group: 'support', critical: false },
  { id: 'dermal', name: 'Peau', icon: '🤚', color: '#6b7280', apiPort: 5002, group: 'support', critical: false },
  { id: 'endocrine', name: 'Système Endocrinien', icon: '⚗️', color: '#8b5cf6', apiPort: 5002, group: 'support', critical: false },
  
  // Groupe Spécialisé (5004)
  { id: 'immune', name: 'Système Immunitaire', icon: '🛡️', color: '#6366f1', apiPort: 5004, group: 'specialized', critical: false },
  { id: 'musculoskeletal', name: 'Système Musculosquelettique', icon: '💪', color: '#ec4899', apiPort: 5004, group: 'specialized', critical: false },
  { id: 'hematological', name: 'Système Sanguin', icon: '🩸', color: '#dc2626', apiPort: 5004, group: 'specialized', critical: true },
  { id: 'reproductive', name: 'Système Reproductif', icon: '👶', color: '#f59e0b', apiPort: 5004, group: 'specialized', critical: false },
];

export const BodyMap: React.FC = () => {
  const { selectedOrgan, selectOrgan, allSystemsStatus } = useAppStore();

  const getOrganStatus = (organId: string) => {
    const status = allSystemsStatus.find(s => s.system === organId);
    return status?.status || 'unknown';
  };

  const getOrganHealth = (organId: string) => {
    const status = allSystemsStatus.find(s => s.system === organId);
    return status?.health_status || 'unknown';
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
        <span className="mr-2">🏥</span> Carte Corporelle Interactive
      </h2>
      
      <div className="relative w-full h-[600px] bg-gradient-to-b from-blue-50 to-white rounded-lg border border-gray-200 overflow-hidden">
        {/* Corps humain SVG simplifié */}
        <svg viewBox="0 0 800 600" className="w-full h-full">
          {/* Contour du corps */}
          <path
            d="M400,50 Q450,100 450,200 Q450,300 420,400 Q400,500 350,550 Q300,550 250,550 Q200,500 180,400 Q150,300 150,200 Q150,100 200,50 Q300,30 400,50"
            fill="#f3f4f6"
            stroke="#d1d5db"
            strokeWidth="2"
          />
          
          {/* Organes positionnés approximativement */}
          {organs.map((organ, index) => {
            const position = getOrganPosition(organ.id);
            const status = getOrganStatus(organ.id);
            const health = getOrganHealth(organ.id);
            const isSelected = selectedOrgan === organ.id;
            const isOnline = status === 'online';
            const isCritical = organ.critical;
            
            return (
              <Tooltip key={organ.id} content={`${organ.name} - ${isOnline ? 'En ligne' : 'Hors ligne'}`}>
                <g
                  onClick={() => selectOrgan(organ.id)}
                  className={`cursor-pointer transition-all duration-200 ${isSelected ? 'scale-110' : 'hover:scale-105'}`}
                >
                  {/* Cercle de l'organe */}
                  <circle
                    cx={position.x}
                    cy={position.y}
                    r={isSelected ? 35 : 30}
                    fill={organ.color}
                    fillOpacity={isOnline ? (isSelected ? 0.9 : 0.7) : 0.3}
                    stroke={isCritical ? '#dc2626' : organ.color}
                    strokeWidth={isCritical ? 3 : 2}
                    className={`${isSelected ? 'animate-pulse' : ''}`}
                  />
                  
                  {/* Icône */}
                  <text
                    x={position.x}
                    y={position.y}
                    textAnchor="middle"
                    dy="0.3em"
                    className="text-2xl select-none"
                    fill="white"
                  >
                    {organ.icon}
                  </text>
                  
                  {/* Indicateur de statut */}
                  <circle
                    cx={position.x + 25}
                    cy={position.y - 25}
                    r="8"
                    fill={isOnline ? '#10b981' : '#ef4444'}
                  />
                  
                  {/* Nom de l'organe */}
                  <text
                    x={position.x}
                    y={position.y + 45}
                    textAnchor="middle"
                    className="text-sm font-semibold select-none"
                    fill={organ.color}
                  >
                    {organ.name.split(' ')[0]}
                  </text>
                </g>
              </Tooltip>
            );
          })}
        </svg>
        
        {/* Légende */}
        <div className="absolute bottom-4 left-4 bg-white/90 backdrop-blur-sm rounded-lg p-4 shadow-lg">
          <h3 className="font-semibold text-gray-700 mb-2">Légende</h3>
          <div className="flex flex-wrap gap-3">
            <div className="flex items-center">
              <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
              <span className="text-sm text-gray-600">En ligne</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
              <span className="text-sm text-gray-600">Hors ligne</span>
            </div>
            <div className="flex items-center">
              <div className="w-3 h-3 border-2 border-red-600 rounded-full mr-2"></div>
              <span className="text-sm text-gray-600">Critique</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Fonction utilitaire pour positionner les organes
function getOrganPosition(organId: string): { x: number; y: number } {
  const positions: Record<string, { x: number; y: number }> = {
    // Tête
    neural: { x: 400, y: 100 },
    
    // Poitrine
    cardiac: { x: 400, y: 200 },
    respiratory: { x: 350, y: 220 },
    
    // Abdomen
    hepatic: { x: 420, y: 320 },
    digestive: { x: 380, y: 350 },
    
    // Bas
    renal: { x: 340, y: 400 },
    
    // Divers
    dermal: { x: 150, y: 250 },
    endocrine: { x: 650, y: 250 },
    immune: { x: 650, y: 350 },
    musculoskeletal: { x: 200, y: 350 },
    hematological: { x: 600, y: 150 },
    reproductive: { x: 400, y: 450 },
  };
  
  return positions[organId] || { x: 400, y: 300 };
}