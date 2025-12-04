import api from './api';

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'CANDIDATE' | 'RECRUITER' | 'ADMIN';
}

export interface AuthResponse {
  success: boolean;
  data: User;
  access?: string;
  refresh?: string;
}

export const authService = {
  async register(data: any) {
    const response = await api.post('/auth/register/', data);
    return response.data;
  },

  async login(data: any) {
    const response = await api.post('/auth/login/', data);
    if (response.data.access) {
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
    }
    return response.data;
  },

  async getCurrentUser() {
    const response = await api.get('/users/me/');
    return response.data;
  },

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    // Optional: Call backend logout endpoint
  }
};
