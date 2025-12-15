# app/main.py
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from config import TELEGRAM_BOT_TOKEN
from permissions import get_user_role
from modules.onboarding import handle_start as onboarding_handle_start

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message and menu when the /start command is issued."""
    chat_id = update.effective_chat.id
    user_role = get_user_role(chat_id)

    logger.info(f"User {chat_id} started conversation with role: {user_role}")

    # Delegate to the onboarding module
    response_text, reply_markup = onboarding_handle_start(user_role)

    await update.message.reply_text(response_text, reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    # TODO: Implement handlers for the different callback queries
    await query.edit_message_text(text=f"Selected option: {query.data}")

def main() -> None:
    """Start the bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is not set in the environment variables.")
        return

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Run the bot until the user presses Ctrl-C
    logger.info("Starting Talía Bot...")
    application.run_polling()

if __name__ == "__main__":
    main()
