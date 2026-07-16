"""Streamlit UI shell for an intergalactic AI chatbot.

Run with:
    streamlit run app.py
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from chatmodels.main import get_reply, new_conversation

# The greeting is used only when a conversation is first created.
INITIAL_MESSAGES = [
    {
        "role": "ai",
        "author": "Nova AI",
        "text": "Greetings, explorer. Your command deck is ready for a new mission.",
        "time": "09:40",
    },
    {
        "role": "user",
        "author": "You",
        "text": "Chart a clean interface for interstellar conversations.",
        "time": "09:41",
    },
    {
        "role": "ai",
        "author": "Nova AI",
        "text": "Interface telemetry is online: polished spacing, responsive panels, and cosmic clarity.",
        "time": "09:42",
    },
]

CHAT_HISTORY_PLACEHOLDERS = [
    "Orion Research Brief",
    "Terraforming Ideas",
    "Deep Space Debugging",
    "Nebula Travel Plan",
]


# Page configuration keeps the browser tab and layout production-ready.
st.set_page_config(
    page_title="Nova | Intergalactic AI Chat",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_global_styles() -> None:
    """Add app-wide CSS using Streamlit's markdown renderer."""
    st.markdown(
        """
        <style>
            :root {
                --bg-deep: #070A1A;
                --bg-panel: rgba(13, 18, 42, 0.82);
                --bg-panel-strong: rgba(17, 24, 53, 0.96);
                --border-soft: rgba(148, 163, 184, 0.20);
                --text-primary: #F8FAFC;
                --text-muted: #A7B0C7;
                --accent-cyan: #22D3EE;
                --accent-violet: #A78BFA;
                --accent-green: #5EEAD4;
                --user-bubble: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);
                --ai-bubble: linear-gradient(135deg, rgba(15, 23, 42, 0.98) 0%, rgba(49, 46, 129, 0.78) 100%);
            }

            html, body, [class*="css"] {
                font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }

            .stApp {
                background:
                    radial-gradient(circle at 15% 10%, rgba(34, 211, 238, 0.18), transparent 28%),
                    radial-gradient(circle at 85% 15%, rgba(167, 139, 250, 0.20), transparent 30%),
                    radial-gradient(circle at 55% 85%, rgba(94, 234, 212, 0.10), transparent 35%),
                    linear-gradient(135deg, #050713 0%, #0B1026 48%, #11133A 100%);
                color: var(--text-primary);
            }

            .stApp::before {
                content: "";
                position: fixed;
                inset: 0;
                pointer-events: none;
                background-image:
                    radial-gradient(#FFFFFF 0.8px, transparent 0.8px),
                    radial-gradient(#67E8F9 0.7px, transparent 0.7px);
                background-position: 0 0, 34px 28px;
                background-size: 82px 82px, 118px 118px;
                opacity: 0.18;
                z-index: 0;
            }

            .block-container {
                max-width: 1180px;
                padding-top: 2rem;
                padding-bottom: 1.25rem;
                position: relative;
                z-index: 1;
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, rgba(7, 10, 26, 0.98), rgba(17, 24, 53, 0.94));
                border-right: 1px solid var(--border-soft);
            }

            [data-testid="stSidebar"] * {
                color: var(--text-primary);
            }

            .hero-card, .chat-shell, .composer-shell, .sidebar-card {
                background: var(--bg-panel);
                border: 1px solid var(--border-soft);
                border-radius: 28px;
                box-shadow: 0 24px 80px rgba(0, 0, 0, 0.36);
                backdrop-filter: blur(18px);
            }

            .hero-card {
                padding: clamp(1.25rem, 3vw, 2.2rem);
                margin-bottom: 1.2rem;
                overflow: hidden;
                position: relative;
            }

            .hero-card::after {
                content: "";
                position: absolute;
                width: 220px;
                height: 220px;
                right: -70px;
                top: -100px;
                border-radius: 999px;
                background: radial-gradient(circle, rgba(34, 211, 238, 0.32), transparent 66%);
            }

            .eyebrow {
                align-items: center;
                color: var(--accent-green);
                display: flex;
                font-size: 0.82rem;
                font-weight: 700;
                gap: 0.5rem;
                letter-spacing: 0.16em;
                text-transform: uppercase;
            }

            .title {
                font-size: clamp(2.3rem, 6vw, 4.7rem);
                font-weight: 800;
                letter-spacing: -0.06em;
                line-height: 0.95;
                margin: 0.65rem 0 0.7rem;
            }

            .gradient-text {
                background: linear-gradient(90deg, #FFFFFF 0%, #67E8F9 45%, #C4B5FD 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .subtitle {
                color: var(--text-muted);
                font-size: clamp(1rem, 2vw, 1.16rem);
                line-height: 1.75;
                max-width: 760px;
            }

            .status-row {
                display: flex;
                flex-wrap: wrap;
                gap: 0.75rem;
                margin-top: 1.35rem;
            }

            .status-pill {
                background: rgba(15, 23, 42, 0.72);
                border: 1px solid var(--border-soft);
                border-radius: 999px;
                color: #DDE7FF;
                font-size: 0.86rem;
                padding: 0.58rem 0.86rem;
            }

            .chat-shell {
                display: flex;
                flex-direction: column;
                gap: 1rem;
                min-height: min(56vh, 620px);
                padding: clamp(1rem, 2.4vw, 1.5rem);
            }

            .chat-header {
                align-items: center;
                border-bottom: 1px solid var(--border-soft);
                display: flex;
                justify-content: space-between;
                padding-bottom: 1rem;
            }

            .chat-header h2 {
                font-size: 1.05rem;
                font-weight: 700;
                margin: 0;
            }

            .orbit-indicator {
                color: var(--accent-cyan);
                font-size: 0.85rem;
                font-weight: 700;
            }

            .message-row {
                display: flex;
                margin: 0.35rem 0;
                width: 100%;
            }

            .message-row.user {
                justify-content: flex-end;
            }

            .message-row.ai {
                justify-content: flex-start;
            }

            .message-bubble {
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 24px;
                max-width: min(78%, 720px);
                padding: 1rem 1.1rem;
                box-shadow: 0 16px 40px rgba(0, 0, 0, 0.26);
            }

            .message-row.ai .message-bubble {
                background: var(--ai-bubble);
                border-bottom-left-radius: 8px;
            }

            .message-row.user .message-bubble {
                background: var(--user-bubble);
                border-bottom-right-radius: 8px;
            }

            .message-meta {
                align-items: center;
                display: flex;
                font-size: 0.78rem;
                font-weight: 700;
                justify-content: space-between;
                margin-bottom: 0.45rem;
                opacity: 0.86;
            }

            .message-text {
                color: #F8FAFC;
                font-size: 0.98rem;
                line-height: 1.65;
            }

            .typing-indicator {
                align-items: center;
                background: rgba(15, 23, 42, 0.78);
                border: 1px solid var(--border-soft);
                border-radius: 999px;
                color: var(--text-muted);
                display: inline-flex;
                gap: 0.45rem;
                margin-top: 0.4rem;
                padding: 0.6rem 0.85rem;
                width: fit-content;
            }

            .typing-dot {
                animation: pulse 1.4s ease-in-out infinite;
                background: var(--accent-cyan);
                border-radius: 999px;
                height: 7px;
                width: 7px;
            }

            .typing-dot:nth-child(2) { animation-delay: 0.18s; }
            .typing-dot:nth-child(3) { animation-delay: 0.36s; }

            @keyframes pulse {
                0%, 80%, 100% { opacity: 0.25; transform: translateY(0); }
                40% { opacity: 1; transform: translateY(-3px); }
            }

            .composer-shell {
                margin-top: 1rem;
                padding: 1rem;
            }

            .stTextArea textarea, .stTextInput input {
                background: rgba(15, 23, 42, 0.86) !important;
                border: 1px solid rgba(148, 163, 184, 0.28) !important;
                border-radius: 18px !important;
                color: #F8FAFC !important;
            }

            .stButton > button {
                background: linear-gradient(135deg, #22D3EE 0%, #8B5CF6 100%);
                border: 0;
                border-radius: 16px;
                color: #FFFFFF;
                font-weight: 800;
                height: 3rem;
                letter-spacing: 0.02em;
                width: 100%;
            }

            .stButton > button:hover {
                border: 0;
                box-shadow: 0 12px 32px rgba(34, 211, 238, 0.28);
                color: #FFFFFF;
                transform: translateY(-1px);
            }

            .sidebar-card {
                border-radius: 22px;
                margin-bottom: 1rem;
                padding: 1rem;
            }

            .sidebar-title {
                color: var(--accent-cyan);
                font-size: 0.82rem;
                font-weight: 800;
                letter-spacing: 0.12em;
                margin-bottom: 0.8rem;
                text-transform: uppercase;
            }

            .history-item {
                background: rgba(15, 23, 42, 0.72);
                border: 1px solid rgba(148, 163, 184, 0.16);
                border-radius: 14px;
                color: #DDE7FF;
                font-size: 0.9rem;
                margin-bottom: 0.55rem;
                padding: 0.72rem 0.8rem;
            }

            .sidebar-note {
                color: var(--text-muted);
                font-size: 0.85rem;
                line-height: 1.55;
            }

            @media (max-width: 760px) {
                .block-container {
                    padding-left: 1rem;
                    padding-right: 1rem;
                }

                .message-bubble {
                    max-width: 92%;
                }

                .chat-header {
                    align-items: flex-start;
                    flex-direction: column;
                    gap: 0.45rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    """Render the sidebar and controls for the current conversation."""
    with st.sidebar:
        st.markdown("## 🛸 Nova Command")
        st.caption("Intergalactic chat workspace")

        if st.button("＋ New Chat", use_container_width=True):
            st.session_state.chat_messages = INITIAL_MESSAGES.copy()
            st.session_state.model_history = new_conversation()
            st.rerun()

        # Chat history placeholder entries.
        st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Chat History</div>', unsafe_allow_html=True)
        for item in CHAT_HISTORY_PLACEHOLDERS:
            st.markdown(f'<div class="history-item">✦ {item}</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sidebar-note">Saved conversations will appear here once chat persistence is added.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Settings controls are visual placeholders only.
        st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Settings</div>', unsafe_allow_html=True)
        st.selectbox("Signal Profile", ["Balanced", "Creative", "Precise"], index=0)
        st.slider("Nebula Temperature", 0.0, 1.0, 0.7, 0.1)
        st.toggle("Starlight Mode", value=True)
        st.markdown(
            '<div class="sidebar-note">Controls are placeholders and do not change chatbot behavior.</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


def render_hero() -> None:
    """Render the title and subtitle area."""
    st.markdown(
        """
        <section class="hero-card">
            <div class="eyebrow">● Quantum Link Established</div>
            <h1 class="title"><span class="gradient-text">Nova</span> Intergalactic AI Chat</h1>
            <p class="subtitle">
                A clean, responsive Streamlit command deck for future AI conversations — designed
                with cosmic depth, polished spacing, and an extensible layout ready for real chatbot logic.
            </p>
            <div class="status-row">
                <span class="status-pill">🌌 Deep-space theme</span>
                <span class="status-pill">🛰️ Responsive layout</span>
                <span class="status-pill">✨ UI-only prototype</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_message(message: dict[str, str]) -> None:
    """Render one styled chat message bubble."""
    st.markdown(
        f"""
        <div class="message-row {message['role']}">
            <div class="message-bubble">
                <div class="message-meta">
                    <span>{message['author']}</span>
                    <span>{message['time']}</span>
                </div>
                <div class="message-text">{message['text']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chat_area(messages: list[dict[str, str]]) -> None:
    """Render the current chat transcript."""
    st.markdown('<section class="chat-shell">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="chat-header">
            <h2>Mission Conversation</h2>
            <span class="orbit-indicator">● Orbiting standby</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for message in messages:
        render_message(message)

    # Typing indicator placeholder for future streaming responses.
    st.markdown(
        """
        <div class="typing-indicator" aria-label="Typing indicator placeholder">
            <span>Nova is calibrating</span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</section>", unsafe_allow_html=True)


def render_prompt_composer() -> None:
    """Collect a prompt, request a reply, and update session state."""
    st.markdown('<section class="composer-shell">', unsafe_allow_html=True)
    with st.form("prompt-form", clear_on_submit=True):
        input_col, button_col = st.columns([5, 1.2], vertical_alignment="bottom")
        with input_col:
            prompt = st.text_input(
                "Prompt",
                placeholder="Transmit a message to the stars...",
                label_visibility="collapsed",
            )
        with button_col:
            submitted = st.form_submit_button("Send", use_container_width=True)
    st.markdown("</section>", unsafe_allow_html=True)

    if not submitted or not prompt.strip():
        return

    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.chat_messages.append(
        {"role": "user", "author": "You", "text": prompt.strip(), "time": timestamp}
    )
    try:
        reply = get_reply(st.session_state.model_history, prompt.strip())
    except Exception as error:
        reply = f"Unable to contact Nova: {error}"

    st.session_state.chat_messages.append(
        {"role": "ai", "author": "Nova AI", "text": reply, "time": timestamp}
    )
    st.rerun()


def main() -> None:
    """Compose the full Streamlit interface."""
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = INITIAL_MESSAGES.copy()
    if "model_history" not in st.session_state:
        st.session_state.model_history = new_conversation()

    inject_global_styles()
    render_sidebar()
    render_hero()
    render_chat_area(st.session_state.chat_messages)
    render_prompt_composer()


if __name__ == "__main__":
    main()
