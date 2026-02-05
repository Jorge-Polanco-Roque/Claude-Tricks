# Voice Service Builder - Skill

Create production-ready voice assistant services with ElevenLabs Conversational AI, FastAPI backend, and Google Sheets as database. Generates a complete backend with webhook tools + embeddable widget for any website.

## Usage

```
/voice-service <business-name> [options]
```

## Invocation Examples

- `/voice-service bella-italia --type="restaurant" --tools="reservations,menu"`
- `/voice-service clinica-dental --type="clinic" --tools="appointments,services"`
- `/voice-service hotel-paradise --type="hotel" --tools="bookings,rooms,amenities"`
- `/voice-service barberia-style --type="barbershop" --tools="appointments"`
- `/voice-service taller-mecanico --type="auto-shop" --tools="appointments,quotes"`

## Instructions for Claude

When this skill is invoked, follow this comprehensive process to create a voice assistant service:

---

## PHASE 1: DISCOVERY & REQUIREMENTS

### 1.1 Business Understanding

Ask the user these questions using AskUserQuestion:

**Business Info:**
- What type of business is this? (restaurant, clinic, hotel, barbershop, gym, etc.)
- What is the business name?
- What language should the agent speak? (Spanish, English, etc.)
- What are the business hours?

**Agent Personality:**
- What personality should the agent have? (formal, casual, friendly, professional)
- What is the agent's name?
- What is the agent's gender? (for voice selection)

**Tools/Features Needed (select all that apply):**
- Appointments/Reservations
- Service catalog / Menu
- Pricing information
- Availability checking
- Cancellations & modifications
- Customer lookup
- FAQ / General questions
- Location & directions

**Google Sheets Setup:**
- Do you already have a Google Cloud project with Sheets API enabled?
- Do you have a Service Account with credentials?
- Do you have a Spreadsheet already created?

**ElevenLabs Setup:**
- Do you have an ElevenLabs account with Conversational AI?
- Do you already have an agent created?
- Do you have an API key?

---

## PHASE 2: PROJECT STRUCTURE

### 2.1 Generate Project Structure

Based on the business type, create this structure:

```
{project-name}/
├── app/
│   ├── __init__.py
│   ├── main.py                        # FastAPI entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── {domain}.py                # API router with webhook endpoints
│   └── services/
│       ├── __init__.py
│       └── google_sheets_service.py   # Google Sheets integration
│
├── .env.example                       # Template for environment variables
├── .gitignore                         # Exclude sensitive files
├── requirements.txt                   # Python dependencies
├── Dockerfile                         # Multi-stage build for Cloud Run
├── cloudrun-env.yaml                  # Cloud Run env vars (non-sensitive)
├── configure_elevenlabs.py            # Script to configure agent tools
├── setup_sheets.py                    # Script to create Sheets structure
├── test.html                          # Test page with ElevenLabs widget
├── README.md                          # Project documentation
└── CLAUDE.md                          # Claude Code documentation
```

### 2.2 Domain Mapping

Map the business type to domain concepts:

| Business Type | Domain | Primary Sheet | Secondary Sheet | Key Fields |
|---------------|--------|---------------|-----------------|------------|
| Restaurant | tables | Mesas | Reservas | capacity, location, date, time, party_size |
| Clinic/Doctor | appointments | Services | Appointments | doctor, specialty, date, time, patient |
| Hotel | rooms | Rooms | Bookings | room_type, capacity, check_in, check_out, guest |
| Barbershop/Salon | appointments | Services | Appointments | service, barber, date, time, client |
| Gym/Studio | classes | Classes | Enrollments | class_type, instructor, date, time, member |
| Auto Shop | services | Services | Appointments | service_type, vehicle, date, time, client |
| Generic | bookings | Resources | Bookings | resource, date, time, client |

---

## PHASE 3: IMPLEMENTATION

### 3.1 FastAPI Main Application (app/main.py)

Create the FastAPI application with:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="{Business Name} Voice Service", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include domain router
from .api.{domain} import router as domain_router
app.include_router(domain_router)

# Health endpoints
@app.get("/health/live")
async def liveness():
    return {"status": "ok", "service": "voice", "version": "1.0.0"}

@app.get("/")
async def root():
    return {
        "service": "{Business Name} Voice Service",
        "version": "1.0.0",
        "status": "running"
    }
```

### 3.2 Google Sheets Service (app/services/google_sheets_service.py)

Create a singleton service that handles ALL Google Sheets operations:

**MUST include:**
- Singleton pattern
- Service Account authentication
- Sheet data reading (`_get_sheet_data`)
- Row appending (`_append_row`)
- Cell updating (`_update_cell`)
- Phone normalization (`_normalize_phone`)
- Time utilities (`_time_to_minutes`, `_add_hours_to_time`)
- Mock data mode (when Sheets is not configured)
- Proper error handling and logging

**Business-specific methods based on type:**

For ALL business types, include:
- `get_all_{resources}()` - List all available resources
- `get_{bookings}_for_date(date)` - Get bookings for a specific date
- `check_availability(date, time, ...)` - Check if resource is available
- `create_{booking}(...)` - Create a new booking
- `search_by_phone(phone)` - Find bookings by phone
- `cancel_{booking}(id, phone)` - Cancel a booking
- `modify_{booking}(id, phone, ...)` - Modify a booking
- `update_notes(id, phone, notes)` - Add notes (ACCUMULATIVE, not replace)

**IMPORTANT PATTERNS:**
1. Availability checking MUST verify no time conflicts exist
2. Notes MUST be accumulative (append, not replace)
3. Phone numbers MUST be normalized (only digits, min 7 chars)
4. Cancellations MUST verify phone before executing
5. Mock data MUST be provided for offline development

### 3.3 API Router (app/api/{domain}.py)

Create webhook endpoints that ElevenLabs will call:

**MUST include these endpoints:**

```
GET  /widget-api/{domain}/v1/         # API documentation
GET  /widget-api/{domain}/v1/health   # Sheets connection status
GET  /widget-api/{domain}/v1/{resources}  # List all resources
POST /widget-api/{domain}/v1/availability # Check availability
POST /widget-api/{domain}/v1/reserve      # Create booking
POST /widget-api/{domain}/v1/search       # Search by phone
POST /widget-api/{domain}/v1/cancel       # Cancel booking
POST /widget-api/{domain}/v1/modify       # Modify booking
POST /widget-api/{domain}/v1/update-notes # Update notes (accumulative)
```

**MUST use Pydantic models for all requests/responses.**

**Phone validation: min_length=7 (no country code required)**

### 3.4 ElevenLabs Configuration Script (configure_elevenlabs.py)

Create a script that:
1. Reads .env for API_KEY, AGENT_ID, WEBHOOK_BASE_URL
2. Defines webhook tools matching the API endpoints
3. Creates tools in ElevenLabs workspace via API
4. Associates tool_ids with the agent via PATCH
5. Includes a "list" mode to show current tools

**IMPORTANT tool description guidelines:**
- NEVER mention internal IDs to the customer
- Phone descriptions: "Teléfono del cliente (solo números)"
- Reserve: "NO menciones códigos de reserva al cliente"
- Cancel/Modify: "Primero busca la reserva con search"
- update_notes: "Agrega notas durante la conversación. Úsalo MÚLTIPLES VECES."

### 3.5 Setup Sheets Script (setup_sheets.py)

Create a script that:
1. Reads Service Account credentials
2. Renames/creates sheets based on business type
3. Adds headers to all sheets
4. Adds initial data (resources with realistic data for the business)

### 3.6 Agent Prompt Template

Generate an agent prompt based on business type. MUST include:

```
# REGLAS IMPORTANTES
1. Si no sabe algo, NO inventar. Decir "Lo siento, no cuento con esa información."
2. Si preguntan algo no relacionado, redirigir: "Mi objetivo es ayudarte con {domain}."
3. NUNCA mencionar códigos internos al cliente.
4. Teléfonos: solo números, sin código de país.

# FLUJO DE {BOOKING_TYPE}
1. Confirmar: fecha, hora, {specific_fields}
2. SIEMPRE preguntar: "{specific_question}" (ej: restricciones alimenticias, alergias, etc.)
3. Preguntar por peticiones especiales
4. Verificar disponibilidad ANTES de confirmar

# ACTUALIZACIÓN DE NOTAS
Usar update_notes MÚLTIPLES VECES durante la llamada para cualquier info adicional.

# MANEJO DE CLIENTES MOLESTOS
- NUNCA quedarse en silencio
- Empatía primero: "Entiendo tu frustración"
- Ofrecer soluciones
- Mantener calma

# PERSONALIDAD
{Personality based on user input}

# TONO
- Respuestas claras y concisas (1-3 frases)
- Siempre responder, nunca silencio
```

### 3.7 Test Page (test.html)

Create an HTML page with:
- Business branding (name, colors)
- Instructions for the user (what they can say)
- ElevenLabs widget embedded
- Link to Google Sheets
- Status indicators

```html
<elevenlabs-convai agent-id="{AGENT_ID}"></elevenlabs-convai>
<script src="https://elevenlabs.io/convai-widget/index.js" async></script>
```

---

## PHASE 4: CONFIGURATION FILES

### 4.1 Requirements (requirements.txt)

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
httpx>=0.25.0
python-dotenv>=1.0.0
google-api-python-client>=2.100.0
google-auth>=2.23.0
pydantic>=2.5.0
```

### 4.2 Dockerfile (Multi-stage for Cloud Run)

```dockerfile
FROM python:3.11-slim AS base
WORKDIR /app
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim AS runner
WORKDIR /app
RUN useradd -m -u 1001 appuser
COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=base /usr/local/bin /usr/local/bin
COPY --chown=appuser:appuser app ./app
USER appuser
ENV PORT=8080
EXPOSE 8080
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 4.3 .env.example

```bash
# ElevenLabs
ELEVENLABS_API_KEY=your_api_key
ELEVENLABS_AGENT_ID=your_agent_id

# Webhook URL (ngrok for dev, production URL for deploy)
WEBHOOK_BASE_URL=https://your-url.ngrok-free.app

# Google Service Account (JSON string)
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}

# Google Sheets
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
GOOGLE_SHEETS_{PRIMARY_SHEET}_SHEET={PrimarySheetName}
GOOGLE_SHEETS_{SECONDARY_SHEET}_SHEET={SecondarySheetName}
```

### 4.4 .gitignore

```
.env
.env.local
*credentials*.json
*service-account*.json
__pycache__/
*.py[cod]
.DS_Store
venv/
*.log
```

---

## PHASE 5: DOCUMENTATION

### 5.1 CLAUDE.md

Generate comprehensive documentation including:
- Project overview and architecture diagram
- Common commands (dev, test, deploy)
- Environment variables reference
- Google Sheets structure (with actual column names)
- ElevenLabs tools configuration
- Agent behavior rules
- API endpoints reference
- Reservation/booking logic
- Testing flow
- Current status checklist

### 5.2 README.md

Generate a clean README with:
- Project description
- Architecture diagram
- Features list
- Installation steps
- Configuration guide
- Development commands
- API endpoints table
- Deployment guide

---

## PHASE 6: POST-CREATION

After generating all files:

1. **Ask if user wants to run setup_sheets.py** to configure Google Sheets
2. **Ask if user wants to run configure_elevenlabs.py** to setup agent tools
3. **Ask if user wants to start the service** locally for testing
4. **Remind about ngrok** for webhook testing
5. **Show the widget embed code** for their website

---

## BUSINESS TYPE TEMPLATES

### Restaurant
- Resources: Tables (capacity, location)
- Bookings: Reservations (date, time, party_size, 2hr duration)
- Special question: "¿Tienen restricciones alimenticias o alergias?"
- Notes: dietary restrictions, celebrations, seating preferences

### Clinic / Doctor
- Resources: Doctors (specialty, availability)
- Bookings: Appointments (date, time, 30min-1hr duration)
- Special question: "¿Es su primera consulta? ¿Tiene algún síntoma que quiera comentar?"
- Notes: symptoms, medical history, insurance info

### Hotel
- Resources: Rooms (type, capacity, amenities, price)
- Bookings: Reservations (check_in, check_out, guests)
- Special question: "¿Necesita algún servicio adicional? ¿Estacionamiento, desayuno?"
- Notes: late check-in, extra bed, special occasion

### Barbershop / Salon
- Resources: Services (name, duration, price, barber)
- Bookings: Appointments (date, time, service, barber preference)
- Special question: "¿Tiene preferencia de estilista?"
- Notes: style preferences, product allergies

### Gym / Studio
- Resources: Classes (type, instructor, schedule, capacity)
- Bookings: Enrollments (class, date, time, member)
- Special question: "¿Tiene alguna lesión o limitación física?"
- Notes: fitness level, goals, injuries

### Auto Shop
- Resources: Services (type, estimated_time, price_range)
- Bookings: Appointments (date, time, vehicle_info, service)
- Special question: "¿Puede describir el problema o síntoma del vehículo?"
- Notes: vehicle details, symptoms, urgency

---

## KEY PRINCIPLES

1. **Security First**: NEVER commit .env or credentials to git
2. **Accumulative Notes**: Notes always APPEND, never replace
3. **Phone Flexibility**: Accept any format, normalize internally (min 7 digits)
4. **No Internal IDs**: Agent never mentions reservation/booking codes to customer
5. **Conflict Prevention**: Always check availability before booking
6. **Mock Data**: Always provide mock mode for offline development
7. **Empathetic Agent**: Handle frustrated customers with empathy, never silence
8. **Always Respond**: Agent must NEVER go silent, always say something
