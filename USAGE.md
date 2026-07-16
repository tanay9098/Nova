# Using Nova

Nova is a Streamlit chat application powered by Mistral AI. It has two ways to
use it:

- **Web app:** the visual Nova Command interface in `app.py`.
- **Terminal chat:** a simple command-line conversation in `chatmodels/main.py`.

## For everyone

### Chat in the web app

1. Open the Nova web-app link supplied by the project owner.
2. Type a message in **“Transmit a message to the stars...”**.
3. Select **Send** to receive Nova's response.
4. Select **New Chat** to clear the current conversation and start again.

Your conversation is kept only for the active browser session. The chat-history
items in the sidebar are visual placeholders; conversations are not saved or
shared between sessions yet.

### If the app says “Unable to contact Nova”

This means the chat provider could not complete the request. If the message
includes `401 Unauthorized`, the deployed app does not have a valid Mistral API
key. Contact the project owner; do not paste an API key into the chat box or
publicly report it.

## For developers

### Prerequisites

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- A Mistral API key

### Set up locally

From the project root:

```bash
uv sync
```

Create a `.env` file in the project root with your own key:

```dotenv
MISTRAL_API_KEY="your_mistral_api_key"
```

Keep `.env` private. It must not be committed to Git or included in screenshots.

### Run the web app

```bash
uv run streamlit run app.py
```

Streamlit prints a local URL, usually `http://localhost:8501`. Open it in a
browser and send a message to test the integration.

### Run the terminal chat

```bash
uv run python -m chatmodels.main
```

Type a prompt at `You:`. Type `exit` to end the session.

## How the code is split

| File | Responsibility |
| --- | --- |
| `app.py` | Streamlit UI, form submission, display formatting, and per-browser-session chat state. |
| `chatmodels/main.py` | Mistral model setup, conversation-message handling, reply generation, and the optional terminal interface. |
| `.env` | Local-only Mistral credentials. |

`app.py` imports `get_reply()` and `new_conversation()` from
`chatmodels/main.py`. Do not put `input()` loops or `print()`-based interactive
code at the top level of `chatmodels/main.py`, because importing it from
Streamlit must not start a terminal loop.

## Deploying to Streamlit Community Cloud

1. Push the repository to GitHub without the `.env` file.
2. Create or update the Streamlit Cloud app so that `app.py` is its entry point.
3. In **Manage app → Settings → Secrets**, add:

   ```toml
   MISTRAL_API_KEY = "your_mistral_api_key"
   ```

4. Save the secret and reboot/redeploy the app.

The deployment needs its own secret configuration: local `.env` files are not
automatically uploaded to Streamlit Cloud.

## Troubleshooting

| Symptom | Likely cause | What to check |
| --- | --- | --- |
| `streamlit: command not found` | Dependencies have not been installed in the active environment. | Run `uv sync`, then use `uv run streamlit run app.py`. |
| `401 Unauthorized` from `api.mistral.ai` | Missing, invalid, or revoked Mistral key. | Check `MISTRAL_API_KEY` locally or Streamlit Cloud Secrets in production. |
| Works locally but not in production | The local `.env` is present, but the deployed secret is missing. | Add `MISTRAL_API_KEY` in the deployment's Secrets settings and redeploy. |
| UI loads but replies do not appear | The request to Mistral failed. | Read the displayed error and confirm the deployment's key and Mistral account access. |
