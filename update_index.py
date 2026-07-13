import re

with open('index.html', 'r') as f:
    content = f.read()

# Define the new HTML and CSS block
new_block = """
<!-- ═══════════════════════════════════════════
     HOME PAGE EXTENSIONS
     ═══════════════════════════════════════════ -->
<style>
/* MANIFESTO */
.manifesto-section { height: 150vh; background: var(--void); position: relative; }
.manifesto-scroll-container {
  position: sticky; top: 0; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden;
}
.manifesto-text {
  font-family: 'Bebas Neue', sans-serif; font-size: 8vw; line-height: 0.9; text-align: center;
  color: var(--ink-dim); text-transform: uppercase;
  background: linear-gradient(180deg, #fff 0%, rgba(255,255,255,0.2) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  padding: 0 24px;
}
.manifesto-highlight {
  color: var(--gold); background: linear-gradient(90deg, #c9a15a 0%, #ffd700 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 10vw;
}

/* PATHWAY TO PRO */
.pathway-section { padding: 120px 24px; background: var(--void-2); border-top: 1px solid var(--line); }
.pathway-header { text-align: center; margin-bottom: 80px; }
.pathway-header h2 { font-family: 'Bebas Neue', sans-serif; font-size: 64px; color: #fff; }
.pathway-header p { color: var(--gold); font-family: monospace; text-transform: uppercase; letter-spacing:0.1em;}
.pathway-container { max-width: 800px; margin: 0 auto; position: relative; }
.pathway-line { position: absolute; left: 50%; top: 0; bottom: 0; width: 2px; background: var(--line); transform: translateX(-50%); }
.pathway-glow {
  position: absolute; top: 0; left: -1px; width: 4px; height: 150px; background: var(--gold);
  box-shadow: 0 0 15px var(--gold); animation: flowDown 6s infinite linear;
}
@keyframes flowDown { 0% { top: 0; opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { top: 100%; opacity: 0; } }
.pathway-step { display: flex; justify-content: flex-end; padding-right: 50%; position: relative; margin-bottom: 60px; }
.pathway-step.right { justify-content: flex-start; padding-right: 0; padding-left: 50%; }
.step-dot {
  position: absolute; left: 50%; top: 0; width: 16px; height: 16px; border-radius: 50%;
  background: var(--void); border: 2px solid var(--gold); transform: translateX(-50%); z-index: 2;
  box-shadow: 0 0 10px rgba(201,161,90,0.5);
}
.step-content {
  width: 85%; background: rgba(255,255,255,0.02); border: 1px solid var(--line);
  padding: 32px; border-radius: 8px; position: relative; backdrop-filter: blur(10px); transition: border-color 0.3s;
}
.step-content:hover { border-color: var(--gold); }
.pathway-step.left .step-content { margin-right: 40px; text-align: right; }
.pathway-step.right .step-content { margin-left: 40px; text-align: left; }
.step-age { font-family: monospace; color: var(--gold); font-size: 14px; margin-bottom: 8px; letter-spacing:0.05em; }
.step-content h3 { font-size: 24px; color: #fff; margin-bottom: 12px; }
.step-content p { color: var(--ink-dim); font-size: 15px; line-height: 1.6; }

/* METRICS DASHBOARD */
.metrics-section { padding: 120px 24px; background: var(--void); border-top: 1px solid var(--line); }
.metrics-header { text-align: center; margin-bottom: 60px; }
.metrics-header h2 { font-family: 'Bebas Neue', sans-serif; font-size: 64px; color: #fff; }
.metrics-header p { color: var(--gold); font-family: monospace; text-transform: uppercase; letter-spacing:0.1em; }
.dashboard-mockup {
  max-width: 1000px; margin: 0 auto; background: rgba(10,10,12,0.8); border: 1px solid var(--line);
  border-radius: 12px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); backdrop-filter: blur(20px); overflow: hidden;
}
.dash-top { display: flex; align-items: center; padding: 12px 20px; border-bottom: 1px solid var(--line); background: rgba(255,255,255,0.02); }
.dash-dot { width: 10px; height: 10px; border-radius: 50%; background: var(--line); margin-right: 8px; }
.dash-dot:nth-child(1) { background: #ff5f56; }
.dash-dot:nth-child(2) { background: #ffbd2e; }
.dash-dot:nth-child(3) { background: #27c93f; }
.dash-title { margin-left: auto; font-family: monospace; color: var(--ink-dim); font-size: 12px; letter-spacing: 0.1em; }
.dash-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: var(--line); }
.dash-card { background: rgba(10,10,12,1); padding: 32px; display: flex; flex-direction: column; justify-content:center;}
.dash-label { font-family: monospace; color: var(--ink-dim); text-transform: uppercase; font-size: 12px; letter-spacing: 0.05em; margin-bottom: 24px; }
.radar-container { width: 100%; aspect-ratio: 1; display: flex; align-items: center; justify-content: center; }
.radar-container svg { width: 80%; height: 80%; filter: drop-shadow(0 0 10px rgba(201,161,90,0.3)); }
.bar-row { display: flex; align-items: center; margin-bottom: 16px; font-family: monospace; font-size: 13px; }
.bar-lbl { width: 60px; color: #fff; }
.bar-track { flex: 1; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; margin: 0 12px; overflow: hidden; }
.bar-fill { height: 100%; background: var(--gold); box-shadow: 0 0 10px var(--gold); }
.bar-val { width: 30px; text-align: right; color: var(--gold); }
.flex-center { align-items: center; justify-content: center; text-align: center; }
.dash-huge-num { font-family: 'Bebas Neue', sans-serif; font-size: 80px; color: #fff; line-height: 1; text-shadow: 0 0 20px rgba(255,255,255,0.2); }
.dash-huge-num span { font-size: 40px; color: var(--gold); }
.dash-trend { color: #27c93f; font-family: monospace; font-size: 12px; margin-top: 16px; }
.metrics-cta { text-align: center; margin-top: 60px; }

@media(max-width: 900px) {
  .manifesto-text { font-size: 14vw; }
  .manifesto-highlight { font-size: 16vw; }
  .pathway-line { left: 20px; }
  .pathway-step, .pathway-step.right { padding: 0 0 0 50px; justify-content: flex-start; }
  .step-dot { left: 20px; }
  .pathway-step.left .step-content, .pathway-step.right .step-content { margin: 0; text-align: left; width: 100%; }
  .dash-grid { grid-template-columns: 1fr; }
}
</style>

<!-- SECTION 3 — MANIFESTO -->
<section class="manifesto-section">
  <div class="manifesto-scroll-container">
    <div class="manifesto-text">
      We don't just train cricketers.<br>
      <span class="manifesto-highlight">We engineer athletes.</span>
    </div>
  </div>
</section>

<!-- SECTION 4 — PATHWAY TO PRO -->
<section class="pathway-section">
  <div class="pathway-header">
    <h2>The Pipeline</h2>
    <p>A structured roadmap from basics to elite performance</p>
  </div>
  <div class="pathway-container">
    <div class="pathway-line">
      <div class="pathway-glow"></div>
    </div>
    <div class="pathway-step left">
      <div class="step-dot"></div>
      <div class="step-content">
        <div class="step-age">Ages 6–10</div>
        <h3>The Foundation</h3>
        <p>Mastering biomechanics, grip, stance, and a love for the game. Building the right muscle memory from day one.</p>
      </div>
    </div>
    <div class="pathway-step right">
      <div class="step-dot"></div>
      <div class="step-content">
        <div class="step-age">Ages 11–15</div>
        <h3>The Crucible</h3>
        <p>Tactical awareness, match simulations, and specialized role development. Learning to read the game under pressure.</p>
      </div>
    </div>
    <div class="pathway-step left">
      <div class="step-dot"></div>
      <div class="step-content">
        <div class="step-age">Ages 16+</div>
        <h3>The Elite Roster</h3>
        <p>High-performance conditioning, mental toughness, and league/state preparation. Transitioning directly into professional cricket.</p>
      </div>
    </div>
  </div>
</section>

<!-- SECTION 5 — THE METRICS -->
<section class="metrics-section">
  <div class="metrics-header">
    <h2>Data-Driven Edge</h2>
    <p>We measure what matters.</p>
  </div>
  <div class="dashboard-mockup">
    <div class="dash-top">
      <div class="dash-dot"></div><div class="dash-dot"></div><div class="dash-dot"></div>
      <div class="dash-title">PERFORMANCE_ANALYTICS_V2</div>
    </div>
    <div class="dash-grid">
      <div class="dash-card">
        <div class="dash-label">Biomechanics Efficiency</div>
        <div class="radar-container">
          <svg viewBox="0 0 100 100">
            <polygon points="50,10 90,30 90,70 50,90 10,70 10,30" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
            <polygon points="50,30 70,40 70,60 50,70 30,60 30,40" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
            <polygon points="50,15 80,45 60,80 30,65 20,35" fill="rgba(201,161,90,0.3)" stroke="var(--gold)" stroke-width="1.5"/>
            <circle cx="50" cy="15" r="2" fill="#fff"/><circle cx="80" cy="45" r="2" fill="#fff"/>
            <circle cx="60" cy="80" r="2" fill="#fff"/><circle cx="30" cy="65" r="2" fill="#fff"/>
            <circle cx="20" cy="35" r="2" fill="#fff"/>
          </svg>
        </div>
      </div>
      <div class="dash-card">
        <div class="dash-label">Impact Velocity</div>
        <div class="bar-chart">
          <div class="bar-row"><div class="bar-lbl">Bat Spd</div><div class="bar-track"><div class="bar-fill" style="width:85%"></div></div><div class="bar-val">85%</div></div>
          <div class="bar-row"><div class="bar-lbl">Release</div><div class="bar-track"><div class="bar-fill" style="width:92%"></div></div><div class="bar-val">92%</div></div>
          <div class="bar-row"><div class="bar-lbl">React</div><div class="bar-track"><div class="bar-fill" style="width:78%"></div></div><div class="bar-val">78%</div></div>
        </div>
      </div>
      <div class="dash-card flex-center">
        <div class="dash-label">Session Intensity</div>
        <div class="dash-huge-num">94<span>%</span></div>
        <div class="dash-trend">▲ +2.4% vs last week</div>
      </div>
    </div>
  </div>
  <div class="metrics-cta">
    <a href="programs.html#apply" class="btn btn--ember">Start Your Journey</a>
  </div>
</section>
"""

# Insert right after `</section>` of hero-founder
split_marker = "</section>\n\n\n<script>"
if split_marker in content:
    new_content = content.replace(split_marker, f"</section>\n\n{new_block}\n\n<script>")
    with open('index.html', 'w') as f:
        f.write(new_content)
    print("Successfully updated index.html")
else:
    print("Could not find the insertion marker in index.html")

