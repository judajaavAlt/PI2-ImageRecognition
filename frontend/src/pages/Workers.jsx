import React, { useState, useEffect } from "react";
import WorkerItem from "../components/WorkerItem";
import WorkerModal from "../components/WorkerModal";
import RoleItem from "../components/RoleItem";
import RoleModal from "../components/RoleModal";
import ConfirmDeleteModal from "../components/ConfirmDeleteModal";
import Notification from "../components/Notification";
// IMPORTANTE: Importamos ambas APIs
import { workersApi, rolesApi } from "../services/api";
import "./workers.css";

function Workers() {
  const [activeTab, setActiveTab] = useState("workers");
  
  // Modales de Trabajadores
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showViewModal, setShowViewModal] = useState(false);
  const [selectedWorker, setSelectedWorker] = useState(null);
  
  // Modales de Roles
  const [showCreateRoleModal, setShowCreateRoleModal] = useState(false);
  const [showEditRoleModal, setShowEditRoleModal] = useState(false);
  const [selectedRole, setSelectedRole] = useState(null);
  
  // Modales de Eliminación
  const [showDeleteWorkerModal, setShowDeleteWorkerModal] = useState(false);
  const [workerToDelete, setWorkerToDelete] = useState(null);
  const [showDeleteRoleModal, setShowDeleteRoleModal] = useState(false);
  const [roleToDelete, setRoleToDelete] = useState(null);

  // Estado general
  const [notification, setNotification] = useState(null);
  const [isClosingNotification, setIsClosingNotification] = useState(false);
  
  // Datos
  const [workers, setWorkers] = useState([]);
  const [roles, setRoles] = useState([]); // Estado para los roles dinámicos
  const [loading, setLoading] = useState(true);

  // Cargar datos al montar el componente
  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    if (notification) {
      const timer = setTimeout(() => {
        handleCloseNotification();
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [notification]);

  // Función para cargar AMBOS: trabajadores y roles
  const loadData = async () => {
    try {
      setLoading(true);
      // Ejecutamos ambas peticiones en paralelo para mayor velocidad
      const [workersData, rolesData] = await Promise.all([
        workersApi.getAll(),
        rolesApi.getAll(),
      ]);
      
      setWorkers(workersData);
      setRoles(rolesData);
    } catch (error) {
      showNotification(
        "❌",
        "Error",
        "No se pudieron cargar los datos del sistema",
        "error"
      );
      console.error("Error loading data:", error);
    } finally {
      setLoading(false);
    }
  };

  // Función auxiliar para recargar solo trabajadores
  const loadWorkers = async () => {
    try {
      const data = await workersApi.getAll();
      setWorkers(data);
    } catch (error) {
      console.error("Error reloading workers:", error);
    }
  };

  // Función auxiliar para recargar solo roles
  const loadRoles = async () => {
    try {
      const data = await rolesApi.getAll();
      setRoles(data);
    } catch (error) {
      console.error("Error reloading roles:", error);
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

  // Función helper para obtener el nombre del rol usando la lista de roles cargada de la API
  const getRoleName = (roleId) => {
    // Convertimos a int porque a veces viene como string desde el form
    const role = roles.find((r) => r.id === parseInt(roleId));
    return role ? role.name : "Sin rol asignado";
  };

  // --- HANDLERS TRABAJADORES ---

  const handleView = (row) => {
    setSelectedWorker(row);
    setShowViewModal(true);
  };

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
        `El trabajador ${workerToDelete.name} ha sido eliminado exitosamente`,
        "success" 
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

  // --- HANDLERS ROLES ---

  const handleEditRole = (role) => {
    setSelectedRole(role);
    setShowEditRoleModal(true);
  };

  const handleDeleteRole = (role) => {
    setRoleToDelete(role);
    setShowDeleteRoleModal(true);
  };

  const confirmDeleteRole = async () => {
    try {
      await rolesApi.delete(roleToDelete.id);
      
      showNotification(
        "🗑️",
        "Rol eliminado",
        `El rol ${roleToDelete.name} ha sido eliminado correctamente`,
        "success" 
      );
      setShowDeleteRoleModal(false);
      setRoleToDelete(null);
      // Recargamos roles y trabajadores (por si un trabajador tenía ese rol)
      await loadData();
    } catch (error) {
      showNotification(
        "❌",
        "Error",
        "No se pudo eliminar el rol (verifique que no esté en uso)",
        "error"
      );
      console.error("Error deleting role:", error);
    }
  };

  const handleCreateRole = async (formData) => {
    try {
      // formData debe tener { name, color }
      await rolesApi.create(formData);
      
      showNotification(
        "✅",
        "Rol creado",
        `El rol ${formData.name} ha sido creado exitosamente`,
        "success"
      );
      setShowCreateRoleModal(false);
      await loadRoles();
    } catch (error) {
      showNotification(
        "❌",
        "Error",
        error.message || "No se pudo crear el rol",
        "error"
      );
      console.error("Error creating role:", error);
    }
  };

  const handleUpdateRole = async (formData) => {
    try {
      await rolesApi.update(selectedRole.id, formData);
      
      showNotification(
        "✏️",
        "Rol actualizado",
        `El rol ${formData.name} ha sido actualizado exitosamente`,
        "success"
      );
      setShowEditRoleModal(false);
      setSelectedRole(null);
      // Recargar todo para actualizar colores/nombres en la tabla de trabajadores también
      await loadData();
    } catch (error) {
      showNotification(
        "❌",
        "Error",
        "No se pudo actualizar el rol",
        "error"
      );
      console.error("Error updating role:", error);
    }
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
          
          {/* Renderizado Condicional */}
          {activeTab === "workers" ? (
            loading ? (
              <div style={{ padding: "40px", textAlign: "center", color: "#64748b" }}>
                Cargando datos...
              </div>
            ) : (
              // AGREGAMOS CLASE "workers-table" AQUÍ 👇
              <table className="table workers-table">
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
                      <td colSpan="5" style={{ padding: "40px", textAlign: "center", color: "#64748b" }}>
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
                        role={getRoleName(worker.role)} // Usamos la función dinámica
                        onView={() => handleView(worker)}
                        onEdit={() => handleEdit(worker)}
                        onDelete={() => handleDelete(worker)}
                      />
                    ))
                  )}
                </tbody>
              </table>
            )
          ) : (
            // TABLA DE ROLES
            <table className="table roles-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nombre del Rol</th>
                  <th>Color representativo</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {roles.length === 0 ? (
                   <tr>
                      <td colSpan="4" style={{ padding: "40px", textAlign: "center", color: "#64748b" }}>
                        {loading ? "Cargando roles..." : "No hay roles registrados"}
                      </td>
                    </tr>
                ) : (
                  roles.map((role) => (
                    <RoleItem
                      key={role.id}
                      id={role.id}
                      name={role.name}
                      color={role.color}
                      onEdit={() => handleEditRole(role)}
                      onDelete={() => handleDeleteRole(role)}
                    />
                  ))
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* MODALES */}
      
      {/* ... (El resto de los modales sigue igual) ... */}
      <WorkerModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        mode="create"
        onSubmit={handleCreateWorker}
      />
      <WorkerModal
        isOpen={showViewModal}
        onClose={() => {
          setShowViewModal(false);
          setSelectedWorker(null);
        }}
        mode="view"
        workerData={selectedWorker}
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