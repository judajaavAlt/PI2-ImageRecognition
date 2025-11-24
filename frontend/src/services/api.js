const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// ============================================================
// WORKERS API
// ============================================================

export const workersApi = {
  // Obtener todos los trabajadores
  getAll: async () => {
    const response = await fetch(`${API_URL}/workers/`);
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error("Error response:", errorData);
      throw new Error(errorData.detail || "Error al obtener trabajadores");
    }
    return response.json();
  },

  // Obtener un trabajador por ID
  getById: async (id) => {
    const response = await fetch(`${API_URL}/workers/${id}`);
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error("Error response:", errorData);
      throw new Error(errorData.detail || "Error al obtener trabajador");
    }
    return response.json();
  },

  // Crear un nuevo trabajador
  create: async (workerData) => {
    const payload = {
      name: workerData.name || "",
      document: workerData.documentId || "",
      role: workerData.role ? parseInt(workerData.role) : 1,
      photo: workerData.photo || "",
    };

    console.log("Payload being sent:", payload);

    const response = await fetch(`${API_URL}/workers/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error("Error response:", errorData);
      
      if (Array.isArray(errorData.detail)) {
        const errorMessages = errorData.detail
          .map((err) => `${err.loc ? err.loc.join(".") : "Campo"}: ${err.msg}`)
          .join(", ");
        throw new Error(errorMessages);
      }

      throw new Error(errorData.detail || "Error al crear trabajador");
    }
    return response.json();
  },

  // Actualizar un trabajador
  update: async (id, workerData) => {
    const payload = {
      name: workerData.name || "",
      document: workerData.documentId || "",
      role: workerData.role ? parseInt(workerData.role) : 1,
      photo: workerData.photo || "",
    };

    console.log("Update payload being sent:", payload);

    const response = await fetch(`${API_URL}/workers/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error("Error response:", errorData);
      throw new Error(errorData.detail || "Error al actualizar trabajador");
    }
    return response.json();
  },

  // Eliminar un trabajador
  delete: async (id) => {
    const response = await fetch(`${API_URL}/workers/${id}`, {
      method: "DELETE",
    });
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error("Error response:", errorData);
      throw new Error(errorData.detail || "Error al eliminar trabajador");
    }
    return response.json();
  },
};

// ============================================================
// ROLES API
// ============================================================

export const rolesApi = {
  // Obtener todos los roles
  getAll: async () => {
    const response = await fetch(`${API_URL}/roles/`);
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || "Error al obtener roles");
    }
    return response.json();
  },

  // Obtener un rol por ID
  getById: async (id) => {
    const response = await fetch(`${API_URL}/roles/${id}`);
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || "Error al obtener rol");
    }
    return response.json();
  },

  // Crear un nuevo rol
  // Según tu backend Python: class RoleCreate(BaseModel): name: str, color: str
  create: async (roleData) => {
    const payload = {
      name: roleData.name,
      color: roleData.color,
    };

    const response = await fetch(`${API_URL}/roles/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || "Error al crear rol");
    }
    return response.json();
  },

  // Actualizar un rol
  update: async (id, roleData) => {
    const payload = {
      name: roleData.name,
      color: roleData.color,
    };

    const response = await fetch(`${API_URL}/roles/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || "Error al actualizar rol");
    }
    return response.json();
  },

  // Eliminar un rol
  delete: async (id) => {
    const response = await fetch(`${API_URL}/roles/${id}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || "Error al eliminar rol");
    }
    return response.json();
  },
};