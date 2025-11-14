import React, { useMemo, useState } from "react";
import WorkerItem from "../components/WorkerItem";
import "./workers.css";

function Workers() {
  const [activeTab, setActiveTab] = useState("workers");

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
    // Placeholder: replace with real navigation or modal
    // eslint-disable-next-line no-alert
    alert(`Editar trabajador #${row.id}`);
  };

  const handleDelete = (row) => {
    // Placeholder: replace con confirm real + llamada API
    // eslint-disable-next-line no-alert
    const ok = confirm(`¿Borrar trabajador #${row.id}?`);
    if (ok) alert("Trabajador eliminado (demo)");
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
          <button className="btn btn-primary">+ Agregar trabajador</button>
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
    </div>
  );
}

export default Workers;
