# app/modules/equipo.py
"""
This module contains functionality for authorized team members.

It includes a conversational flow for proposing new activities that require
approval from the owner, as well as a function to check the status of
previously submitted requests.
"""
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

# Define the states for the activity proposal conversation.
DESCRIPTION, DURATION = range(2)

async def propose_activity_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Starts the conversation for a team member to propose a new activity.
    This is typically triggered by an inline button press.
    """
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Por favor, describe la actividad que quieres proponer."
    )
    # The function returns the next state, which is DESCRIPTION.
    return DESCRIPTION

async def get_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Stores the activity description provided by the user and asks for the duration.
    """
    context.user_data['activity_description'] = update.message.text
    await update.message.reply_text(
        "Entendido. Ahora, por favor, indica la duración estimada en horas (ej. 2, 4.5)."
    )
    # The function returns the next state, DURATION.
    return DURATION

async def get_duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Stores the activity duration, confirms the proposal to the user, and ends the conversation.
    """
    try:
        duration = float(update.message.text)
        context.user_data['activity_duration'] = duration
        description = context.user_data.get('activity_description', 'N/A')

        confirmation_text = (
            f"Gracias. Se ha enviado la siguiente propuesta para aprobación:\n\n"
            f"📝 *Actividad:* {description}\n"
            f"⏳ *Duración:* {duration} horas\n\n"
            "Recibirás una notificación cuando sea revisada."
        )

        # TODO: Send this proposal to the owner for approval, for example,
        # by sending a webhook or saving it to a database.
        await update.message.reply_text(confirmation_text, parse_mode='Markdown')

        # Clean up user_data to prevent data leakage into other conversations.
        context.user_data.clear()

        # End the conversation.
        return ConversationHandler.END
    except ValueError:
        # If the user provides an invalid number for the duration, ask again.
        await update.message.reply_text("Por favor, introduce un número válido para la duración en horas.")
        return DURATION

async def cancel_proposal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Cancels and ends the activity proposal conversation.
    This is triggered by the /cancel command.
    """
    await update.message.reply_text("La propuesta de actividad ha sido cancelada.")
    context.user_data.clear()
    return ConversationHandler.END

def view_requests_status():
    """
    Allows a team member to see the status of their recent requests.

    Currently, this returns a hardcoded sample status. In a real-world
    application, this would fetch the user's requests from a database.
    """
    # TODO: Fetch the status of recent requests from a persistent data source.
    return "Aquí está el estado de tus solicitudes recientes:\n\n- Grabación de proyecto (4h): Aprobado\n- Taller de guion (2h): Pendiente"
