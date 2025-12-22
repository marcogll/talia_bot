# bot/modules/message_handler.py
# This module handles the processing of text and voice messages.

import logging
import os
from telegram import Update
from telegram.ext import ContextTypes

from bot.modules.transcription import transcribe_audio
from bot.modules.dispatcher import send_step_message

logger = logging.getLogger(__name__)

async def text_and_voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles text and voice messages for the flow engine."""
    user_id = update.effective_user.id
    flow_engine = context.bot_data["flow_engine"]

    state = flow_engine.get_conversation_state(user_id)
    if not state:
        return

    user_response = update.message.text
    if update.message.voice:
        voice = update.message.voice
        temp_dir = 'temp_files'
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, f"{voice.file_id}.ogg")

        try:
            voice_file = await context.bot.get_file(voice.file_id)
            await voice_file.download_to_drive(file_path)
            logger.info(f"Voice message saved to {file_path}")

            user_response = transcribe_audio(file_path)
            logger.info(f"Transcription result: '{user_response}'")

        except Exception as e:
            logger.error(f"Error during voice transcription: {e}")
            user_response = "Error al procesar el mensaje de voz."
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    result = flow_engine.handle_response(user_id, user_response)

    if result["status"] == "in_progress":
        await send_step_message(update, result["step"])
    elif result["status"] == "complete":
        if "sales_pitch" in result:
            await update.message.reply_text(result["sales_pitch"])
        elif "nfc_tag" in result:
            await update.message.reply_text(result["nfc_tag"], parse_mode='Markdown')
        else:
            await update.message.reply_text("Gracias por completar el flujo.")
    elif result["status"] == "error":
        await update.message.reply_text(result["message"])
