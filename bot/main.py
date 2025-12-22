# bot/main.py
# Este es el archivo principal del bot. Aquí se inicia todo y se configuran los comandos.

import logging
import sys
from pathlib import Path
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Ensure package imports work even if the file is executed directly
if __package__ is None:
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

# Importamos las configuraciones y herramientas que creamos en otros archivos
from bot.config import TELEGRAM_BOT_TOKEN
from bot.modules.identity import get_user_role
from bot.modules.onboarding import handle_start as onboarding_handle_start
from bot.modules.printer import handle_document, check_print_status
from bot.db import setup_database, close_db_connection
from bot.modules.flow_engine import FlowEngine
from bot.modules.dispatcher import button_dispatcher
from bot.modules.message_handler import text_and_voice_handler
from bot.scheduler import schedule_daily_summary

# Configuramos el sistema de logs para ver mensajes de estado en la consola
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Se ejecuta cuando el usuario escribe /start.
    Muestra un mensaje de bienvenida y un menú según el rol del usuario.
    """
    chat_id = update.effective_chat.id

    # Reset any existing conversation flow
    flow_engine = context.bot_data.get("flow_engine")
    if flow_engine:
        flow_engine.end_flow(chat_id)
        logger.info(f"User {chat_id} started a new conversation, clearing any previous state.")

    user_role = get_user_role(chat_id)
    logger.info(f"Usuario {chat_id} inició conversación con el rol: {user_role}")

    # Obtenemos el texto y los botones de bienvenida desde el módulo de onboarding
    response_text, reply_markup = onboarding_handle_start(user_role, flow_engine)

    # Respondemos al usuario
    await update.message.reply_text(response_text, reply_markup=reply_markup)


async def check_print_status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Command to check print status."""
    user_id = update.effective_user.id
    response = await check_print_status(user_id)
    await update.message.reply_text(response)


async def reset_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Resets the conversation state for the user."""
    user_id = update.effective_user.id
    flow_engine = context.bot_data["flow_engine"]
    flow_engine.end_flow(user_id)
    await update.message.reply_text("🔄 Conversación reiniciada. Puedes empezar de nuevo.")
    logger.info(f"User {user_id} reset their conversation.")


def main() -> None:
    """Función principal que arranca el bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN no está configurado en las variables de entorno.")
        return

    setup_database()

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    flow_engine = FlowEngine()
    application.bot_data["flow_engine"] = flow_engine

    schedule_daily_summary(application)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reset", reset_conversation))
    application.add_handler(CommandHandler("check_print_status", check_print_status_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND | filters.VOICE, text_and_voice_handler))
    application.add_handler(CallbackQueryHandler(button_dispatcher))

    logger.info("Iniciando Talía Bot...")
    try:
        application.run_polling()
    finally:
        close_db_connection()


if __name__ == "__main__":
    main()
