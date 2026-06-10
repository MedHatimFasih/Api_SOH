export interface Organ {
  id: string;
  name: string;
  icon: string;
  color: string;
  apiPort: number;
  group: string;
  critical: boolean;
  description?: string;
}

export interface OrganData {
  system: string;
  name: string;
  icon: string;
  status: 'online' | 'offline' | 'error';
  health_status: string;
  current_condition?: string;
  metrics: Record<string, any>;
  parameters?: Record<string, any>;
  timestamp: string;
}

export interface Group {
  id: string;
  name: string;
  description: string;
  color: string;
  priority: number;
  systems: Organ[];
}

export interface SystemStatus {
  group: string;
  system: string;
  status: string;
  health_status: string;
  response_time_ms?: number;
}

export interface Alert {
  timestamp: string;
  level: 'critical' | 'error' | 'warning' | 'info';
  message: string;
  group?: string;
  system?: string;
}

export interface DashboardData {
  timestamp: string;
  overview: {
    total_groups: number;
    total_systems: number;
    online_systems: number;
    health_percentage: number;
    critical_offline: number | string;
  };
  groups_health: Record<string, any>;
  systems_health: Record<string, any>;
  recent_alerts: Alert[];
}