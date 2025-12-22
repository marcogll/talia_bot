# bot/modules/dispatcher.py
# This module is responsible for dispatching user interactions to the correct handlers.

import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.modules.onboarding import get_admin_secondary_menu
from bot.modules.agenda import get_agenda
from bot.modules.citas import request_appointment
from bot.modules.equipo import view_requests_status
from bot.modules.aprobaciones import view_pending, handle_approval_action
from bot.modules.admin import get_system_status
from bot.modules.vikunja import get_projects_list, get_tasks_list

logger = logging.getLogger(__name__)

async def send_step_message(update: Update, step: dict):
    """Helper to send a message for a flow step, including options if available."""
    text = step["question"]
    reply_markup = None

    options = []
    if "options" in step and step["options"]:
        options = step["options"]
    elif "input_type" in step:
        if step["input_type"] == "dynamic_keyboard_vikunja_projects":
            projects = get_projects_list()
            options = [p.get('title', 'Unknown') for p in projects]
        elif step["input_type"] == "dynamic_keyboard_vikunja_tasks":
            tasks = get_tasks_list(1)
            options = [t.get('title', 'Unknown') for t in tasks]

    if options:
        keyboard = []
        row = []
        for option in options:
            cb_data = str(option)[:64]
            row.append(InlineKeyboardButton(str(option), callback_data=cb_data))
            if len(row) >= 2:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup)

async def button_dispatcher(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles button clicks and dispatches them to the appropriate handlers.
    """
    query = update.callback_query
    await query.answer()
    logger.info(f"El despachador recibió una consulta: {query.data}")

    response_text = "Acción no reconocida."
    reply_markup = None

    simple_handlers = {
        'view_agenda': get_agenda,
        'view_requests_status': view_requests_status,
        'schedule_appointment': request_appointment,
        'view_system_status': get_system_status,
        'manage_users': lambda: "Función de gestión de usuarios no implementada.",
    }

    complex_handlers = {
        'admin_menu': get_admin_secondary_menu,
        'view_pending': view_pending,
    }

    try:
        if query.data in simple_handlers:
            handler = simple_handlers[query.data]
            logger.info(f"Ejecutando simple_handler para: {query.data}")
            if asyncio.iscoroutinefunction(handler):
                response_text = await handler()
            else:
                response_text = handler()
        elif query.data in complex_handlers:
            handler = complex_handlers[query.data]
            logger.info(f"Ejecutando complex_handler para: {query.data}")
            if asyncio.iscoroutinefunction(handler):
                response_text, reply_markup = await handler()
            else:
                response_text, reply_markup = handler()
        elif query.data.startswith(('approve:', 'reject:')):
            logger.info(f"Ejecutando acción de aprobación: {query.data}")
            response_text = handle_approval_action(query.data)
        else:
            flow_engine = context.bot_data["flow_engine"]
            flow_to_start = next((flow for flow in flow_engine.flows if flow.get("trigger_button") == query.data), None)

            if flow_to_start:
                logger.info(f"Iniciando flujo: {flow_to_start['id']}")
                initial_step = flow_engine.start_flow(update.effective_user.id, flow_to_start["id"])
                if initial_step:
                    await send_step_message(update, initial_step)
                else:
                    logger.error("No se pudo iniciar el flujo (paso inicial vacío).")
                return

            state = flow_engine.get_conversation_state(update.effective_user.id)
            if state:
                logger.info(f"Procesando paso de flujo para usuario {update.effective_user.id}. Data: {query.data}")
                result = flow_engine.handle_response(update.effective_user.id, query.data)

                if result["status"] == "in_progress":
                    logger.info("Flujo en progreso, enviando siguiente paso.")
                    await send_step_message(update, result["step"])
                elif result["status"] == "complete":
                     logger.info("Flujo completado.")
                     if "sales_pitch" in result:
                         await query.edit_message_text(result["sales_pitch"])
                     elif "nfc_tag" in result:
                         await query.edit_message_text(result["nfc_tag"], parse_mode='Markdown')
                     else:
                         await query.edit_message_text("Gracias por completar el flujo.")
                elif result["status"] == "error":
                     logger.error(f"Error en el flujo: {result['message']}")
                     await query.edit_message_text(f"Error: {result['message']}")
                return

            logger.warning(f"Consulta no manejada por el despachador: {query.data}")
            await query.edit_message_text(text=response_text)
            return

    except Exception as exc:
        logger.exception(f"Error al procesar la acción {query.data}: {exc}")
        response_text = "❌ Ocurrió un error al procesar tu solicitud. Intenta de nuevo."
        reply_markup = None

    await query.edit_message_text(text=response_text, reply_markup=reply_markup, parse_mode='Markdown')
