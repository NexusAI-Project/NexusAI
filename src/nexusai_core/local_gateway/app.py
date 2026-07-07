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
<html lang=\"en\" data-lang=\"en\">
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
      margin: 0; min-height: 100vh;
      font-family: ui-rounded, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif;
      background: radial-gradient(circle at top right, rgba(54, 163, 255, 0.26), transparent 34rem), radial-gradient(circle at 10% 10%, rgba(255, 255, 255, 0.08), transparent 20rem), var(--bg);
      color: var(--text);
    }}
    .shell {{ width: min(1120px, calc(100% - 32px)); margin: 0 auto; padding: 28px 0 48px; }}
    header {{ display: flex; align-items: center; justify-content: space-between; gap: 16px; }}
    .wordmark {{ font-size: 1.25rem; font-weight: 900; letter-spacing: -0.045em; line-height: 1; }}
    .wordmark .nexus {{ color: #ffffff; text-shadow: 0 0 18px rgba(255,255,255,0.16); }}
    [data-theme=\"light\"] .wordmark .nexus {{ color: #07111f; text-shadow: none; }}
    .wordmark .ai {{ color: var(--blue); }}
    .header-actions {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; justify-content: flex-end; }}
    button, .badge-button {{
      border: 1px solid var(--line); border-radius: 999px; padding: 10px 14px;
      background: linear-gradient(180deg, var(--panel-strong), var(--panel)); color: var(--text);
      cursor: pointer; font-weight: 800; box-shadow: 0 10px 24px rgba(0,0,0,0.16), inset 0 1px rgba(255,255,255,0.08);
      transition: transform 120ms ease, border-color 120ms ease, box-shadow 120ms ease;
    }}
    button:active {{ transform: translateY(1px) scale(0.99); }}
    .lang-toggle {{ min-width: 104px; }}
    .hero {{ margin-top: 56px; max-width: 780px; }}
    .eyebrow {{ color: var(--blue); font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; font-size: 0.78rem; }}
    h1 {{ font-size: clamp(2.5rem, 7vw, 5.6rem); letter-spacing: -0.075em; line-height: 0.95; margin: 14px 0 18px; }}
    .subtitle {{ color: var(--muted); font-size: clamp(1.15rem, 2.2vw, 1.55rem); line-height: 1.5; margin: 0; }}
    .grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; margin-top: 36px; }}
    .card, .panel {{ border: 1px solid var(--line); border-radius: 24px; background: var(--panel); box-shadow: var(--shadow); backdrop-filter: blur(16px); }}
    .card {{ padding: 20px; }}
    .label {{ color: var(--muted); font-size: 0.82rem; margin-bottom: 10px; }}
    .value {{ font-size: 1.05rem; font-weight: 850; }}
    .console {{ margin-top: 18px; padding: 22px; background: var(--panel-strong); }}
    h2 {{ margin: 0 0 16px; font-size: 1rem; }}
    .console-screen {{ min-height: 124px; border: 1px solid var(--line); border-radius: 18px; padding: 14px; color: var(--muted); background: rgba(2, 8, 18, 0.36); font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }}
    .console-input {{ width: 100%; margin-top: 12px; border: 1px solid var(--line); border-radius: 16px; padding: 13px 14px; color: var(--text); background: var(--blue-soft); }}
    .content {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-top: 18px; }}
    .panel {{ padding: 22px; background: var(--panel-strong); }}
    .preset-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    .preset {{ min-height: 118px; width: 100%; border-radius: 18px; text-align: left; display: grid; grid-template-columns: auto 1fr auto; gap: 10px; align-items: start; padding: 14px; }}
    .preset.selected {{ border-color: var(--blue); box-shadow: 0 0 0 1px rgba(54,163,255,0.34), 0 18px 38px rgba(54,163,255,0.12); }}
    .preset-num {{ color: var(--blue); font-weight: 900; }}
    .preset-name {{ display: block; font-weight: 900; margin-bottom: 6px; }}
    .preset-desc {{ display: block; color: var(--muted); font-weight: 650; line-height: 1.35; }}
    .lock {{ color: var(--muted); font-size: 1.05rem; }}
    .actions {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }}
    .actions button {{ min-height: 46px; width: 100%; }}
    .quick-links {{ display: flex; flex-wrap: wrap; gap: 10px; }}
    a {{ color: var(--text); text-decoration: none; border: 1px solid var(--line); border-radius: 999px; padding: 9px 12px; background: var(--blue-soft); }}
    #models {{ display: grid; gap: 10px; color: var(--muted); }}
    .model {{ color: var(--text); border: 1px solid var(--line); border-radius: 14px; padding: 10px 12px; background: var(--blue-soft); }}
    @media (max-width: 820px) {{ .grid, .content, .preset-grid, .actions {{ grid-template-columns: 1fr; }} .hero {{ margin-top: 42px; }} }}
  </style>
</head>
<body>
  <div class=\"shell\">
    <header>
      <div class=\"wordmark\" aria-label=\"NexusAI\"><span class=\"nexus\">Nexus</span><span class=\"ai\">AI</span></div>
      <div class=\"header-actions\">
        <button id=\"language-toggle\" class=\"lang-toggle\" type=\"button\" aria-label=\"Language selector\">🌐 EN / FR</button>
        <button id=\"theme-toggle\" type=\"button\" aria-label=\"Toggle theme\" data-i18n=\"themeButton\">Dark / Light</button>
      </div>
    </header>

    <main>
      <section class=\"hero\" aria-labelledby=\"page-title\">
        <div class=\"eyebrow\" data-i18n=\"eyebrow\">Local control interface</div>
        <h1 id=\"page-title\">{SERVICE_NAME}</h1>
        <p class=\"subtitle\" data-i18n=\"subtitle\">A calm local gateway for trusted AI.</p>
      </section>

      <section class=\"grid\" aria-label=\"Gateway status\">
        <div class=\"card\"><div class=\"label\" data-i18n=\"gateway\">Gateway</div><div class=\"value\" data-i18n=\"local\">Local</div></div>
        <div class=\"card\"><div class=\"label\" data-i18n=\"bind\">Bind</div><div class=\"value\">{GATEWAY_BIND}</div></div>
        <div class=\"card\"><div class=\"label\" data-i18n=\"ollamaTarget\">Ollama Target</div><div class=\"value\">{OLLAMA_TARGET}</div></div>
        <div class=\"card\"><div class=\"label\" data-i18n=\"security\">Security</div><div class=\"value\" data-i18n=\"localOnly\">Local-only</div></div>
      </section>

      <section class=\"console panel\" aria-labelledby=\"console-title\">
        <h2 id=\"console-title\" data-i18n=\"consoleTitle\">Nexus Console</h2>
        <div class=\"console-screen\" id=\"console-output\">help / aide · status / état / etat · models / modèles / modeles · presets / préréglages / prereglages · clear / effacer · links / liens · schema / schéma / schema</div>
        <input class=\"console-input\" id=\"console-input\" data-i18n-placeholder=\"consolePlaceholder\" placeholder=\"Type help, status, models, presets, links, or schema…\" aria-label=\"Console command\">
      </section>

      <section class=\"content\">
        <div class=\"panel\">
          <h2 data-i18n=\"presetFeeling\">NexusAI Preset Feeling</h2>
          <div class=\"preset-grid\">
            <button class=\"preset selected\" type=\"button\"><span class=\"preset-num\">01</span><span><span class=\"preset-name\" data-i18n=\"presetBalanced\">Balanced</span><span class=\"preset-desc\" data-i18n=\"presetBalancedDesc\">Everyday comfort and reliable flow.</span></span></button>
            <button class=\"preset\" type=\"button\"><span class=\"preset-num\">02</span><span><span class=\"preset-name\" data-i18n=\"presetDeep\">Deep Focus</span><span class=\"preset-desc\" data-i18n=\"presetDeepDesc\">More coherence for careful work.</span></span></button>
            <button class=\"preset\" type=\"button\"><span class=\"preset-num\">03</span><span><span class=\"preset-name\" data-i18n=\"presetSwift\">Swift</span><span class=\"preset-desc\" data-i18n=\"presetSwiftDesc\">Lightweight answers with lower slow risk.</span></span></button>
            <button class=\"preset\" type=\"button\"><span class=\"preset-num\">04</span><span><span class=\"preset-name\" data-i18n=\"presetStudio\">Studio</span><span class=\"preset-desc\" data-i18n=\"presetStudioDesc\">Creative polish when power allows.</span></span><span class=\"lock\" aria-label=\"Locked\">🔒</span></button>
          </div>
        </div>
        <div class=\"panel\">
          <h2 data-i18n=\"readiness\">Model readiness</h2>
          <div class=\"grid\" style=\"grid-template-columns: repeat(2, minmax(0, 1fr)); margin-top: 0;\">
            <div class=\"card\"><div class=\"label\" data-i18n=\"confidence\">Confidence</div><div class=\"value\">High</div></div>
            <div class=\"card\"><div class=\"label\" data-i18n=\"power\">Power</div><div class=\"value\">Local</div></div>
            <div class=\"card\"><div class=\"label\" data-i18n=\"fluidity\">Fluidity</div><div class=\"value\">Smooth</div></div>
            <div class=\"card\"><div class=\"label\" data-i18n=\"coherence\">Coherence</div><div class=\"value\">Steady</div></div>
            <div class=\"card\"><div class=\"label\" data-i18n=\"slowRisk\">Slow risk</div><div class=\"value\">Low</div></div>
            <div class=\"card\"><div class=\"label\" data-i18n=\"estimate\">NexusAI estimate</div><div class=\"value\">Ready</div></div>
          </div>
          <div class=\"actions\" style=\"margin-top: 14px;\">
            <button type=\"button\" data-i18n=\"actionRefresh\">Refresh status</button>
            <button type=\"button\" data-i18n=\"actionCheck\">Check models</button>
            <button type=\"button\" data-i18n=\"actionDocs\">Open docs</button>
            <button type=\"button\" data-i18n=\"actionSchema\">View schema</button>
          </div>
        </div>
        <div class=\"panel\">
          <h2 data-i18n=\"quickLinks\">Quick links</h2>
          <nav class=\"quick-links\" aria-label=\"Quick links\"><a href=\"/health\">/health</a><a href=\"/docs\">/docs</a><a href=\"/api/tags\">/api/tags</a><a href=\"/api/schema.json\">/api/schema.json</a></nav>
        </div>
        <div class=\"panel\">
          <h2 data-i18n=\"installedModels\">Installed models</h2>
          <div id=\"models\" data-i18n=\"loadingModels\">Loading local models…</div>
        </div>
      </section>
    </main>
  </div>
  <script>
    const root = document.documentElement;
    const translations = {{
      en: {{ themeButton: 'Dark / Light', eyebrow: 'Local control interface', subtitle: 'A calm local gateway for trusted AI.', gateway: 'Gateway', local: 'Local', bind: 'Bind', ollamaTarget: 'Ollama Target', security: 'Security', localOnly: 'Local-only', consoleTitle: 'Nexus Console', consolePlaceholder: 'Type help, status, models, presets, links, or schema…', presetFeeling: 'NexusAI Preset Feeling', presetBalanced: 'Balanced', presetBalancedDesc: 'Everyday comfort and reliable flow.', presetDeep: 'Deep Focus', presetDeepDesc: 'More coherence for careful work.', presetSwift: 'Swift', presetSwiftDesc: 'Lightweight answers with lower slow risk.', presetStudio: 'Studio', presetStudioDesc: 'Creative polish when power allows.', readiness: 'Model readiness', confidence: 'Confidence', power: 'Power', fluidity: 'Fluidity', coherence: 'Coherence', slowRisk: 'Slow risk', estimate: 'NexusAI estimate', actionRefresh: 'Refresh status', actionCheck: 'Check models', actionDocs: 'Open docs', actionSchema: 'View schema', quickLinks: 'Quick links', installedModels: 'Installed models', loadingModels: 'Loading local models…', noModels: 'Ollama unavailable or no models detected.' }},
      fr: {{ themeButton: 'Sombre / Clair', eyebrow: 'Interface de contrôle locale', subtitle: 'Une passerelle locale apaisée pour une IA de confiance.', gateway: 'Passerelle', local: 'Local', bind: 'Adresse', ollamaTarget: 'Cible Ollama', security: 'Sécurité', localOnly: 'Local uniquement', consoleTitle: 'Console Nexus', consolePlaceholder: 'Tapez aide, état, modèles, préréglages, liens ou schéma…', presetFeeling: 'Ressenti préréglage NexusAI', presetBalanced: 'Équilibré', presetBalancedDesc: 'Confort quotidien et flux fiable.', presetDeep: 'Concentration', presetDeepDesc: 'Plus de cohérence pour un travail attentif.', presetSwift: 'Rapide', presetSwiftDesc: 'Réponses légères avec risque de lenteur réduit.', presetStudio: 'Studio', presetStudioDesc: 'Finition créative quand la puissance le permet.', readiness: 'Préparation du modèle', confidence: 'Confiance', power: 'Puissance', fluidity: 'Fluidité', coherence: 'Cohérence', slowRisk: 'Risque de lenteur', estimate: 'Estimation NexusAI', actionRefresh: 'Actualiser le statut', actionCheck: 'Vérifier les modèles', actionDocs: 'Ouvrir la doc', actionSchema: 'Voir le schéma', quickLinks: 'Liens rapides', installedModels: 'Modèles installés', loadingModels: 'Chargement des modèles locaux…', noModels: 'Ollama indisponible ou aucun modèle détecté.' }}
    }};
    const savedTheme = localStorage.getItem('nexusai-theme') || 'dark';
    root.dataset.theme = savedTheme;
    const applyLanguage = (lang) => {{
      const safeLang = lang === 'fr' ? 'fr' : 'en';
      root.dataset.lang = safeLang; root.lang = safeLang;
      for (const item of document.querySelectorAll('[data-i18n]')) {{ item.textContent = translations[safeLang][item.dataset.i18n]; }}
      for (const item of document.querySelectorAll('[data-i18n-placeholder]')) {{ item.placeholder = translations[safeLang][item.dataset.i18nPlaceholder]; }}
      localStorage.setItem('nexusai-language', safeLang);
    }};
    applyLanguage(localStorage.getItem('nexusai-language') || 'en');
    document.getElementById('language-toggle').addEventListener('click', () => applyLanguage(root.dataset.lang === 'en' ? 'fr' : 'en'));
    document.getElementById('theme-toggle').addEventListener('click', () => {{
      const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
      root.dataset.theme = next;
      localStorage.setItem('nexusai-theme', next);
    }});

    const modelBox = document.getElementById('models');
    fetch('/api/tags')
      .then((response) => response.ok ? response.json() : Promise.reject())
      .then((data) => {{
        const models = Array.isArray(data.models) ? data.models : [];
        const names = models.map((model) => model && model.name).filter(Boolean);
        modelBox.textContent = '';
        if (!names.length) {{ modelBox.textContent = translations[root.dataset.lang].noModels; return; }}
        for (const name of names) {{ const item = document.createElement('div'); item.className = 'model'; item.textContent = name; modelBox.appendChild(item); }}
      }})
      .catch(() => {{ modelBox.textContent = translations[root.dataset.lang].noModels; }});
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
