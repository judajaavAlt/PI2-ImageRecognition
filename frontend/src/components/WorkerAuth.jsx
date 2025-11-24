import { useState, useRef } from "react";
import "./WorkerAuth.css";

const WorkerAuth = () => {
  const [image, setImage] = useState(null);
  const [stream, setStream] = useState(null);
  const [isCapturing, setIsCapturing] = useState(false);
  const [cedula, setCedula] = useState("");
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
            <button className="retry-btn" onClick={retakePhoto}>
              Retomar foto
            </button>
            <button className="submit-btn">Autenticar</button>
          </div>
        )}
      </div>

      <canvas ref={canvasRef} style={{ display: "none" }} />
    </div>
  );
};

export default WorkerAuth;
