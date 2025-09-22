# career_agent.py
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import gradio as gr

# =========================
# Setup & Constants
# =========================

load_dotenv(override=True)

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Optional Pushover (won’t crash if missing)
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_URL = "https://api.pushover.net/1/messages.json"

# Content files
PROFILE_PDF = Path("me/profile.pdf")
SUMMARY_TXT = Path("me/summary.txt")

# Persona
NAME = "Carlos Vallejo"


# =========================
# Utilities
# =========================

def push(message: str) -> None:
    """Send a Pushover notification if credentials exist; otherwise just print."""
    print(f"[Push] {message}")
    if not (PUSHOVER_USER and PUSHOVER_TOKEN):
        return  # Silently ignore if not configured
    try:
        payload = {"user": PUSHOVER_USER, "token": PUSHOVER_TOKEN, "message": message}
        requests.post(PUSHOVER_URL, data=payload, timeout=10)
    except requests.RequestException as e:
        print(f"[Push][WARN] Failed to send pushover: {e}")


def read_pdf_text(path: Path) -> str:
    """Extract text from a PDF, safely."""
    if not path.exists():
        print(f"[IO][WARN] PDF not found at: {path}")
        return ""
    text_all: List[str] = []
    try:
        reader = PdfReader(str(path))
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text_all.append(page_text)
    except Exception as e:
        print(f"[PDF][WARN] Could not read {path}: {e}")
    return "\n".join(text_all).strip()


def read_text_file(path: Path) -> str:
    """Read a UTF-8 text file, safely."""
    if not path.exists():
        print(f"[IO][WARN] Text file not found at: {path}")
        return ""
    try:
        return path.read_text(encoding="utf-8").strip()
    except Exception as e:
        print(f"[IO][WARN] Could not read {path}: {e}")
        return ""


# =========================
# Tool Implementations
# =========================

def record_user_details(email: str, name: str = "Name not provided", notes: str = "not provided") -> Dict[str, str]:
    """Record user’s contact details (demo: send a push & return ok)."""
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}


def record_unknown_question(question: str) -> Dict[str, str]:
    """Record a question the agent couldn’t answer (demo: send a push & return ok)."""
    push(f"Recording '{question}' asked that I couldn't answer")
    return {"recorded": "ok"}


# Dispatcher mapping for simpler tool routing (no big if/elif)
TOOL_DISPATCH = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question,
}

# JSON schemas the model can “see”
RECORD_USER_DETAILS_SCHEMA = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name, if they provided it"},
            "notes": {"type": "string", "description": "Extra context worth recording"},
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

RECORD_UNKNOWN_QUESTION_SCHEMA = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that couldn't be answered"},
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}

TOOLS = [
    {"type": "function", "function": RECORD_USER_DETAILS_SCHEMA},
    {"type": "function", "function": RECORD_UNKNOWN_QUESTION_SCHEMA},
]


# =========================
# LLM Client
# =========================

openai = OpenAI()


# =========================
# Prompt Assembly
# =========================

def build_system_prompt(name: str, summary: str, linkedin_text: str) -> str:
    prompt = (
        f"You are acting as {name}. You are answering questions on {name}'s website, "
        f"particularly questions related to {name}'s career, background, skills and experience. "
        f"Your responsibility is to represent {name} for interactions on the website as faithfully as possible. "
        f"You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. "
        f"Be professional and engaging, as if talking to a potential client or future employer who came across the website. "
        f"If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, "
        f"even if it's about something trivial or unrelated to career. "
        f"If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and name "
        f"and record it using your record_user_details tool. "
        f"Before calling the record_user_details tool, ask for the user's email address and name together."
        f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin_text}\n\n"
        f"With this context, please chat with the user, always staying in character as {name}."
    )
    return prompt


# =========================
# Tool Call Handling
# =========================

def handle_tool_calls(tool_calls: Any) -> List[Dict[str, Any]]:
    """
    Execute tool calls returned by the model and return tool messages
    that can be appended to the conversation.
    """
    results: List[Dict[str, Any]] = []
    for tc in tool_calls:
        tool_name = tc.function.name
        raw_args = tc.function.arguments or "{}"
        args = json.loads(raw_args)
        print(f"[Tool] {tool_name}({args})")

        func = TOOL_DISPATCH.get(tool_name)
        if not func:
            print(f"[Tool][WARN] No handler for tool '{tool_name}'")
            result: Dict[str, Any] = {"error": f"unknown tool {tool_name}"}
        else:
            try:
                result = func(**args)
            except TypeError as e:
                # Argument mismatch, surface helpful detail
                result = {"error": f"bad arguments for {tool_name}: {e}"}
            except Exception as e:
                result = {"error": f"tool {tool_name} failed: {e}"}

        results.append(
            {
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tc.id,
            }
        )
    return results


# =========================
# Chat Loop (for Gradio)
# =========================

def chat(message: str, history: List[Dict[str, str]]) -> str:
    """
    Gradio expects a function (message, history) -> reply string.
    We keep a simple tool loop until the model returns a normal message.
    """
    # Load dynamic content once per request (fast enough; can be lifted to module scope if static)
    linkedin_text = read_pdf_text(PROFILE_PDF)
    summary = read_text_file(SUMMARY_TXT)
    system_prompt = build_system_prompt(NAME, summary, linkedin_text)

    messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]
    # Gradio passes history as [{"role": "user"/"assistant", "content": "..."}]
    messages.extend(history)
    messages.append({"role": "user", "content": message})

    while True:
        response = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            tools=TOOLS,
        )
        choice = response.choices[0]
        finish_reason = choice.finish_reason

        if finish_reason == "tool_calls":
            # Let’s execute and append tool results; then continue the loop
            model_msg = choice.message
            tool_calls = model_msg.tool_calls or []
            results = handle_tool_calls(tool_calls)
            messages.append({"role": "assistant", "content": model_msg.content or "", "tool_calls": tool_calls})
            messages.extend(results)
            continue

        # Normal message
        return choice.message.content or ""
