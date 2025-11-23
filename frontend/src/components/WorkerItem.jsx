import React from "react";

function WorkerItem({ index, name, documentId, role, onEdit, onDelete, onView }) {
  return (
    <tr style={{ cursor: "pointer" }}>
      <td className="w-num" onClick={onView}>{index}</td>
      <td onClick={onView}>{name}</td>
      <td onClick={onView}>{documentId}</td>
      <td onClick={onView}>{role}</td>
      <td className="actions">
        <div>
          <button className="btn btn-view" onClick={onView}>
            👁️ Ver
          </button>
          <button className="btn btn-edit" onClick={onEdit}>
            ✏️ Editar
          </button>
          <button className="btn btn-delete" onClick={onDelete}>
            🗑️ Borrar
          </button>
        </div>
      </td>
    </tr>
  );
}

export default WorkerItem;
