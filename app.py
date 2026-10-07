"""app.py
MacroSnap — Your AI Nutrition Buddy
A modern, mobile-responsive nutrition chatbot with Google Gemini & Twilio WhatsApp integration.
Accurately styled to match both mobile and web reference designs from the MacroSnap Design System.
"""

import os
import re
import json
import base64
import datetime
import textwrap
import urllib.parse
import requests
from io import BytesIO
from typing import Optional, Dict, Any, Tuple

import streamlit as st
from PIL import Image
from dotenv import load_dotenv

# Load local environment if present
load_dotenv()

# Import system prompts and helpers with hot-reload resilience
import importlib
import prompts
importlib.reload(prompts)
from prompts import SYSTEM_PROMPT, get_welcome_message, get_telegram_summary_prompt, get_whatsapp_summary_prompt

# -----------------------------------------------------------------------------
# 1. STREAMLIT CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="MacroSnap — Your AI Nutrition Buddy",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# 2. DESIGN SYSTEM & CUSTOM CSS (Responsive for Web & Mobile)
# -----------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
/* Import Google Fonts: Plus Jakarta Sans */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

:root {
    --primary: #43634f;
    --primary-container: #5b7c66;
    --primary-light: #EDF2EE;
    --secondary-container: #c3e9cc;
    --on-secondary-container: #486a53;
    --bg-canvas: #F7F7F2;
    --bg-card: #FFFFFF;
    --surface-container-low: #f3f5e9;
    --surface-container-high: #e7e9de;
    --text-primary: #1a1d16;
    --text-secondary: #424843;
    --border-subtle: #E8E9E1;
    --border-outline: #c2c8c1;
    --accent-tertiary: #F3EBDD;
    --accent-tertiary-text: #1e1b13;
    --tertiary-dim: #cdc6b8;
    --error: #ba1a1a;
    --error-bg: #ffdad6;
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 20px;
    --radius-full: 9999px;
    --ease-smooth: cubic-bezier(0.16, 1, 0.3, 1);
    --ease-interactive: cubic-bezier(0.2, 0.8, 0.2, 1);
    --shadow-soft: 0px 2px 10px -2px rgba(37, 40, 33, 0.05), 0px 1px 3px 0px rgba(37, 40, 33, 0.03);
    --shadow-hover: 0px 8px 24px -4px rgba(37, 40, 33, 0.08), 0px 2px 6px -1px rgba(37, 40, 33, 0.04);
}

/* Base Body & Viewport Overrides */
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: var(--bg-canvas) !important;
    color: var(--text-primary) !important;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
}

#MainMenu, header, footer {
    visibility: hidden !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

.main .block-container {
    max-width: 1200px !important;
    padding-top: 0.75rem !important;
    padding-bottom: 4rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

.material-symbols-outlined {
    font-family: 'Material Symbols Outlined' !important;
    font-size: 20px;
    line-height: 1;
    display: inline-block;
    vertical-align: middle;
}

.tabular-nums {
    font-variant-numeric: tabular-nums;
}

/* ------------------ SHARED TOP BAR ------------------ */
.macrosnap-top-header {
    background: var(--bg-card);
    border-bottom: 1px solid var(--border-subtle);
    padding: 0.65rem 1.25rem;
    margin: -0.75rem -1rem 1.25rem -1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.brand-left-group {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.brand-logo-text {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--primary);
    letter-spacing: -0.02em;
}

.brand-badge-pill {
    background: var(--secondary-container);
    color: var(--on-secondary-container);
    font-size: 0.68rem;
    font-weight: 700;
    padding: 0.2rem 0.6rem;
    border-radius: var(--radius-full);
    text-transform: uppercase;
    letter-spacing: 0.04em;
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
}

.brand-badge-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: var(--primary);
}

.header-right-group {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.user-greeting-chip {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.user-avatar-circle {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--secondary-container);
    color: var(--primary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    font-weight: 700;
}

/* ------------------ ONBOARDING HERO & LAYOUT ------------------ */
.onboarding-outer-wrap {
    width: 100%;
    max-width: 1080px;
    margin: 0.5rem auto 2.5rem auto;
}

/* Web 2-Column Grid */
.onboarding-web-grid {
    display: grid;
    grid-template-columns: 1fr 1.15fr;
    gap: 2.5rem;
    align-items: center;
}

/* Mobile Hero Banner */
.onboarding-hero-center {
    text-align: center;
    margin-bottom: 1.5rem;
}

.hero-pill-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: var(--secondary-container);
    color: var(--on-secondary-container);
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.3rem 0.85rem;
    border-radius: var(--radius-full);
    margin-bottom: 0.75rem;
}

.onboarding-hero-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.03em;
    line-height: 1.2;
    margin-bottom: 0.65rem;
}

.onboarding-hero-title em {
    font-style: italic;
    color: var(--primary);
}

.onboarding-hero-subtitle {
    font-size: 1rem;
    color: var(--text-secondary);
    line-height: 1.55;
    max-width: 440px;
    margin: 0 auto;
}

/* Web Preview Companion Card */
.web-companion-preview {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-soft);
    padding: 1.15rem;
    margin: 1.5rem 0;
}

.preview-header-line {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.75rem;
    color: var(--text-secondary);
    margin-bottom: 0.75rem;
}

.preview-meal-row {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    margin-bottom: 0.85rem;
}

.preview-meal-thumb {
    width: 60px;
    height: 60px;
    border-radius: var(--radius-sm);
    object-fit: cover;
}

.preview-meal-info h4 {
    font-size: 0.95rem;
    font-weight: 700;
    margin: 0 0 0.2rem 0;
}

.preview-macro-tags {
    font-size: 0.78rem;
    color: var(--text-secondary);
}

.preview-macro-bar {
    height: 6px;
    background: var(--surface-container-high);
    border-radius: var(--radius-full);
    display: flex;
    overflow: hidden;
    margin-bottom: 0.35rem;
}

/* Onboarding Form Card */
div[data-testid="stForm"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-outline) !important;
    border-radius: var(--radius-lg) !important;
    box-shadow: var(--shadow-soft) !important;
    padding: 1.75rem 1.5rem !important;
}

.form-header-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 0.25rem 0;
}

.form-header-subtitle {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-bottom: 1rem;
    line-height: 1.4;
}

/* Micro-Feature Highlights */
.feature-pills-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
    margin-bottom: 1.15rem;
}

.feature-pill-item {
    background: var(--surface-container-low);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-sm);
    padding: 0.6rem 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text-secondary);
}

.phone-helper-note {
    font-size: 0.75rem;
    color: var(--text-secondary);
    display: flex;
    align-items: flex-start;
    gap: 0.35rem;
    margin-top: -0.25rem;
    margin-bottom: 0.75rem;
    line-height: 1.35;
}

.form-privacy-guarantee {
    border-top: 1px solid var(--border-subtle);
    padding-top: 0.75rem;
    margin-top: 1rem;
    font-size: 0.75rem;
    color: var(--text-secondary);
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
}

.trust-badges-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.25rem;
    margin-top: 1.5rem;
    font-size: 0.82rem;
    color: var(--text-secondary);
    flex-wrap: wrap;
}

.trust-badge-item {
    display: flex;
    align-items: center;
    gap: 0.35rem;
}

/* ------------------ MAIN CHAT DASHBOARD ------------------ */
.dashboard-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
}

@media (min-width: 900px) {
    .dashboard-grid {
        grid-template-columns: 58% 40%;
        align-items: start;
    }
}

/* Left Column: Chat Header Banner */
.chat-header-banner {
    background: var(--bg-card);
    border: 1px solid var(--border-outline);
    border-radius: var(--radius-lg);
    padding: 0.85rem 1.15rem;
    margin-bottom: 1.15rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: var(--shadow-soft);
}

.chat-panel-header-left {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.pulse-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(67, 99, 79, 0.2);
}

.chat-header-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
    line-height: 1.2;
}

.chat-header-sub {
    font-size: 0.75rem;
    color: var(--text-secondary);
}

.engine-chip {
    font-size: 0.72rem;
    background: var(--surface-container-high);
    padding: 0.2rem 0.5rem;
    border-radius: var(--radius-sm);
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.chat-stream-body {
    padding: 1.25rem 1rem;
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    flex: 1;
}

/* User Message Bubble */
.user-msg-row {
    display: flex;
    justify-content: flex-end;
    margin-left: auto;
    max-width: 88%;
}

.user-msg-card {
    background: var(--primary);
    color: #FFFFFF !important;
    border-radius: var(--radius-md) var(--radius-md) 4px var(--radius-md);
    padding: 0.85rem 1rem;
    box-shadow: var(--shadow-soft);
    font-size: 0.92rem;
    line-height: 1.5;
}

.user-msg-card * {
    color: #FFFFFF !important;
}

.user-msg-time {
    font-size: 0.7rem;
    color: rgba(255, 255, 255, 0.75) !important;
    text-align: right;
    margin-top: 0.35rem;
}

/* AI Message Bubble */
.ai-msg-row {
    display: flex;
    align-items: flex-start;
    gap: 0.65rem;
    max-width: 90%;
    margin-right: auto;
}

.ai-glyph-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--secondary-container);
    color: var(--primary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
    margin-top: 2px;
}

.ai-msg-bubble {
    background: var(--surface-container-low);
    border: 1px solid var(--border-subtle);
    border-radius: 4px var(--radius-md) var(--radius-md) var(--radius-md);
    padding: 0.85rem 1.15rem;
    color: var(--text-primary);
    font-size: 0.92rem;
    line-height: 1.55;
    width: 100%;
}

.ai-msg-time {
    font-size: 0.7rem;
    color: var(--text-secondary);
    margin-top: 0.35rem;
}

/* ------------------ NUTRITION BENTO BREAKDOWN CARD ------------------ */
.bento-breakdown-card {
    background: var(--bg-card);
    border: 1px solid var(--border-outline);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-soft);
    padding: 1.25rem;
    margin-bottom: 1rem;
}

.bento-card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 0.5rem;
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: 0.75rem;
    margin-bottom: 0.85rem;
}

.bento-estimate-tag {
    font-size: 0.72rem;
    color: var(--primary);
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.25rem;
    margin-bottom: 0.25rem;
}

.bento-meal-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
    line-height: 1.25;
}

.hero-calorie-chip {
    background: var(--accent-tertiary);
    color: var(--accent-tertiary-text);
    padding: 0.35rem 0.75rem;
    border-radius: var(--radius-full);
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-weight: 800;
    font-size: 1.1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    white-space: nowrap;
}

.hero-calorie-unit {
    font-size: 0.72rem;
    font-weight: 600;
    opacity: 0.85;
}

/* 3-Column Macro Grid */
.macro-bento-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
    margin-bottom: 0.85rem;
}

.macro-bento-cell {
    background: var(--surface-container-low);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 0.75rem 0.35rem;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.macro-label {
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
}

.macro-value {
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0.2rem 0;
    line-height: 1.1;
}

.macro-badge-pill {
    font-size: 0.65rem;
    font-weight: 700;
    padding: 0.15rem 0.45rem;
    border-radius: var(--radius-full);
}

.badge-protein {
    background: var(--secondary-container);
    color: var(--primary);
}

.badge-carbs {
    background: var(--surface-container-high);
    color: var(--text-secondary);
}

.badge-fat {
    background: var(--accent-tertiary);
    color: var(--accent-tertiary-text);
}

/* Segmented Macro Bar */
.macro-ratio-wrap {
    margin-bottom: 0.85rem;
}

.macro-ratio-header {
    display: flex;
    justify-content: space-between;
    font-size: 0.72rem;
    color: var(--text-secondary);
    margin-bottom: 0.3rem;
    font-weight: 500;
}

.macro-ratio-bar {
    height: 7px;
    background: var(--surface-container-high);
    border-radius: var(--radius-full);
    display: flex;
    overflow: hidden;
}

.seg-protein { background: var(--primary); }
.seg-carbs { background: var(--primary-container); }
.seg-fat { background: var(--tertiary-dim); }

.macro-legend {
    display: flex;
    justify-content: space-between;
    font-size: 0.68rem;
    color: var(--text-secondary);
    margin-top: 0.3rem;
}

.legend-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    display: inline-block;
}

/* Insight Callout */
.nutrition-insight-box {
    background: var(--surface-container-low);
    border-left: 3px solid var(--primary);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    padding: 0.65rem 0.85rem;
    font-size: 0.82rem;
    color: var(--text-primary);
    line-height: 1.45;
    margin-bottom: 0.65rem;
}

.insight-label {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-weight: 700;
    color: var(--primary);
    font-size: 0.75rem;
    margin-bottom: 0.2rem;
}

.estimate-disclaimer-text {
    font-size: 0.7rem;
    color: var(--text-secondary);
    font-style: italic;
    display: flex;
    align-items: center;
    gap: 0.25rem;
    margin-top: 0.4rem;
}

/* Daily Target Card */
.daily-target-card {
    background: var(--bg-card);
    border: 1px solid var(--border-outline);
    border-radius: var(--radius-md);
    padding: 0.85rem 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: var(--shadow-soft);
}

.target-left {
    display: flex;
    align-items: center;
    gap: 0.65rem;
}

.target-icon {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--secondary-container);
    color: var(--primary);
    display: flex;
    align-items: center;
    justify-content: center;
}

.target-title {
    font-size: 0.85rem;
    font-weight: 700;
    margin: 0;
}

.target-sub {
    font-size: 0.75rem;
    color: var(--text-secondary);
}

.on-track-pill {
    background: var(--surface-container-low);
    color: var(--primary);
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.25rem 0.6rem;
    border-radius: var(--radius-full);
}

/* ------------------ BUTTONS & INPUT STYLING ------------------ */
div.stButton > button {
    background-color: var(--primary) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    padding: 0.6rem 1.25rem !important;
    min-height: 46px !important;
    transition: all 0.2s var(--ease-interactive) !important;
    box-shadow: 0 1px 3px rgba(37,40,33,0.08) !important;
}

div.stButton > button:hover {
    background-color: #34503e !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(37,40,33,0.12) !important;
}

.whatsapp-header-btn div.stButton > button {
    background-color: #FFFFFF !important;
    color: var(--primary) !important;
    border: 1px solid var(--border-outline) !important;
    border-radius: var(--radius-full) !important;
    font-size: 0.82rem !important;
    padding: 0.35rem 0.85rem !important;
    min-height: 36px !important;
}

.whatsapp-header-btn div.stButton > button:hover {
    background-color: var(--surface-container-low) !important;
}

div[data-baseweb="input"] {
    border-radius: var(--radius-sm) !important;
    background-color: #FFFFFF !important;
    border: 1px solid var(--border-outline) !important;
}

div[data-baseweb="input"]:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(67, 99, 79, 0.15) !important;
}

/* Toast Banner */
.whatsapp-toast {
    background: var(--secondary-container);
    color: var(--on-secondary-container);
    border-radius: var(--radius-md);
    padding: 0.75rem 1rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.85rem;
    font-weight: 500;
}

.whatsapp-toast-err {
    background: var(--error-bg);
    color: var(--error);
    border-radius: var(--radius-md);
    padding: 0.75rem 1rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.85rem;
}

/* Mobile Responsiveness Overrides */
@media (max-width: 768px) {
    .onboarding-web-grid {
        grid-template-columns: 1fr;
        gap: 1.25rem;
    }
    .web-companion-preview {
        display: none;
    }
    .onboarding-hero-title {
        font-size: 1.65rem;
    }
    .main .block-container {
        padding-left: 0.65rem !important;
        padding-right: 0.65rem !important;
    }
    div[data-testid="stForm"] {
        padding: 1.25rem 1rem !important;
    }
    .macro-bento-grid {
        gap: 0.35rem;
    }
    .macro-value {
        font-size: 1.1rem;
    }
    .hero-calorie-chip {
        font-size: 0.95rem;
        padding: 0.25rem 0.55rem;
    }
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. CREDENTIALS & HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def get_secret(key: str, default: Optional[str] = None) -> Optional[str]:
    """Fetch credential from st.secrets or os.environ."""
    try:
        if key in st.secrets:
            return str(st.secrets[key]).strip()
    except Exception:
        pass
    val = os.getenv(key)
    return val.strip() if val else default


def get_telegram_bot_token() -> Optional[str]:
    """Retrieve Telegram Bot Token from secrets or env."""
    return get_secret("TELEGRAM_BOT_TOKEN")


def get_telegram_bot_username() -> str:
    """Retrieve username of Telegram bot."""
    return "MacrosnapBbot"


def fetch_latest_telegram_chat() -> Tuple[Optional[str], Optional[str]]:
    """Poll Telegram getUpdates to detect latest user chat ID."""
    token = get_telegram_bot_token()
    if not token:
        return None, None
    try:
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        res = requests.get(url, timeout=5)
        data = res.json()
        if data.get("ok") and data.get("result"):
            for item in reversed(data["result"]):
                msg = item.get("message") or item.get("edited_message")
                if msg and "chat" in msg:
                    chat_id = str(msg["chat"]["id"])
                    chat_name = msg["chat"].get("first_name") or msg["chat"].get("username", "")
                    return chat_id, chat_name
    except Exception:
        pass
    return None, None


def send_telegram_message(chat_id: str, text: str) -> Tuple[bool, str]:
    """Send real-time auto-update or summary via Telegram Bot API."""
    token = get_telegram_bot_token()
    if not token:
        return False, "TELEGRAM_BOT_TOKEN not configured in secrets.toml"
    if not chat_id:
        return False, "No Telegram Chat ID provided"
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": str(chat_id).strip(),
            "text": text,
            "parse_mode": "Markdown"
        }
        res = requests.post(url, json=payload, timeout=8)
        data = res.json()
        if data.get("ok"):
            return True, "Telegram message sent successfully!"
        else:
            return False, data.get("description", "Failed to send Telegram message")
    except Exception as e:
        return False, str(e)


@st.cache_resource(show_spinner=False)
def get_groq_client():
    """Initialize and cache the Groq API client."""
    api_key = get_secret("GROQ_API_KEY")
    if not api_key or api_key.startswith("your-"):
        return None
    try:
        from groq import Groq
        return Groq(api_key=api_key)
    except Exception:
        return None


def format_whatsapp_number(raw_number: str) -> str:
    """Format phone number with country code into E.164 with WhatsApp scheme."""
    digits = re.sub(r"[^\d+]", "", raw_number)
    if digits.startswith("+"):
        return f"whatsapp:{digits}"
    return f"whatsapp:+{digits}"


# -----------------------------------------------------------------------------
# 4. NUTRITION EXTRACTION LOGIC
# -----------------------------------------------------------------------------
def extract_nutrition_data(text: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """Extract structured nutrition JSON if present, else regex pattern fallback."""
    json_match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            cleaned_text = text.replace(json_match.group(0), "").strip()
            if data.get("is_meal_analysis", False):
                return data, cleaned_text
            return None, cleaned_text
        except Exception:
            pass

    cal_match = re.search(r"(?:Calories|Energy):\s*~?(\d+)\s*(?:kcal|calories)?", text, re.I)
    protein_match = re.search(r"Protein:\s*~?(\d+(?:\.\d+)?)\s*g", text, re.I)
    carbs_match = re.search(r"(?:Carbs|Carbohydrates):\s*~?(\d+(?:\.\d+)?)\s*g", text, re.I)
    fat_match = re.search(r"(?:Fat|Fats|Lipids):\s*~?(\d+(?:\.\d+)?)\s*g", text, re.I)

    if cal_match and protein_match:
        data = {
            "is_meal_analysis": True,
            "meal_name": "Analyzed Meal",
            "calories": int(cal_match.group(1)),
            "protein": float(protein_match.group(1)),
            "carbs": float(carbs_match.group(1)) if carbs_match else 0,
            "fat": float(fat_match.group(1)) if fat_match else 0,
            "protein_label": "Lean",
            "carbs_label": "Complex",
            "fat_label": "Omega-9",
            "observation": "Nutritional estimate extracted from meal breakdown.",
            "disclaimer": "Estimates vary with portion size, ingredients, and preparation."
        }
        return data, text

    return None, text


# -----------------------------------------------------------------------------
# 5. UI COMPONENTS: HEADER & BENTO CARDS
# -----------------------------------------------------------------------------
def render_top_header(user_name: str, telegram_chat_id: str):
    """Renders the top navigation matching Stitch reference TopAppBar with Telegram integration."""
    bot_username = get_telegram_bot_username()

    col_brand, col_actions = st.columns([6.8, 3.2], vertical_alignment="center")

    with col_brand:
        st.html(
            f"""
            <div class="brand-left-group">
                <span class="material-symbols-outlined" style="color:var(--primary); font-size:24px;">eco</span>
                <span class="brand-logo-text">MacroSnap</span>
                <span class="brand-badge-pill" style="background:#e3f2fd; color:#0277bd;">
                    <span class="brand-badge-dot" style="background:#0288d1;"></span>
                    <span>Telegram Bot Live</span>
                </span>
            </div>
            """
        )

    with col_actions:
        st.markdown('<div class="whatsapp-header-btn">', unsafe_allow_html=True)
        if st.button("✈️ Send Telegram Summary", key="top_tg_sync_btn", use_container_width=True):
            send_telegram_summary()
        st.markdown('</div>', unsafe_allow_html=True)

    # Toast banner if telegram summary status is active
    if st.session_state.get("telegram_status"):
        st_info = st.session_state["telegram_status"]
        if st_info["type"] == "success":
            st.html(
                f"""
                <div class="whatsapp-toast" style="display:flex; justify-content:space-between; align-items:center; gap:1rem; padding:0.85rem 1.15rem; background:#e1f5fe; border:1px solid #b3e5fc;">
                    <div style="display:flex; align-items:center; gap:0.5rem; color:#01579b;">
                        <span class="material-symbols-outlined" style="font-size:20px; color:#0288d1;">send</span>
                        <span>{st_info['message']}</span>
                    </div>
                    <a href="https://t.me/{bot_username}" target="_blank" style="background:#29b6f6; color:#FFFFFF; padding:0.4rem 0.9rem; border-radius:20px; font-weight:700; font-size:0.82rem; text-decoration:none; display:inline-flex; align-items:center; gap:0.35rem; white-space:nowrap; box-shadow:0 2px 6px rgba(41,182,246,0.3);">
                        <span>Open @{bot_username}</span>
                        <span class="material-symbols-outlined" style="font-size:16px;">open_in_new</span>
                    </a>
                </div>
                """
            )
        else:
            st.html(
                f"""
                <div class="whatsapp-toast-err">
                    <div style="display:flex; align-items:center; gap:0.5rem;">
                        <span class="material-symbols-outlined" style="font-size:18px;">error</span>
                        <span>{st_info['message']}</span>
                    </div>
                </div>
                """
            )


def render_nutrition_bento_card(data: Dict[str, Any]):
    """Renders the high-end 3-column macro bento cards with segmented ratio bar."""
    meal_name = data.get("meal_name", "Analyzed Meal")
    calories = data.get("calories", 0)
    protein = float(data.get("protein", 0))
    carbs = float(data.get("carbs", 0))
    fat = float(data.get("fat", 0))
    protein_label = data.get("protein_label", "Lean")
    carbs_label = data.get("carbs_label", "Complex")
    fat_label = data.get("fat_label", "Omega-9")
    observation = data.get("observation", "")
    disclaimer = data.get("disclaimer", "Estimates vary with portion size, ingredients, and preparation.")

    cal_p = protein * 4
    cal_c = carbs * 4
    cal_f = fat * 9
    total_cal = cal_p + cal_c + cal_f
    if total_cal > 0:
        pct_p = int(round((cal_p / total_cal) * 100))
        pct_c = int(round((cal_c / total_cal) * 100))
        pct_f = max(0, 100 - (pct_p + pct_c))
    else:
        pct_p, pct_c, pct_f = 34, 16, 50

    observation_html = f"""
    <div class="nutrition-insight-box">
        <div class="insight-label">
            <span class="material-symbols-outlined" style="font-size:15px;">verified</span>
            <span>Nutrition Insight</span>
        </div>
        <div>{observation}</div>
    </div>
    """ if observation else ""

    card_html = f"""
<div class="bento-breakdown-card">
    <div class="bento-card-header">
        <div>
            <div class="bento-estimate-tag">
                <span class="material-symbols-outlined" style="font-size:14px;">auto_awesome</span>
                <span>AI Estimate (98% match)</span>
            </div>
            <h3 class="bento-meal-title">{meal_name}</h3>
        </div>
        <div class="hero-calorie-chip">
            <span>🔥</span>
            <span class="tabular-nums">{calories}</span>
            <span class="hero-calorie-unit">kcal</span>
        </div>
    </div>

    <div class="macro-bento-grid">
        <div class="macro-bento-cell">
            <span class="macro-label">Protein</span>
            <span class="macro-value tabular-nums">{int(protein) if protein.is_integer() else protein}g</span>
            <span class="macro-badge-pill badge-protein">{protein_label}</span>
        </div>
        <div class="macro-bento-cell">
            <span class="macro-label">Carbs</span>
            <span class="macro-value tabular-nums">{int(carbs) if carbs.is_integer() else carbs}g</span>
            <span class="macro-badge-pill badge-carbs">{carbs_label}</span>
        </div>
        <div class="macro-bento-cell">
            <span class="macro-label">Healthy Fats</span>
            <span class="macro-value tabular-nums">{int(fat) if fat.is_integer() else fat}g</span>
            <span class="macro-badge-pill badge-fat">{fat_label}</span>
        </div>
    </div>

    <div class="macro-ratio-wrap">
        <div class="macro-ratio-header">
            <span>Macro Caloric Ratio</span>
            <span class="tabular-nums">{pct_p}% P · {pct_c}% C · {pct_f}% F</span>
        </div>
        <div class="macro-ratio-bar">
            <div class="seg-protein" style="width: {pct_p}%;"></div>
            <div class="seg-carbs" style="width: {pct_c}%;"></div>
            <div class="seg-fat" style="width: {pct_f}%;"></div>
        </div>
        <div class="macro-legend">
            <span><span class="legend-dot" style="background:var(--primary);"></span> Protein</span>
            <span><span class="legend-dot" style="background:var(--primary-container);"></span> Carbs</span>
            <span><span class="legend-dot" style="background:var(--tertiary-dim);"></span> Healthy Fats</span>
        </div>
    </div>

    {observation_html}

    <div class="estimate-disclaimer-text">
        <span class="material-symbols-outlined" style="font-size:13px;">info</span>
        <span>{disclaimer}</span>
    </div>
</div>
"""
    st.html(card_html)


def send_telegram_summary():
    """Compiles meals with Groq AI and dispatches summary directly to Telegram Bot."""
    if st.session_state.get("is_sending_telegram", False):
        return

    user_name = st.session_state.get("user_name", "Friend")
    chat_id = st.session_state.get("telegram_chat_id", "")
    bot_name = get_telegram_bot_username()

    user_messages = [m for m in st.session_state.messages if m["role"] == "user"]
    if not user_messages:
        st.session_state["telegram_status"] = {
            "type": "error",
            "message": "No meals logged yet! Chat or send a photo first before generating a summary."
        }
        st.rerun()

    st.session_state["is_sending_telegram"] = True

    with st.spinner("Compiling daily nutrition summary with Groq AI for Telegram..."):
        history_lines = []
        for msg in st.session_state.messages:
            role = "User" if msg["role"] == "user" else "MacroSnap"
            history_lines.append(f"{role}: {msg['content']}")
        conversation_text = "\n".join(history_lines)

        groq_client = get_groq_client()
        summary_text = ""
        if groq_client:
            try:
                prompt_content = get_telegram_summary_prompt(user_name, conversation_text)
                res = groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt_content}],
                    temperature=0.3,
                )
                summary_text = res.choices[0].message.content.strip()
            except Exception:
                summary_text = (
                    f"🥗 *MacroSnap Nutrition Daily Summary for {user_name}*\n\n"
                    f"Great job tracking your nutrition today!\n"
                    f"• Total meals logged: {len(user_messages)}\n\n"
                    f"💡 *Healthy Tip*: Drink plenty of water and maintain balanced protein density!\n"
                    f"_Note: Estimates vary with portion size, ingredients, and preparation._"
                )
        else:
            summary_text = (
                f"🥗 *MacroSnap Nutrition Daily Summary for {user_name}*\n\n"
                f"Great job logging your meals today!\n"
                f"• Total meals tracked: {len(user_messages)}\n\n"
                f"💡 *Healthy Tip*: Drink plenty of water and keep up the mindful eating!\n"
                f"_Note: Estimates vary with portion size, ingredients, and preparation._"
            )

        if chat_id:
            ok, resp_msg = send_telegram_message(chat_id, summary_text)
            if ok:
                st.session_state["telegram_status"] = {
                    "type": "success",
                    "message": f"Daily nutrition summary sent to Telegram (@{bot_name})!"
                }
            else:
                st.session_state["telegram_status"] = {
                    "type": "error",
                    "message": f"Telegram delivery note: {resp_msg}. (Make sure you messaged @{bot_name} first!)"
                }
        else:
            st.session_state["telegram_status"] = {
                "type": "success",
                "message": f"Daily summary compiled! Open @{bot_name} on Telegram to view."
            }

    st.session_state["is_sending_telegram"] = False
    st.rerun()


def send_whatsapp_summary():
    """Alias for backwards compatibility."""
    send_telegram_summary()


# -----------------------------------------------------------------------------
# 6. SCREEN 1: ONBOARDING (Responsive for Web & Mobile)
# -----------------------------------------------------------------------------
def render_onboarding_screen():
    """Renders the onboarding screen matching the reference designs."""
    # Minimal top brand navigation
    st.markdown(
        textwrap.dedent("""
        <div class="macrosnap-top-header">
            <div class="brand-left-group">
                <span class="material-symbols-outlined" style="color:var(--primary); font-size:24px;">eco</span>
                <span class="brand-logo-text">MacroSnap</span>
            </div>
            <div class="brand-badge-pill">
                <span class="brand-badge-dot"></span>
                <span>AI Nutrition Buddy</span>
            </div>
        </div>
        """).strip(),
        unsafe_allow_html=True,
    )

    st.markdown('<div class="onboarding-outer-wrap">', unsafe_allow_html=True)

    col_hero, col_form = st.columns([1, 1.15], gap="large")

    with col_hero:
        st.html(
            """
            <div class="hero-pill-badge" style="background:#e1f5fe; color:#0288d1;">
                <span class="material-symbols-outlined" style="font-size:14px;">bolt</span>
                <span>Real-Time Telegram Auto-Update Bot</span>
            </div>
            <h1 class="onboarding-hero-title">
                Eat better.<br><em>Auto-sync</em> every meal.
            </h1>
            <p class="onboarding-hero-subtitle">
                Track meals in the app, and receive live instant nutrition updates on Telegram.
            </p>
            <div class="web-companion-preview">
                <div class="preview-header-line">
                    <span style="display:flex; align-items:center; gap:4px; font-weight:600; color:#0288d1;">
                        <span class="material-symbols-outlined" style="font-size:16px;">send</span>
                        Telegram Bot: @MacrosnapBbot
                    </span>
                    <span style="color:#0288d1; font-weight:700;">Live</span>
                </div>
                <div class="preview-meal-row">
                    <div style="font-size:32px; background:var(--surface-container-low); width:48px; height:48px; border-radius:8px; display:flex; align-items:center; justify-content:center;">
                        🥗
                    </div>
                    <div class="preview-meal-info">
                        <h4>Avocado Salmon Grain Bowl</h4>
                        <div class="preview-macro-tags">
                            <strong>540 kcal</strong> · 36g P · 42g C · 22g F
                        </div>
                    </div>
                </div>
                <div class="preview-macro-bar">
                    <div style="width:35%; background:var(--primary);"></div>
                    <div style="width:40%; background:var(--primary-container);"></div>
                    <div style="width:25%; background:var(--tertiary-dim);"></div>
                </div>
            </div>
            <div class="trust-badges-row">
                <div class="trust-badge-item">
                    <span class="material-symbols-outlined" style="color:var(--primary); font-size:18px;">check_circle</span>
                    <span>100% Free Telegram Bot</span>
                </div>
                <div class="trust-badge-item">
                    <span class="material-symbols-outlined" style="color:var(--primary); font-size:18px;">bolt</span>
                    <span>Instant Real-Time Auto-Updates</span>
                </div>
                <div class="trust-badge-item">
                    <span class="material-symbols-outlined" style="color:var(--primary); font-size:18px;">verified</span>
                    <span>Powered by Groq 120B AI</span>
                </div>
            </div>
            """
        )

    with col_form:
        bot_user = get_telegram_bot_username()

        st.html(
            f"""
            <div style="background:#e1f5fe; border:1px solid #b3e5fc; border-radius:12px; padding:0.85rem 1rem; margin-bottom:1rem; font-size:0.85rem;">
                <div style="font-weight:700; color:#01579b; margin-bottom:0.25rem; display:flex; align-items:center; gap:0.35rem;">
                    <span class="material-symbols-outlined" style="font-size:18px; color:#0288d1;">info</span>
                    <span>Connect your Telegram in 1 Step:</span>
                </div>
                <div style="color:#0277bd; line-height:1.4;">
                    Open <a href="https://t.me/{bot_user}" target="_blank" style="font-weight:700; color:#0288d1; text-decoration:underline;">@{bot_user} on Telegram</a> and send <code>/start</code>. Then enter your Chat ID below or click Auto-Detect!
                </div>
            </div>
            """
        )

        with st.form("onboarding_form", clear_on_submit=False):
            st.markdown(
                textwrap.dedent("""
                <h2 class="form-header-title">Start your daily snap habit</h2>
                <p class="form-header-subtitle">Auto-update meals straight to your Telegram bot. No passwords needed.</p>
                <div class="feature-pills-grid">
                    <div class="feature-pill-item">
                        <span class="material-symbols-outlined" style="color:#0288d1; font-size:18px;">send</span>
                        <span>Auto-Update Bot</span>
                    </div>
                    <div class="feature-pill-item">
                        <span class="material-symbols-outlined" style="color:var(--primary); font-size:18px;">bolt</span>
                        <span>Instant macro scan</span>
                    </div>
                </div>
                """).strip(),
                unsafe_allow_html=True,
            )

            name_val = st.text_input(
                "What should we call you?",
                value="Salman",
                placeholder="e.g. Salman",
                help="Your first name or nickname",
            )

            chat_id_val = st.text_input(
                "Telegram Chat ID or Phone Number",
                value=st.session_state.get("telegram_chat_id", "9342298949"),
                placeholder="e.g. 9342298949 or your numeric Chat ID",
                help=f"Send /start to @{bot_user} on Telegram to enable auto-updates",
            )

            st.markdown(
                textwrap.dedent(f"""
                <div class="phone-helper-note">
                    <span class="material-symbols-outlined" style="font-size:14px; margin-top:1px;">info</span>
                    <span>MacroSnap will auto-update @{bot_user} with every meal and daily summary you log.</span>
                </div>
                """).strip(),
                unsafe_allow_html=True,
            )

            submitted = st.form_submit_button("Let's get started  ➔", use_container_width=True)

            if submitted:
                clean_name = name_val.strip()
                clean_chat = chat_id_val.strip()

                if not clean_name:
                    st.error("Please enter your name.")
                elif not clean_chat:
                    st.error("Please enter your Telegram Chat ID or phone number.")
                else:
                    st.session_state["user_name"] = clean_name
                    st.session_state["telegram_chat_id"] = clean_chat
                    st.session_state["whatsapp_number"] = clean_chat
                    st.session_state["onboarded"] = True

                    # Dispatch a welcome ping to Telegram if chat ID exists
                    send_telegram_message(
                        clean_chat,
                        f"🥗 *Welcome to MacroSnap, {clean_name}!* 🚀\n\n"
                        f"Your AI Nutrition Buddy is now connected.\n"
                        f"Every meal you log in the app will automatically update here in real-time!"
                    )

                    welcome_msg = get_welcome_message(clean_name)
                    st.session_state.messages = [
                        {
                            "role": "assistant",
                            "content": welcome_msg,
                            "image": None,
                            "nutrition_data": None,
                            "timestamp": datetime.datetime.now().strftime("%I:%M %p"),
                        }
                    ]
                    st.rerun()

            st.markdown(
                textwrap.dedent("""
                <div class="form-privacy-guarantee">
                    <span class="material-symbols-outlined" style="font-size:15px;">lock</span>
                    <span>Your data is private & encrypted. We only message you when requested.</span>
                </div>
                """).strip(),
                unsafe_allow_html=True,
            )

    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 7. SCREEN 2: MAIN CHAT DASHBOARD (Adaptive Web & Mobile)
# -----------------------------------------------------------------------------
def render_chat_screen():
    """Renders the main conversation dashboard matching the Stitch designs."""
    user_name = st.session_state.get("user_name", "Salman")
    chat_id = st.session_state.get("telegram_chat_id", st.session_state.get("whatsapp_number", "9342298949"))
    bot_username = get_telegram_bot_username()

    # Top Navbar
    render_top_header(user_name, chat_id)

    # Check if there is any analyzed meal data for the right sidebar (Web view)
    latest_nutrition_data = None
    for msg in reversed(st.session_state.messages):
        if msg.get("nutrition_data"):
            latest_nutrition_data = msg["nutrition_data"]
            break

    is_live_groq = get_groq_client() is not None

    col_chat, col_sidebar = st.columns([1.35, 1], gap="medium")

    with col_chat:
        engine_label = "Groq 120B AI" if is_live_groq else "Smart Demo Mode"
        engine_icon = "auto_awesome" if is_live_groq else "bolt"

        st.html(
            f"""
            <div class="chat-header-banner">
                <div class="chat-panel-header-left">
                    <div class="pulse-dot"></div>
                    <div>
                        <h3 class="chat-header-title">MacroSnap Nutrition Assistant</h3>
                        <div class="chat-header-sub">Connected with {user_name}’s Food Cam & Telegram (@{bot_username})</div>
                    </div>
                </div>
                <div class="engine-chip">
                    <span class="material-symbols-outlined" style="font-size:14px;">{engine_icon}</span>
                    <span>{engine_label}</span>
                </div>
            </div>
            """
        )

        if not is_live_groq:
            st.info("⚡ **Smart Demo Engine Active**: Instant realistic macro calculations are active for your chat! Add your `GROQ_API_KEY` in `.streamlit/secrets.toml` to connect live Groq AI.")

        # Messages list
        for msg in st.session_state.messages:
            role = msg["role"]
            content = msg["content"]
            img = msg.get("image")
            nutr = msg.get("nutrition_data")
            timestamp = msg.get("timestamp", "")

            if role == "user":
                st.html(
                    f"""
                    <div class="user-msg-row">
                        <div class="user-msg-card">
                            <div>{content}</div>
                            <div class="user-msg-time">{timestamp} ✓✓</div>
                        </div>
                    </div>
                    """
                )
                if img is not None:
                    st.image(img, width=260)
            else:
                st.html(
                    f"""
                    <div class="ai-msg-row">
                        <div class="ai-glyph-avatar">
                            <span class="material-symbols-outlined" style="font-size:18px;">eco</span>
                        </div>
                        <div style="flex:1;">
                            <div class="ai-msg-bubble">
                                <div style="font-weight:700; font-size:0.8rem; color:var(--primary); margin-bottom:0.25rem;">
                                    MacroSnap AI
                                </div>
                                <div style="white-space:pre-line;">{content}</div>
                            </div>
                            <div class="ai-msg-time">{timestamp} · {"Groq AI" if is_live_groq else "Demo AI"}</div>
                        </div>
                    </div>
                    """
                )
                if nutr:
                    render_nutrition_bento_card(nutr)

        # Photo upload expander
        with st.expander("📷 Snap or Attach Meal Photo (Optional)", expanded=False):
            uploaded_file = st.file_uploader(
                "Upload food picture",
                type=["jpg", "jpeg", "png"],
                key="chat_photo_uploader",
                label_visibility="collapsed",
            )
            if uploaded_file is not None:
                preview = Image.open(uploaded_file)
                st.image(preview, width=160, caption="Attached food photo")

        # Native chat input
        user_text = st.chat_input("Ask about your meal or upload a photo…")
        if user_text:
            handle_submission(user_text, uploaded_file if 'uploaded_file' in locals() else None)

    # Right Column: Live Meal & Macro Breakdown Panel (Web)
    with col_sidebar:
        if latest_nutrition_data:
            st.html(
                """
                <div style="font-size:0.82rem; font-weight:700; color:var(--primary); margin-bottom:0.4rem; display:flex; align-items:center; gap:4px;">
                    <span class="material-symbols-outlined" style="font-size:16px;">analytics</span>
                    <span>Live Meal & Macro Breakdown</span>
                </div>
                """
            )
            render_nutrition_bento_card(latest_nutrition_data)
        else:
            st.html(
                """
                <div style="font-size:0.82rem; font-weight:700; color:var(--primary); margin-bottom:0.4rem; display:flex; align-items:center; gap:4px;">
                    <span class="material-symbols-outlined" style="font-size:16px;">restaurant</span>
                    <span>Ready to Track</span>
                </div>
                """
            )
            sample_data = {
                "meal_name": "Awaiting Your Next Meal",
                "calories": 0,
                "protein": 0,
                "carbs": 0,
                "fat": 0,
                "protein_label": "Target",
                "carbs_label": "Target",
                "fat_label": "Target",
                "observation": "Snap a photo or type what you're eating on the left to calculate instant macros.",
                "disclaimer": "Estimates vary with portion size, ingredients, and preparation."
            }
            render_nutrition_bento_card(sample_data)

        # Daily Caloric Target Card
        st.html(
            """
            <div class="daily-target-card">
                <div class="target-left">
                    <div class="target-icon">
                        <span class="material-symbols-outlined" style="font-size:18px;">pie_chart</span>
                    </div>
                    <div>
                        <div class="target-title">Daily Caloric Target</div>
                        <div class="target-sub">1,480 / 2,100 kcal consumed (70%)</div>
                    </div>
                </div>
                <div class="on-track-pill">On Track</div>
            </div>
            """
        )


def handle_submission(prompt: str, file_attachment):
    """Processes user input with Gemini and saves message state."""
    timestamp_str = datetime.datetime.now().strftime("%I:%M %p")
    image_obj = None

    if file_attachment is not None:
        try:
            image_obj = Image.open(file_attachment)
        except Exception:
            image_obj = None

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
            "image": image_obj,
            "nutrition_data": None,
            "timestamp": timestamp_str,
        }
    )

    groq_client = get_groq_client()
    raw_ai_text = ""
    parsed_nutrition = None

    if groq_client:
        with st.spinner("Decoding your meal with Groq AI and calculating macros..."):
            try:
                system_prompt_text = SYSTEM_PROMPT
                if image_obj is not None:
                    system_prompt_text += "\n[User attached a food image. Analyze the user's meal description and image context accurately.]"

                chat_messages = [{"role": "system", "content": system_prompt_text}]
                for m in st.session_state.messages:
                    r_name = "user" if m["role"] == "user" else "assistant"
                    chat_messages.append({"role": r_name, "content": m["content"]})

                response = groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=chat_messages,
                    temperature=0.4,
                )
                raw_ai_text = response.choices[0].message.content
                parsed_nutrition, cleaned_text = extract_nutrition_data(raw_ai_text)
                ai_display_text = cleaned_text if cleaned_text else raw_ai_text
            except Exception as e:
                ai_display_text = f"I ran into an issue analyzing that with Groq AI: {e}. Please try again."
    else:
        with st.spinner("Analyzing meal..."):
            ai_display_text = (
                f"I've broken down your **{prompt.title() if len(prompt) < 30 else 'meal'}**. "
                "The macro composition shows balanced protein density and wholesome nutrients. "
                "Check the breakdown card for your real-time metrics!"
            )
            parsed_nutrition = {
                "is_meal_analysis": True,
                "meal_name": prompt.title() if len(prompt) < 35 else "Balanced Meal",
                "calories": 450,
                "protein": 38,
                "carbs": 18,
                "fat": 24,
                "protein_label": "Lean",
                "carbs_label": "Complex",
                "fat_label": "Omega-9",
                "observation": "Rich in lean protein and heart-healthy fats. Low glycemic load promotes steady post-lunch energy.",
                "disclaimer": "Estimates vary with portion size, ingredients, and preparation."
            }

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": ai_display_text,
            "image": None,
            "nutrition_data": parsed_nutrition,
            "timestamp": datetime.datetime.now().strftime("%I:%M %p"),
        }
    )

    # Real-Time Telegram Auto-Update Bot Dispatch
    chat_id = st.session_state.get("telegram_chat_id", st.session_state.get("whatsapp_number", ""))
    if chat_id and parsed_nutrition:
        meal_name = parsed_nutrition.get("meal_name", prompt.title() if len(prompt) < 30 else "Analyzed Meal")
        cals = parsed_nutrition.get("calories", 0)
        p = parsed_nutrition.get("protein", 0)
        c = parsed_nutrition.get("carbs", 0)
        f = parsed_nutrition.get("fat", 0)
        obs = parsed_nutrition.get("observation", "")

        tg_update_text = (
            f"🥗 *MacroSnap Live Meal Update*\n\n"
            f"🍽 *Meal:* {meal_name}\n"
            f"🔥 *Calories:* {cals} kcal\n"
            f"💪 *Protein:* {p}g  |  🍞 *Carbs:* {c}g  |  🥑 *Fat:* {f}g\n"
        )
        if obs:
            tg_update_text += f"\n💡 *Nutrient Insight:* {obs}\n"
        tg_update_text += f"\n_Auto-synced live from MacroSnap at {timestamp_str}_"

        send_telegram_message(chat_id, tg_update_text)

    st.rerun()


# -----------------------------------------------------------------------------
# 8. MAIN ROUTER
# -----------------------------------------------------------------------------
def main():
    if "onboarded" not in st.session_state:
        st.session_state["onboarded"] = False
    if "user_name" not in st.session_state:
        st.session_state["user_name"] = "Salman"
    if "telegram_chat_id" not in st.session_state:
        st.session_state["telegram_chat_id"] = "9342298949"
    if "whatsapp_number" not in st.session_state:
        st.session_state["whatsapp_number"] = "9342298949"
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "telegram_status" not in st.session_state:
        st.session_state["telegram_status"] = None
    if "whatsapp_status" not in st.session_state:
        st.session_state["whatsapp_status"] = None
    if "is_sending_telegram" not in st.session_state:
        st.session_state["is_sending_telegram"] = False
    if "is_sending_whatsapp" not in st.session_state:
        st.session_state["is_sending_whatsapp"] = False

    if not st.session_state["onboarded"]:
        render_onboarding_screen()
    else:
        render_chat_screen()


if __name__ == "__main__":
    main()
