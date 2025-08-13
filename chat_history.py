import json
from datetime import datetime
import threading

import os
HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),'chat_history.jsonl')

_lock = threading.Lock()

def save_interaction(user_id: str, prompt: str, response: str, roles: str):
    """
    Guarda una interacción de chat en el historial.
    Parámetros:
        user_id (str): ID del usuario.
        prompt (str): Mensaje enviado por el usuario.
        response (str): Respuesta generada por el bot.
        roles (str): Rol de quien escribió el mensaje.
    """
    entry = {
        "user_id": user_id,
        "prompt": prompt,
        "response": response,
        "roles": roles,
        "timestamp": datetime.now().isoformat()
    }
    with _lock:
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def load_history(user_id: str, limit: int = 10):
    """
    Devuelve las últimas N interacciones de un usuario específico.
    Parámetros:
        user_id (str): ID del usuario.
        limit (int, opcional): Número máximo de interacciones a devolver (por defecto 10).
    Retorna:
        list: Lista de interacciones (dict) del usuario.
    """
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        user_lines = [json.loads(line) for line in lines if json.loads(line).get("user_id") == user_id]
        return user_lines[-limit:]
    except FileNotFoundError:
        return []
    except Exception:
        return []
