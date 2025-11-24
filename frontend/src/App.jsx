import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import "./App.css";
import AuthPage from "./pages/AuthPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/auth" element={<AuthPage />} />
      </Routes>
    </Router>
  );
}

function Home() {
  return (
    <div style={{ textAlign: "center", padding: "50px" }}>
      <h1>Bienvenido al Sistema de Reconocimiento de Imágenes</h1>
      <div style={{ marginTop: "30px" }}>
        <Link
          to="/auth"
          style={{
            padding: "15px 30px",
            background: "#2196f3",
            color: "white",
            textDecoration: "none",
            borderRadius: "8px",
            fontSize: "16px",
            fontWeight: "500",
          }}
        >
          Ir a Autenticación
        </Link>
      </div>
    </div>
  );
}

export default App;
