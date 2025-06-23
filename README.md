# -SA-Tarea3-201602805


Este proyecto corresponde a una implementación práctica de una CMDB (Base de Datos de Gestión de Configuración) desarrollada en Python utilizando el framework FastAPI y PostgreSQL como motor de base de datos relacional.

## ¿Qué hace este sistema?
Permite registrar, consultar, modificar y eliminar diferentes elementos de infraestructura, software, servicios, bases de datos y cualquier otro componente tecnológico relevante para la organización. También permite establecer relaciones de dependencia entre CIs y dejar constancia de los cambios realizados sobre cada uno, facilitando la auditoría y el control de activos.

### Estructura

- **`app/main.py`**: Define los endpoints REST y la configuración principal de FastAPI.
- **`app/models.py`**: Modelos de datos que representan las tablas en la base de datos.
- **`app/schemas.py`**: Esquemas de Pydantic usados para validación y documentación.
- **`app/database.py`**: Configuración de la conexión a PostgreSQL.
- **`app/crud.py`**: Funciones para operaciones CRUD y consultas avanzadas.
- **`app/seed.py`**: Script para cargar datos de ejemplo en la base.
- **`app/audit.py`**: Lógica relacionada con la auditoría de cambios.
- **`app/test_main.py`**: Pruebas unitarias automáticas.
- **`requirements.txt`**: Lista de dependencias necesarias.
- **`diagram_er.png`**: Imagen del diagrama Entidad-Relación generado.

## Requisitos para ejecutar el proyecto

- Python 3.8 o superior
- PostgreSQL instalado y corriendo en tu máquina
- pip y virtualenv para gestionar dependencias

## Pasos de instalación y realizar pruebas

1. **Clona el repositorio y entra al proyecto:**
    ```bash
    git clone <URL_DEL_REPO>
    cd cmdb-fastapi
    ```

2. **Crea un entorno virtual y actívalo:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Crea la base de datos en PostgreSQL:**
    - Ingresa a psql:
      ```bash
      psql -U postgres
      ```
    - Ejecuta:
      ```sql
      CREATE DATABASE tarea3;
      \q
      ```

5. **Configura los parámetros de conexión en `app/database.py`** si tus credenciales son diferentes.

6. **Carga datos de ejemplo ejecutando:**
    ```bash
    python -m app.seed
    ```

7. **Inicia el servidor de FastAPI:**
    ```bash
    uvicorn app.main:app --reload
    ```

8. **Accede a la documentación interactiva en:**  
    [http://localhost:8000/docs](http://localhost:8000/docs)


## Diagrama ER
![Diagrama_ER](/backend/app/diagrama_ER.jpeg)

## Documentacion API
![API](/backend/app/API.jpeg)

## Pruebas
![Pruebas](/backend/app/test1.jpeg)

