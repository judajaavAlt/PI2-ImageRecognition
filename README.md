
# 🧩 Worker Management App

Aplicación para la **gestión y control de trabajadores** mediante reconocimiento facial y verificación de uniforme.  
El sistema permite reconocer a los trabajadores **que entran, que salen** y validar **si usan el uniforme correcto**.



## 📁 Estructura del repositorio

````
worker-management-app/
│
├── frontend/                   # Aplicación cliente (React + Vite)
│   ├── src/                    # Código fuente
│   ├── public/                 # Archivos estáticos
│   ├── tests/                  # Pruebas unitarias (Jest + RTL)
│   ├── package.json
│   └── Dockerfile
│
├── backend/                    # API y lógica de negocio (FastAPI + Python)
│   ├── app/
│   │   ├── api/                # Endpoints HTTP (entradas, salidas, uniforme)
│   │   ├── core/               # Configuración (CORS, logs, etc.)
│   │   ├── db/                 # Configuración de base de datos
│   │   ├── models/             # Modelos Pydantic / ORM
│   │   ├── services/           # Lógica de negocio (reconocimiento, etc.)
│   │   ├── tests/              # Pruebas unitarias y de integración (pytest)
│   │   └── main.py             # Punto de entrada de FastAPI
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── .github/workflows/          # CI/CD (construcción, pruebas, despliegue)
│   └── backend-ci.yml
│
└── README.md

````



## ⚙️ Arquitectura general

El sistema está dividido en dos capas principales:

| Capa | Tecnología | Arquitectura | Metodología |
|------|-------------|---------------|--------------|
| **Frontend** | React + Vite | Component-Based / Atomic Design | Kanban + Unit Testing |
| **Backend** | FastAPI (Python) | Clean Architecture | TDD + CI/CD (GitHub Actions) |

### 🧠 Backend (FastAPI)
- API RESTful con separación de capas (dominio, aplicación, infraestructura).
- Pruebas bajo TDD con **pytest**.
- Despliegue como contenedor **Docker**.
- CI/CD con **GitHub Actions** para ejecutar pruebas y subir imágenes a Docker Hub.

### 💻 Frontend (React + Vite)
- Arquitectura basada en componentes.
- Comunicación con la API mediante **Axios**.
- Manejo de estado global con **Zustand** o **Redux Toolkit**.
- Pruebas unitarias con **Jest + React Testing Library**.



## 🚀 Configuración de entorno local

### 🔹 Requisitos previos

Asegúrate de tener instalados:
- [Node.js ≥ 18](https://nodejs.org/)
- [Python ≥ 3.11](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Git](https://git-scm.com/)



## 🐳 Backend (FastAPI con Docker)

### 1️⃣ Construir la imagen Docker

Desde la raíz del repositorio:
```bash
cd backend
docker build -t worker-backend:dev .
````

### 2️⃣ Ejecutar el contenedor

```bash
docker run -p 8000:8000 worker-backend:dev
```

> Esto iniciará el backend en `http://localhost:8000`.

### 3️⃣ Probar la API

Accede a la documentación interactiva:

* Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)
* Redoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)



## ⚛️ Frontend (React + Vite)

### 1️⃣ Instalar dependencias

```bash
cd frontend
npm install
```

### 2️⃣ Iniciar el entorno de desarrollo

```bash
npm run dev
```

> La app estará disponible en [http://localhost:5173](http://localhost:5173).

Asegúrate de que el backend (Docker) esté corriendo para probar las funcionalidades completas.



## 🧪 Sistema de pruebas

Antes de hacer una *pull request*, asegúrate de que **todas las pruebas pasen**.

### 🔹 Backend

Ejecuta pruebas con `pytest` dentro del contenedor o localmente:

```bash
cd backend
pytest --maxfail=1 --disable-warnings -q
```

### 🔹 Frontend

Ejecuta las pruebas con Jest:

```bash
cd frontend
npm test
```



## 🔄 Flujo de desarrollo (TDD + CI/CD)

1. Crea una rama nueva:

   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
2. Implementa los tests **antes** del código (TDD).
3. Implementa el código hasta que las pruebas pasen.
4. Verifica localmente:

   ```bash
   pytest && npm test
   ```
5. Crea una Pull Request hacia `main`.

> El pipeline CI/CD ejecutará automáticamente las pruebas y construirá la imagen Docker antes de aprobar el merge.



## 🐙 CI/CD (GitHub Actions)

* Ubicación del workflow: `.github/workflows/backend-ci.yml`
* Etapas:

  1. Checkout del código.
  2. Instalación de dependencias.
  3. Ejecución de pruebas (pytest).
  4. Build y push de la imagen Docker.



## 🧾 Licencia

Este proyecto se distribuye bajo licencia **MIT**.
Puedes usarlo, modificarlo y desplegarlo libremente citando la fuente.



## 👥 Autores

Equipo de desarrollo — Arquitectura basada en **FastAPI + React + Docker + TDD**
