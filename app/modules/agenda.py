# app/modules/agenda.py
"""
This module is responsible for handling agenda-related requests.

It provides functionality to fetch and display the user's schedule for the day.
"""

def get_agenda():
    """
    Fetches and displays the user's agenda for the current day.

    Currently, this function returns a hardcoded sample agenda for demonstration
    purposes. The plan is to replace this with a real integration that fetches
    events from a service like Google Calendar.
    """
    # TODO: Fetch the agenda dynamically from Google Calendar.
    agenda_text = (
        "📅 *Agenda para Hoy*\n\n"
        "• *10:00 AM - 11:00 AM*\n"
        "  Reunión de Sincronización - Proyecto A\n\n"
        "• *12:30 PM - 1:30 PM*\n"
        "  Llamada con Cliente B\n\n"
        "• *4:00 PM - 5:00 PM*\n"
        "  Bloque de trabajo profundo - Desarrollo Talía"
    )
    return agenda_text
