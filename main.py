from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import (
    get_all_users, get_user_by_id, create_user, 
    update_user, delete_user
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
def read_root():
    """INICIO"""
    return {
        "message": "¡Bienvenido a Music API POR STIVEN ALVAREZ!",
        "version": "1.0.0",
        "endpoints": {
            "usuarios": "/users",
            "spotify_canciones": "/spotify/search/song",
            "spotify_artistas": "/spotify/search/artist"
        }
    }

# Ver usuario con filtro por ID

@app.get("/users")
def list_users():
    """VER TODOS LOS USUARIOS"""
    users = get_all_users()
    return {"total": len(users), "users": users}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    """VER USUARIO POR ID"""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# Crear usuario
@app.post("/users")
def create_new_user(user: User):
    """CCREAR USUARIO"""
    result = create_user(
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
def update_existing_user(user_id: int, user: UserUpdate):
    """Actualiza un usuario existente"""
    existing_user = get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="Usuario no se encontro")
    
    result = update_user(
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
def delete_existing_user(user_id: int):
    """Eliminar un usuario"""
    existing_user = get_user_by_id(user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="Usuario no se encontro")
    
    result = delete_user(user_id)
    return result

# Parte de Spotify
### BUSCAR CANCION
@app.get("/spotify/search/song")
def search_spotify_song(q: str):
    """Busca una canción en Spotify"""
    if not q:
        raise HTTPException(status_code=400, detail="Parámetro 'q' es requerido")
    
    result = search_song(q)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

## BUSCAR ARTISTA
@app.get("/spotify/search/artist")
def search_spotify_artist(q: str):
    """Busca un artista en Spotify"""
    if not q:
        raise HTTPException(status_code=400, detail="Parámetro 'q' es requerido")
    
    result = search_artist(q)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

###APIIII

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)