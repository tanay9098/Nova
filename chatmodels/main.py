"""Conversation logic shared by the Streamlit app and the optional CLI."""

from __future__ import annotations

from functools import lru_cache

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_mistralai import ChatMistralAI

SYSTEM_PROMPT = (
    "You are an extraterrestrial species from an advanced civilization helping "
    "human beings navigate their day-to-day life problems with philosophical insights."
)

load_dotenv()


@lru_cache(maxsize=1)
def get_model() -> ChatMistralAI:
    """Create and reuse the Mistral client for this Python process."""
    return ChatMistralAI(
        model_name="mistral-small-2506",
        temperature=0.9,
        max_tokens=150,
    )


def new_conversation() -> list[BaseMessage]:
    """Return a fresh conversation containing the chatbot instructions."""
    return [SystemMessage(content=SYSTEM_PROMPT)]


def get_reply(history: list[BaseMessage], prompt: str) -> str:
    """Add a user prompt to ``history`` and return the model's next reply."""
    history.append(HumanMessage(content=prompt))
    response = get_model().invoke(history)
    reply = str(response.content)
    history.append(AIMessage(content=reply))
    return reply


def run_cli() -> None:
    """Run the original terminal-chat interface."""
    history = new_conversation()
    print("Nova is ready. Type 'exit' to quit.")
    while True:
        prompt = input("You: ").strip()
        if prompt.lower() == "exit":
            break
        if prompt:
            print("Response:", get_reply(history, prompt))


if __name__ == "__main__":
    run_cli()
