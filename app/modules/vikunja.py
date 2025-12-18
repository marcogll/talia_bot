# app/modules/vikunja.py
# Este módulo maneja la integración con Vikunja para la gestión de tareas.

import requests
import logging
from config import VIKUNJA_API_URL, VIKUNJA_API_TOKEN

logger = logging.getLogger(__name__)

def get_vikunja_headers():
    """Devuelve los headers necesarios para la API de Vikunja."""
    return {
        "Authorization": f"Bearer {VIKUNJA_API_TOKEN}",
        "Content-Type": "application/json"
    }

def get_tasks():
    """
    Obtiene la lista de tareas desde Vikunja.
    """
    if not VIKUNJA_API_TOKEN:
        return "Error: VIKUNJA_API_TOKEN no configurado."

    try:
        # Endpoint para obtener todas las tareas (ajustar según necesidad)
        response = requests.get(f"{VIKUNJA_API_URL}/tasks/all", headers=get_vikunja_headers())
        response.raise_for_status()
        tasks = response.json()

        if not tasks:
            return "No tienes tareas pendientes en Vikunja."

        text = "📋 *Tus Tareas en Vikunja*\n\n"
        for task in tasks[:10]: # Mostrar las primeras 10
            status = "✅" if task.get('done') else "⏳"
            text += f"{status} *{task.get('title')}*\n"
        
        return text
    except Exception as e:
        logger.error(f"Error al obtener tareas de Vikunja: {e}")
        return f"Error al conectar con Vikunja: {e}"

def add_task(title):
    """
    Agrega una nueva tarea a Vikunja.
    """
    if not VIKUNJA_API_TOKEN:
        return "Error: VIKUNJA_API_TOKEN no configurado."

    try:
        data = {"title": title}
        # Nota: Vikunja suele requerir un project_id. Aquí usamos uno genérico o el primero disponible.
        # Por ahora, este es un placeholder para el flujo /vik.
        response = requests.put(f"{VIKUNJA_API_URL}/tasks", headers=get_vikunja_headers(), json=data)
        response.raise_for_status()
        return f"✅ Tarea añadida: *{title}*"
    except Exception as e:
        logger.error(f"Error al añadir tarea a Vikunja: {e}")
        return f"Error al añadir tarea: {e}"
