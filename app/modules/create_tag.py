# app/modules/create_tag.py
"""
This module contains the functionality for the /create_tag command.

It uses a ConversationHandler to guide the user through a series of questions
to collect data (name, employee number, branch, and Telegram ID), and then
generates a Base64-encoded JSON string from that data. This string is intended
to be used for creating an NFC tag.
"""
import base64
import json
import logging
from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

# Enable logging to monitor the bot's operation and for debugging.
logger = logging.getLogger(__name__)

# Define the states for the conversation. These states are used to track the
# user's progress through the conversation and determine which handler function
# should be executed next.
NAME, NUM_EMP, SUCURSAL, TELEGRAM_ID = range(4)

async def create_tag_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Starts the conversation to create a new tag when the /create_tag command
    is issued. It prompts the user for the first piece of information (name).
    """
    await update.message.reply_text("Vamos a crear un nuevo tag. Por favor, dime el nombre:")
    # The function returns the next state, which is NAME, so the conversation
    # knows which handler to call next.
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Stores the user's provided name in the context and then asks for the
    next piece of information, the employee number.
    """
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Gracias. Ahora, por favor, dime el número de empleado:")
    # The function returns the next state, NUM_EMP.
    return NUM_EMP

async def get_num_emp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Stores the employee number and proceeds to ask for the branch name.
    """
    context.user_data['num_emp'] = update.message.text
    await update.message.reply_text("Entendido. Ahora, por favor, dime la sucursal:")
    # The function returns the next state, SUCURSAL.
    return SUCURSAL

async def get_sucursal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Stores the branch name and asks for the final piece of information,
    the user's Telegram ID.
    """
    context.user_data['sucursal'] = update.message.text
    await update.message.reply_text("Perfecto. Finalmente, por favor, dime el ID de Telegram:")
    # The function returns the next state, TELEGRAM_ID.
    return TELEGRAM_ID

async def get_telegram_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Stores the Telegram ID, assembles all the collected data into a JSON
    object, encodes it into a Base64 string, and sends the result back to
    the user. This function concludes the conversation.
    """
    context.user_data['telegram_id'] = update.message.text

    # Create a dictionary from the data collected and stored in user_data.
    tag_data = {
        "name": context.user_data.get('name'),
        "num_emp": context.user_data.get('num_emp'),
        "sucursal": context.user_data.get('sucursal'),
        "telegram_id": context.user_data.get('telegram_id'),
    }

    # Convert the Python dictionary into a JSON formatted string.
    json_string = json.dumps(tag_data)

    # Encode the JSON string into Base64. The string is first encoded to
    # UTF-8 bytes, which is then encoded to Base64 bytes, and finally
    # decoded back to a UTF-8 string for display.
    base64_bytes = base64.b64encode(json_string.encode('utf-8'))
    base64_string = base64_bytes.decode('utf-8')

    await update.message.reply_text(f"¡Gracias! Aquí está tu tag en formato Base64:\n\n`{base64_string}`", parse_mode='Markdown')

    # Clean up the user_data dictionary to ensure no data from this
    # conversation is accidentally used in another one.
    context.user_data.clear()

    # End the conversation.
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Cancels and ends the conversation if the user issues the /cancel command.
    It also clears any data that has been collected so far.
    """
    await update.message.reply_text("Creación de tag cancelada.")
    context.user_data.clear()
    return ConversationHandler.END

def create_tag_conv_handler():
    """
    Creates and returns a ConversationHandler for the /create_tag command.
    This handler manages the entire conversational flow, from starting the
    conversation to handling user inputs and ending the conversation.
    """
    return ConversationHandler(
        # The entry_points list defines how the conversation can be started.
        # In this case, it's started by the /create_tag command.
        entry_points=[CommandHandler('create_tag', create_tag_start)],

        # The states dictionary maps the conversation states to their
        # respective handler functions. When the conversation is in a
        # particular state, the corresponding handler is called to process
        # the user's message.
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            NUM_EMP: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_num_emp)],
            SUCURSAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_sucursal)],
            TELEGRAM_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_telegram_id)],
        },

        # The fallbacks list defines handlers that are called if the user
        # sends a message that doesn't match the current state's handler.
        # Here, it's used to handle the /cancel command.
        fallbacks=[CommandHandler('cancel', cancel)],

        # per_message=False means the conversation is tied to the user, not
        # to a specific message, which is standard for this type of flow.
        per_message=False
    )
