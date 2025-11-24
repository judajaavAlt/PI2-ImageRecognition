import React from "react";

function RoleItem({ id, name, color, onEdit, onDelete }) {
  return (
    <tr>
      <td className="w-num">{id}</td>
      <td>{name}</td>
      <td>
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <span
            style={{
              display: "inline-block",
              width: "20px",
              height: "20px",
              borderRadius: "50%",
              backgroundColor: color,
            }}
          ></span>
          <span>{color}</span>
        </div>
      </td>
      <td className="actions">
        <div>
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

export default RoleItem;
