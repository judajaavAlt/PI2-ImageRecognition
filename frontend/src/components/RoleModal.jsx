import React, { useState, useEffect } from "react";
import "./RoleModal.css";

function RoleModal({
  isOpen,
  onClose,
  mode = "create", // "create", "edit", "view"
  roleData = null,
  onSubmit,
}) {
  const [formData, setFormData] = useState({
    name: "",
    color: "#3b82f6",
  });

  // ESTE ES EL CAMBIO IMPORTANTE:
  // Actualizar el formulario cuando cambia roleData o el modo
  useEffect(() => {
    if (isOpen) {
      if (mode === "edit" && roleData) {
        setFormData({
          name: roleData.name || "",
          color: roleData.color || "#3b82f6",
        });
      } else if (mode === "create") {
        setFormData({
          name: "",
          color: "#3b82f6",
        });
      }
    }
  }, [isOpen, mode, roleData]);

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

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevenir recarga del navegador
    if (onSubmit) {
      onSubmit(formData);
    }
    // No cierres el modal aquí inmediatamente si quieres manejar errores de API
    // Pero por ahora lo dejaremos así para mantener tu flujo:
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
          {/* Agregamos onSubmit al form para permitir Enter key */}
          <form id="roleForm" onSubmit={handleSubmit}>
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
                required // Validación básica HTML
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
                  pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$" // Regex para Hex color
                />
                <div
                  className="color-preview"
                  style={{ backgroundColor: formData.color }}
                ></div>
              </div>
            </div>
          </form>
        </div>

        <div className="modal-footer">
          {!isViewMode && (
            // El botón activa el submit del formulario por ID o estando dentro
            <button className="btn btn-primary-modal" type="submit" form="roleForm">
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