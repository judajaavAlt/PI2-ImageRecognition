import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";
import App from "./App.jsx";
import Workers from "./pages/Workers.jsx";
import Login from "./components/Login/Login.jsx";
import ProtectedRoute from "./components/ProtectedRoute/ProtectedRoute.jsx";
import PublicRoute from "./components/PublicRoute/PublicRoute.jsx";
import AuthPage from "./pages/AuthPage.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        {/* Ruta "/" - Comprobador (pública) */}
        <Route path="/" element={<App />} />
        
        {/* Ruta "/admin" - Login (solo pública) */}
        <Route 
          path="/admin" 
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          } 
        />
        {/* Autenticación del trabajador - PÚBLICA */}
        <Route path="/auth" element={<AuthPage />} />
        
        {/* Ruta "/monitoring" - Protegida */}
        <Route 
          path="/monitoring" 
          element={
            <ProtectedRoute>
              <Workers />
            </ProtectedRoute>
          } 
        />
        
      </Routes>
    </BrowserRouter>
  </StrictMode>
);