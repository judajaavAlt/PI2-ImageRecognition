import React, { useState } from "react";
import "./WorkerModal.css";

function WorkerModal({
  isOpen,
  onClose,
  mode = "create", // "create", "edit", "view"
  workerData = null,
  onSubmit,
}) {
  const [formData, setFormData] = useState({
    name: workerData?.name || "",
    documentId: workerData?.documentId || "",
    role: workerData?.role || "",
    photo: workerData?.photo || null,
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

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">{getTitle()}</h2>
          <button className="modal-close-btn" onClick={onClose}>
            ✕ Cerrar
          </button>
        </div>

        <div className="modal-body">
          <div className="modal-left">
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

            <div className="form-group">
              <label htmlFor="documentId">Cédula / Documento</label>
              <input
                type="text"
                id="documentId"
                name="documentId"
                value={formData.documentId}
                onChange={handleChange}
                disabled={isViewMode}
                placeholder="Cédula / Documento"
              />
            </div>

            <div className="form-group">
              <label htmlFor="role">Rol asignado</label>
              <select
                id="role"
                name="role"
                value={formData.role}
                onChange={handleChange}
                disabled={isViewMode}
              >
                <option value="">Seleccionar rol</option>
                <option value="Manufacturero">Manufacturero</option>
                <option value="Supervisor">Supervisor</option>
                <option value="Operario">Operario</option>
                <option value="Técnico">Técnico</option>
              </select>
            </div>
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

export default WorkerModal;
