# app/modules/agenda.py
# Este módulo se encarga de manejar las peticiones relacionadas con la agenda.
# Permite obtener y mostrar las actividades programadas para el día.

import datetime
from calendar import get_events

def get_agenda():
    """
    Obtiene y muestra la agenda del usuario para el día actual desde Google Calendar.
    """
    now = datetime.datetime.utcnow()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + datetime.timedelta(days=1)

    events = get_events(start_of_day, end_of_day)

    if not events:
        return "📅 *Agenda para Hoy*\n\nNo tienes eventos programados para hoy."

    agenda_text = "📅 *Agenda para Hoy*\n\n"
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        # Formatear la hora si es posible
        if "T" in start:
            time_str = start.split("T")[1][:5]
        else:
            time_str = "Todo el día"
        
        summary = event.get("summary", "(Sin título)")
        agenda_text += f"• *{time_str}* - {summary}\n"

    return agenda_text
