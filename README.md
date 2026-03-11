# ⚡ FireReach — Autonomous Outreach Engine

> **Groq Llama 3.3 · DuckDuckGo · SMTP · Streamlit**  
> A fully autonomous B2B cold outreach agent that harvests live signals, synthesizes account briefs, and dispatches hyper-personalized emails — end-to-end, zero templates.

---

## Overview

FireReach is a multi-tool AI agent pipeline built for GTM (Go-To-Market) teams. Given a target company and recipient, it:

1. **Harvests live signals** — funding rounds, hiring trends, leadership changes, tech stack shifts, product launches
2. **Synthesizes an account brief** — 2-paragraph analysis of pain points and strategic alignment with your ICP
3. **Generates & sends a cold email** — signal-grounded, zero-template, dispatched via SMTP

---

## Architecture

```
User Input (ICP + Target)
        │
        ▼
┌──────────────────┐
│ Signal Harvester │  ← DuckDuckGo (live web search, no API key)
└────────┬─────────┘
         │ raw signals (funding, hiring, leadership, techstack, social)
         ▼
┌──────────────────┐
│ Research Analyst │  ← Groq Llama 3.3-70B
└────────┬─────────┘
         │ account brief (pain points + ICP alignment)
         ▼
┌──────────────────────┐
│ Outreach Auto-Sender │  ← Groq (email gen) + SMTP (dispatch)
└──────────────────────┘
```

The agent is orchestrated via **Groq's tool-calling API** — the LLM decides when to call each tool and in what order, with a hard-coded execution constraint enforced via the system prompt.

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq — `llama-3.3-70b-versatile` (free tier) |
| Web Search | `ddgs` (DuckDuckGo, no API key required) |
| Email Dispatch | Python `smtplib` + Gmail SMTP |
| UI | Streamlit |
| Env Config | `python-dotenv` |

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Aryaajaiswal/OutReach-FireReach.git
cd OutReach-FireReach
```

### 2. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
# LLM — free key at https://console.groq.com
GROQ_API_KEY=your_groq_api_key

# Email (Gmail App Password — NOT your real password)
# Google Account → Security → 2FA → App Passwords → Generate
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=you@gmail.com
SMTP_PASS=xxxx xxxx xxxx xxxx
FROM_EMAIL=you@gmail.com
```

> **Note:** If `SMTP_USER` / `SMTP_PASS` are not set, the agent will still generate the email — it just won't dispatch it.

### 5. Run

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501).

---

## Usage

1. Fill in the **sidebar** (Control Panel):
   - **ICP Parameters** — what you sell and to whom
   - **Target Entity** — company name to research
   - **Key Contact** — recipient name
   - **Sink Address** — recipient email
   - **Operator ID** — your name and company
2. Click **INITIATE SEQUENCE**
3. Watch the pipeline execute live — signals → brief → email

---

## Pipeline Details

### Tool 1 — Signal Harvester
- Runs up to 4 DuckDuckGo searches per target (funding, hiring, leadership, techstack)
- Uses `backend='lite'` to avoid rate limits
- Returns a structured `summary` list and `raw_signals` dict

### Tool 2 — Research Analyst
- Groq LLM call with the live signals + ICP
- Outputs a 2-paragraph account brief (max 120 words)
- Para 1: growth stage + pain points; Para 2: ICP strategic fit

### Tool 3 — Outreach Auto-Sender
- Groq LLM generates a signal-grounded cold email (subject + body)
- Zero-template policy: must name-drop at least one real signal
- Dispatches via SMTP if configured; otherwise returns generated text

---

## Project Structure

```
Firereach2/
├── app.py              # Main Streamlit app (agent + UI)
├── requirements.txt    # Python dependencies
├── .env                # Secrets (not committed)
├── .gitignore
└── document.md         # This file
```

---

## Requirements

```
streamlit
groq
ddgs
python-dotenv
```
##Output
<img width="1920" height="1344" alt="image" src="https://github.com/user-attachments/assets/fee37bff-6f6a-4a3d-be85-5052b28444f2" />

---

## Notes

- **No paid APIs required** — Groq free tier + DuckDuckGo
- **Email is optional** — without SMTP config the email is generated and displayed, but not sent
- The agent enforces strict tool execution order via the system prompt to prevent hallucinated signals
