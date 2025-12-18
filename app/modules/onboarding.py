# app/modules/onboarding.py
"""
This module handles the initial interaction with the user, specifically the
/start command.

It is responsible for identifying the user's role and presenting them with a
customized menu of options based on their permissions. This ensures that each
user sees only the actions relevant to them.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_owner_menu():
    """Creates and returns the main menu keyboard for the 'owner' role."""
    keyboard = [
        [InlineKeyboardButton("📅 Ver mi agenda", callback_data='view_agenda')],
        [InlineKeyboardButton("⏳ Ver pendientes", callback_data='view_pending')],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_menu():
    """Creates and returns the main menu keyboard for the 'admin' role."""
    keyboard = [
        [InlineKeyboardButton("📊 Ver estado del sistema", callback_data='view_system_status')],
        [InlineKeyboardButton("👥 Gestionar usuarios", callback_data='manage_users')],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_team_menu():
    """Creates and returns the main menu keyboard for the 'team' role."""
    keyboard = [
        [InlineKeyboardButton("🕒 Proponer actividad", callback_data='propose_activity')],
        [InlineKeyboardButton("📄 Ver estatus de solicitudes", callback_data='view_requests_status')],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_client_menu():
    """Creates and returns the main menu keyboard for the 'client' role."""
    keyboard = [
        [InlineKeyboardButton("🗓️ Agendar una cita", callback_data='schedule_appointment')],
        [InlineKeyboardButton("ℹ️ Información de servicios", callback_data='get_service_info')],
    ]
    return InlineKeyboardMarkup(keyboard)

def handle_start(user_role):
    """
    Handles the /start command by sending a role-based welcome message and menu.

    This function acts as a router, determining which menu to display based on
    the user's role, which is passed in as an argument.
    """
    welcome_message = "Hola, soy Talía. ¿En qué puedo ayudarte hoy?"

    if user_role == "owner":
        menu = get_owner_menu()
    elif user_role == "admin":
        menu = get_admin_menu()
    elif user_role == "team":
        menu = get_team_menu()
    else: # Default to the client menu for any other role.
        menu = get_client_menu()

    return welcome_message, menu
