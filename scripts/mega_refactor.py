import re
import sys

def refactor_about():
    print("Refactoring about.html...")
    with open('about.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove the roster CSS
    # From: /* Wall of Fame */ or similar to the end of .roster-stat h3 block
    css_pattern = r'(\s*/\* Wall of Fame \*/[\s\S]*?\.roster-stat h3\s*\{[\s\S]*?\})'
    if not re.search(css_pattern, content):
        css_pattern = r'(\s*/\*\s*═══════════════════════════════════════════════\s*USA CRICKET NATIONALS[\s\S]*?\.roster-stat h3\s*\{[\s\S]*?\})'
    
    if re.search(css_pattern, content):
        content = re.sub(css_pattern, '', content)
    else:
        print("Warning: Could not find roster CSS in about.html")
        # Try generic fallback
        content = re.sub(r'(\s*\.roster-section\s*\{[\s\S]*?\.roster-stat h3\s*\{[\s\S]*?\})', '', content)

    # Remove the roster HTML
    html_pattern = r'(<!-- (WALL OF FAME|USA CRICKET NATIONALS) -->[\s\S]*?</section>)'
    if re.search(html_pattern, content):
        content = re.sub(html_pattern, '', content)
    else:
        print("Warning: Could not find roster HTML in about.html")

    # Remove intersection observer JS if it exists
    js_pattern = r'(\s*// Ember bar reveal for player cards[\s\S]*?playerObserver\.observe\(card\)\);)'
    if re.search(js_pattern, content):
        content = re.sub(js_pattern, '', content)

    with open('about.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Done about.html")

def refactor_index():
    print("Refactoring index.html...")
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Pipeline modifications
    old_glow_css = r'\.pathway-glow\s*\{[\s\S]*?animation:\s*flowDown[\s\S]*?\}'
    new_glow_css = r'''  .pathway-glow {
    position:absolute; top:0; left:-15px; width:30px; height:120px;
    animation: flowDown 4s linear infinite;
    display: flex; flex-direction: column; align-items: center; justify-content: flex-end;
  }
  .fire-ball {
    width: 16px; height: 16px; background: var(--ember-glow); border-radius: 50%;
    box-shadow: 0 0 10px 4px rgba(255,86,34,0.6), 0 0 20px 8px rgba(226,56,10,0.4);
    position: relative; z-index: 2;
  }
  .fire-tail {
    width: 4px; height: 100px;
    background: linear-gradient(to bottom, transparent, var(--ember-glow));
    margin-bottom: -8px; position: relative; z-index: 1;
  }'''
    if re.search(old_glow_css, content):
        content = re.sub(old_glow_css, new_glow_css, content)
    else:
        print("Warning: Could not find pathway-glow CSS in index.html")

    old_glow_html = r'<div class="pathway-glow"></div>'
    new_glow_html = r'''<div class="pathway-glow">
        <div class="fire-tail"></div>
        <div class="fire-ball"></div>
      </div>'''
    if old_glow_html in content:
        content = content.replace(old_glow_html, new_glow_html)
    else:
        print("Warning: Could not find pathway-glow HTML in index.html")

    # 2. Add New Dashboard Charts to .dash-grid
    new_charts = r'''      <div class="dash-card">
        <div class="dash-label">Worm Line: Match Progression</div>
        <div class="worm-container" style="height:120px; position:relative; margin-top:20px;">
          <svg viewBox="0 0 100 50" style="width:100%; height:100%; overflow:visible;">
             <polyline points="0,45 10,40 20,42 30,30 40,32 50,20 60,18 70,10 80,12 90,5 100,2" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="1.5" stroke-dasharray="2,2"/>
             <polyline points="0,48 10,45 20,38 30,35 40,25 50,28 60,15 70,12 80,5 90,8 100,0" fill="none" stroke="var(--gold)" stroke-width="2" style="filter: drop-shadow(0 4px 6px rgba(201,161,90,0.5));"/>
             <circle cx="100" cy="0" r="2" fill="var(--ember-glow)"/>
          </svg>
        </div>
      </div>
      <div class="dash-card">
        <div class="dash-label">Shot Distribution (Histogram)</div>
        <div class="histogram" style="display:flex; align-items:flex-end; gap:4px; height:120px; margin-top:20px; border-bottom:1px solid rgba(255,255,255,0.1);">
           <div style="flex:1; background:var(--gold); height:20%; opacity:0.6;"></div>
           <div style="flex:1; background:var(--gold); height:40%; opacity:0.7;"></div>
           <div style="flex:1; background:var(--gold); height:85%; filter: drop-shadow(0 0 8px var(--gold));"></div>
           <div style="flex:1; background:var(--gold); height:60%; opacity:0.8;"></div>
           <div style="flex:1; background:var(--gold); height:30%; opacity:0.6;"></div>
           <div style="flex:1; background:var(--gold); height:50%; opacity:0.7;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:9px; color:var(--ink-dim); margin-top:8px;">
          <span>Cover</span><span>Point</span><span>Mid</span><span>Square</span><span>Fine</span><span>Long</span>
        </div>
      </div>
      <div class="dash-card flex-center">
        <div class="dash-label">Wicket Type (Pie Chart)</div>
        <div class="pie-chart" style="width:100px; height:100px; border-radius:50%; background: conic-gradient(var(--ember) 0% 60%, var(--gold) 60% 85%, var(--void-2) 85% 100%); margin-top:16px; position:relative; box-shadow: 0 4px 12px rgba(0,0,0,0.5);">
          <div style="position:absolute; inset:20px; background:var(--void-2); border-radius:50%; display:flex; align-items:center; justify-content:center; font-family:'Bebas Neue', sans-serif; font-size:24px; color:var(--ink);">60%</div>
        </div>
        <div style="display:flex; gap:12px; margin-top:16px; font-size:10px; color:var(--ink-dim);">
           <span style="display:flex; align-items:center; gap:4px;"><span style="width:8px;height:8px;background:var(--ember);border-radius:2px;"></span>Bowled</span>
           <span style="display:flex; align-items:center; gap:4px;"><span style="width:8px;height:8px;background:var(--gold);border-radius:2px;"></span>Caught</span>
        </div>
      </div>
    </div>'''
    dash_grid_end = r'    </div>\n  </div>\n  <div class="metrics-cta">'
    if re.search(dash_grid_end, content):
        content = re.sub(r'(\s*</div>\n\s*</div>\n\s*<div class="metrics-cta">)', '\n' + new_charts + r'\n  </div>\n  <div class="metrics-cta">', content)
    else:
        print("Warning: Could not find end of dash-grid in index.html")

    # 3. Add Roster CSS to index.html style block
    roster_css = '''
  /* ═══════════════════════════════════════════════
     USA CRICKET NATIONALS — Scroll-Snap Roster Strip
     ═══════════════════════════════════════════════ */
  .roster-section {
    padding: 100px 0 120px; background: #0a0806; position: relative; border-top: 1px solid var(--line); overflow: hidden;
  }
  .roster-header { padding: 0 clamp(24px, 5vw, 80px); margin-bottom: 56px; }
  .roster-eyebrow {
    font-size: 11px; text-transform: uppercase; letter-spacing: 0.22em; color: var(--ember); font-weight: 700;
    margin-bottom: 16px; display: flex; align-items: center; gap: 12px;
  }
  .roster-eyebrow::before { content: ''; display: block; width: 32px; height: 1px; background: var(--ember); }
  .roster-header h2 { font-family: 'Bebas Neue', sans-serif; font-size: clamp(40px, 6vw, 72px); color: var(--ink); letter-spacing: 0.02em; line-height: 0.9; max-width: 700px; }
  .roster-header p { color: var(--ink-dim); font-size: 15px; line-height: 1.6; margin-top: 20px; max-width: 560px; }
  .roster-strip {
    display: flex; gap: 24px; padding: 0 clamp(24px, 5vw, 80px) 40px;
    overflow-x: auto; scroll-snap-type: x mandatory; -webkit-overflow-scrolling: touch; scrollbar-width: none;
  }
  .roster-strip::-webkit-scrollbar { display: none; }
  .player-card {
    flex: 0 0 clamp(260px, 75vw, 320px); scroll-snap-align: center;
    position: relative; border-radius: 8px; overflow: hidden; background: var(--void-2);
    --bar-scale: 0; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  }
  .player-img { aspect-ratio: 3 / 4; position: relative; overflow: hidden; }
  .player-img img {
    width: 100%; height: 100%; object-fit: cover; object-position: center top; display: block;
    transition: transform 0.8s cubic-bezier(.16,1,.3,1);
  }
  @media (hover: hover) { .player-card:hover .player-img img { transform: scale(1.05); } }
  .player-img::after {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(to top, rgba(7,8,10,0.95) 0%, rgba(7,8,10,0.4) 40%, transparent 70%); pointer-events: none;
  }
  .player-info { position: absolute; bottom: 0; left: 0; right: 0; padding: 24px; z-index: 2; }
  .player-name { font-family: 'Bebas Neue', sans-serif; font-size: 32px; color: var(--ink); letter-spacing: 0.03em; line-height: 1; margin-bottom: 6px; }
  .player-cred { font-size: 11px; text-transform: uppercase; letter-spacing: 0.14em; color: var(--gold); font-weight: 600; }
  .player-card::after {
    content: ''; position: absolute; bottom: 0; left: 0; height: 4px; width: 100%;
    background: linear-gradient(90deg, var(--ember), var(--ember-glow));
    transform-origin: left; transform: scaleX(var(--bar-scale)); transition: transform 0.9s cubic-bezier(.16,1,.3,1);
  }
  .player-card.is-lit { --bar-scale: 1; }
  @media (min-width: 1200px) {
    .roster-strip { overflow-x: visible; flex-wrap: nowrap; justify-content: center; }
    .player-card { flex: 1 1 0; min-width: 0; }
  }
  .roster-stat {
    text-align: center; margin: 60px clamp(24px, 5vw, 80px) 0; padding: 32px 40px;
    border: 1px solid rgba(201,161,90, 0.18);
    background: radial-gradient(ellipse at center, rgba(201,161,90,0.04) 0%, transparent 70%);
    max-width: 800px; margin-left: auto; margin-right: auto;
  }
  .roster-stat h3 { font-family: 'Bebas Neue', sans-serif; font-size: clamp(28px, 4vw, 44px); color: var(--gold); letter-spacing: 0.05em; }
'''
    if '</style>' in content:
        content = content.replace('</style>', roster_css + '\n</style>')
    else:
        print("Warning: Could not find </style> in index.html")

    # 4. Add Roster HTML to index.html after metrics section
    roster_html = '''

  <!-- USA CRICKET NATIONALS -->
  <section class="roster-section">
    <div class="roster-header">
      <div class="roster-eyebrow">From This Academy</div>
      <h2>USA Cricket<br>National Representatives</h2>
      <p>Elite players coached at Bowncer Sportz who went on to wear the USA Cricket badge at the national level. The proof is in the names.</p>
    </div>
    <div class="roster-strip" id="rosterStrip">
      <div class="player-card js-player">
        <div class="player-img"><img src="assets/shiva_vashisht.webp" alt="Shiva Vashisht" loading="lazy" decoding="async"></div>
        <div class="player-info">
          <div class="player-name">Shiva Vashisht</div>
          <div class="player-cred">USA U-19 · National Captain</div>
        </div>
      </div>
      <div class="player-card js-player">
        <div class="player-img"><img src="assets/amogh.webp" alt="Amogh" loading="lazy" decoding="async"></div>
        <div class="player-info">
          <div class="player-name">Amogh</div>
          <div class="player-cred">USA Cricket · Cape Cobras</div>
        </div>
      </div>
      <div class="player-card js-player">
        <div class="player-img"><img src="assets/sanjay_stanley.webp" alt="Sanjay Stanley" loading="lazy" decoding="async"></div>
        <div class="player-info">
          <div class="player-name">Sanjay Stanley</div>
          <div class="player-cred">USA Cricket · Captain</div>
        </div>
      </div>
      <div class="player-card js-player">
        <div class="player-img"><img src="assets/utkarsh_srivastava.webp" alt="Utkarsh Srivastava" loading="lazy" decoding="async"></div>
        <div class="player-info">
          <div class="player-name">Utkarsh Srivastava</div>
          <div class="player-cred">USA Cricket</div>
        </div>
      </div>
      <div class="player-card js-player">
        <div class="player-img"><img src="assets/aaron_jones.webp" alt="Aaron Jones" loading="lazy" decoding="async"></div>
        <div class="player-info">
          <div class="player-name">Aaron Jones</div>
          <div class="player-cred">USA Cricket · ICC T20 World Cup</div>
        </div>
      </div>
    </div>
    <div class="roster-stat">
      <h3>5 National Representatives &amp; Counting</h3>
    </div>
  </section>
'''
    if '</section>' in content:
        # We need to insert it right after metrics-section
        metrics_end = r'(</section>\s*(?:<!--.*?-->\s*)?<script>)'
        if re.search(metrics_end, content):
            content = re.sub(metrics_end, r'</section>\n' + roster_html + r'\n<script>', content)
        else:
            print("Warning: Could not find metrics section end in index.html")
    
    # 5. Add JS for ember bar
    observer_js = '''
    // Ember bar reveal for player cards
    const playerObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-lit');
        }
      });
    }, { threshold: 0.2 });

    document.querySelectorAll('.js-player').forEach(card => playerObserver.observe(card));
'''
    if "document.querySelectorAll('.nav-links a').forEach" in content:
        content = content.replace("document.querySelectorAll('.nav-links a').forEach", observer_js + "\n    document.querySelectorAll('.nav-links a').forEach")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Done index.html")

if __name__ == '__main__':
    refactor_about()
    refactor_index()
