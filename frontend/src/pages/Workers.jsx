import React, { useMemo, useState, useEffect } from "react";
import WorkerItem from "../components/WorkerItem";
import WorkerModal from "../components/WorkerModal";
import RoleItem from "../components/RoleItem";
import RoleModal from "../components/RoleModal";
import ConfirmDeleteModal from "../components/ConfirmDeleteModal";
import Notification from "../components/Notification";
import { workersApi } from "../services/api";
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
  const [workers, setWorkers] = useState([]);
  const [loading, setLoading] = useState(true);

  // Cargar trabajadores al montar el componente
  useEffect(() => {
    loadWorkers();
  }, []);

  useEffect(() => {
    if (notification) {
      const timer = setTimeout(() => {
        handleCloseNotification();
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [notification]);

  const loadWorkers = async () => {
    try {
      setLoading(true);
      const data = await workersApi.getAll();
      setWorkers(data);
    } catch (error) {
      showNotification(
        "❌",
        "Error",
        "No se pudieron cargar los trabajadores",
        "error"
      );
      console.error("Error loading workers:", error);
    } finally {
      setLoading(false);
    }
  };

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

  const confirmDeleteWorker = async () => {
    try {
      await workersApi.delete(workerToDelete.id);
      showNotification(
        "🗑️",
        "Trabajador eliminado",
        `El trabajador ${workerToDelete.name} ha sido eliminado del registro exitosamente`,
        "error"
      );
      setShowDeleteWorkerModal(false);
      setWorkerToDelete(null);
      await loadWorkers();
    } catch (error) {
      showNotification(
        "❌",
        "Error",
        "No se pudo eliminar el trabajador",
        "error"
      );
      console.error("Error deleting worker:", error);
    }
  };

  const handleCreateWorker = async (formData) => {
    try {
      console.log("Sending worker data:", formData);
      await workersApi.create(formData);
      showNotification(
        "✅",
        "Trabajador creado",
        `El trabajador ${formData.name} ha sido agregado exitosamente`,
        "success"
      );
      setShowCreateModal(false);
      await loadWorkers();
    } catch (error) {
      showNotification(
        "❌",
        "Error",
        error.message || "No se pudo crear el trabajador",
        "error"
      );
      console.error("Error creating worker:", error);
    }
  };

  const handleUpdateWorker = async (formData) => {
    try {
      await workersApi.update(selectedWorker.id, formData);
      showNotification(
        "✏️",
        "Trabajador actualizado",
        `Los datos de ${formData.name} han sido actualizados exitosamente`,
        "success"
      );
      setShowEditModal(false);
      setSelectedWorker(null);
      await loadWorkers();
    } catch (error) {
      showNotification(
        "❌",
        "Error",
        "No se pudo actualizar el trabajador",
        "error"
      );
      console.error("Error updating worker:", error);
    }
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
            👥 Trabajadores
          </button>
          <button
            className={`tab ${activeTab === "roles" ? "active" : ""}`}
            onClick={() => setActiveTab("roles")}
          >
            👤 Roles
          </button>
        </div>

        <div className="table-wrap">
          <div className="tab-content-header">
            {activeTab === "workers" && (
              <button
                className="btn btn-primary"
                onClick={() => setShowCreateModal(true)}
              >
                👤+ Agregar trabajador
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
          {activeTab === "workers" ? (
            loading ? (
              <div
                style={{
                  padding: "40px",
                  textAlign: "center",
                  color: "#64748b",
                }}
              >
                Cargando trabajadores...
              </div>
            ) : (
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
                  {workers.length === 0 ? (
                    <tr>
                      <td
                        colSpan="5"
                        style={{
                          padding: "40px",
                          textAlign: "center",
                          color: "#64748b",
                        }}
                      >
                        No hay trabajadores registrados
                      </td>
                    </tr>
                  ) : (
                    workers.map((worker, idx) => (
                      <WorkerItem
                        key={worker.id}
                        index={idx + 1}
                        name={worker.name}
                        documentId={worker.document}
                        role={worker.role}
                        onEdit={() => handleEdit(worker)}
                        onDelete={() => handleDelete(worker)}
                      />
                    ))
                  )}
                </tbody>
              </table>
            )
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
