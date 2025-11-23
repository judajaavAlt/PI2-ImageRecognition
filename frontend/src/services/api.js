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
      console.error("Error detail:", JSON.stringify(errorData.detail, null, 2));

      // Si detail es un array de errores de validación
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
