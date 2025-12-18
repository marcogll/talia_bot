# app/modules/print.py
"""
This module provides a command for administrators to print out the current
configuration details of the bot.

It is a debugging and administrative tool that allows authorized users to quickly
inspect key configuration variables without accessing the environment directly.
"""
from telegram import Update
from telegram.ext import ContextTypes
from ..permissions import is_admin
from ..config import TIMEZONE, CALENDAR_ID, N8N_WEBHOOK_URL

async def print_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /print command.

    When triggered, this function first checks if the user has admin privileges.
    If they do, it replies with a formatted message displaying the current values
    of the TIMEZONE, CALENDAR_ID, and N8N_WEBHOOK_URL configuration variables.
    If the user is not an admin, it sends a simple "not authorized" message.
    """
    chat_id = update.effective_chat.id
    if is_admin(chat_id):
        config_details = (
            f"**Configuration Details**\n"
            f"Timezone: `{TIMEZONE}`\n"
            f"Calendar ID: `{CALENDAR_ID}`\n"
            f"n8n Webhook URL: `{N8N_WEBHOOK_URL}`\n"
        )
        await update.message.reply_text(config_details, parse_mode='Markdown')
    else:
        await update.message.reply_text("You are not authorized to use this command.")
