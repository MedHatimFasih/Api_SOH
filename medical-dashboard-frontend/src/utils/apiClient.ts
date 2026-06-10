import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import { useAppStore } from '../stores/appStore';
import { DashboardData, SystemStatus, Alert, OrganData } from '../types/medical';

const ORCHESTRATION_API = import.meta.env.VITE_ORCHESTRATION_API_URL || 'http://localhost:5000';

export class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: ORCHESTRATION_API,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Intercepteurs
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error.message);
        return Promise.reject(error);
      }
    );
  }

  async getDashboard(): Promise<DashboardData> {
    const response = await this.client.get('/api/dashboard');
    return response.data;
  }

  async getSystemStatus(group: string, system: string): Promise<OrganData> {
    const response = await this.client.get(`/api/system/${group}/${system}`);
    return response.data;
  }

  async getAllSystemsStatus(): Promise<{ by_group: Record<string, SystemStatus[]>, summary: any }> {
    const response = await this.client.get('/api/systems/status');
    return response.data;
  }

  async simulateCondition(group: string, system: string, condition: string): Promise<any> {
    const response = await this.client.post(`/api/simulate/${group}/${system}`, {
      condition,
    });
    return response.data;
  }

  async getAlerts(limit: number = 10): Promise<Alert[]> {
    const response = await this.client.get(`/api/alerts?limit=${limit}`);
    return response.data;
  }

  async getMetrics(): Promise<any> {
    const response = await this.client.get('/api/metrics');
    return response.data;
  }
}

export const apiClient = new ApiClient();