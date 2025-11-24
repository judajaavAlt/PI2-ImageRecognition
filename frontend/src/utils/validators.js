export const validateLoginForm = (username, password) => {
  const errors = {};

  if (!username || username.trim() === '') {
    errors.username = 'El usuario es requerido';
  }

  if (!password || password.trim() === '') {
    errors.password = 'La contraseña es requerida';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};