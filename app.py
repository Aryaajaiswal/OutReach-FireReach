import streamlit as st
from groq import Groq
from ddgs import DDGS
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FireReach — Autonomous Outreach Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

/* Main Theme Colors */
:root {
    --bg-dark: #050505;
    --bg-panel: #0a0a0f;
    --neon-blue: #00f3ff;
    --neon-purple: #bc13fe;
    --neon-pink: #ff007f;
    --neon-green: #00ff66;
    --text-main: #e0e5ff;
    --text-muted: #8a94b5;
    --border-color: rgba(0, 243, 255, 0.2);
}

/* Global Typography & Background */
html, body, [class*="css"] { 
    font-family: 'Rajdhani', sans-serif; 
    background-color: var(--bg-dark) !important;
    color: var(--text-main) !important;
}

/* App Background */
.stApp { 
    background: radial-gradient(circle at 50% 0%, #150030 0%, var(--bg-dark) 50%, var(--bg-dark) 100%) !important;
}

/* Sidebar Customization */
[data-testid="stSidebar"] { 
    background: rgba(10, 10, 15, 0.8) !important; 
    backdrop-filter: blur(10px);
    border-right: 1px solid var(--border-color) !important; 
    box-shadow: 2px 0 15px rgba(0, 243, 255, 0.05);
}
[data-testid="stSidebar"] label { 
    color: var(--neon-blue) !important; 
    font-family: 'Orbitron', sans-serif !important;
    font-size: 13px !important; 
    font-weight: 700 !important; 
    text-transform: uppercase; 
    letter-spacing: 1.5px; 
    text-shadow: 0 0 5px rgba(0, 243, 255, 0.5);
}

/* Headers & Highlights */
h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: var(--text-main) !important;
    text-shadow: 0 0 10px rgba(188, 19, 254, 0.5);
}

/* Input Fields (Text & Textarea) */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(0, 0, 0, 0.5) !important; 
    border: 1px solid var(--border-color) !important;
    border-radius: 4px !important; 
    color: var(--neon-blue) !important; 
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    padding: 10px 15px !important;
    box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.8);
    transition: all 0.3s ease;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus { 
    border-color: var(--neon-purple) !important; 
    box-shadow: 0 0 15px rgba(188, 19, 254, 0.4), inset 0 0 10px rgba(0, 0, 0, 0.8) !important; 
    color: #fff !important;
}
/* Placeholder text color */
::placeholder {
    color: rgba(138, 148, 181, 0.5) !important;
}

/* Button Customization - Cyberpunk Style */
.stButton > button {
    background: transparent !important; 
    color: var(--neon-blue) !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important; 
    font-size: 16px !important; 
    text-transform: uppercase;
    letter-spacing: 2px;
    border: 1px solid var(--neon-blue) !important;
    border-radius: 2px !important; 
    padding: 14px 28px !important; 
    width: 100% !important;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    box-shadow: 0 0 10px rgba(0, 243, 255, 0.2), inset 0 0 10px rgba(0, 243, 255, 0.1);
}
.stButton > button:hover { 
    background: rgba(0, 243, 255, 0.1) !important;
    box-shadow: 0 0 20px rgba(0, 243, 255, 0.6), inset 0 0 20px rgba(0, 243, 255, 0.3) !important;
    color: #fff !important;
    border-color: #fff !important;
}
/* Button specific for the Launch button to make it pop */
[data-testid="stSidebar"] .stButton > button {
    border-color: var(--neon-purple) !important;
    color: var(--neon-purple) !important;
    box-shadow: 0 0 10px rgba(188, 19, 254, 0.2), inset 0 0 10px rgba(188, 19, 254, 0.1);
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(188, 19, 254, 0.1) !important;
    box-shadow: 0 0 20px rgba(188, 19, 254, 0.6), inset 0 0 20px rgba(188, 19, 254, 0.3) !important;
}


/* Expander (Tool Calls) */
.streamlit-expanderHeader { 
    background: rgba(10, 10, 15, 0.9) !important; 
    border: 1px solid var(--border-color) !important; 
    border-radius: 4px !important; 
    color: var(--text-main) !important; 
    font-family: 'Orbitron', sans-serif !important;
    transition: all 0.2s;
}
.streamlit-expanderHeader:hover {
    border-color: var(--neon-blue) !important;
    color: var(--neon-blue) !important;
}

/* Hide Streamlit default UI elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; }

/* Custom Scrollbar for a futuristic feel */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: var(--bg-dark); 
}
::-webkit-scrollbar-thumb {
    background: rgba(0, 243, 255, 0.3); 
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 243, 255, 0.8); 
}

/* Selected text highlighting */
::selection {
    background: var(--neon-purple);
    color: #fff;
}
</style>
""", unsafe_allow_html=True)


# ── Groq Client ───────────────────────────────────────────────────────────────
@st.cache_resource
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        st.error("⚠️ GROQ_API_KEY not set. Get a free key at console.groq.com then add to .env")
        st.stop()
    return Groq(api_key=api_key)

client = get_groq_client()
MODEL  = "llama-3.3-70b-versatile"   # Best free Groq model for tool calling


# ── Tool Schemas (OpenAI-compatible format for Groq) ─────────────────────────
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "tool_signal_harvester",
            "description": (
                "Fetches LIVE buyer signals for a target company using Serper web search. "
                "Returns deterministic data on funding, hiring, leadership changes, tech stack, social mentions. "
                "Must NOT guess — only returns signals actually found on the web."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {"type": "string", "description": "Exact target company name"},
                    "signal_types": {
                        "type": "array", "items": {"type": "string"},
                        "description": "Signal categories: funding, hiring, leadership, techstack, social"
                    }
                },
                "required": ["company_name", "signal_types"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_research_analyst",
            "description": (
                "Takes harvested signals + seller ICP and generates a 2-paragraph Account Brief "
                "highlighting specific pain points and strategic alignment."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name":    {"type": "string"},
                    "signals":         {"type": "object", "description": "Raw output from tool_signal_harvester"},
                    "icp_description": {"type": "string", "description": "Seller's Ideal Customer Profile"}
                },
                "required": ["company_name", "signals", "icp_description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_outreach_automated_sender",
            "description": (
                "Generates a hyper-personalized cold email grounded in signals and account brief, "
                "then dispatches it via SMTP. Zero-template policy: must cite real signals explicitly."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient_email":  {"type": "string"},
                    "recipient_name":   {"type": "string"},
                    "company_name":     {"type": "string"},
                    "account_brief":    {"type": "string"},
                    "signals":          {"type": "object"},
                    "icp_description":  {"type": "string"},
                    "sender_name":      {"type": "string"},
                    "sender_company":   {"type": "string"}
                },
                "required": ["recipient_email", "recipient_name", "company_name",
                             "account_brief", "signals", "icp_description"]
            }
        }
    }
]

SYSTEM_PROMPT = """You are FireReach, an autonomous B2B outreach agent built for GTM teams.
Your persona: a sharp, data-driven SDR who never sends generic emails.

STRICT EXECUTION ORDER — always call tools in this exact sequence:
  1. tool_signal_harvester   → fetch live signals first
  2. tool_research_analyst   → analyse signals against ICP
  3. tool_outreach_automated_sender → generate + send the email

HARD CONSTRAINTS:
- Never guess or fabricate signals. Use ONLY data returned by tool_signal_harvester.
- The outreach email MUST name-drop at least one specific signal (funding amount, job title hired, product launched, etc.)
- Do not ask for clarification. Execute autonomously end-to-end.
- After the sender tool returns, write a 2-sentence summary of what was done.

Signal types to always harvest: ["funding", "hiring", "leadership", "techstack", "social"]"""


# ── Tool 1: Signal Harvester (DuckDuckGo — no API key needed) ────────────────
def tool_signal_harvester(company_name: str, signal_types: list) -> dict:
    """Search the web via DuckDuckGo (free, no key) for live company signals."""
    query_map = {
        "funding":    f"{company_name} funding round raised 2024 2025",
        "hiring":     f"{company_name} hiring jobs engineer 2025",
        "leadership": f"{company_name} new CTO CEO VP appointed 2024 2025",
        "techstack":  f"{company_name} infrastructure migration cloud AWS Azure",
        "social":     f"{company_name} product launch announcement 2025",
    }

    signals = {
        "company":     company_name,
        "fetched_at":  datetime.utcnow().isoformat(),
        "summary":     [],
        "raw_signals": {}
    }

    with DDGS() as ddgs:
        for stype in signal_types[:4]:   # cap at 4 searches
            query = query_map.get(stype)
            if not query:
                continue
            try:
                results = list(ddgs.text(query, max_results=3, backend='lite'))
                if results:
                    top     = results[0]
                    finding = f"{top.get('title', '')}: {top.get('body', '')[:180]}"
                    signals["summary"].append(finding)
                    signals["raw_signals"][stype] = {
                        "signal_type": stype,
                        "finding":     finding,
                        "source":      top.get("href", ""),
                        "confidence":  "high"
                    }
            except Exception as e:
                signals["raw_signals"][stype] = {"error": str(e)}

    if not signals["summary"]:
        signals["summary"] = [
            f"{company_name} is an active technology company. "
            "No specific live signals found — check your internet connection."
        ]

    return signals


# ── Tool 2: Research Analyst (Groq LLM synthesis) ────────────────────────────
def tool_research_analyst(company_name: str, signals: dict, icp_description: str) -> dict:
    signal_text = "\n".join(signals.get("summary", ["No signals found."]))
    resp = client.chat.completions.create(
        model=MODEL, max_tokens=500,
        messages=[
            {"role": "system", "content": "You are a sharp B2B account researcher. Be specific and concise."},
            {"role": "user",   "content": (
                f"Company: {company_name}\n"
                f"Live Signals:\n{signal_text}\n\n"
                f"Seller ICP: {icp_description}\n\n"
                f"Write a 2-paragraph Account Brief (max 120 words).\n"
                f"Para 1: Current growth stage + specific pain points implied by the signals.\n"
                f"Para 2: Strategic alignment — why the seller's ICP fits RIGHT NOW.\n"
                f"Be specific. Reference actual signals. No buzzwords."
            )}
        ]
    )
    return {
        "company":       company_name,
        "account_brief": resp.choices[0].message.content.strip(),
        "signals_used":  signals.get("summary", [])
    }


# ── Tool 3: Outreach Sender (Groq email gen + SMTP dispatch) ─────────────────
def tool_outreach_sender(
    recipient_email: str, recipient_name: str, company_name: str,
    account_brief: str, signals: dict, icp_description: str,
    sender_name: str = "Alex Rivera", sender_company: str = "SecureScale"
) -> dict:
    signal_text = "\n".join(signals.get("summary", []))
    resp = client.chat.completions.create(
        model=MODEL, max_tokens=600,
        messages=[
            {"role": "system", "content": "You write cold emails that feel human and get replies. No buzzwords. No templates."},
            {"role": "user",   "content": (
                f"Write a cold outreach email. ZERO-TEMPLATE POLICY — must reference real signals.\n\n"
                f"Sender: {sender_name} at {sender_company}\n"
                f"Recipient: {recipient_name} at {company_name}\n"
                f"Seller ICP: {icp_description}\n\n"
                f"Live Signals:\n{signal_text}\n\n"
                f"Account Brief:\n{account_brief}\n\n"
                f"Rules:\n"
                f"- Subject: punchy, signal-specific, max 8 words\n"
                f"- Body: 4-5 sentences, conversational tone\n"
                f"- Name-drop at least one specific signal (raise amount, role hired, product launched)\n"
                f"- Single soft CTA: 15-min call\n"
                f"- Output format exactly:\nSUBJECT: <subject line>\n\nBODY:\n<email body>"
            )}
        ]
    )
    raw = resp.choices[0].message.content.strip()

    subject = f"Quick note for {company_name}"
    body    = raw
    if "SUBJECT:" in raw:
        parts   = raw.split("BODY:", 1)
        subject = parts[0].replace("SUBJECT:", "").strip()
        body    = parts[1].strip() if len(parts) > 1 else raw

    # SMTP dispatch
    smtp_host  = os.getenv("SMTP_HOST",  "smtp.gmail.com")
    smtp_port  = int(os.getenv("SMTP_PORT", "587"))
    smtp_user  = os.getenv("SMTP_USER",  "")
    smtp_pass  = os.getenv("SMTP_PASS",  "")
    from_email = os.getenv("FROM_EMAIL", smtp_user)

    sent, error_msg = False, None
    if smtp_user and smtp_pass:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"]    = f"{sender_name} <{from_email}>"
            msg["To"]      = recipient_email
            msg.attach(MIMEText(body, "plain"))
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(from_email, recipient_email, msg.as_string())
            sent = True
        except Exception as e:
            error_msg = str(e)
    else:
        error_msg = "SMTP not configured — email generated but not sent. Add SMTP_USER + SMTP_PASS to .env"

    return {
        "status":             "sent" if sent else "generated_only",
        "recipient":          recipient_email,
        "subject":            subject,
        "body":               body,
        "error":              error_msg,
        "signals_referenced": signals.get("summary", [])
    }


# ── Tool Router ───────────────────────────────────────────────────────────────
def execute_tool(name: str, args: dict) -> dict:
    if name == "tool_signal_harvester":
        return tool_signal_harvester(**args)
    elif name == "tool_research_analyst":
        return tool_research_analyst(**args)
    elif name == "tool_outreach_automated_sender":
        return tool_outreach_sender(**args)
    return {"error": f"Unknown tool: {name}"}


def _parse_args(raw: str) -> dict:
    """Parse tool arguments, handling the Groq/Llama quirk of wrapping in a list."""
    parsed = json.loads(raw)
    if isinstance(parsed, list):
        parsed = parsed[0] if parsed else {}
    return parsed


# ── Agent Loop (generator → live Streamlit updates) ──────────────────────────
def run_agent(icp, company, recipient_email, recipient_name, sender_name, sender_company):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": (
            f"ICP: {icp}\n"
            f"Target company: {company}\n"
            f"Recipient: {recipient_name} <{recipient_email}>\n"
            f"Sender: {sender_name} at {sender_company}\n\n"
            f"Execute the full outreach pipeline now."
        )}
    ]

    for _ in range(10):   # safety cap on iterations
        try:
            response = client.chat.completions.create(
                model=MODEL, max_tokens=2000,
                tools=TOOLS, tool_choice="auto",
                messages=messages
            )
        except Exception as e:
            yield {"type": "final", "text": f"⚠ Groq API error: {e}"}
            return

        msg    = response.choices[0].message
        reason = response.choices[0].finish_reason

        if msg.content:
            yield {"type": "thinking", "text": msg.content}

        if reason == "stop":
            yield {"type": "final", "text": msg.content or "Pipeline complete."}
            return

        if reason == "tool_calls" and msg.tool_calls:
            messages.append({
                "role": "assistant",
                "content": msg.content,
                "tool_calls": msg.tool_calls
            })

            for tc in msg.tool_calls:
                try:
                    args = _parse_args(tc.function.arguments)
                except Exception as e:
                    yield {"type": "final", "text": f"⚠ Failed to parse tool arguments: {e}"}
                    return

                yield {"type": "tool_call", "tool_name": tc.function.name, "inputs": args}

                try:
                    result = execute_tool(tc.function.name, args)
                except Exception as e:
                    result = {"error": str(e)}

                yield {"type": "tool_result", "tool_name": tc.function.name, "result": result}

                # Trim the signals payload before sending back to the LLM
                # to prevent the model from re-sending the full nested object
                # (which triggers Groq's tool_use_failed on the next step)
                trimmed = result.copy() if isinstance(result, dict) else result
                if tc.function.name == "tool_signal_harvester" and isinstance(trimmed, dict):
                    trimmed = {
                        "company":    trimmed.get("company", ""),
                        "fetched_at": trimmed.get("fetched_at", ""),
                        "summary":    trimmed.get("summary", []),
                    }

                messages.append({
                    "role":         "tool",
                    "tool_call_id": tc.id,
                    "content":      json.dumps(trimmed)
                })



# ── UI: Step Renderers ────────────────────────────────────────────────────────
TOOL_META = {
    "tool_signal_harvester":          {"label": "Signal Harvester", "color": "#ff6b35", "emoji": "📡"},
    "tool_research_analyst":          {"label": "Research Analyst", "color": "#7c3aed", "emoji": "🧠"},
    "tool_outreach_automated_sender": {"label": "Outreach Sender",  "color": "#059669", "emoji": "📤"},
}

def render_step(step: dict):
    t = step["type"]

    if t == "thinking":
        st.markdown(f"""
        <div style="padding:8px 14px;border-left:2px solid #374151;margin-bottom:6px;opacity:0.6">
        <span style="font-size:12px;color:#9ca3af;font-family:monospace">
        ◆ {step['text'][:220]}{'…' if len(step['text'])>220 else ''}
        </span></div>""", unsafe_allow_html=True)

    elif t == "tool_call":
        meta = TOOL_META.get(step["tool_name"], {"label": step["tool_name"], "emoji": "🔧"})
        with st.expander(f"{meta['emoji']} **TOOL CALL** — {meta['label']}", expanded=False):
            st.json(step["inputs"])

    elif t == "tool_result":
        result = step["result"]

        if step["tool_name"] == "tool_signal_harvester":
            bullets = "".join(
                f'<div style="background:rgba(0,0,0,0.6);border:1px solid var(--border-color);border-left:3px solid var(--neon-blue);border-radius:4px;'
                f'padding:8px 12px;margin-bottom:6px;font-size:14px;color:var(--text-main);box-shadow:inset 0 0 10px rgba(0,243,255,0.05)">'
                f'<span style="color:var(--neon-blue);margin-right:8px">❖</span> {s}</div>'
                for s in result.get("summary", [])
            )
            st.markdown(f"""
            <div style="background:rgba(5,5,5,0.8);border:1px solid var(--neon-blue);border-radius:6px;padding:16px;margin-bottom:10px;box-shadow:0 0 15px rgba(0,243,255,0.1), inset 0 0 20px rgba(0,0,0,0.8);position:relative;overflow:hidden">
                <div style="position:absolute;top:0;left:0;width:100%;height:2px;background:linear-gradient(90deg, transparent, var(--neon-blue), transparent)"></div>
                <div style="font-family:'Orbitron', sans-serif;font-size:12px;color:var(--neon-blue);font-weight:700;text-transform:uppercase;letter-spacing:2px;margin-bottom:12px;text-shadow:0 0 8px rgba(0,243,255,0.5)">
                    <span style="font-size:14px;margin-right:6px">📡</span> SYSTEM OVERRIDE: SIGNALS ACQUIRED — {result.get('company','')}
                </div>
                {bullets}
                <div style="font-family:'Rajdhani', sans-serif;font-size:11px;color:var(--text-muted);margin-top:10px;text-align:right">TIMESTAMP: {result.get('fetched_at','')}</div>
            </div>""", unsafe_allow_html=True)

        elif step["tool_name"] == "tool_research_analyst":
            st.markdown(f"""
            <div style="background:rgba(5,5,5,0.8);border:1px solid var(--neon-purple);border-radius:6px;padding:16px;margin-bottom:10px;box-shadow:0 0 15px rgba(188,19,254,0.1), inset 0 0 20px rgba(0,0,0,0.8);position:relative;overflow:hidden">
                <div style="position:absolute;top:0;left:0;width:100%;height:2px;background:linear-gradient(90deg, transparent, var(--neon-purple), transparent)"></div>
                <div style="font-family:'Orbitron', sans-serif;font-size:12px;color:var(--neon-purple);font-weight:700;text-transform:uppercase;letter-spacing:2px;margin-bottom:12px;text-shadow:0 0 8px rgba(188,19,254,0.5)">
                    <span style="font-size:14px;margin-right:6px">🧠</span> NEURAL SYNTHESIS: ACCOUNT BRIEF
                </div>
                <div style="font-family:'Rajdhani', sans-serif;font-size:15px;color:var(--text-main);line-height:1.6;white-space:pre-wrap">{result.get('account_brief','')}</div>
            </div>""", unsafe_allow_html=True)

        elif step["tool_name"] == "tool_outreach_automated_sender":
            status  = result.get("status", "")
            badge   = (
                '<span style="background:rgba(0,255,102,0.1);border:1px solid var(--neon-green);color:var(--neon-green);'
                'border-radius:2px;padding:3px 10px;font-family:\'Orbitron\', sans-serif;font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;text-shadow:0 0 5px rgba(0,255,102,0.5)">[ TRANSMITTED ]</span>'
                if status == "sent" else
                '<span style="background:rgba(255,0,127,0.1);border:1px solid var(--neon-pink);color:var(--neon-pink);'
                'border-radius:2px;padding:3px 10px;font-family:\'Orbitron\', sans-serif;font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;text-shadow:0 0 5px rgba(255,0,127,0.5)">[ SIMULATED - NO SMTP ]</span>'
            )
            err_html = (
                f'<div style="margin-top:12px;font-family:\'Rajdhani\', sans-serif;font-size:14px;color:var(--neon-pink);background:rgba(255,0,127,0.05);'
                f'border-left:3px solid var(--neon-pink);padding:10px 14px">⚠ ERROR SEQUENCE: {result["error"]}</div>'
                if result.get("error") else ""
            )
            st.markdown(f"""
            <div style="background:rgba(5,5,5,0.8);border:1px solid var(--neon-green);border-radius:6px;padding:16px;margin-bottom:10px;box-shadow:0 0 15px rgba(0,255,102,0.15), inset 0 0 20px rgba(0,0,0,0.8);position:relative;overflow:hidden">
                <div style="position:absolute;top:0;left:0;width:100%;height:2px;background:linear-gradient(90deg, transparent, var(--neon-green), transparent)"></div>
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;border-bottom:1px solid rgba(0,255,102,0.2);padding-bottom:10px">
                    <span style="font-family:'Orbitron', sans-serif;font-size:12px;color:var(--neon-green);font-weight:700;text-transform:uppercase;letter-spacing:2px;text-shadow:0 0 8px rgba(0,255,102,0.5)">
                        <span style="font-size:14px;margin-right:6px">📤</span> OUTREACH DISPATCH LOG
                    </span>
                    {badge}
                </div>
                <div style="display:grid;grid-template-columns:1fr 2fr;gap:10px;margin-bottom:16px;font-family:'Rajdhani', sans-serif;font-size:15px">
                    <div style="color:var(--text-muted)">TARGET VECTOR:</div><div style="color:var(--text-main);font-weight:600">{result.get('recipient','')}</div>
                    <div style="color:var(--text-muted)">COMM PROTOCOL:</div><div style="color:var(--text-main);font-weight:600">{result.get('subject','')}</div>
                </div>
                <div style="font-family:'Orbitron', sans-serif;font-size:10px;color:var(--neon-green);text-transform:uppercase;letter-spacing:2px;margin-bottom:10px;opacity:0.8">DATA PAYLOAD:</div>
                <div style="background:rgba(0,0,0,0.6);border:1px solid rgba(0,255,102,0.3);border-radius:4px;padding:16px;font-family:'Rajdhani', sans-serif;font-size:15px;color:var(--text-main);line-height:1.6;white-space:pre-wrap;box-shadow:inset 0 0 10px rgba(0,0,0,0.8)">{result.get('body','')}</div>
                {err_html}
            </div>""", unsafe_allow_html=True)

    elif t == "final":
        st.markdown(f"""
        <div style="background:rgba(5,5,5,0.8);border:1px double var(--neon-blue);border-radius:4px;padding:20px;margin-top:20px;box-shadow:0 0 20px rgba(0,243,255,0.1), inset 0 0 20px rgba(0,0,0,0.8);text-align:center">
            <div style="font-family:'Orbitron', sans-serif;font-size:14px;color:var(--neon-blue);font-weight:700;text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;text-shadow:0 0 10px rgba(0,243,255,0.6)">✓ SEQUENCE TERMINATED</div>
            <div style="font-family:'Rajdhani', sans-serif;font-size:16px;color:var(--text-main);line-height:1.6">{step['text']}</div>
        </div>""", unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;justify-content:center;flex-direction:column;gap:10px;padding:10px 0 30px;border-bottom:1px solid var(--border-color);margin-bottom:30px;position:relative">
    <div style="position:absolute;bottom:0;left:10%;width:80%;height:1px;background:linear-gradient(90deg, transparent, var(--neon-blue), var(--neon-purple), transparent)"></div>
    <div style="font-family:'Orbitron', sans-serif;font-size:42px;font-weight:900;letter-spacing:6px;color:transparent;background:linear-gradient(45deg, var(--neon-blue), var(--neon-purple));-webkit-background-clip:text;text-shadow:0 0 20px rgba(0,243,255,0.3)">
        F1R3R3ACH
    </div>
    <div style="font-family:'Rajdhani', sans-serif;font-size:14px;color:var(--text-muted);letter-spacing:4px;text-transform:uppercase;font-weight:600">
        <span style="color:var(--neon-blue)">AUTONOMOUS NEURAL OUTREACH</span> /<span style="color:var(--neon-purple)">/ GROQ-70B </span> /<span style="color:var(--neon-green)">/ DEPLOYED </span>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h3 style='font-family:\"Orbitron\", sans-serif;color:var(--neon-blue);letter-spacing:2px;text-shadow:0 0 10px rgba(0,243,255,0.4)'><span style='margin-right:8px'>⚙️</span> SYSTEMS CONFIG</h3>", unsafe_allow_html=True)
    st.markdown("<div style='height:1px;background:linear-gradient(90deg,var(--neon-blue),transparent);margin-bottom:20px'></div>", unsafe_allow_html=True)

    icp = st.text_area(
        "ICP PARAMETERS",
        value="We sell high-end cybersecurity training to Series B startups.",
        height=90,
        help="Your Ideal Customer Profile — what you sell and to whom."
    )
    company         = st.text_input("TARGET ENTITY",   value="Stripe",      placeholder="e.g. Notion, Linear, Mistral")
    recipient_name  = st.text_input("KEY CONTACT",   value="Jordan Lee")
    recipient_email = st.text_input("SINK ADDRESS *", placeholder="target@company.com")

    st.markdown("<div style='height:1px;background:linear-gradient(90deg,var(--neon-purple),transparent);margin:20px 0'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-family:\"Orbitron\", sans-serif;font-size:12px;color:var(--neon-purple);letter-spacing:2px;margin-bottom:10px'>OPERATOR ID</div>", unsafe_allow_html=True)
    sender_name    = st.text_input("ALIAS",    value="Alex Rivera")
    sender_company = st.text_input("FACTION", value="SecureScale")

    st.markdown("<div style='height:1px;background:linear-gradient(90deg,var(--neon-green),transparent);margin:20px 0 10px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Rajdhani', sans-serif;font-size:13px;color:var(--text-muted);line-height:2;background:rgba(0,0,0,0.4);border:1px solid rgba(0,255,102,0.2);padding:15px;border-radius:4px">
        <b style="font-family:'Orbitron', sans-serif;color:var(--neon-green);font-size:11px;letter-spacing:1px;display:block;margin-bottom:8px">SEQUENCE PATH</b>
        <span style="color:var(--neon-blue)">[1]</span> SIGNAL HARVESTER <span style="color:var(--text-muted);font-size:11px">[CORE_SEARCH]</span><br>
        <span style="color:var(--neon-purple)">[2]</span> NEURAL SYNTHESIS <span style="color:var(--text-muted);font-size:11px">[LLM_GROQ]</span><br>
        <span style="color:var(--neon-green)">[3]</span> OUTREACH DISPATCH <span style="color:var(--text-muted);font-size:11px">[SMTP_LINK]</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("INITIATE SEQUENCE", use_container_width=True)


# ── Main Panel ────────────────────────────────────────────────────────────────
completed = st.session_state.get("completed_tools", set())
cols = st.columns(3)
for i, (tool, meta) in enumerate(TOOL_META.items()):
    done = tool in completed
    
    # Custom color logic for the widgets based on completion
    if done:
        border_color = f"var(--neon-{'blue' if i==0 else 'purple' if i==1 else 'green'})"
        box_shadow = f"0 0 15px rgba({0 if i!=1 else 188}, {243 if i==0 else 19 if i==1 else 255}, {255 if i==0 else 254 if i==1 else 102}, 0.2)"
        bg_color = "rgba(0,0,0,0.6)"
        text_color = border_color
    else:
        border_color = "rgba(255,255,255,0.1)"
        box_shadow = "none"
        bg_color = "rgba(0,0,0,0.3)"
        text_color = "var(--text-muted)"

    with cols[i]:
        top_bar     = f'<div style="position:absolute;top:0;left:0;width:100%;height:2px;background:{border_color}"></div>' if done else ""
        opacity     = "1" if done else "0.5"
        status_text = "[ ONLINE ]" if done else "[ STANDBY ]"
        widget_html = (
            f'<div style="background:{bg_color};border:1px solid {border_color};border-radius:4px;'
            f'padding:15px;text-align:center;box-shadow:{box_shadow};transition:all 0.3s ease;'
            f'position:relative;overflow:hidden">'
            f'{top_bar}'
            f'<div style="font-size:24px;margin-bottom:8px;opacity:{opacity}">{meta["emoji"]}</div>'
            f'<div style="font-family:Orbitron,sans-serif;font-size:11px;color:{text_color};'
            f'font-weight:700;letter-spacing:1px;text-transform:uppercase">{meta["label"]}</div>'
            f'<div style="font-family:Rajdhani,sans-serif;font-size:10px;color:{text_color};margin-top:5px;opacity:0.7">'
            f'{status_text}</div>'
            f'</div>'
        )
        st.markdown(widget_html, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

if "steps" not in st.session_state:
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
         min-height:350px;gap:20px;background:rgba(0,0,0,0.4);border:1px dashed var(--border-color);border-radius:8px">
        <div style="width:80px;height:80px;border-radius:50%;border:2px solid rgba(0,243,255,0.3);display:flex;align-items:center;justify-content:center;animation:pulse 2s infinite">
            <div style="font-size:32px;color:var(--neon-blue);text-shadow:0 0 15px rgba(0,243,255,0.8)">◈</div>
        </div>
        <div style="text-align:center">
            <div style="font-family:'Orbitron', sans-serif;font-size:18px;font-weight:700;color:var(--text-main);letter-spacing:3px;text-shadow:0 0 10px rgba(0,243,255,0.3)">SYSTEM IDLE</div>
            <div style="font-family:'Rajdhani', sans-serif;font-size:15px;color:var(--text-muted);margin-top:8px;letter-spacing:1px">AWAITING CONFIGURATION IN CONTROL PANEL</div>
        </div>
    </div>
    <style>@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(0,243,255,0.4); } 70% { box-shadow: 0 0 0 20px rgba(0,243,255,0); } 100% { box-shadow: 0 0 0 0 rgba(0,243,255,0); } }</style>
    """, unsafe_allow_html=True)

if run_btn:
    if not recipient_email:
        st.error("⚠️ Recipient email is required.")
    else:
        st.session_state["steps"] = []
        st.session_state["completed_tools"] = set()
        with st.container():
            for step in run_agent(icp, company, recipient_email, recipient_name, sender_name, sender_company):
                st.session_state["steps"].append(step)
                if step["type"] == "tool_result":
                    st.session_state.setdefault("completed_tools", set()).add(step["tool_name"])
                render_step(step)

elif "steps" in st.session_state and st.session_state["steps"]:
    for step in st.session_state["steps"]:
        render_step(step)
