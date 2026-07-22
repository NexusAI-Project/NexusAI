"""FastAPI application for the NexusAI Local Gateway.

The gateway is intended to run on 127.0.0.1 only. It must not be exposed on
0.0.0.0 by default. In v0, it only proxies selected Ollama-compatible routes
to the local Ollama service at http://127.0.0.1:11434.
"""

from __future__ import annotations

from typing import Any, Awaitable
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

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

    static_dir = Path(__file__).with_name("static")
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=static_dir), name="static")

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
    """Build a self-contained local NexusAI Control Center homepage."""

    html = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__SERVICE_NAME__</title>
  <style>
    :root { color-scheme: dark; --bg:#050812; --panel:rgba(13,22,39,.84); --panel-strong:rgba(16,29,51,.96); --text:#f8fbff; --muted:#9fb1c8; --line:rgba(128,184,255,.22); --blue:#36a3ff; --blue-soft:rgba(54,163,255,.16); --ok:#3ddc97; --warn:#ff9f1c; --error:#ff4d6d; --debug:#8b95a7; --shadow:0 24px 80px rgba(0,0,0,.45); }
    [data-theme="light"] { color-scheme: light; --bg:#eef5ff; --panel:rgba(255,255,255,.84); --panel-strong:rgba(255,255,255,.97); --text:#07111f; --muted:#52657c; --line:rgba(37,99,235,.2); --blue:#075eea; --blue-soft:rgba(7,94,234,.12); --shadow:0 24px 80px rgba(50,83,126,.22); }
    * { box-sizing:border-box; } body { margin:0; min-height:100vh; font-family:ui-rounded,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; background:radial-gradient(circle at top right,rgba(54,163,255,.26),transparent 34rem),radial-gradient(circle at 10% 10%,rgba(255,255,255,.08),transparent 20rem),var(--bg); color:var(--text); }
    .shell { width:min(1180px,calc(100% - 32px)); margin:0 auto; padding:28px 0 48px; } header { display:flex; align-items:center; justify-content:space-between; gap:16px; }
    .wordmark { font-size:1.25rem; font-weight:900; letter-spacing:-.045em; line-height:1; } .wordmark .nexus { color:#fff; text-shadow:0 0 18px rgba(255,255,255,.16); } [data-theme="light"] .wordmark .nexus { color:#07111f; text-shadow:none; } .wordmark .ai,.eyebrow { color:var(--blue); }
    button,a { border:1px solid var(--line); border-radius:14px; padding:10px 13px; background:var(--panel); color:var(--text); cursor:pointer; font-weight:750; text-decoration:none; box-shadow:inset 0 1px 0 rgba(255,255,255,.06),0 8px 20px rgba(0,0,0,.12); transition:transform .08s ease,border-color .15s ease,background .15s ease; } button:active { transform:translateY(1px) scale(.99); } button:hover,a:hover { border-color:var(--blue); background:var(--blue-soft); }
    .hero { margin-top:54px; max-width:850px; } .eyebrow { font-weight:800; letter-spacing:.14em; text-transform:uppercase; font-size:.78rem; } h1 { font-size:clamp(2.4rem,6vw,5.2rem); letter-spacing:-.075em; line-height:.95; margin:14px 0 18px; } .subtitle { color:var(--muted); font-size:clamp(1.1rem,2vw,1.45rem); line-height:1.5; margin:0; }
    .grid { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:14px; margin-top:34px; } .panel,.card,.console { border:1px solid var(--line); border-radius:24px; background:var(--panel); box-shadow:var(--shadow); backdrop-filter:blur(16px); } .card { padding:18px; } .label { color:var(--muted); font-size:.82rem; margin-bottom:10px; } .value { font-size:1.05rem; font-weight:850; }
    .matrix-layout { display:grid; grid-template-columns:.85fr 1.15fr; gap:18px; margin-top:18px; } .panel { padding:22px; background:var(--panel-strong); } h2,h3 { margin:0 0 16px; } .preset-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; } .preset-btn { text-align:left; border-radius:16px; min-height:58px; } .preset-btn.active { outline:2px solid var(--blue); background:linear-gradient(180deg,var(--blue-soft),transparent); } .lock { color:var(--warn); float:right; }
    .controls,.quick-links { display:flex; flex-wrap:wrap; gap:10px; margin-top:16px; } .roles { display:grid; gap:10px; } .role { display:grid; grid-template-columns:160px 1fr auto; gap:10px; align-items:start; border:1px solid var(--line); border-radius:16px; padding:12px; background:rgba(255,255,255,.03); } .status-ok { color:var(--ok); } .status-warn { color:var(--warn); } .command { color:var(--warn); font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.9rem; margin-top:6px; } .compat { font-size:1.2rem; font-weight:900; color:var(--blue); } input,select { border:1px solid var(--line); border-radius:12px; padding:10px; color:var(--text); background:var(--panel); }
    details { margin-top:18px; } summary { cursor:pointer; color:var(--blue); font-weight:850; } #models { display:grid; gap:10px; color:var(--muted); margin-top:12px; } .model { color:var(--text); border:1px solid var(--line); border-radius:14px; padding:10px 12px; background:var(--blue-soft); }
    .console { margin-top:18px; padding:18px; background:#05070d; } [data-theme="light"] .console { background:#f8fbff; } .log { height:220px; overflow:auto; display:flex; flex-direction:column; gap:6px; font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.9rem; } .OK{color:var(--ok)} .INFO{color:var(--blue)} .WARN{color:var(--warn)} .ERROR{color:var(--error)} .DEBUG{color:var(--debug)} .console-row { display:flex; gap:8px; margin-top:12px; } .console-row input { flex:1; }
    .brand { display:flex; align-items:center; gap:12px; font-weight:900; }
    .brand-logo { width:42px; height:42px; object-fit:contain; filter:drop-shadow(0 0 14px rgba(54,163,255,.42)); }
    .brand-fallback { font-size:1.25rem; letter-spacing:-.045em; }
    .top-actions { display:flex; flex-wrap:wrap; gap:10px; align-items:center; justify-content:flex-end; }
    .pulse { border-color:rgba(61,220,151,.45); color:var(--ok); background:rgba(61,220,151,.08); }
    @media (max-width:860px) { .grid,.matrix-layout { grid-template-columns:1fr; } .role { grid-template-columns:1fr; } .hero { margin-top:42px; } }
  </style>
</head>
<body>
  <div class="shell">
    <header><div class="brand" aria-label="NexusAI"><img class="brand-logo" src="/static/nexusai-logo.png" alt="NexusAI logo" onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'inline\';"><span class="brand-fallback" style="display:none">NexusAI</span></div><div class="top-actions"><button id="pulse" class="pulse" type="button">NexusAI Pulse</button><button id="theme-toggle" type="button">Dark / Light</button></div></header>
    <main>
      <section class="hero"><div class="eyebrow">Local control interface</div><h1>__SERVICE_NAME__</h1><p class="subtitle">Le cœur lumineux d’une intelligence de confiance.</p></section>
      <section class="grid" aria-label="Gateway status"><div class="card"><div class="label">Gateway</div><div class="value">Local</div></div><div class="card"><div class="label">Bind</div><div class="value">__GATEWAY_BIND__</div></div><div class="card"><div class="label">Ollama Target</div><div class="value">__OLLAMA_TARGET__</div></div><div class="card"><div class="label">Security</div><div class="value">Local-only</div></div></section>
      <section class="matrix-layout" aria-label="NexusAI Preset Matrix"><div class="panel"><h2>Preset Matrix</h2><div id="preset-grid" class="preset-grid"></div><div class="controls"><button id="load">Load Preset</button><button id="save">Save Preset</button><button id="rename">Rename Preset</button><button id="lock">Lock / Unlock</button><button id="restore">Restore Default</button><button id="copy-json">Copy Config JSON</button><button id="smart">Generate Smart Preset</button><button id="refresh">Refresh Models</button></div></div><div class="panel"><h2 id="preset-title">Preset</h2><div class="compat" id="compatibility">Compatibility estimate: 0%</div><p id="lock-state" class="label"></p><div id="roles" class="roles"></div></div></section>
      <details><summary>Show installed models</summary><div class="panel"><h2>Local models</h2><div id="models">Loading local models…</div></div></details>
      <section class="panel"><h2>Quick links</h2><nav class="quick-links"><a href="/health">/health</a><a href="/docs">/docs</a><a href="/api/tags">/api/tags</a><a href="/api/schema.json">/api/schema.json</a></nav></section>
      <section class="console"><h2>Nexus Console</h2><div id="log" class="log"></div><div class="console-row"><input id="console-input" placeholder="help, status, models, presets, clear, links, schema"><button id="console-run">Run</button></div></section>
    </main>
  </div>
<script>
const ROLES=['Heart Model','Brain Model','Fast Model','Heavy Model','Vision Model','Code Model','Chat Model','Fallback Model'];
const KEYS=['heart','brain','fast','heavy','vision','code','chat','fallback'];
const DEFAULT_PRESETS=[
{id:1,short:'Default',name:'NexusAI Default 14B+',locked:true,roles:{heart:'mistral-nemo:12b',brain:'qwen3:14b',fast:'qwen2.5:14b',heavy:'gpt-oss:20b',vision:'llava:13b',code:'qwen2.5-coder:14b',chat:'qwen2.5:14b',fallback:'phi4:14b'}},
{id:2,short:'Architect',name:'Architect / Deep Brain',locked:false,roles:{heart:'qwen3:14b',brain:'qwen3:30b',fast:'qwen2.5:14b',heavy:'qwen2.5:32b',vision:'gemma3:12b',code:'qwen2.5-coder:32b',chat:'qwen3:14b',fallback:'phi4:14b'}},
{id:3,short:'Code Forge',name:'Code Forge',locked:false,roles:{heart:'mistral-nemo:12b',brain:'qwen2.5:14b',fast:'phi4:14b',heavy:'qwen2.5-coder:32b',vision:'llava:13b',code:'qwen2.5-coder:14b',chat:'qwen3:14b',fallback:'qwen2.5:14b'}},
{id:4,short:'Vision Lab',name:'Vision Lab',locked:false,roles:{heart:'qwen3:14b',brain:'gemma3:27b',fast:'gemma3:12b',heavy:'gpt-oss:20b',vision:'llava:13b',code:'qwen2.5-coder:14b',chat:'gemma3:12b',fallback:'qwen2.5:14b'}},
{id:5,short:'Heavy',name:'Heavy Reasoning',locked:false,roles:{heart:'mistral-nemo:12b',brain:'deepseek-r1:32b',fast:'phi4:14b',heavy:'gpt-oss:20b',vision:'gemma3:12b',code:'qwen2.5-coder:32b',chat:'qwen3:14b',fallback:'qwen2.5:14b'}},
{id:6,short:'Soul',name:'French / Dialogue / Soul',locked:false,roles:{heart:'mistral-nemo:12b',brain:'qwen3:14b',fast:'qwen2.5:14b',heavy:'mixtral:8x7b',vision:'gemma3:12b',code:'qwen2.5-coder:14b',chat:'qwen2.5:14b',fallback:'phi4:14b'}},
{id:7,short:'Daily',name:'Safe Daily Driver',locked:false,roles:{heart:'phi4:14b',brain:'qwen2.5:14b',fast:'gemma3:12b',heavy:'qwen3:14b',vision:'llava:13b',code:'qwen2.5-coder:14b',chat:'qwen2.5:14b',fallback:'mistral-nemo:12b'}},
{id:8,short:'Experimental',name:'Experimental',locked:false,roles:{heart:'qwen3:14b',brain:'deepseek-r1:14b',fast:'phi4:14b',heavy:'qwen3:30b',vision:'gemma3:27b',code:'qwen2.5-coder:32b',chat:'mixtral:8x7b',fallback:'qwen2.5:14b'}},
{id:9,short:'Monster',name:'Monster Mode',locked:false,roles:{heart:'mistral-nemo:12b',brain:'qwen2.5:32b',fast:'qwen3:14b',heavy:'deepseek-r1:32b',vision:'gemma3:27b',code:'qwen2.5-coder:32b',chat:'mixtral:8x7b',fallback:'phi4:14b'}},
{id:10,short:'Random',name:'Smart Random',locked:false,roles:{heart:'auto',brain:'auto',fast:'auto',heavy:'auto',vision:'auto',code:'auto',chat:'auto',fallback:'auto'}}];
let installed=[],activeId=Number(localStorage.getItem('nexusai-active-preset')||1); let presets=JSON.parse(localStorage.getItem('nexusai-presets')||'null')||structuredClone(DEFAULT_PRESETS);
const root=document.documentElement; root.dataset.theme=localStorage.getItem('nexusai-theme')||'dark'; document.getElementById('theme-toggle').onclick=()=>{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark'; localStorage.setItem('nexusai-theme',root.dataset.theme); log('INFO','Theme set to '+root.dataset.theme)};
document.getElementById('pulse')?.addEventListener('click',()=>log('INFO','NexusAI Pulse — Audit modèle bientôt disponible'));
function saveLocal(){localStorage.setItem('nexusai-presets',JSON.stringify(presets)); localStorage.setItem('nexusai-active-preset',activeId)}
function log(level,msg){const box=document.getElementById('log'); const line=document.createElement('div'); line.className=level; line.textContent='['+level+'] '+msg; box.appendChild(line); box.scrollTop=box.scrollHeight; const logs=[...box.children].slice(-80).map(x=>({level:x.className,msg:x.textContent})); localStorage.setItem('nexusai-console',JSON.stringify(logs));}
function restoreLogs(){(JSON.parse(localStorage.getItem('nexusai-console')||'[]')).slice(-20).forEach(x=>log(x.level||'INFO',(x.msg||'').replace(/^\[[A-Z]+\] /,'')));}
function active(){return presets.find(p=>p.id===activeId)||presets[0]}
function familyUrl(model){const fam=(model||'').split(':')[0]; return /^[a-z0-9][a-z0-9._-]*$/i.test(fam)?'https://ollama.com/library/'+encodeURIComponent(fam):''}
function compatibility(p){let score=0; for(const k of KEYS){const m=p.roles[k]; if(m&&m!=='auto') score+=7; if(installed.includes(m)) score+=6;} ['code','vision','heavy','fallback'].forEach(k=>{if(installed.includes(p.roles[k])) score+=5}); for(const k of KEYS){const m=p.roles[k]; if(!m||m==='auto') score-=4; else if(!installed.includes(m)) score-=5;} return Math.max(0,Math.min(100,Math.round(score)));}
function render(){const grid=document.getElementById('preset-grid'); grid.textContent=''; presets.forEach(p=>{const b=document.createElement('button'); b.className='preset-btn'+(p.id===activeId?' active':''); b.innerHTML='<strong>'+p.id+' '+p.short+'</strong>'+(p.locked?'<span class="lock">🔒</span>':'')+'<br><span class="label">'+p.name+'</span>'; b.onclick=()=>{activeId=p.id; saveLocal(); render(); log('INFO','Preset selected: '+p.name)}; grid.appendChild(b)}); const p=active(); document.getElementById('preset-title').textContent=p.name; document.getElementById('lock-state').textContent=p.locked?'Locked preset: load/copy only':'Unlocked preset'; document.getElementById('compatibility').textContent='Compatibility estimate: '+compatibility(p)+'%'; const roles=document.getElementById('roles'); roles.textContent=''; KEYS.forEach((k,i)=>{const m=p.roles[k]||''; const ok=installed.includes(m); const row=document.createElement('div'); row.className='role'; let safe=familyUrl(m); row.innerHTML='<strong>'+ROLES[i]+'</strong><div><div>'+m+'</div><div class="'+(ok?'status-ok':'status-warn')+'">'+(ok?'detected':'missing')+'</div>'+(!ok&&m&&m!=='auto'?'<div class="command">ollama pull '+m+'</div>':'')+'</div><div>'+(!ok&&m&&m!=='auto'?'<button data-copy="ollama pull '+m+'">Copy command</button> '+(safe?'<a target="_blank" rel="noopener noreferrer" href="'+safe+'">Open Ollama page</a>':''):'')+'</div>'; roles.appendChild(row); if(!ok&&m&&m!=='auto') log('WARN',ROLES[i]+' '+m+' not detected. Suggested command: ollama pull '+m);}); document.querySelectorAll('[data-copy]').forEach(b=>b.onclick=()=>navigator.clipboard.writeText(b.dataset.copy).then(()=>log('INFO','Command copied: '+b.dataset.copy)));}
function choose(words){return installed.find(n=>words.some(w=>n.includes(w)))||installed[0]||'auto'}
function smart(){return {heart:choose(['mistral-nemo','phi4','qwen3']),brain:choose(['qwen3','qwen2.5','deepseek-r1']),fast:choose(['gemma3:12b','gemma3:4b','phi4','qwen2.5:14b']),heavy:choose(['gpt-oss','deepseek-r1','32b','30b','mixtral']),vision:choose(['llava','gemma3']),code:choose(['qwen2.5-coder','codellama']),chat:choose(['qwen2.5','qwen3','mistral-nemo']),fallback:choose(['phi4','mistral-nemo','llama3.2','qwen2.5'])}}
function block(action){log('WARN','Locked preset blocks '+action+'. Unlock before modifying.')}
document.getElementById('load').onclick=()=>log('OK','Preset loaded: '+active().name);
document.getElementById('save').onclick=()=>active().locked?block('save'):(saveLocal(),log('OK','Preset saved: '+active().name));
document.getElementById('rename').onclick=()=>{let p=active(); if(p.locked) return block('rename'); const name=prompt('Preset name',p.name); if(name){p.name=name; p.short=name.slice(0,18); saveLocal(); render(); log('OK','Preset renamed: '+name)}};
document.getElementById('lock').onclick=()=>{let p=active(); p.locked=!p.locked; saveLocal(); render(); log('INFO','Preset '+(p.locked?'locked':'unlocked')+': '+p.name)};
document.getElementById('restore').onclick=()=>{let p=active(); if(p.locked) return block('restore default'); presets[p.id-1]=structuredClone(DEFAULT_PRESETS[p.id-1]); saveLocal(); render(); log('OK','Default restored for preset '+p.id)};
document.getElementById('copy-json').onclick=()=>navigator.clipboard.writeText(JSON.stringify(active(),null,2)).then(()=>log('INFO','Config JSON copied'));
document.getElementById('smart').onclick=()=>{let p=active(); if(p.locked) return block('smart preset generation'); p.roles=smart(); p.name=p.id===10?'Smart Random':'Smart '+p.name; saveLocal(); render(); log('OK','Smart preset generated. Picks prefer vision/code/heavy/brain/fast/heart/chat/fallback heuristics from detected local models.')};
document.getElementById('refresh').onclick=refresh;
function consoleCommand(){const input=document.getElementById('console-input'); const c=input.value.trim().toLowerCase(); input.value=''; if(c==='clear'){document.getElementById('log').textContent=''; localStorage.removeItem('nexusai-console'); return} const map={help:'Commands: help, status, models, presets, clear, links, schema',status:'Active preset '+active().name+'; compatibility '+compatibility(active())+'%; detected models '+installed.length,models:installed.join(', ')||'No models detected',presets:presets.map(p=>p.id+': '+p.name+(p.locked?' locked':'')).join(' | '),links:'/health /docs /api/tags /api/schema.json',schema:'Schema route: /api/schema.json; /openapi.json intentionally unavailable'}; log('INFO',map[c]||'Unknown UI-only command. Type help.');}
document.getElementById('console-run').onclick=consoleCommand; document.getElementById('console-input').addEventListener('keydown',e=>{if(e.key==='Enter')consoleCommand()});
function refresh(){fetch('/api/tags').then(r=>r.ok?r.json():Promise.reject()).then(data=>{installed=(Array.isArray(data.models)?data.models:[]).map(m=>m&&m.name).filter(Boolean); const box=document.getElementById('models'); box.textContent=''; if(!installed.length) box.textContent='Ollama unavailable or no models detected.'; installed.forEach(n=>{const d=document.createElement('div'); d.className='model'; d.textContent=n; box.appendChild(d)}); render(); log('OK','Models refreshed: '+installed.length+' detected')}).catch(()=>{installed=[]; document.getElementById('models').textContent='Ollama unavailable or no models detected.'; render(); log('ERROR','Models refresh failed or Ollama unavailable')});}
restoreLogs(); log('INFO','NexusAI Local Gateway démarre...'); log('INFO','Interface de contrôle locale initialisée'); log('INFO','Gateway : __GATEWAY_BIND__'); log('INFO','Ollama Target : __OLLAMA_TARGET__'); log('INFO','Sécurité : local uniquement'); fetch('/health').then(r=>r.json()).then(d=>log('OK','/health '+JSON.stringify(d))).catch(()=>log('WARN','/health unavailable')); render(); log('INFO','Nexus Console ready. Type help.'); refresh();
</script>
</body>
</html>"""
    return (
        html.replace("__SERVICE_NAME__", SERVICE_NAME)
        .replace("__GATEWAY_BIND__", GATEWAY_BIND)
        .replace("__OLLAMA_TARGET__", OLLAMA_TARGET)
    )


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
