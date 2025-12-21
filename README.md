# 🤖 Talia Bot: Asistente Personal & Orquestador de Negocio

Talia es un **Middleware de Inteligencia Artificial** diseñado para orquestar operaciones de negocio a través de Telegram. Funciona como un asistente personal que responde a roles de usuario específicos, conectando servicios externos como **Vikunja (Gestión de Proyectos)** y **Google Calendar** en una única interfaz conversacional.

---

## 🚀 Concepto Central: Arquitectura Modular y Roles de Usuario

La funcionalidad del bot se basa en dos pilares:

1.  **Enrutamiento por Identidad**: El bot identifica a cada usuario por su Telegram ID y le asigna un rol (`admin`, `crew`, `client`). Cada rol tiene acceso a un conjunto diferente de funcionalidades y menús, definidos en una base de datos SQLite.
2.  **Motor de Flujos de Conversación**: En lugar de código rígido, las conversaciones se definen como "flujos" en archivos **JSON** (`talia_bot/data/flows/`). Un motor central (`flow_engine.py`) interpreta estos archivos para guiar al usuario a través de una serie de preguntas y respuestas, haciendo que el sistema sea altamente escalable y fácil de mantener.

| Rol     | Icono | Descripción         | Permisos Clave                                                              |
| :------ | :---: | :------------------ | :-------------------------------------------------------------------------- |
| **Admin** |  👑   | Dueño / Gerente     | Control total: gestión de proyectos, agenda, y configuración del sistema.   |
| **Crew**  |  👷   | Equipo Operativo    | Funciones limitadas: solicitud de agenda, impresión de documentos.          |
| **Cliente** |  👤   | Usuario Externo     | Embudo de ventas: captación de datos y presentación de servicios.           |

---

## 📋 Flujos de Trabajo Modulares (Features)

El comportamiento del bot se define a través de **flujos de conversación modulares** gestionados por un motor central (`flow_engine.py`). Cada flujo es un archivo `.json` independiente ubicado en `talia_bot/data/flows/`, lo que permite modificar o crear nuevas conversaciones sin alterar el código principal.

### 1. 👑 Gestión Admin (Proyectos & Identidad)

*   **Proyectos (Vikunja)**:
    *   Resumen inteligente de estatus de proyectos.
    *   Comandos naturales: *"Marca el proyecto de web como terminado y comenta que se envió factura"*.
*   **Wizard de Identidad (NFC)**:
    *   Flujo paso a paso para dar de alta colaboradores.
    *   Genera JSON de registro y String Base64 listo para escribir en Tags NFC.
    *   Inputs: Nombre, ID Empleado, Sucursal (Botones), Telegram ID.

### 2. 👷 Gestión Crew (Agenda & Tareas)

*   **Solicitud de Tiempo (Wizard)**:
    *   Solicita espacios de 1 a 4 horas.
    *   **Reglas de Negocio**:
        *   No permite fechas > 3 meses a futuro.
        *   **Gatekeeper**: Verifica Google Calendar. Si hay evento "Privado" del Admin, rechaza automáticamente.
*   **Modo Buzón (Vikunja)**:
    *   Crea tareas asignadas al Admin.
    *   **Privacidad**: Solo pueden consultar el estatus de tareas creadas por ellos mismos.

### 3. 🖨️ Sistema de Impresión Remota (Print Loop)

*   Permite enviar archivos desde Telegram a la impresora física de la oficina.
*   **Envío (SMTP)**: El bot envía el documento a un correo designado.
*   **Tracking**: El asunto del correo lleva un hash único: `PJ:{uuid}#TID:{telegram_id}`.
*   **Confirmación (IMAP Listener)**: Un proceso en background escucha la respuesta de la impresora y notifica al usuario en Telegram.

El sistema opera con el siguiente flujo:

1.  **Recepción de Mensajes**: `main.py` recibe todos los inputs (texto, botones, comandos) desde Telegram.
2.  **Identificación de Usuario**: Se consulta la base de datos (`users.db`) para obtener el rol del usuario.
3.  **Dispatching de Acciones**:
    *   Si el usuario no está en una conversación, se le muestra un menú de botones basado en los flujos JSON disponibles para su rol.
    *   Si el usuario ya está en una conversación, el `flow_engine.py` gestiona la respuesta.
4.  **Ejecución de Módulos**: El motor de flujos invoca módulos específicos (`vikunja.py`, `calendar.py`, etc.) para interactuar con APIs externas según sea necesario.

---

## ⚙️ Instalación y Configuración

### Prerrequisitos

*   Python 3.9+
*   Docker y Docker Compose
*   Cuenta de Telegram Bot (@BotFather)
*   Instancia de Vikunja (Self-hosted)
*   Credenciales de Cuenta de Servicio de Google Cloud (para Calendar API)

### 1. Clonar y Configurar el Entorno

```bash
# Clona el repositorio oficial
git clone https://github.com/marcogll/talia_bot.git
cd talia_bot

# Copia el archivo de ejemplo para las variables de entorno
cp .env.example .env
```

### 2. Variables de Entorno (`.env`)

Abre el archivo `.env` y rellena las siguientes variables. **No subas este archivo a Git.**

```env
# Token de tu bot de Telegram
TELEGRAM_TOKEN=tu_token_telegram

# Tu Telegram ID numérico para permisos de administrador
ADMIN_ID=tu_telegram_id

# Clave de API de OpenAI (si se usa)
OPENAI_API_KEY=sk-...

# URL y Token de tu instancia de Vikunja
VIKUNJA_API_URL=https://tu_vikunja.com/api/v1
VIKUNJA_TOKEN=tu_token_vikunja

# ID del Calendario de Google a gestionar
CALENDAR_ID=tu_id_de_calendario@group.calendar.google.com

# Ruta al archivo de credenciales de Google Cloud.
# Este archivo debe estar en el directorio raíz y se llama 'google_key.json' por defecto.
GOOGLE_SERVICE_ACCOUNT_FILE=./google_key.json
```

### 3. Estructura de Datos y Credenciales

*   **Base de Datos**: La base de datos `users.db` se creará automáticamente si no existe. Para asignar roles, debes agregar manualmente los Telegram IDs en la tabla `users`.
*   **Credenciales de Google**: Coloca tu archivo de credenciales de la cuenta de servicio de Google Cloud en el directorio raíz del proyecto y renómbralo a `google_key.json`. **El archivo `.gitignore` ya está configurado para ignorar este archivo y proteger tus claves.**
*   **Flujos de Conversación**: Para modificar o añadir flujos, edita los archivos JSON en `talia_bot/data/flows/`.

Asegúrate de tener los archivos y directorios base en `talia_bot/data/`:
*   `servicios.json`: Catálogo de servicios para el RAG de ventas.
*   `credentials.json`: Credenciales de Google Cloud.
*   `users.db`: Base de datos SQLite que almacena los roles de los usuarios.
*   `flows/`: Directorio que contiene las definiciones de los flujos de conversación en formato JSON. Cada archivo representa una conversación completa para un rol específico.

---

## 📂 Estructura del Proyecto

```text
talia_bot/
├── .env                       # (Local) Variables de entorno y secretos
├── .env.example               # Plantilla de variables de entorno
├── .gitignore                 # Archivos ignorados por Git
├── Dockerfile                 # Define el contenedor de la aplicación
├── docker-compose.yml         # Orquesta el servicio del bot
├── google_key.json            # (Local) Credenciales de Google Cloud
├── requirements.txt           # Dependencias de Python
├── talia_bot/
│   ├── main.py              # Entry Point y dispatcher principal
│   ├── db.py                # Gestión de la base de datos SQLite
│   ├── config.py            # Carga de variables de entorno
│   ├── modules/
│   │   ├── flow_engine.py   # Motor de flujos de conversación (lee los JSON)
│   │   ├── identity.py      # Lógica de Roles y Permisos
│   │   ├── llm_engine.py    # Cliente OpenAI/Gemini
│   │   ├── vikunja.py       # API Manager para Tareas
│   │   ├── calendar.py      # Google Calendar Logic & Rules
│   │   ├── printer.py       # SMTP/IMAP Loop
│   │   └── sales_rag.py     # Lógica de Ventas y Servicios
│   └── data/
│       ├── flows/           # Directorio con los flujos de conversación en JSON
│       ├── servicios.json   # Base de conocimiento para ventas
│       ├── credentials.json # Credenciales de Google
│       └── users.db         # Base de datos de usuarios
├── .env.example             # Plantilla de variables de entorno
├── requirements.txt         # Dependencias
├── Dockerfile               # Configuración del contenedor
└── docker-compose.yml       # Orquestador de Docker
```

---

## 🗓️ Roadmap

- [ ] Implementar Wizard de creación de Tags NFC (Base64).
- [ ] Conectar Loop de Impresión (SMTP/IMAP).
- [ ] Migrar de OpenAI a Google Gemini 1.5 Pro.
- [ ] Implementar soporte para fotos en impresión.

---

Desarrollado por: Marco G.
Asistente Personalizado v1.0
