import mysql.connector
from config import DB_CONFIG
from typing import List, Dict, Optional

def get_connection():
    """Obtiene una conexión a la base de datos"""
    return mysql.connector.connect(**DB_CONFIG)

# USUARIOS
## todos los usuarios
def get_all_users() -> List[Dict]:
    """Obtiene todos los usuarios"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users
    except Exception as e:
        print(f"Error al obtener este usuario: {e}")
        return []
    
## usuario por id
def get_user_by_id(user_id: int) -> Optional[Dict]:
    """Obtiene un usuario por ID"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    except Exception as e:
        print(f"Error al obtener este usuario: {e}")
        return None
    
## crear usuario
def create_user(username: str, email: str, age: int, favorite_genre: str, favorite_artist: str) -> Dict:
    """Crea un nuevo usuario"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO users (username, email, age, favorite_genre, favorite_artist)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (username, email, age, favorite_genre, favorite_artist))
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return {"id": user_id, "message": "Usuario creado exitosamente"}
    except Exception as e:
        print(f"Error al crear este usuario: {e}")
        return {"error": str(e)}
    
#actualizar
def update_user(user_id: int, username: str = None, email: str = None, age: int = None, 
                favorite_genre: str = None, favorite_artist: str = None) -> Dict:
    """Actualizar un usuario"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if username is not None:
            updates.append("username = %s")
            params.append(username)
        if email is not None:
            updates.append("email = %s")
            params.append(email)
        if age is not None:
            updates.append("age = %s")
            params.append(age)
        if favorite_genre is not None:
            updates.append("favorite_genre = %s")
            params.append(favorite_genre)
        if favorite_artist is not None:
            updates.append("favorite_artist = %s")
            params.append(favorite_artist)
        
        if not updates:
            return {"error": "No hay ninguna dato a actualizar"}
        
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Se actualizo exitosamente"}
    except Exception as e:
        print(f"Error al actualizar : {e}")
        return {"error": str(e)}

## Eliminar
def delete_user(user_id: int) -> Dict:
    """Elimina un usuario"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Usuario eliminado"}
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        return {"error": str(e)}
