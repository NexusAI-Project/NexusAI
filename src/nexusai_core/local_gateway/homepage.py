"""Self-contained public face for the local NexusAI gateway."""

from __future__ import annotations


def homepage_html() -> str:
    """Return the dependency-free, local-first NexusAI homepage."""

    return """<!doctype html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="NexusAI is a local-first modular intelligence ecosystem: one core, many connected capabilities.">
  <title>NexusAI — One core. Many capabilities.</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #05070d; --surface: #0b101b; --panel: rgba(13, 20, 34, .86);
      --panel-strong: #101827; --text: #f1f5fb; --muted: #92a0b5;
      --line: rgba(143, 168, 208, .16); --blue: #68a8ff; --cyan: #5ee7e7;
      --violet: #a98cff; --success: #6ee7ae; --danger: #ff8292;
      --blue-soft: rgba(104, 168, 255, .11); --shadow: 0 24px 80px rgba(0, 0, 0, .38);
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body { margin: 0; min-height: 100vh; color: var(--text); background:
      radial-gradient(circle at 80% 0, rgba(73, 120, 255, .16), transparent 32rem),
      radial-gradient(circle at 10% 25%, rgba(94, 231, 231, .06), transparent 26rem), var(--bg);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
    body::before { content: ""; position: fixed; inset: 0; pointer-events: none; opacity: .22;
      background-image: linear-gradient(var(--line) 1px, transparent 1px), linear-gradient(90deg, var(--line) 1px, transparent 1px);
      background-size: 64px 64px; mask-image: linear-gradient(to bottom, black, transparent 70%); }
    a { color: inherit; } button, textarea, select { font: inherit; }
    button:focus-visible, a:focus-visible, textarea:focus-visible, select:focus-visible { outline: 2px solid var(--cyan); outline-offset: 3px; }
    .shell { width: min(1160px, calc(100% - 36px)); margin: auto; position: relative; }
    .site-header { min-height: 78px; display: flex; align-items: center; justify-content: space-between; gap: 22px; border-bottom: 1px solid var(--line); }
    .brand { display: inline-flex; align-items: center; gap: 10px; text-decoration: none; font-weight: 850; letter-spacing: -.04em; font-size: 1.15rem; }
    .brand-mark { width: 30px; aspect-ratio: 1; display: grid; place-items: center; border: 1px solid rgba(104,168,255,.5); border-radius: 9px; color: var(--blue); background: var(--blue-soft); box-shadow: 0 0 28px rgba(104,168,255,.16); }
    .brand span:last-child { color: var(--blue); }
    .nav { display: flex; gap: 24px; align-items: center; }
    .nav a { color: var(--muted); text-decoration: none; font-size: .86rem; font-weight: 650; }
    .nav a:hover { color: var(--text); }
    .status-pill { display: inline-flex; align-items: center; gap: 8px; padding: 8px 12px; border: 1px solid var(--line); border-radius: 999px; background: var(--panel); color: var(--muted); font-size: .78rem; }
    .dot { width: 7px; height: 7px; border-radius: 50%; background: var(--success); box-shadow: 0 0 12px var(--success); }
    .hero { min-height: 610px; display: grid; grid-template-columns: 1.08fr .92fr; align-items: center; gap: 70px; padding: 70px 0; }
    .eyebrow { color: var(--cyan); font-size: .72rem; font-weight: 800; letter-spacing: .17em; text-transform: uppercase; }
    h1 { font-size: clamp(3.3rem, 7vw, 6.3rem); line-height: .93; letter-spacing: -.075em; margin: 20px 0 24px; max-width: 820px; }
    .gradient { color: transparent; background: linear-gradient(110deg, var(--blue), var(--cyan)); background-clip: text; }
    .lede { color: var(--muted); font-size: clamp(1.05rem, 2vw, 1.28rem); line-height: 1.65; max-width: 650px; }
    .actions { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 34px; }
    .button { display: inline-flex; justify-content: center; align-items: center; min-height: 44px; padding: 0 18px; border-radius: 10px; border: 1px solid var(--line); text-decoration: none; font-weight: 750; font-size: .88rem; cursor: pointer; }
    .button-primary { color: #04101d; background: linear-gradient(135deg, var(--cyan), var(--blue)); border-color: transparent; }
    .button-secondary { background: var(--panel); color: var(--text); }
    .core-map { min-height: 390px; position: relative; display: grid; place-items: center; }
    .orbit { position: absolute; border: 1px solid var(--line); border-radius: 50%; width: 340px; height: 340px; animation: spin 38s linear infinite; }
    .orbit:nth-child(2) { width: 245px; height: 245px; animation-direction: reverse; animation-duration: 27s; }
    .orbit::before, .orbit::after { content: ""; position: absolute; width: 10px; height: 10px; border-radius: 50%; background: var(--blue); box-shadow: 0 0 18px var(--blue); }
    .orbit::before { top: 18%; left: 7%; } .orbit::after { bottom: 8%; right: 20%; background: var(--violet); }
    .core { width: 150px; aspect-ratio: 1; display: grid; place-items: center; text-align: center; border-radius: 50%; border: 1px solid rgba(94,231,231,.45); background: radial-gradient(circle, rgba(94,231,231,.2), var(--surface) 68%); box-shadow: 0 0 80px rgba(94,231,231,.15); font-weight: 800; }
    @keyframes spin { to { transform: rotate(360deg); } }
    section { scroll-margin-top: 30px; }
    .section { padding: 96px 0; border-top: 1px solid var(--line); }
    .section-heading { display: grid; grid-template-columns: .8fr 1.2fr; gap: 50px; align-items: end; margin-bottom: 42px; }
    h2 { margin: 8px 0 0; font-size: clamp(2rem, 4vw, 3.2rem); letter-spacing: -.055em; line-height: 1.05; }
    .section-copy { color: var(--muted); line-height: 1.7; margin: 0; max-width: 680px; }
    .principles { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
    .panel { border: 1px solid var(--line); border-radius: 18px; background: var(--panel); box-shadow: var(--shadow); }
    .principle { padding: 24px; }
    .number { color: var(--blue); font-family: ui-monospace, monospace; font-size: .72rem; }
    h3 { margin: 18px 0 9px; font-size: 1.05rem; }
    .principle p, .module p, .update p { color: var(--muted); line-height: 1.6; font-size: .9rem; margin: 0; }
    .modules { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
    .module { padding: 22px; min-height: 175px; position: relative; overflow: hidden; }
    .module::after { content: ""; position: absolute; inset: auto -45px -55px auto; width: 120px; height: 120px; border: 1px solid var(--line); border-radius: 50%; }
    .module.core-module { border-color: rgba(94,231,231,.35); background: linear-gradient(145deg, rgba(94,231,231,.09), var(--panel)); }
    .module-top { display: flex; align-items: center; justify-content: space-between; }
    .icon { color: var(--cyan); font-family: ui-monospace, monospace; font-size: .8rem; }
    .tag { color: var(--muted); border: 1px solid var(--line); border-radius: 999px; padding: 4px 8px; font-size: .64rem; text-transform: uppercase; letter-spacing: .08em; }
    .tag.live { color: var(--success); }
    .chat-layout { display: grid; grid-template-columns: .7fr 1.3fr; gap: 34px; align-items: start; }
    .chat-note { position: sticky; top: 20px; }
    .security-list { margin: 28px 0 0; padding: 0; list-style: none; display: grid; gap: 14px; color: var(--muted); font-size: .86rem; }
    .security-list li { display: flex; gap: 10px; } .check { color: var(--success); }
    .chat { overflow: hidden; }
    .chat-header { padding: 17px 20px; border-bottom: 1px solid var(--line); display: flex; justify-content: space-between; gap: 12px; align-items: center; }
    .chat-title { font-weight: 750; font-size: .9rem; } .connection { color: var(--muted); font-size: .72rem; }
    .chat-messages { height: 380px; overflow-y: auto; padding: 22px; display: flex; flex-direction: column; gap: 16px; background: rgba(4,8,15,.48); }
    .message { max-width: 82%; }
    .message.user { align-self: flex-end; } .message.assistant { align-self: flex-start; }
    .message-label { color: var(--muted); font-size: .65rem; text-transform: uppercase; letter-spacing: .1em; margin: 0 0 6px 3px; }
    .bubble { padding: 13px 15px; border: 1px solid var(--line); border-radius: 4px 14px 14px 14px; background: var(--panel-strong); white-space: pre-wrap; overflow-wrap: anywhere; line-height: 1.55; font-size: .9rem; }
    .user .bubble { border-radius: 14px 4px 14px 14px; background: var(--blue-soft); border-color: rgba(104,168,255,.28); }
    .typing { display: inline-flex; gap: 5px; align-items: center; min-height: 16px; }
    .typing i { width: 5px; height: 5px; border-radius: 50%; background: var(--muted); animation: pulse 1s infinite alternate; }
    .typing i:nth-child(2) { animation-delay: .2s; } .typing i:nth-child(3) { animation-delay: .4s; }
    @keyframes pulse { to { opacity: .25; transform: translateY(-2px); } }
    .chat-error { display: none; margin: 0; padding: 10px 20px; color: var(--danger); background: rgba(255,130,146,.07); border-top: 1px solid rgba(255,130,146,.18); font-size: .78rem; }
    .chat-error.visible { display: block; }
    .composer { padding: 15px; border-top: 1px solid var(--line); }
    .composer-row { display: flex; gap: 10px; align-items: end; }
    textarea { width: 100%; min-height: 46px; max-height: 130px; resize: vertical; padding: 12px 14px; color: var(--text); background: #080e18; border: 1px solid var(--line); border-radius: 10px; }
    textarea::placeholder { color: #66758a; } textarea:disabled { opacity: .55; cursor: not-allowed; }
    .send { min-width: 80px; height: 46px; border: 0; border-radius: 10px; color: #04101d; background: linear-gradient(135deg, var(--cyan), var(--blue)); font-weight: 800; cursor: pointer; }
    .send:disabled { opacity: .45; cursor: not-allowed; }
    .composer-meta { display: flex; justify-content: space-between; gap: 8px; margin-top: 9px; color: var(--muted); font-size: .68rem; }
    .roadmap { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; }
    .phase { padding: 23px; border-top: 1px solid var(--line); position: relative; }
    .phase::before { content: ""; position: absolute; width: 7px; height: 7px; border-radius: 50%; background: var(--blue); top: -4px; left: 23px; box-shadow: 0 0 12px var(--blue); }
    .phase p { color: var(--muted); line-height: 1.55; font-size: .82rem; }
    .phase-label { color: var(--blue); font: .7rem ui-monospace, monospace; }
    .updates-grid { display: grid; grid-template-columns: 1.4fr .6fr; gap: 14px; }
    .update { padding: 25px; } .update time { color: var(--blue); font-size: .72rem; }
    .community { padding: 34px; display: flex; justify-content: space-between; gap: 30px; align-items: center; background: linear-gradient(130deg, rgba(169,140,255,.1), var(--panel)); }
    .community p { margin: 8px 0 0; color: var(--muted); }
    .disabled-link { opacity: .55; cursor: not-allowed; }
    footer { padding: 34px 0 46px; border-top: 1px solid var(--line); display: flex; justify-content: space-between; gap: 20px; color: var(--muted); font-size: .75rem; }
    .footer-links { display: flex; flex-wrap: wrap; gap: 18px; } .footer-links span { color: #718096; }
    @media (max-width: 900px) {
      .nav a { display: none; } .hero { grid-template-columns: 1fr; gap: 10px; padding-top: 85px; }
      .core-map { min-height: 330px; } .section-heading, .chat-layout { grid-template-columns: 1fr; }
      .chat-note { position: static; } .modules { grid-template-columns: repeat(2, 1fr); }
      .roadmap { grid-template-columns: repeat(2, 1fr); row-gap: 30px; }
    }
    @media (max-width: 600px) {
      .shell { width: min(100% - 24px, 1160px); } .site-header { min-height: 66px; }
      .status-pill { font-size: 0; padding: 10px; } .status-pill .dot { width: 8px; height: 8px; }
      .hero { min-height: auto; padding: 68px 0; } h1 { font-size: clamp(3rem, 17vw, 4.4rem); }
      .core-map { transform: scale(.82); margin: -25px; } .section { padding: 70px 0; }
      .principles, .modules, .roadmap, .updates-grid { grid-template-columns: 1fr; }
      .roadmap { gap: 28px; } .message { max-width: 94%; } .chat-messages { height: 400px; padding: 16px; }
      .composer-row { align-items: stretch; flex-direction: column; } .send { width: 100%; }
      .community, footer { align-items: flex-start; flex-direction: column; }
    }
    @media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } .orbit, .typing i { animation: none; } }
  </style>
</head>
<body>
  <header class="shell site-header">
    <a class="brand" href="#top" aria-label="NexusAI home"><span class="brand-mark">N</span><span>Nexus<span>AI</span></span></a>
    <nav class="nav" aria-label="Primary navigation"><a href="#vision">Vision</a><a href="#modules">Modules</a><a href="#chatbox">Chatbox</a><a href="#roadmap">Roadmap</a></nav>
    <span class="status-pill"><span class="dot"></span>Local gateway · 127.0.0.1</span>
  </header>

  <main id="top" class="shell">
    <section class="hero" aria-labelledby="page-title">
      <div><div class="eyebrow">A modular intelligence ecosystem</div><h1 id="page-title">One core.<br><span class="gradient">Many capabilities.</span></h1>
        <p class="lede">NexusAI is a long-term system designed to understand, coordinate, and evolve—connecting independent modules around one central intelligence while keeping the Founder in control.</p>
        <div class="actions"><a class="button button-primary" href="#chatbox">Open local chat</a><a class="button button-secondary" href="#modules">Explore the system</a></div>
      </div>
      <div class="core-map" role="img" aria-label="A central NexusAI core connected through two modular orbits"><div class="orbit"></div><div class="orbit"></div><div class="core">NEXUS<br>CORE</div></div>
    </section>

    <section id="vision" class="section"><div class="section-heading"><div><div class="eyebrow">The vision</div><h2>Built as a system,<br>not a single app.</h2></div><p class="section-copy">Every capability remains an independent, testable module. The Core understands context and coordinates work; adapters connect platforms without defining the intelligence itself.</p></div>
      <div class="principles"><article class="panel principle"><span class="number">01 / INTELLIGENCE</span><h3>Understand before acting</h3><p>Reason about intent, context, consequences, and the place of each request in the wider ecosystem.</p></article><article class="panel principle"><span class="number">02 / MODULARITY</span><h3>Capabilities without coupling</h3><p>Add, isolate, test, or disable modules without rebuilding the central intelligence.</p></article><article class="panel principle"><span class="number">03 / CONTROL</span><h3>Founder authority by design</h3><p>Explain sensitive actions, require confirmation, and keep permissions explicit and reviewable.</p></article></div>
    </section>

    <section id="modules" class="section"><div class="section-heading"><div><div class="eyebrow">System map</div><h2>The ecosystem</h2></div><p class="section-copy">A shared event and API layer allows modules to communicate while preserving clear boundaries, limited permissions, and independent evolution.</p></div>
      <div class="modules">
        <article class="panel module core-module"><div class="module-top"><span class="icon">◉ CORE</span><span class="tag live">Foundation</span></div><h3>Central intelligence</h3><p>Understanding, reasoning, decisions, and orchestration—kept independent from every platform.</p></article>
        <article class="panel module"><div class="module-top"><span class="icon">›_ CHAT</span><span class="tag live">Prototype</span></div><h3>Chatbox</h3><p>A focused interface for local model conversations through the protected gateway.</p></article>
        <article class="panel module"><div class="module-top"><span class="icon">◇ MEMORY</span><span class="tag">Planned</span></div><h3>Memory</h3><p>Conversation context, durable decisions, technical history, and a project knowledge base.</p></article>
        <article class="panel module"><div class="module-top"><span class="icon">↻ AUTO</span><span class="tag">Future</span></div><h3>Automation</h3><p>Permission-aware workflows, service checks, notifications, and reversible routines.</p></article>
        <article class="panel module"><div class="module-top"><span class="icon"># DISCORD</span><span class="tag">Future</span></div><h3>Discord</h3><p>Community operations, moderation, support, and events through a bounded adapter.</p></article>
        <article class="panel module"><div class="module-top"><span class="icon">⌘ CODEX</span><span class="tag">Future</span></div><h3>GitHub Codex</h3><p>Reviewed development workflows for repositories, issues, tests, and pull requests.</p></article>
        <article class="panel module"><div class="module-top"><span class="icon">▦ MINECRAFT</span><span class="tag">Future</span></div><h3>Minecraft</h3><p>Game events, alerts, commands, and protections behind an independent integration.</p></article>
        <article class="panel module"><div class="module-top"><span class="icon">⬡ XR / OS</span><span class="tag">Vision</span></div><h3>VR &amp; Desktop</h3><p>Immersive and native control surfaces for understanding the ecosystem at a glance.</p></article>
        <article class="panel module"><div class="module-top"><span class="icon">↔ API</span><span class="tag">Evolving</span></div><h3>API layer</h3><p>Versioned, secured communication for commands, state, memory, and module events.</p></article>
      </div>
    </section>

    <section id="chatbox" class="section"><div class="chat-layout"><div class="chat-note"><div class="eyebrow">Local prototype</div><h2>Talk to the local model.</h2><p class="section-copy">The chatbox detects models served by local Ollama and sends requests only through this same-origin, loopback gateway. If no model is available, it stays honest and disconnected.</p>
        <ul class="security-list"><li><span class="check">✓</span>No API keys or secrets in the browser</li><li><span class="check">✓</span>Input is trimmed and limited to 2,000 characters</li><li><span class="check">✓</span>Messages render as text, never executable HTML</li></ul></div>
        <div class="panel chat" aria-label="NexusAI local chat prototype"><div class="chat-header"><div><div class="chat-title">NexusAI Chatbox</div><div id="connection" class="connection" role="status">Checking local model connection…</div></div><select id="model-select" aria-label="Local AI model" disabled><option>Detecting models…</option></select></div>
          <div id="chat-messages" class="chat-messages" aria-live="polite"><div class="message assistant"><div class="message-label">NexusAI · Local gateway</div><div class="bubble">This is an early local prototype. Select an available model to begin; no conversation is stored by this interface.</div></div></div>
          <p id="chat-error" class="chat-error" role="alert"></p>
          <form id="chat-form" class="composer"><div class="composer-row"><textarea id="prompt" rows="1" maxlength="2000" placeholder="Waiting for a local model…" aria-label="Message" disabled></textarea><button id="send" class="send" type="submit" disabled>Send</button></div><div class="composer-meta"><span>Enter to send · Shift + Enter for a new line</span><span id="count">0 / 2000</span></div></form>
        </div></div>
    </section>

    <section id="roadmap" class="section"><div class="section-heading"><div><div class="eyebrow">Long-term direction</div><h2>Roadmap</h2></div><p class="section-copy">Progress happens in deliberate phases. Dates are not promised; each layer earns the right to support the next.</p></div>
      <div class="roadmap"><article class="phase"><span class="phase-label">PHASE 01 · ACTIVE</span><h3>Foundations</h3><p>Identity, governance, secure local gateway, core primitives, and protected history.</p></article><article class="phase"><span class="phase-label">PHASE 02</span><h3>Functional Core</h3><p>Configuration, permissions, memory foundations, logging, and module communication.</p></article><article class="phase"><span class="phase-label">PHASE 03</span><h3>Interfaces</h3><p>Dashboard, local models, reviewed automation, Discord, and GitHub adapters.</p></article><article class="phase"><span class="phase-label">PHASE 04</span><h3>Intelligent agents</h3><p>Specialized agents coordinated by the Core with bounded permissions and verification.</p></article></div>
    </section>

    <section id="updates" class="section"><div class="section-heading"><div><div class="eyebrow">Project signal</div><h2>Updates</h2></div><p class="section-copy">A transparent record of real milestones. No invented customer counts, launch dates, or production claims.</p></div><div class="updates-grid"><article class="panel update"><time>Current foundation</time><h3>The local gateway has a clearer public face</h3><p>The dashboard now explains the modular architecture and offers an honest local chat prototype with connection, loading, and error feedback.</p></article><article class="panel update"><time>Next signal</time><h3>Core ↔ module contract</h3><p>Define a stable, tested communication boundary before adding platform integrations.</p></article></div></section>

    <section class="section"><div class="panel community"><div><div class="eyebrow">Discord community</div><h3>Build the ecosystem with us.</h3><p>The public community space is planned. No private or unverified invite is published here.</p></div><span class="button button-secondary disabled-link" aria-disabled="true">Invite coming later</span></div></section>
  </main>

  <footer class="shell"><div><strong>NexusAI</strong> · Founded by Damien<br>Built to evolve without losing its center.</div><div class="footer-links"><a href="/docs">Local API docs</a><a href="#updates">Updates</a><span>Privacy · placeholder</span><span>Terms · placeholder</span></div></footer>

  <script>
    (() => {
      'use strict';
      const MAX_LENGTH = 2000;
      const messages = document.getElementById('chat-messages');
      const form = document.getElementById('chat-form');
      const prompt = document.getElementById('prompt');
      const send = document.getElementById('send');
      const modelSelect = document.getElementById('model-select');
      const connection = document.getElementById('connection');
      const errorBox = document.getElementById('chat-error');
      const count = document.getElementById('count');
      let history = [];
      let busy = false;

      function setError(message = '') {
        errorBox.textContent = message;
        errorBox.classList.toggle('visible', Boolean(message));
      }
      function addMessage(role, content, loading = false) {
        const wrapper = document.createElement('div');
        wrapper.className = `message ${role}`;
        const label = document.createElement('div');
        label.className = 'message-label';
        label.textContent = role === 'user' ? 'You' : 'NexusAI · Local model';
        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        if (loading) {
          bubble.className += ' typing';
          bubble.setAttribute('aria-label', 'Local model is responding');
          for (let index = 0; index < 3; index += 1) bubble.appendChild(document.createElement('i'));
        } else {
          bubble.textContent = content;
        }
        wrapper.append(label, bubble);
        messages.appendChild(wrapper);
        messages.scrollTop = messages.scrollHeight;
        return wrapper;
      }
      function setEnabled(enabled) {
        prompt.disabled = !enabled || busy;
        send.disabled = !enabled || busy;
        modelSelect.disabled = !enabled || busy;
      }
      async function loadModels() {
        try {
          const response = await fetch('/api/tags', { headers: { Accept: 'application/json' } });
          if (!response.ok) throw new Error('Model discovery failed');
          const data = await response.json();
          const names = Array.isArray(data.models) ? data.models.map(item => item && item.name).filter(name => typeof name === 'string' && name.trim()).slice(0, 100) : [];
          modelSelect.replaceChildren();
          if (!names.length) throw new Error('No local models detected');
          for (const name of names) {
            const option = document.createElement('option');
            option.value = name;
            option.textContent = name;
            modelSelect.appendChild(option);
          }
          connection.textContent = `${names.length} local model${names.length === 1 ? '' : 's'} available`;
          prompt.placeholder = 'Message the selected local model…';
          setEnabled(true);
        } catch (error) {
          modelSelect.replaceChildren(new Option('No local model', ''));
          connection.textContent = 'Disconnected · prototype mode';
          prompt.placeholder = 'Start Ollama with a local model to enable chat';
          setEnabled(false);
        }
      }
      prompt.addEventListener('input', () => { count.textContent = `${prompt.value.length} / ${MAX_LENGTH}`; });
      prompt.addEventListener('keydown', event => {
        if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); form.requestSubmit(); }
      });
      form.addEventListener('submit', async event => {
        event.preventDefault();
        const content = prompt.value.trim();
        const model = modelSelect.value;
        if (busy || !model || !content) return;
        if (content.length > MAX_LENGTH) { setError('Message is too long. Keep it under 2,000 characters.'); return; }
        setError(); addMessage('user', content); history.push({ role: 'user', content });
        prompt.value = ''; count.textContent = `0 / ${MAX_LENGTH}`; busy = true; setEnabled(true);
        const loadingMessage = addMessage('assistant', '', true);
        try {
          const response = await fetch('/api/chat', {
            method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
            body: JSON.stringify({ model, messages: history.slice(-20), stream: false })
          });
          if (!response.ok) throw new Error(response.status === 502 ? 'The local model service is unavailable.' : 'The local gateway could not complete this request.');
          const data = await response.json();
          const reply = data && data.message && typeof data.message.content === 'string' ? data.message.content.trim() : '';
          if (!reply) throw new Error('The local model returned an empty response.');
          loadingMessage.remove(); addMessage('assistant', reply); history.push({ role: 'assistant', content: reply });
        } catch (error) {
          loadingMessage.remove(); setError(error instanceof Error ? error.message : 'An unexpected local error occurred.');
        } finally { busy = false; setEnabled(Boolean(modelSelect.value)); prompt.focus(); }
      });
      loadModels();
    })();
  </script>
</body>
</html>"""
