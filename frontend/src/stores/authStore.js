import { create } from 'zustand';
import { authService } from '../services/authService';

export const useAuthStore = create((set, get) => ({
  user: null,
  token: sessionStorage.getItem('auth_token'),
  isAuthenticated: !!sessionStorage.getItem('auth_token'),
  isLoading: false,
  error: null,
  
  login: async (credentials) => {
    set({ isLoading: true, error: null });
    
    try {
      const response = await authService.login(credentials);
      
      // Guardar token en sessionStorage
      sessionStorage.setItem('auth_token', response.access_token);
      sessionStorage.setItem('user_data', JSON.stringify(response.user));
      
      set({
        user: response.user,
        token: response.access_token,
        isAuthenticated: true,
        isLoading: false,
        error: null
      });
      
      return { success: true };
    } catch (error) {
      set({
        isLoading: false,
        error: error.message,
        isAuthenticated: false,
        token: null,
        user: null
      });
      
      return { success: false, error: error.message };
    }
  },
  
  logout: () => {
    authService.logout();
    set({
      user: null,
      token: null,
      isAuthenticated: false,
      error: null
    });
  },
  
  clearError: () => set({ error: null })
}));