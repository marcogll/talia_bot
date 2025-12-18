# Talía Development Tasks

This file tracks the development tasks for the Talía project.

## Phase 1: Project Scaffolding

- [x] Create `tasks.md` to track project development.
- [x] Create the basic directory structure (`app`, `app/modules`).
- [x] Create placeholder files in the root directory (`docker-compose.yml`, `Dockerfile`, `.env.example`).
- [x] Create placeholder files in the `app` directory.
- [x] Create placeholder files in the `app/modules` directory.

## Phase 2: Core Logic Implementation

- [x] Implement `main.py` as the central orchestrator.
- [x] Implement `config.py` to handle environment variables.
- [x] Implement `permissions.py` for role-based access control.
- [x] Implement `webhook_client.py` for n8n communication.

## Phase 3: Module Implementation

- [x] Implement `onboarding.py` module.
- [x] Implement `agenda.py` module.
- [x] Implement `citas.py` module.
- [x] Implement `equipo.py` module.
- [x] Implement `aprobaciones.py` module.
- [x] Implement `servicios.py` module.
- [x] Implement `admin.py` module.
- [x] Add `/print` command for authorized users.

## Phase 4: Integrations

- [x] Implement `calendar.py` for Google Calendar integration.
- [x] Implement `llm.py` for AI-powered responses.
- [x] Implement `scheduler.py` for daily summaries.
- [x] Implement `vikunja.py` module for task management.

## Phase 5: Refactoring and Bugfixing

- [x] Restructure admin menu into a two-level system.
- [x] Refactor Vikunja module to integrate with the new admin menu.
- [x] Add "edit task" functionality to the Vikunja module.
- [x] Fix critical bug in `button_dispatcher` related to `async` function handling.
- [x] Fix `create_tag` conversation handler integration.
- [x] Stabilize and verify all admin menu functionalities.

## Log

### 2024-05-22

- Created `tasks.md` to begin tracking development.
- Completed initial project scaffolding.
- Implemented the core logic for the bot, including the central orchestrator, permissions, and onboarding.
- Implemented the `agenda` and `citas` modules.
- Implemented the conversational flow for proposing and approving activities.
- Completed Phase 3 by implementing all modules and refactoring the main dispatcher.

### 2024-05-23

- Add `/print` command for authorized users.

### 2024-05-24

- Implemented Vikunja integration module.
- Restructured the admin menu into a primary and secondary menu.
- Added "edit task" functionality to the Vikunja module.
- Fixed a critical bug in the `button_dispatcher` that was causing timeouts and unresponsive buttons.
- Corrected the `create_tag` conversation handler to be initiated by a command instead of a button.
- Verified that all admin menu options are now functioning correctly.
