# app/modules/aprobaciones.py
"""
This module manages the approval workflow for requests made by the team.

It provides functions to view pending requests and to handle the approval or
rejection of those requests. The primary user for this module is the "owner"
role, who has the authority to approve or deny requests.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_approval_menu(request_id):
    """
    Creates and returns an inline keyboard with "Approve" and "Reject" buttons.

    Each button is associated with a specific request_id through the
    callback_data, allowing the bot to identify which request is being acted upon.
    """
    keyboard = [
        [
            InlineKeyboardButton("✅ Aprobar", callback_data=f'approve:{request_id}'),
            InlineKeyboardButton("❌ Rechazar", callback_data=f'reject:{request_id}'),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def view_pending():
    """
    Shows the owner a list of pending requests that require their attention.

    Currently, this function uses a hardcoded list of proposals for demonstration.
    In a production environment, this would fetch data from a database or another
    persistent storage mechanism where pending requests are tracked.
    """
    # TODO: Fetch pending requests dynamically from a database or webhook events.
    proposals = [
        {"id": "prop_001", "desc": "Grabación de proyecto", "duration": 4, "user": "Equipo A"},
        {"id": "prop_002", "desc": "Taller de guion", "duration": 2, "user": "Equipo B"},
    ]

    if not proposals:
        return "No hay solicitudes pendientes.", None

    # For demonstration purposes, we'll just show the first pending proposal.
    proposal = proposals[0]

    text = (
        f"⏳ *Nueva Solicitud Pendiente*\n\n"
        f"🙋‍♂️ *Solicitante:* {proposal['user']}\n"
        f"📝 *Actividad:* {proposal['desc']}\n"
        f"⏳ *Duración:* {proposal['duration']} horas"
    )

    # Attach the approval menu to the message.
    reply_markup = get_approval_menu(proposal['id'])

    return text, reply_markup

def handle_approval_action(callback_data):
    """
    Handles the owner's response (approve or reject) to a request.

    This function is triggered when the owner clicks one of the buttons created
    by get_approval_menu. It parses the callback_data to determine the action
    and the request ID.
    """
    action, request_id = callback_data.split(':')

    if action == 'approve':
        # TODO: Implement logic to update the request's status to 'approved'.
        # This could involve updating a database and notifying the requester.
        return f"✅ La solicitud *{request_id}* ha sido aprobada."
    elif action == 'reject':
        # TODO: Implement logic to update the request's status to 'rejected'.
        # This could involve updating a database and notifying the requester.
        return f"❌ La solicitud *{request_id}* ha sido rechazada."

    return "Acción desconocida.", None
