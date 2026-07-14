# 🤖 Multi-Agent Scheduling Assistant

An AI-powered Multi-Agent Scheduling Assistant built using **LangGraph**, **FastAPI**, and **Mistral AI**. The assistant intelligently routes user requests, manages appointment bookings, validates inputs, persists conversation state, and sends booking confirmations through a webhook.

## 🚀 Live Demo

**API:** https://scheduling-assistant-agent-1.onrender.com

**Swagger Documentation:** https://scheduling-assistant-agent-1.onrender.com/docs

---

# ✨ Features

- 🤖 Multi-Agent architecture using LangGraph
- 🧠 Intelligent intent routing (Triage Agent)
- 📅 Booking Specialist Agent
- 📆 Relative date normalization
  - "Book tomorrow"
  - "Book next Monday"
- ✅ Appointment slot validation
- 💾 SQLite-based conversation persistence
- 📩 Mock email/WhatsApp notifications using Webhook.site
- 🌐 FastAPI REST API
- 📖 Interactive Swagger documentation
- 📊 Professional logging with Loguru
- ☁️ Deployed on Render

---

# 🏗️ Architecture

```text
                 User
                  │
                  ▼
            FastAPI (/chat)
                  │
                  ▼
          LangGraph Workflow
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
   Triage Agent      General Response
        │
        ▼
 Booking Specialist
        │
        ├──────────────┐
        │              │
        ▼              ▼
 Check Availability  Reserve Slot
        │              │
        └──────┬───────┘
               ▼
     Send Webhook Notification
               │
               ▼
           SQLite Memory
```

---

# 🧠 Multi-Agent Workflow

## 1️⃣ Triage Agent

Responsibilities:

- Understand user intent
- Detect booking requests
- Route general questions
- Transfer control to Booking Specialist

Example:

```
User:
Book tomorrow
```

↓

Routes to Booking Agent

---

## 2️⃣ Booking Specialist

Responsibilities:

- Extract booking details
- Normalize dates
- Check availability
- Reserve slots
- Validate email
- Send confirmation

Example Conversation

```
User:
Book tomorrow

↓

Assistant:
Available slots:
09:00
10:00
11:00

↓

User:
11:00

↓

Assistant:
Please provide your email.

↓

User:
john@gmail.com

↓

Appointment Confirmed 🎉
```

---

# 🛠️ Tech Stack

## Backend

- FastAPI
- LangGraph
- LangChain
- Mistral AI

## Database

- SQLite

## AI

- Mistral Large

## Notifications

- Webhook.site

## Logging

- Loguru

## Deployment

- Render

---

# 📂 Project Structure

```text
app/
│
├── agents/
│   ├── booking.py
│   └── triage.py
│
├── api/
│   └── routes.py
│
├── database/
│
├── graph/
│   ├── workflow.py
│   ├── router.py
│   ├── session_router.py
│   └── state.py
│
├── schemas/
│
├── services/
│
├── tools/
│   ├── availability.py
│   ├── reservation.py
│   └── notification.py
│
├── utils/
│   ├── date_parser.py
│   └── logger.py
│
├── config.py
└── main.py
```

---

# ⚙️ Environment Variables

Create a `.env` file.

```env
MISTRAL_API_KEY=your_api_key

WEBHOOK_URL=https://webhook.site/your-webhook-url

DATABASE_URL=sqlite:///appointments.db

CHECKPOINT_DB=memory.db
```

---

# 📦 Installation

Clone the repository

```bash
git clone https://github.com/UkatoSpeaks/Scheduling-Assistant-Agent.git
```

Go inside

```bash
cd Scheduling-Assistant-Agent
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the server

```bash
uvicorn app.main:app --reload
```

---

# 📡 API Endpoints

## Health

```
GET /health
```

Response

```json
{
  "status": "healthy",
  "service": "Multi-Agent Scheduling Assistant",
  "database": "connected",
  "llm": "available"
}
```

---

## Chat

```
POST /chat
```

Example Request

```json
{
  "thread_id": "user123",
  "message": "Book tomorrow"
}
```

Response

```json
{
  "response": "Available slots on 2026-07-16..."
}
```

---

# 💾 Persistent Memory

Conversation state is stored using:

- SQLite
- LangGraph Checkpointer

This allows the assistant to remember previous booking information across multiple requests using the same `thread_id`.

---

# 🔔 Notification Flow

After successful booking:

- Appointment saved
- Webhook triggered
- Confirmation returned

Example Payload

```json
{
  "email": "john@gmail.com",
  "date": "2026-07-16",
  "time": "11:00",
  "status": "confirmed"
}
```

---

# 🧪 Example Conversation

```
User:
Book tomorrow

Assistant:
Available slots...

User:
11:00

Assistant:
Please provide your email.

User:
john@gmail.com

Assistant:
🎉 Appointment booked successfully!
```

---

# 🌍 Deployment

Hosted on Render

API

https://scheduling-assistant-agent-1.onrender.com

Swagger

https://scheduling-assistant-agent-1.onrender.com/docs

---

# 🎥 Demo

A complete walkthrough of the project demonstrating:

- Multi-Agent workflow
- Booking process
- Persistent memory
- Webhook notification
- Swagger API

---

# 🚀 Future Improvements

- Google Calendar integration
- Outlook Calendar support
- Gmail notifications
- Twilio WhatsApp integration
- OAuth authentication
- PostgreSQL
- Docker support
- Redis memory
- Streaming responses

---

# 👨‍💻 Author

**Anurag Chaudhary**

GitHub:
https://github.com/UkatoSpeaks
