import axios from 'axios';
import { API_BASE_URL } from '../utils/constants';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { 
    'Content-Type': 'application/json'
  },
  timeout: 10000
});

// Interceptor para manejar errores globalmente
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // El servidor respondió con un código de error
      throw new Error(error.response.data.detail || 'Error del servidor');
    } else if (error.request) {
      // La petición fue hecha pero no se recibió respuesta
      throw new Error('No se pudo conectar con el servidor');
    } else {
      // Algo pasó en la configuración de la petición
      throw new Error('Error de configuración de la petición');
    }
  }
);