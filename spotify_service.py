import requests
import base64
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_AUTH_URL, SPOTIFY_API_URL

# Token de Spotify
spotify_token = None

def get_spotify_token():
    """Obtiene un token de autenticación de Spotify"""
    global spotify_token
    
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        return {"error": "Credenciales de Spotify no configuradas"}
    
    try:
        credentials = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
        credentials_b64 = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {credentials_b64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "client_credentials"
        }
        
        response = requests.post(SPOTIFY_AUTH_URL, headers=headers, data=data)
        
        if response.status_code == 200:
            spotify_token = response.json()['access_token']
            return {"token": spotify_token}
        else:
            return {"error": f"Error de autenticación: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def search_song(song_name: str):
    """Busca una canción en Spotify"""
    if not spotify_token:
        token_response = get_spotify_token()
        if "error" in token_response:
            return token_response
    
    try:
        headers = {
            "Authorization": f"Bearer {spotify_token}"
        }
        
        params = {
            "q": song_name,
            "type": "track",
            "limit": 5
        }
        
        response = requests.get(f"{SPOTIFY_API_URL}/search", headers=headers, params=params)
        
        if response.status_code == 200:
            results = response.json()
            tracks = results.get('tracks', {}).get('items', [])
            return {
                "songs": [
                    {
                        "name": track['name'],
                        "artist": track['artists'][0]['name'],
                        "url": track['external_urls']['spotify']
                    }
                    for track in tracks
                ]
            }
        else:
            return {"error": f"Error en búsqueda: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def search_artist(artist_name: str):
    """Busca un artista en Spotify"""
    if not spotify_token:
        token_response = get_spotify_token()
        if "error" in token_response:
            return token_response
    
    try:
        headers = {
            "Authorization": f"Bearer {spotify_token}"
        }
        
        params = {
            "q": artist_name,
            "type": "artist",
            "limit": 5
        }
        
        response = requests.get(f"{SPOTIFY_API_URL}/search", headers=headers, params=params)
        
        if response.status_code == 200:
            results = response.json()
            artists = results.get('artists', {}).get('items', [])
            return {
                "artists": [
                    {
                        "name": artist['name'],
                        "genres": artist.get('genres', []),
                        "url": artist['external_urls']['spotify']
                    }
                    for artist in artists
                ]
            }
        else:
            return {"error": f"Error en búsqueda: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
