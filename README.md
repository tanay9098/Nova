# Nova

Nova is a Streamlit chat application powered by Mistral AI. The Streamlit
interface lives in `app.py`, while the reusable conversation and model logic
lives in `chatmodels/main.py`.

## Developer setup

### Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- A valid Mistral API key

### Install dependencies

Clone the repository and change into its directory, then run:

```bash
uv sync
```

This creates or updates the project virtual environment from `pyproject.toml`
and `uv.lock`.

### Configure credentials

Create a `.env` file in the project root:

```dotenv
MISTRAL_API_KEY="your_mistral_api_key"
```

The application loads this value through `python-dotenv`. Keep `.env` local and
private; never commit it, paste it into the UI, or include the key in logs or
screenshots.

### Run the Streamlit UI

```bash
uv run streamlit run app.py
```

Open the local URL printed by Streamlit, normally
`http://localhost:8501`. Enter a prompt and select **Send** to exercise the
full UI-to-model path.

### Run the terminal interface

```bash
uv run python -m chatmodels.main
```

Type prompts at `You:` and type `exit` to end the session. The terminal mode
and Streamlit mode share the same `get_reply()` model function.

## Project structure

| File | Responsibility |
| --- | --- |
| `app.py` | Streamlit layout, CSS, form submission, display messages, and browser-session state. |
| `chatmodels/main.py` | Mistral client creation, LangChain message history, reply generation, and optional CLI entry point. |
| `pyproject.toml` | Project metadata and dependency declarations. |
| `uv.lock` | Locked dependency versions used by `uv sync`. |
| `.env` | Local-only credentials; do not commit. |

`app.py` imports `new_conversation()` and `get_reply()` from
`chatmodels/main.py`. The model module must not run an `input()` loop when it is
imported by Streamlit; the CLI loop is protected by its `__main__` guard.

## Deploy to Streamlit Community Cloud

1. Push the repository to GitHub without `.env`.
2. Set `app.py` as the Streamlit app entry point.
3. In **Manage app → Settings → Secrets**, add:

   ```toml
   MISTRAL_API_KEY = "your_mistral_api_key"
   ```

4. Save the secret and reboot or redeploy the app.

The local `.env` file is not uploaded to Streamlit Cloud. A deployment that
loads the UI but returns `401 Unauthorized` from `api.mistral.ai` has a missing,
invalid, revoked, or incorrectly named production secret. The expected name is
exactly `MISTRAL_API_KEY`.

## Troubleshooting

| Symptom | Resolution |
| --- | --- |
| `streamlit: command not found` | Run `uv sync` and start it with `uv run streamlit run app.py`. |
| UI loads but replies fail with `401 Unauthorized` | Check the Mistral key locally in `.env` or in Streamlit Cloud Secrets. |
| Local works but production fails | Configure `MISTRAL_API_KEY` in the deployment; local `.env` is not deployed. |
| Importing the model starts terminal input | Keep interactive code inside `run_cli()` and under `if __name__ == "__main__":`. |

For a user-oriented walkthrough, see [USAGE.md](USAGE.md).
