import { useState, useRef } from "react";
import "./WorkerAuth.css";
import { workersApi } from "../services/api";
import Notification from "./Notification";

const WorkerAuth = () => {
  const [image, setImage] = useState(null);
  const [stream, setStream] = useState(null);
  const [isCapturing, setIsCapturing] = useState(false);
  const [cedula, setCedula] = useState("");
  const [notification, setNotification] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const handleCedulaChange = (e) => {
    const value = e.target.value;
    // Solo permitir números
    if (/^\d*$/.test(value)) {
      setCedula(value);
    }
  };

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user" },
      });
      setStream(mediaStream);
      setIsCapturing(true);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (error) {
      console.error("Error al acceder a la cámara:", error);
      alert(
        "No se pudo acceder a la cámara. Por favor, verifica los permisos."
      );
    }
  };

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0);

      const imageData = canvas.toDataURL("image/jpeg");
      setImage(imageData);

      // Detener la cámara
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
        setStream(null);
      }
      setIsCapturing(false);
    }
  };

  const retakePhoto = () => {
    setImage(null);
    startCamera();
  };

  const handleTakePhoto = () => {
    if (isCapturing) {
      capturePhoto();
    } else {
      startCamera();
    }
  };

  const handleAuthenticate = async () => {
    // Validaciones
    if (!cedula || cedula.trim() === "") {
      setNotification({
        type: "error",
        title: "Error",
        message: "Por favor ingrese su número de cédula",
      });
      return;
    }

    if (!image) {
      setNotification({
        type: "error",
        title: "Error",
        message: "Por favor capture su foto",
      });
      return;
    }

    setIsLoading(true);
    setNotification(null);

    try {
      // Extraer solo la parte base64 (sin el prefijo data:image/jpeg;base64,)
      const base64Image = image.split(",")[1] || image;

      const result = await workersApi.verify(cedula, base64Image);

      if (result.match) {
        setNotification({
          type: "success",
          title: "Autenticación exitosa",
          message: result.message || "Usuario autenticado correctamente",
        });

        // Limpiar formulario después de 2 segundos
        setTimeout(() => {
          setImage(null);
          setCedula("");
          setNotification(null);
        }, 3000);
      } else {
        setNotification({
          type: "error",
          title: "Autenticación fallida",
          message: result.message || "No se pudo autenticar al usuario",
        });
      }
    } catch (error) {
      console.error("Error al autenticar:", error);
      setNotification({
        type: "error",
        title: "Error",
        message: error.message || "Error al comunicarse con el servidor",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="worker-auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1 className="auth-title">Autenticación del</h1>
          <h2 className="auth-subtitle">Trabajador</h2>
        </div>

        <div className="photo-container">
          {!isCapturing && !image && (
            <div className="placeholder-photo">
              <div className="user-silhouette">
                <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="100" cy="70" r="35" fill="#d0d0d0" />
                  <path
                    d="M 50 150 Q 50 110, 100 110 Q 150 110, 150 150 L 150 200 L 50 200 Z"
                    fill="#d0d0d0"
                  />
                </svg>
              </div>
            </div>
          )}

          {isCapturing && (
            <div className="camera-view">
              <video
                ref={videoRef}
                autoPlay
                playsInline
                className="video-feed"
              />
              <div className="camera-overlay">
                <svg
                  className="silhouette-guide"
                  viewBox="0 0 200 300"
                  xmlns="http://www.w3.org/2000/svg"
                  preserveAspectRatio="xMidYMid slice"
                >
                  {/* Cabeza */}
                  <ellipse
                    cx="100"
                    cy="95"
                    rx="45"
                    ry="55"
                    fill="none"
                    stroke="rgba(255, 255, 255, 0.7)"
                    strokeWidth="3"
                    strokeDasharray="8,6"
                  />

                  {/* Cuello */}
                  <path
                    d="M 75 140 L 75 175 L 125 175 L 125 140"
                    fill="none"
                    stroke="rgba(255, 255, 255, 0.7)"
                    strokeWidth="3"
                    strokeDasharray="8,6"
                  />

                  {/* Hombros */}
                  <path
                    d="M 30 300 Q 40 195, 75 175 L 125 175 Q 160 195, 170 300"
                    fill="none"
                    stroke="rgba(255, 255, 255, 0.7)"
                    strokeWidth="3"
                    strokeDasharray="8,6"
                  />
                </svg>
                <p className="guide-text">
                  Posicione su rostro dentro de la guía
                </p>
              </div>
            </div>
          )}

          {image && !isCapturing && (
            <div className="captured-photo">
              <img src={image} alt="Foto capturada" />
            </div>
          )}

          <div className="photo-label">Cedula / Documento</div>
        </div>

        <input
          type="text"
          className="cedula-input"
          placeholder="Ingrese su número de cédula"
          value={cedula}
          onChange={handleCedulaChange}
          maxLength="15"
        />

        {!image && (
          <button className="take-photo-btn" onClick={handleTakePhoto}>
            {isCapturing ? "Capturar" : "Tomar foto"}
          </button>
        )}

        {image && (
          <div className="action-buttons">
            <button
              className="retry-btn"
              onClick={retakePhoto}
              disabled={isLoading}
            >
              Retomar foto
            </button>
            <button
              className="submit-btn"
              onClick={handleAuthenticate}
              disabled={isLoading}
            >
              {isLoading ? "Verificando..." : "Autenticar"}
            </button>
          </div>
        )}
      </div>

      {notification && (
        <Notification
          icon={notification.type === "success" ? "✓" : "✕"}
          title={notification.title}
          content={notification.message}
          onClose={() => setNotification(null)}
          className={notification.type}
        />
      )}

      <canvas ref={canvasRef} style={{ display: "none" }} />
    </div>
  );
};

export default WorkerAuth;
