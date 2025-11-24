import React, { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { validateLoginForm } from '../../utils/validators';
// REMOVER esta línea: import { ADMIN_CREDENTIALS } from '../../types/auth.types';
import styles from './Login.module.css';

const Login = () => {
  const { login, isLoading, error, clearError } = useAuth();

  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });

  const [formErrors, setFormErrors] = useState({});
  const [touched, setTouched] = useState({
    username: false,
    password: false
  });

  // Limpiar errores cuando el usuario empiece a escribir
  useEffect(() => {
    if (error) {
      clearError();
    }
  }, [formData.username, formData.password, clearError]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleBlur = (field) => {
    setTouched(prev => ({
      ...prev,
      [field]: true
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validar formulario
    const validation = validateLoginForm(formData.username, formData.password);

    if (!validation.isValid) {
      setFormErrors(validation.errors);
      setTouched({ username: true, password: true });
      return;
    }

    setFormErrors({});

    const result = await login(formData);

    if (result.success) {
      console.log('Login exitoso', result.user);
      // Redirección después de login exitoso
      window.location.href = '/dashboard'; // O usa navigate si estás usando React Router
    }
  };

  // REMOVER la función fillAdminCredentials ya que las credenciales vienen del backend
  // const fillAdminCredentials = () => {
  //   setFormData({
  //     username: ADMIN_CREDENTIALS.username,
  //     password: ADMIN_CREDENTIALS.password
  //   });
  //   setFormErrors({});
  //   clearError();
  // };

  const getFieldError = (field) => {
    return touched[field] && formErrors[field];
  };

  return (
    <div className={styles.loginContainer}>
      <div className={styles.circleGreen} />
      <div className={styles.circleOrange} />

      <form onSubmit={handleSubmit} className={styles.loginForm}>
        <h1 className={styles.title}>Inicio de sesión</h1>
        <p className={styles.subtitle}>Administrador</p>

        {/* Información sobre las credenciales */}
        <div className={styles.credentialsInfo}>
          <p>Ingrese las credenciales de administrador configuradas en el servidor</p>
        </div>

        {/* Campo Usuario */}
        <div className={styles.formGroup}>
          <label htmlFor="username" className={styles.label}>
            Usuario
          </label>
          <input
            id="username"
            name="username"
            type="text"
            value={formData.username}
            onChange={handleInputChange}
            onBlur={() => handleBlur('username')}
            className={`${styles.input} ${getFieldError('username') ? styles.inputError : ''}`}
            placeholder="Ingrese su usuario"
            disabled={isLoading}
            autoComplete="username"
          />
          {getFieldError('username') && (
            <span className={styles.errorMessage}>{formErrors.username}</span>
          )}
        </div>

        {/* Campo Contraseña */}
        <div className={styles.formGroup}>
          <label htmlFor="password" className={styles.label}>
            Contraseña
          </label>
          <input
            id="password"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleInputChange}
            onBlur={() => handleBlur('password')}
            className={`${styles.input} ${getFieldError('password') ? styles.inputError : ''}`}
            placeholder="Ingrese su contraseña"
            disabled={isLoading}
            autoComplete="current-password"
          />
          {getFieldError('password') && (
            <span className={styles.errorMessage}>{formErrors.password}</span>
          )}
        </div>

        {/* Error del servidor */}
        {error && (
          <div className={styles.errorMessage} style={{ 
            marginBottom: '1rem', 
            padding: '0.5rem',
            backgroundColor: '#ffe6e6',
            border: '1px solid #ffcccc',
            borderRadius: '4px'
          }}>
            {error}
          </div>
        )}

        {/* Botón */}
        <button
          type="submit"
          className={`${styles.submitButton} ${isLoading ? styles.loading : ''}`}
          disabled={isLoading}
        >
          <span className={styles.buttonIcon}>&rarr;</span>
          {isLoading ? 'Validando...' : 'Ingresar'}
        </button>
      </form>
    </div>
  );
};

export default Login;