# Vikunja Integration Flow (/vik)

## Objective

Implement a temporary flow controlled by the `/vik` command to manage tasks in Vikunja (https://tasks.soul23.cloud). This flow is exclusive to the Admin/Owner.

## Features

- **View Tasks**: List current tasks from Vikunja.
- **Add Task**: Remote task creation.
- **Edit Task**: Basic task modification.

## Technical Requirements

- **API Base**: `https://tasks.soul23.cloud/api/v1`
- **Authentication**: Bearer Token (to be configured in `.env`).
- **Access Control**: Only the Admin/Owner can trigger this flow.

## Webhook Fallback Logic

The system should implement a dual-webhook strategy:

1. **Primary**: `N8N_WEBHOOK_URL` (Normal/Production).
2. **Fallback**: `N8N_TEST_WEBHOOK_URL` (Test/Development).

If the primary webhook fails or is not configured, the system must attempt to use the fallback.

## Project Webhooks

Vikunja supports sending webhooks per project. This can be used to notify the bot (via n8n) when tasks are created or updated directly in the Vikunja interface, keeping the bot's context in sync.

---

> [!NOTE]
> This document serves as a specification for the development of the Vikunja module.
