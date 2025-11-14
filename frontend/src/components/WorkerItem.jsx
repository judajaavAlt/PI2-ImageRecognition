import React from "react";

function WorkerItem({ index, name, documentId, role, onEdit, onDelete }) {
  return (
    <tr>
      <td className="w-num">{index}</td>
      <td>{name}</td>
      <td>{documentId}</td>
      <td>{role}</td>
      <td className="actions">
        <button className="btn btn-edit" onClick={onEdit}>
          ✏️ Editar
        </button>
        <button className="btn btn-delete" onClick={onDelete}>
          🗑️ Borrar
        </button>
      </td>
    </tr>
  );
}

export default WorkerItem;
