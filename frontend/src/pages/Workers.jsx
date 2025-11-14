import React, { useMemo, useState } from "react";
import WorkerItem from "../components/WorkerItem";
import WorkerModal from "../components/WorkerModal";
import "./workers.css";

function Workers() {
  const [activeTab, setActiveTab] = useState("workers");
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedWorker, setSelectedWorker] = useState(null);

  const data = useMemo(
    () =>
      Array.from({ length: 9 }).map((_, i) => ({
        id: i + 1,
        name: "pepito perez de la cruz",
        documentId: "1.234.523.432",
        role: "Manufacturero",
      })),
    []
  );

  const handleEdit = (row) => {
    setSelectedWorker(row);
    setShowEditModal(true);
  };

  const handleDelete = (row) => {
    // Placeholder: replace con confirm real + llamada API
    // eslint-disable-next-line no-alert
    const ok = confirm(`¿Borrar trabajador #${row.id}?`);
    if (ok) alert("Trabajador eliminado (demo)");
  };

  const handleCreateWorker = (formData) => {
    // eslint-disable-next-line no-alert
    alert(`Trabajador creado: ${formData.name}`);
    console.log("Datos del nuevo trabajador:", formData);
    // Aquí iría la llamada a la API para crear el trabajador
  };

  const handleUpdateWorker = (formData) => {
    // eslint-disable-next-line no-alert
    alert(`Trabajador actualizado: ${formData.name}`);
    console.log("Datos actualizados del trabajador:", formData);
    // Aquí iría la llamada a la API para actualizar el trabajador
  };

  return (
    <div className="workers-page">
      <div className="panel">
        <div className="panel-title">Panel de Gestión de Trabajadores</div>

        <div className="tabs-bar">
          <button
            className={`tab ${activeTab === "workers" ? "active" : ""}`}
            onClick={() => setActiveTab("workers")}
          >
            Trabajadores
          </button>
          <button
            className={`tab ${activeTab === "roles" ? "active" : ""}`}
            onClick={() => setActiveTab("roles")}
          >
            Roles
          </button>
          <div className="spacer" />
          {activeTab === "workers" && (
            <button
              className="btn btn-primary"
              onClick={() => setShowCreateModal(true)}
            >
              + Agregar trabajador
            </button>
          )}
        </div>

        <div className="table-wrap">
          {activeTab === "workers" ? (
            <table className="table">
              <thead>
                <tr>
                  <th>N. de registro</th>
                  <th>Nombre completo</th>
                  <th>Cédula / Documento</th>
                  <th>Rol asignado</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {data.map((row, idx) => (
                  <WorkerItem
                    key={row.id}
                    index={idx + 1}
                    name={row.name}
                    documentId={row.documentId}
                    role={row.role}
                    onEdit={() => handleEdit(row)}
                    onDelete={() => handleDelete(row)}
                  />
                ))}
              </tbody>
            </table>
          ) : (
            <div className="construction-message">
              <h2>🚧 En construcción</h2>
            </div>
          )}
        </div>
      </div>

      <WorkerModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        mode="create"
        onSubmit={handleCreateWorker}
      />

      <WorkerModal
        isOpen={showEditModal}
        onClose={() => {
          setShowEditModal(false);
          setSelectedWorker(null);
        }}
        mode="edit"
        workerData={selectedWorker}
        onSubmit={handleUpdateWorker}
      />
    </div>
  );
}

export default Workers;
