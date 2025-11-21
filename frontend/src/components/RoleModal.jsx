import React, { useState } from "react";
import "./RoleModal.css";

function RoleModal({
  isOpen,
  onClose,
  mode = "create", // "create", "edit", "view"
  roleData = null,
  onSubmit,
}) {
  const [formData, setFormData] = useState({
    name: roleData?.name || "",
    color: roleData?.color || "#3b82f6",
  });

  const isViewMode = mode === "view";
  const isEditMode = mode === "edit";
  const isCreateMode = mode === "create";

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = () => {
    if (onSubmit) {
      onSubmit(formData);
    }
    onClose();
  };

  const getTitle = () => {
    if (isCreateMode) return "Agregar rol";
    if (isEditMode) return "Editar rol";
    return "Ver rol";
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        className="modal-content role-modal-content"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-header">
          <h2 className="modal-title">{getTitle()}</h2>
          <button className="modal-close-btn" onClick={onClose}>
            ✕ Cerrar
          </button>
        </div>

        <div className="modal-body role-modal-body">
          <div className="form-group">
            <label htmlFor="name">Nombre del Rol</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              disabled={isViewMode}
              placeholder="Nombre del rol"
            />
          </div>

          <div className="form-group">
            <label htmlFor="color">Color representativo</label>
            <div className="color-picker-container">
              <input
                type="color"
                id="color"
                name="color"
                value={formData.color}
                onChange={handleChange}
                disabled={isViewMode}
                className="color-input"
              />
              <input
                type="text"
                value={formData.color}
                onChange={handleChange}
                name="color"
                disabled={isViewMode}
                placeholder="#000000"
                className="color-text-input"
              />
              <div
                className="color-preview"
                style={{ backgroundColor: formData.color }}
              ></div>
            </div>
          </div>
        </div>

        <div className="modal-footer">
          {!isViewMode && (
            <button className="btn btn-primary-modal" onClick={handleSubmit}>
              + {isCreateMode ? "Agregar" : "Guardar cambios"}
            </button>
          )}
          <button className="btn btn-cancel" onClick={onClose}>
            ✕ Cancelar
          </button>
        </div>
      </div>
    </div>
  );
}

export default RoleModal;
