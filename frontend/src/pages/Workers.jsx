import React, { useMemo, useState, useEffect } from "react";
import WorkerItem from "../components/WorkerItem";
import WorkerModal from "../components/WorkerModal";
import RoleItem from "../components/RoleItem";
import RoleModal from "../components/RoleModal";
import ConfirmDeleteModal from "../components/ConfirmDeleteModal";
import Notification from "../components/Notification";
import "./workers.css";

function Workers() {
  const [activeTab, setActiveTab] = useState("workers");
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedWorker, setSelectedWorker] = useState(null);
  const [showCreateRoleModal, setShowCreateRoleModal] = useState(false);
  const [showEditRoleModal, setShowEditRoleModal] = useState(false);
  const [selectedRole, setSelectedRole] = useState(null);
  const [showDeleteWorkerModal, setShowDeleteWorkerModal] = useState(false);
  const [workerToDelete, setWorkerToDelete] = useState(null);
  const [showDeleteRoleModal, setShowDeleteRoleModal] = useState(false);
  const [roleToDelete, setRoleToDelete] = useState(null);
  const [notification, setNotification] = useState(null);
  const [isClosingNotification, setIsClosingNotification] = useState(false);

  useEffect(() => {
    if (notification) {
      const timer = setTimeout(() => {
        handleCloseNotification();
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [notification]);

  const handleCloseNotification = () => {
    setIsClosingNotification(true);
    setTimeout(() => {
      setNotification(null);
      setIsClosingNotification(false);
    }, 300);
  };

  const showNotification = (icon, title, content, type = "info") => {
    setNotification({ icon, title, content, type });
  };

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

  const rolesData = useMemo(
    () => [
      { id: 1, name: "Manufacturero", color: "#fcba03" },
      { id: 2, name: "Obrero", color: "#3d7462" },
      { id: 3, name: "Operario de producción", color: "#e85a4f" },
      { id: 4, name: "Inspector de calidad", color: "#2b8bc3" },
      { id: 5, name: "Mantenimiento", color: "#d2f1d0" },
    ],
    []
  );

  const handleEdit = (row) => {
    setSelectedWorker(row);
    setShowEditModal(true);
  };

  const handleDelete = (row) => {
    setWorkerToDelete(row);
    setShowDeleteWorkerModal(true);
  };

  const confirmDeleteWorker = () => {
    console.log("Trabajador eliminado:", workerToDelete);
    showNotification(
      "🗑️",
      "Trabajador eliminado",
      `El trabajador ${workerToDelete.name} ha sido eliminado del registro exitosamente`,
      "error"
    );
    // Aquí iría la llamada a la API para eliminar el trabajador
  };

  const handleCreateWorker = (formData) => {
    console.log("Datos del nuevo trabajador:", formData);
    showNotification(
      "✅",
      "Trabajador creado",
      `El trabajador ${formData.name} ha sido agregado exitosamente`,
      "success"
    );
    // Aquí iría la llamada a la API para crear el trabajador
  };

  const handleUpdateWorker = (formData) => {
    console.log("Datos actualizados del trabajador:", formData);
    showNotification(
      "✏️",
      "Trabajador actualizado",
      `Los datos de ${formData.name} han sido actualizados exitosamente`,
      "success"
    );
    // Aquí iría la llamada a la API para actualizar el trabajador
  };

  const handleEditRole = (role) => {
    setSelectedRole(role);
    setShowEditRoleModal(true);
  };

  const handleDeleteRole = (role) => {
    setRoleToDelete(role);
    setShowDeleteRoleModal(true);
  };

  const confirmDeleteRole = () => {
    // eslint-disable-next-line no-alert
    alert(`Rol eliminado: ${roleToDelete.name}`);
    console.log("Rol eliminado:", roleToDelete);
    // Aquí iría la llamada a la API para eliminar el rol
  };

  const handleCreateRole = (formData) => {
    // eslint-disable-next-line no-alert
    alert(`Rol creado: ${formData.name}`);
    console.log("Datos del nuevo rol:", formData);
    // Aquí iría la llamada a la API para crear el rol
  };

  const handleUpdateRole = (formData) => {
    // eslint-disable-next-line no-alert
    alert(`Rol actualizado: ${formData.name}`);
    console.log("Datos actualizados del rol:", formData);
    // Aquí iría la llamada a la API para actualizar el rol
  };

  return (
    <div className="workers-page">
      {notification && (
        <div
          className={`notification-overlay ${
            isClosingNotification ? "closing" : ""
          }`}
        >
          <Notification
            className={notification.type}
            icon={notification.icon}
            title={notification.title}
            content={notification.content}
            onClose={handleCloseNotification}
          />
        </div>
      )}

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
          {activeTab === "roles" && (
            <button
              className="btn btn-primary"
              onClick={() => setShowCreateRoleModal(true)}
            >
              + Agregar Rol
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
            <table className="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nombre del Rol</th>
                  <th>Color representativo</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {rolesData.map((role) => (
                  <RoleItem
                    key={role.id}
                    id={role.id}
                    name={role.name}
                    color={role.color}
                    onEdit={() => handleEditRole(role)}
                    onDelete={() => handleDeleteRole(role)}
                  />
                ))}
              </tbody>
            </table>
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

      <RoleModal
        isOpen={showCreateRoleModal}
        onClose={() => setShowCreateRoleModal(false)}
        mode="create"
        onSubmit={handleCreateRole}
      />

      <RoleModal
        isOpen={showEditRoleModal}
        onClose={() => {
          setShowEditRoleModal(false);
          setSelectedRole(null);
        }}
        mode="edit"
        roleData={selectedRole}
        onSubmit={handleUpdateRole}
      />

      <ConfirmDeleteModal
        isOpen={showDeleteWorkerModal}
        onClose={() => {
          setShowDeleteWorkerModal(false);
          setWorkerToDelete(null);
        }}
        onConfirm={confirmDeleteWorker}
        itemName={workerToDelete?.name || ""}
        itemType="trabajador"
      />

      <ConfirmDeleteModal
        isOpen={showDeleteRoleModal}
        onClose={() => {
          setShowDeleteRoleModal(false);
          setRoleToDelete(null);
        }}
        onConfirm={confirmDeleteRole}
        itemName={roleToDelete?.name || ""}
        itemType="rol"
      />
    </div>
  );
}

export default Workers;
