import React, { useState } from "react";
import "./ConfirmDeleteModal.css";

function ConfirmDeleteModal({
  isOpen,
  onClose,
  onConfirm,
  itemName,
  itemType = "trabajador", // "trabajador" o "rol"
}) {
  const [confirmName, setConfirmName] = useState("");

  const handleConfirm = () => {
    if (confirmName.toLowerCase() === itemName.toLowerCase()) {
      onConfirm();
      handleClose();
    }
  };

  const handleClose = () => {
    setConfirmName("");
    onClose();
  };

  const isConfirmDisabled =
    confirmName.toLowerCase() !== itemName.toLowerCase();

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={handleClose}>
      <div
        className="confirm-modal-content"
        onClick={(e) => e.stopPropagation()}
      >
        <button className="confirm-modal-close-btn" onClick={handleClose}>
          ✕ Cerrar
        </button>

        <h2 className="confirm-modal-title">Eliminar {itemType}</h2>

        <div className="confirm-modal-body">
          <p className="confirm-modal-question">¿Estas seguro?</p>

          <div className="confirm-modal-warning">
            <p>
              Esta accion NO se puede deshacer, esto eliminar permanentemente al{" "}
              {itemType} <strong>{itemName}</strong> del registro.
            </p>
            <p>
              Para eliminarlo escribe su nombre (<strong>{itemName}</strong>) a
              continuación:
            </p>
            <input
              type="text"
              value={confirmName}
              onChange={(e) => setConfirmName(e.target.value)}
              placeholder={`Escribe "${itemName}"`}
              className="confirm-input"
            />
          </div>
        </div>

        <div className="confirm-modal-footer">
          <button className="btn-confirm-cancel" onClick={handleClose}>
            ✕ Cancelar
          </button>
          <button
            className="btn-confirm-delete"
            onClick={handleConfirm}
            disabled={isConfirmDisabled}
          >
            Entiendo, Eliminar al {itemType} del registro
          </button>
        </div>
      </div>
    </div>
  );
}

export default ConfirmDeleteModal;
