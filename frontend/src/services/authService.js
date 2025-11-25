import { apiClient } from './apiClient';
import { API_ENDPOINTS } from '../types/auth.types';

export const authService = {
  async login(credentials) {
    try {
      const response = await apiClient.post(API_ENDPOINTS.LOGIN, credentials);
      
      // El endpoint retorna un booleano, no un token
      if (response.data === true) {
        // Como el backend solo valida pero no retorna token,
        // creamos uno simbólico para el frontend
        const mockToken = btoa(JSON.stringify({
          username: credentials.username,
          timestamp: Date.now()
        }));
        
        const userData = {
          username: credentials.username,
          role: 'admin'
        };
        
        return {
          access_token: mockToken,
          user: userData
        };
      } else {
        throw new Error('Credenciales inválidas');
      }
    } catch (error) {
      // Manejar errores específicos del nuevo endpoint
      if (error.response && error.response.status === 401) {
        throw new Error('Credenciales inválidas');
      }
      throw new Error(error.message || 'Error durante la validación de credenciales');
    }
  },

  logout() {
    sessionStorage.removeItem('auth_token');
    sessionStorage.removeItem('user_data');
  },

  getToken() {
    return sessionStorage.getItem('auth_token');
  },

  isAuthenticated() {
    return !!sessionStorage.getItem('auth_token');
  }
};