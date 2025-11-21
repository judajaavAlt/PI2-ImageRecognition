import React from "react";
import "./Notification.css";

function Notification({ icon, title, content, onClose, className = "" }) {
  return (
    <div className={`notification ${className}`}>
      <div className="notification-icon">{icon}</div>
      <div className="notification-content">
        <div className="notification-title">{title}</div>
        <div className="notification-text">{content}</div>
      </div>
      {onClose && (
        <button className="notification-close" onClick={onClose}>
          ✕
        </button>
      )}
    </div>
  );
}

export default Notification;
