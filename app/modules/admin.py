# app/modules/admin.py
"""
This module contains administrative functions for the bot.

Currently, it provides a simple way to check the system's status.
"""

def get_system_status():
    """
    Returns a formatted string with the current status of the bot and its integrations.

    This function currently returns a hardcoded status message. In the future,
    it could be expanded to perform real-time checks on the different services.
    """
    # TODO: Implement real-time status checks for more accurate monitoring.
    status_text = (
        "📊 *Estado del Sistema*\n\n"
        "- *Bot Principal:* Activo ✅\n"
        "- *Conexión Telegram API:* Estable ✅\n"
        "- *Integración n8n:* Operacional ✅\n"
        "- *Google Calendar:* Conectado ✅"
    )
    return status_text
