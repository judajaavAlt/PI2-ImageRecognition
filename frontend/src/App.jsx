import React from 'react';
import './App.css'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';
import Login from './components/Login/Login';
import ProtectedRoute from './components/ProtectedRoute/ProtectedRoute';
// Importa tus otros componentes aquí

// Componente para rutas públicas
const PublicRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return !isAuthenticated ? children : <Navigate to="/monitoring" replace />;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Ruta raíz */}
        <Route path="/" element={<Navigate to="/admin" replace />} />
        
        {/* Login - solo público */}
        <Route 
          path="/admin" 
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          } 
        />
        
        {/* Rutas PROTEGIDAS */}
        <Route 
          path="/monitoring" 
          element={
            <ProtectedRoute>
              {/* Aquí va tu componente Monitoring */}
              <div>Página de Monitoring</div>
            </ProtectedRoute>
          } 
        />
        
        <Route 
          path="/health" 
          element={
            <ProtectedRoute>
              {/* Aquí va tu componente Health */}
              <div>Página de Health</div>
            </ProtectedRoute>
          } 
        />
        
        <Route 
          path="/info" 
          element={
            <ProtectedRoute>
              {/* Aquí va tu componente Info */}
              <div>Página de Info</div>
            </ProtectedRoute>
          } 
        />
        
        <Route 
          path="/services/health" 
          element={
            <ProtectedRoute>
              {/* Aquí va tu componente ServicesHealth */}
              <div>Página de Services Health</div>
            </ProtectedRoute>
          } 
        />

        {/* Ruta 404 */}
        <Route path="*" element={<Navigate to="/admin" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
