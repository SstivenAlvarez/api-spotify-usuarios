from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import (
    tod_user, todos_users_id, crear_usuario, 
    actua_user, eliminar_user
)
from spotify_service import search_song, search_artist

# Fast API
app = FastAPI(
    title="Music API",
    description="API para gestión de usuarios y preferencias musicales con Spotify",
    version="1.0.0"
)

## Formato crear usuario

class User(BaseModel):
    """Modelo para crear usuarios"""
    username: str
    email: str
    age: int
    favorite_genre: str
    favorite_artist: str

## Formato actualizar usuario
class UserUpdate(BaseModel):
    """Modelo para actualizar usuarios """
    username: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    favorite_genre: Optional[str] = None
    favorite_artist: Optional[str] = None


@app.get("/")
def Bienvenia_Al_root():
    """INICIO"""
    return {
        "message": "¡Bienvenido a Music API POR STIVEN ALVAREZ!",
        "TAREA 1": "API REST",
        "version": "1.0.0",
        "endpoints": {
            "usuarios": "/users",
            "Spotify_canciones": "/spotify/search/song",
            "Spotify_artistas": "/spotify/search/artist"
        }
    }

# Ver usuario con filtro por ID

@app.get("/users")
def LISTA_DE_USUARIOS():
    """VER TODOS LOS USUARIOS"""
    users = tod_user()
    return {"total": len(users), "users": users}

@app.get("/users/{user_id}")
def BUSCAR_USUARIO_POR_ID(user_id: int):
    """VER USUARIO POR ID"""
    user = todos_users_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# Crear usuario
@app.post("/users")
def AGREGAR_USUARIO(user: User):
    """CCREAR USUARIO"""
    result = crear_usuario(
        username=user.username,
        email=user.email,
        age=user.age,
        favorite_genre=user.favorite_genre,
        favorite_artist=user.favorite_artist
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# Actulizar Usuario
@app.put("/users/{user_id}")
def ACTUALIZAR_USUARIO(user_id: int, user: UserUpdate):
    """Actualiza un usuario existente"""
    existing_user = todos_users_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="Usuario no se encontro")
    
    result = actua_user(
        user_id=user_id,
        username=user.username,
        email=user.email,
        age=user.age,
        favorite_genre=user.favorite_genre,
        favorite_artist=user.favorite_artist
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

#Delete user
@app.delete("/users/{user_id}")
def ELIMINAR_USUARIO(user_id: int):
    """Eliminar un usuario"""
    existing_user = todos_users_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="Usuario no se encontro")
    
    result = eliminar_user(user_id)
    return result

# Parte de Spotify
### BUSCAR CANCION
@app.get("/spotify/search/song")
def BUSCAR_CANCION_DE_SPOTIFY(uem: str):
    """Busca una canción en Spotify"""
    if not uem:
        raise HTTPException(status_code=400, detail="Parámetro 'uem' es requerido")
    
    result = search_song(uem)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

## BUSCAR ARTISTA
@app.get("/spotify/search/artist")
def BUSCAR_ARTISTA_DE_SPOTIFY(uem: str):
    """Busca un artista en Spotify"""
    if not uem:
        raise HTTPException(status_code=400, detail="Parámetro 'uem' es requerido")
    
    result = search_artist(uem)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

###APIIII

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)