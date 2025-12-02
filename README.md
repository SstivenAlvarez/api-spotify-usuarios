# Fundamentos de Backend con Python APIs REST Unidad 2 # 
 Nombre: Music API - FastAPI con Spotify
 API RESTful para gestión de usuarios y búsqueda de información musical desde Spotify.

##  Descripción corta
Esta API sencilla permite lo siguiente:
- Crear, leer, actualizar y eliminar usuarios
- Almacenar géneros y artistas favoritos
- Buscar canciones y artistas en tiempo real
- Persistencia de datos en base de datos local

# Tecnologías utilizadas en la actividad

- FastAPI 
- Python 3.13-
- MySQL
- Spotify Web API
- Uvicorn

# Requisitos

- Python 3.10+
- MySQL Server instalado y corriendo
- Pip (gestor de paquetes de Python)
- Cuenta en Spotify Developer

# Instalación y Configuración

1. Clonar el repositorio
    - https://github.com/SstivenAlvarez/api-spotify-usuarios

2. Crear entorno virtual venv y acivarlo

3. Instalar requirements.txt

4. Base de datos
    -codigo CREATE DATABASE music_api;
    USE music_api;

    CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    age INT,
    favorite_genre VARCHAR(100),
    favorite_artist VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

5. crear el .env con el formato
    -
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=tu_contraseña
    DB_NAME=music_api
    DB_PORT=3306
    SPOTIFY_CLIENT_ID=tu_client_id
    SPOTIFY_CLIENT_SECRET=tu_client_secret

6. credenciales de spotify

7. Ejecutar python main.py 
    - http://127.0.0.1:8000/docs
