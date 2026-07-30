import re

with open('about.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. REPLACE ROSTER CSS ─────────────────────────────────────────────────────
old_css = '''  /* Wall of Fame */
  .roster-section {
    padding: 120px 40px;
    background: #0a0806;
    position: relative;
    border-top: 1px solid var(--line);
  }

  .roster-header {
    text-align: center;
    margin-bottom: 80px;
  }
  .roster-header h2 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(48px, 6vw, 72px);
    color: var(--ink);
    letter-spacing: 0.02em;
  }
  .roster-header p {
    color: var(--gold);
    font-family: monospace;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 16px;
  }

  .roster-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(280px, 400px));
    justify-content: center;
    gap: 32px;
    max-width: 1200px;
    margin: 0 auto;
  }

  .player-card {
    background: var(--void-2);
    border: 1px solid var(--line);
    border-radius: 8px;
    overflow: hidden;
    position: relative;
    transition: transform 0.3s ease, border-color 0.3s ease;
  }
  .player-card:hover {
    transform: translateY(-8px);
    border-color: var(--gold);
  }

  .player-img {
    height: 300px;
    background: #111;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .player-img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: top;
    filter: grayscale(80%) sepia(20%) hue-rotate(5deg);
    transition: filter 0.4s ease;
  }
  .player-card:hover .player-img img {
    filter: grayscale(0%) sepia(0%);
  }
  .player-img::after {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(180deg, transparent 50%, var(--void-2) 100%);
  }

  .player-info {
    padding: 24px;
    position: relative;
    z-index: 2;
  }
  .player-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 32px;
    color: var(--ink);
    margin-bottom: 8px;
    letter-spacing: 0.02em;
  }
  .player-cred {
    color: var(--gold);
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
  }

  .roster-stat {
    text-align: center;
    margin-top: 80px;
    padding: 40px;
    border: 1px solid rgba(201,161,90, 0.2);
    background: radial-gradient(ellipse at center, rgba(201,161,90,0.05) 0%, transparent 70%);
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
  }
  .roster-stat h3 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(32px, 4vw, 48px);
    color: var(--gold);
    letter-spacing: 0.05em;
  }'''

new_css = '''  /* ═══════════════════════════════════════════════
     USA CRICKET NATIONALS — Scroll-Snap Roster Strip
     ═══════════════════════════════════════════════ */
  .roster-section {
    padding: 100px 0 120px;
    background: #0a0806;
    position: relative;
    border-top: 1px solid var(--line);
    overflow: hidden;
  }

  .roster-header {
    padding: 0 clamp(24px, 5vw, 80px);
    margin-bottom: 56px;
  }
  .roster-eyebrow {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.22em;
    color: var(--ember);
    font-weight: 700;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .roster-eyebrow::before {
    content: '';
    display: block;
    width: 32px;
    height: 1px;
    background: var(--ember);
  }
  .roster-header h2 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(40px, 6vw, 72px);
    color: var(--ink);
    letter-spacing: 0.02em;
    line-height: 0.9;
    max-width: 700px;
  }
  .roster-header p {
    color: var(--ink-dim);
    font-size: 15px;
    line-height: 1.6;
    margin-top: 20px;
    max-width: 560px;
  }

  /* Horizontal scroll-snap strip */
  .roster-strip {
    display: flex;
    gap: 16px;
    padding: 0 clamp(24px, 5vw, 80px) 40px;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }
  .roster-strip::-webkit-scrollbar { display: none; }

  .player-card {
    flex: 0 0 clamp(240px, 72vw, 300px);
    scroll-snap-align: start;
    position: relative;
    border-radius: 4px;
    overflow: hidden;
    background: var(--void-2);
    --bar-scale: 0;
  }

  /* Tall portrait aspect — no fixed px height that causes cropping */
  .player-img {
    aspect-ratio: 3 / 4;
    position: relative;
    overflow: hidden;
  }
  .player-img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center center;
    display: block;
    transition: transform 0.8s cubic-bezier(.16,1,.3,1);
  }
  @media (hover: hover) {
    .player-card:hover .player-img img {
      transform: scale(1.04);
    }
  }

  /* Bottom fade so name is always readable */
  .player-img::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to top,
      rgba(7,8,10,0.95) 0%,
      rgba(7,8,10,0.45) 40%,
      transparent 68%
    );
    pointer-events: none;
  }

  /* Name + cred overlaid on photo */
  .player-info {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    padding: 20px 20px 18px;
    z-index: 2;
  }
  .player-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 28px;
    color: var(--ink);
    letter-spacing: 0.03em;
    line-height: 1;
    margin-bottom: 5px;
  }
  .player-cred {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--gold);
    font-weight: 600;
  }

  /* Ember bar — the signature element.
     Scales from 0 → 1 when card enters viewport via JS */
  .player-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    height: 3px;
    width: 100%;
    background: linear-gradient(90deg, var(--ember), var(--ember-glow));
    transform-origin: left;
    transform: scaleX(var(--bar-scale));
    transition: transform 0.9s cubic-bezier(.16,1,.3,1);
  }
  .player-card.is-lit {
    --bar-scale: 1;
  }

  /* Desktop: natural row, no overflow scroll */
  @media (min-width: 1100px) {
    .roster-strip {
      overflow-x: visible;
    }
    .player-card {
      flex: 1 1 0;
      min-width: 0;
    }
  }

  .roster-stat {
    text-align: center;
    margin: 60px clamp(24px, 5vw, 80px) 0;
    padding: 32px 40px;
    border: 1px solid rgba(201,161,90, 0.18);
    background: radial-gradient(ellipse at center, rgba(201,161,90,0.04) 0%, transparent 70%);
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
  }
  .roster-stat h3 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(28px, 4vw, 44px);
    color: var(--gold);
    letter-spacing: 0.05em;
  }'''

# ── 2. REPLACE ROSTER HTML ─────────────────────────────────────────────────────
old_html = '''  <!-- WALL OF FAME -->
  <section class="roster-section">
    <div class="roster-header">
      <h2>The Legacy</h2>
      <p>Players Developed &amp; Elite Alumni</p>
    </div>
    
    <div class="roster-grid">
      <!-- Player 1: Shiva Vashisht -->
      <div class="player-card">
        <div class="player-img">
          <img src="assets/shiva_vashisht.webp" alt="Shiva Vashisht" loading="lazy" decoding="async">
        </div>
        <div class="player-info">
          <div class="player-name">Shiva Vashisht</div>
          <div class="player-cred">USA U-19 National Team Captain</div>
        </div>
      </div>

      <!-- Player 2: Amogh -->
      <div class="player-card">
        <div class="player-img">
          <img src="assets/amogh.webp" alt="Amogh" loading="lazy" decoding="async">
        </div>
        <div class="player-info">
          <div class="player-name">Amogh</div>
          <div class="player-cred">USA Cricket · Cape Cobras</div>
        </div>
      </div>

      <!-- Player 3: Sanjay Stanley -->
      <div class="player-card">
        <div class="player-img">
          <img src="assets/sanjay_stanley.webp" alt="Sanjay Stanley" loading="lazy" decoding="async">
        </div>
        <div class="player-info">
          <div class="player-name">Sanjay Stanley</div>
          <div class="player-cred">USA Captain</div>
        </div>
      </div>

      <!-- Player 4: Utkarsh Srivastava -->
      <div class="player-card">
        <div class="player-img">
          <img src="assets/utkarsh_srivastava.webp" alt="Utkarsh Srivastava" loading="lazy" decoding="async">
        </div>
        <div class="player-info">
          <div class="player-name">Utkarsh Srivastava</div>
          <div class="player-cred">USA Cricket</div>
        </div>
      </div>
    </div>
    
    <div class="roster-stat">
      <h3>More than 20 players represented for Nationals</h3>
    </div>
  </section>'''

new_html = '''  <!-- USA CRICKET NATIONALS -->
  <section class="roster-section">
    <div class="roster-header">
      <div class="roster-eyebrow">From This Academy</div>
      <h2>USA Cricket<br>National Representatives</h2>
      <p>Five players coached at Bowncer Sportz who went on to wear the USA Cricket badge at national level.</p>
    </div>

    <div class="roster-strip" id="rosterStrip">

      <div class="player-card js-player">
        <div class="player-img">
          <img src="assets/shiva_vashisht.webp" alt="Shiva Vashisht" loading="lazy" decoding="async">
        </div>
        <div class="player-info">
          <div class="player-name">Shiva Vashisht</div>
          <div class="player-cred">USA U-19 · National Captain</div>
        </div>
      </div>

      <div class="player-card js-player">
        <div class="player-img">
          <img src="assets/amogh.webp" alt="Amogh" loading="lazy" decoding="async">
        </div>
        <div class="player-info">
          <div class="player-name">Amogh</div>
          <div class="player-cred">USA Cricket · Cape Cobras</div>
        </div>
      </div>

      <div class="player-card js-player">
        <div class="player-img">
          <img src="assets/sanjay_stanley.webp" alt="Sanjay Stanley" loading="lazy" decoding="async">
        </div>
        <div class="player-info">
          <div class="player-name">Sanjay Stanley</div>
          <div class="player-cred">USA Cricket · Captain</div>
        </div>
      </div>

      <div class="player-card js-player">
        <div class="player-img">
          <img src="assets/utkarsh_srivastava.webp" alt="Utkarsh Srivastava" loading="lazy" decoding="async">
        </div>
        <div class="player-info">
          <div class="player-name">Utkarsh Srivastava</div>
          <div class="player-cred">USA Cricket</div>
        </div>
      </div>

      <div class="player-card js-player">
        <div class="player-img">
          <img src="assets/aaron_jones.webp" alt="Aaron Jones" loading="lazy" decoding="async">
        </div>
        <div class="player-info">
          <div class="player-name">Aaron Jones</div>
          <div class="player-cred">USA Cricket · ICC T20 World Cup</div>
        </div>
      </div>

    </div>

    <div class="roster-stat">
      <h3>5 National Representatives &amp; Counting</h3>
    </div>
  </section>'''

# ── 3. ADD INTERSECTION OBSERVER JS before </script> that closes the nav JS ──
observer_js = '''
    // Ember bar reveal for player cards
    const playerObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-lit');
        }
      });
    }, { threshold: 0.2 });

    document.querySelectorAll('.js-player').forEach(card => playerObserver.observe(card));'''

content = content.replace(old_css, new_css)
content = content.replace(old_html, new_html)

# Insert the observer JS before the closing of the existing DOMContentLoaded block
content = content.replace(
    "      document.querySelectorAll('.nav-links a').forEach(link => {",
    observer_js + "\n      document.querySelectorAll('.nav-links a').forEach(link => {"
)

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done. Checking replacements...")
checks = [
    ('roster-strip', 'scroll-snap strip'),
    ('js-player', 'player cards with JS class'),
    ('aaron_jones.webp', 'Aaron Jones'),
    ('is-lit', 'ember bar trigger'),
    ('aspect-ratio: 3 / 4', 'portrait aspect ratio'),
    ('playerObserver', 'intersection observer JS'),
]
for needle, label in checks:
    found = needle in content
    print(f"  {'OK' if found else 'MISSING'} - {label}")
