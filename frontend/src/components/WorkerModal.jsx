import React, { useState, useEffect } from "react";
import "./WorkerModal.css";

function WorkerModal({
  isOpen,
  onClose,
  mode = "create", // "create", "edit", "view"
  workerData = null,
  onSubmit,
}) {
  const [formData, setFormData] = useState({
    name: "",
    documentId: "",
    role: "",
    photo: null,
  });

  // Actualizar formData cuando cambia workerData o mode
  useEffect(() => {
    if (mode === "create" || !workerData) {
      // Limpiar el formulario para modo create
      setFormData({
        name: "",
        documentId: "",
        role: "",
        photo: null,
      });
    } else {
      // Cargar datos del trabajador para edit/view
      setFormData({
        name: workerData.name || "",
        documentId: workerData.document || "",
        role: workerData.role || "",
        photo: workerData.photo || null,
      });
    }
  }, [workerData, mode, isOpen]);

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

  const handlePhotoUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setFormData((prev) => ({
          ...prev,
          photo: reader.result,
        }));
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = () => {
    if (onSubmit) {
      onSubmit(formData);
    }
    onClose();
  };

  const getTitle = () => {
    if (isCreateMode) return "Agregar al trabajador";
    if (isEditMode) return "Editar trabajador";
    return "Ver trabajador";
  };

  // Validar que todos los campos requeridos estén completos
  const isFormValid = () => {
    return (
      formData.name.trim() !== "" &&
      formData.documentId.trim() !== "" &&
      formData.role !== "" &&
      formData.photo !== null
    );
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2 className="modal-title">{getTitle()}</h2>
          <button className="modal-close-btn" onClick={onClose}>
            ✕ Cerrar
          </button>
        </div>

        <div className="modal-body">
          <div className="modal-left">
            <div className="form-fields-container">
              <div className="input-card">
                <div className="form-group">
                  <label htmlFor="name">Nombre completo</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    disabled={isViewMode}
                    placeholder="Nombre completo"
                  />
                </div>
              </div>

              <div className="input-card">
                <div className="form-group">
                  <label htmlFor="documentId">Cédula / Documento</label>
                  <input
                    type="text"
                    id="documentId"
                    name="documentId"
                    value={formData.documentId}
                    onChange={(e) => {
                      const value = e.target.value;
                      // Solo permitir números
                      if (value === "" || /^[0-9]+$/.test(value)) {
                        handleChange(e);
                      }
                    }}
                    disabled={isViewMode}
                    placeholder="Cédula / Documento"
                  />
                </div>
              </div>

              <div className="form-group-role">
                <label htmlFor="role" className="role-label">
                  Rol asignado
                </label>
                <select
                  id="role"
                  name="role"
                  value={formData.role}
                  onChange={handleChange}
                  disabled={isViewMode}
                  className="role-select"
                >
                  <option value="">Seleccionar rol</option>
                  <option value="1">Manufacturero</option>
                  <option value="2">Obrero</option>
                  <option value="3">Operario de producción</option>
                  <option value="4">Inspector de calidad</option>
                  <option value="5">Mantenimiento</option>
                </select>
              </div>
            </div>

            {!isViewMode && (
              <div className="modal-left-buttons">
                <button
                  className="btn btn-primary-modal"
                  onClick={handleSubmit}
                  disabled={!isFormValid()}
                  style={{
                    opacity: isFormValid() ? 1 : 0.5,
                    cursor: isFormValid() ? "pointer" : "not-allowed",
                  }}
                >
                  + {isCreateMode ? "Agregar" : "Guardar cambios"}
                </button>
                <button className="btn btn-cancel" onClick={onClose}>
                  ✕ Cancelar
                </button>
              </div>
            )}
          </div>

          <div className="modal-right">
            <div className="photo-upload-area">
              {formData.photo ? (
                <img
                  src={formData.photo}
                  alt="Vista previa"
                  className="photo-preview"
                />
              ) : (
                <div className="photo-placeholder">Foto</div>
              )}
            </div>
            {!isViewMode && (
              <button
                className="btn-upload"
                onClick={() => document.getElementById("photo-input").click()}
              >
                🖼️ Subir imagen
              </button>
            )}
            <input
              type="file"
              id="photo-input"
              accept="image/*"
              onChange={handlePhotoUpload}
              style={{ display: "none" }}
            />
          </div>
        </div>

        {isViewMode && (
          <div className="modal-footer">
            <button className="btn btn-cancel" onClick={onClose}>
              ✕ Cancelar
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default WorkerModal;
