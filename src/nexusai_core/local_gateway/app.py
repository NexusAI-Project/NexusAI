"""FastAPI application for the NexusAI Local Gateway.

The gateway is intended to run on 127.0.0.1 only. It must not be exposed on
0.0.0.0 by default. In v0, it only proxies selected Ollama-compatible routes
to the local Ollama service at http://127.0.0.1:11434.
"""

from __future__ import annotations

from typing import Any, Awaitable

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse

from .ollama_client import OllamaClient

SERVICE_NAME = "NexusAI Local Gateway"
DEFAULT_BIND_HOST = "127.0.0.1"
GATEWAY_BIND = "127.0.0.1:11435"
OLLAMA_TARGET = "127.0.0.1:11434"


def create_app(ollama_client: OllamaClient | None = None) -> FastAPI:
    """Create the local-only NexusAI Gateway app."""

    client = ollama_client or OllamaClient()
    app = FastAPI(
        title=SERVICE_NAME,
        description="Local-first gateway for NexusAI.",
        version="0.1.0",
        docs_url="/docs",
        redoc_url=None,
        openapi_url="/api/schema.json",
    )

    @app.get("/", response_class=HTMLResponse)
    async def homepage() -> str:
        """Return the local NexusAI dashboard homepage."""

        return _homepage_html()

    @app.get("/health")
    async def health() -> dict[str, str]:
        """Return local gateway health information."""

        return {
            "status": "ok",
            "service": SERVICE_NAME,
            "bind": DEFAULT_BIND_HOST,
        }

    @app.get("/api/tags")
    async def api_tags() -> Any:
        """Proxy Ollama /api/tags."""

        return await _proxy_ollama_call(client.get_tags())

    @app.post("/api/generate")
    async def api_generate(request: Request) -> Any:
        """Proxy Ollama /api/generate without logging prompt content."""

        payload = await request.json()
        return await _proxy_ollama_call(client.generate(payload))

    @app.post("/api/chat")
    async def api_chat(request: Request) -> Any:
        """Proxy Ollama /api/chat without logging message content."""

        payload = await request.json()
        return await _proxy_ollama_call(client.chat(payload))

    return app


def _homepage_html() -> str:
    """Build a self-contained local dashboard for the gateway."""

    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{SERVICE_NAME}</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #050812;
      --panel: rgba(13, 22, 39, 0.82);
      --panel-strong: rgba(16, 29, 51, 0.94);
      --text: #f8fbff;
      --muted: #9fb1c8;
      --line: rgba(128, 184, 255, 0.18);
      --blue: #36a3ff;
      --blue-soft: rgba(54, 163, 255, 0.16);
      --shadow: 0 24px 80px rgba(0, 0, 0, 0.45);
    }}
    [data-theme=\"light\"] {{
      color-scheme: light;
      --bg: #eef5ff;
      --panel: rgba(255, 255, 255, 0.82);
      --panel-strong: rgba(255, 255, 255, 0.96);
      --text: #07111f;
      --muted: #52657c;
      --line: rgba(37, 99, 235, 0.18);
      --blue: #075eea;
      --blue-soft: rgba(7, 94, 234, 0.12);
      --shadow: 0 24px 80px rgba(50, 83, 126, 0.22);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      font-family: ui-rounded, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at top right, rgba(54, 163, 255, 0.26), transparent 34rem),
        radial-gradient(circle at 10% 10%, rgba(255, 255, 255, 0.08), transparent 20rem),
        var(--bg);
      color: var(--text);
    }}
    .shell {{ width: min(1120px, calc(100% - 32px)); margin: 0 auto; padding: 28px 0 48px; }}
    header {{ display: flex; align-items: center; justify-content: space-between; gap: 16px; }}
    .wordmark {{ font-size: 1.25rem; font-weight: 900; letter-spacing: -0.045em; line-height: 1; }}
    .wordmark .nexus {{ color: #ffffff; text-shadow: 0 0 18px rgba(255,255,255,0.16); }}
    [data-theme=\"light\"] .wordmark .nexus {{ color: #07111f; text-shadow: none; }}
    .wordmark .ai {{ color: var(--blue); }}
    button {{
      border: 1px solid var(--line); border-radius: 999px; padding: 10px 14px;
      background: var(--panel); color: var(--text); cursor: pointer; font-weight: 700;
    }}
    .hero {{ margin-top: 74px; max-width: 760px; }}
    .eyebrow {{ color: var(--blue); font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; font-size: 0.78rem; }}
    h1 {{ font-size: clamp(2.5rem, 7vw, 5.6rem); letter-spacing: -0.075em; line-height: 0.95; margin: 14px 0 18px; }}
    .subtitle {{ color: var(--muted); font-size: clamp(1.15rem, 2.2vw, 1.55rem); line-height: 1.5; margin: 0; }}
    .grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; margin-top: 44px; }}
    .card, .links, .models {{
      border: 1px solid var(--line); border-radius: 24px; background: var(--panel);
      box-shadow: var(--shadow); backdrop-filter: blur(16px);
    }}
    .card {{ padding: 20px; }}
    .label {{ color: var(--muted); font-size: 0.82rem; margin-bottom: 10px; }}
    .value {{ font-size: 1.05rem; font-weight: 850; }}
    .content {{ display: grid; grid-template-columns: 0.9fr 1.1fr; gap: 18px; margin-top: 18px; }}
    .links, .models {{ padding: 22px; background: var(--panel-strong); }}
    h2 {{ margin: 0 0 16px; font-size: 1rem; }}
    .quick-links {{ display: flex; flex-wrap: wrap; gap: 10px; }}
    a {{ color: var(--text); text-decoration: none; border: 1px solid var(--line); border-radius: 999px; padding: 9px 12px; background: var(--blue-soft); }}
    #models {{ display: grid; gap: 10px; color: var(--muted); }}
    .model {{ color: var(--text); border: 1px solid var(--line); border-radius: 14px; padding: 10px 12px; background: var(--blue-soft); }}
    @media (max-width: 820px) {{ .grid, .content {{ grid-template-columns: 1fr; }} .hero {{ margin-top: 48px; }} }}
  </style>
</head>
<body>
  <div class=\"shell\">
    <header>
      <div class=\"wordmark\" aria-label=\"NexusAI\"><span class=\"nexus\">Nexus</span><span class=\"ai\">AI</span></div>
      <button id=\"theme-toggle\" type=\"button\" aria-label=\"Toggle theme\">Dark / Light</button>
    </header>

    <main>
      <section class=\"hero\" aria-labelledby=\"page-title\">
        <div class=\"eyebrow\">Local control interface</div>
        <h1 id=\"page-title\">{SERVICE_NAME}</h1>
        <p class=\"subtitle\">Le cœur lumineux d’une intelligence de confiance.</p>
      </section>

      <section class=\"grid\" aria-label=\"Gateway status\">
        <div class=\"card\"><div class=\"label\">Gateway</div><div class=\"value\">Local</div></div>
        <div class=\"card\"><div class=\"label\">Bind</div><div class=\"value\">{GATEWAY_BIND}</div></div>
        <div class=\"card\"><div class=\"label\">Ollama Target</div><div class=\"value\">{OLLAMA_TARGET}</div></div>
        <div class=\"card\"><div class=\"label\">Security</div><div class=\"value\">Local-only</div></div>
      </section>

      <section class=\"content\">
        <div class=\"links\">
          <h2>Quick links</h2>
          <nav class=\"quick-links\" aria-label=\"Quick links\">
            <a href=\"/health\">/health</a><a href=\"/docs\">/docs</a><a href=\"/api/tags\">/api/tags</a><a href=\"/api/schema.json\">/api/schema.json</a>
          </nav>
        </div>
        <div class=\"models\">
          <h2>Local models</h2>
          <div id=\"models\">Loading local models…</div>
        </div>
      </section>
    </main>
  </div>
  <script>
    const root = document.documentElement;
    const savedTheme = localStorage.getItem('nexusai-theme') || 'dark';
    root.dataset.theme = savedTheme;
    document.getElementById('theme-toggle').addEventListener('click', () => {{
      const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
      root.dataset.theme = next;
      localStorage.setItem('nexusai-theme', next);
    }});

    const modelBox = document.getElementById('models');
    const emptyMessage = 'Ollama unavailable or no models detected.';
    fetch('/api/tags')
      .then((response) => response.ok ? response.json() : Promise.reject())
      .then((data) => {{
        const models = Array.isArray(data.models) ? data.models : [];
        const names = models.map((model) => model && model.name).filter(Boolean);
        modelBox.textContent = '';
        if (!names.length) {{
          modelBox.textContent = emptyMessage;
          return;
        }}
        for (const name of names) {{
          const item = document.createElement('div');
          item.className = 'model';
          item.textContent = name;
          modelBox.appendChild(item);
        }}
      }})
      .catch(() => {{ modelBox.textContent = emptyMessage; }});
  </script>
</body>
</html>"""


async def _proxy_ollama_call(call: Awaitable[Any]) -> Any:
    """Convert local Ollama errors into safe HTTP responses."""

    try:
        return await call
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail="Local Ollama returned an error.",
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to reach local Ollama service.",
        ) from exc


app = create_app()
