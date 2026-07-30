import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the Header text
content = content.replace('<div class="roster-eyebrow">From This Academy</div>', '<div class="roster-eyebrow">Trained by the Coach</div>')
content = content.replace('Elite players coached at Bowncer Sportz who went on to wear the USA Cricket badge at the national level. The proof is in the names.', 'Elite athletes forged under uncompromising standards. The proof is in the names.')

# 2. Re-write the Roster CSS to be "Out of the box" beautiful
old_css_start = r'/\* ═══════════════════════════════════════════════\s*USA CRICKET NATIONALS'
old_css_end = r'\.roster-stat h3 \{ font-family: \'Bebas Neue\', sans-serif; font-size: clamp\(28px, 4vw, 44px\); color: var\(--gold\); letter-spacing: 0\.05em; \}'

# Let's find the exact block to replace
css_match = re.search(old_css_start + r'[\s\S]*?' + old_css_end, content)
if css_match:
    new_css = '''/* ═══════════════════════════════════════════════
     USA CRICKET NATIONALS — Cinematic Mural
     ═══════════════════════════════════════════════ */
  .roster-section {
    padding: 100px 0 0; background: var(--void); position: relative; border-top: 1px solid var(--line);
  }
  .roster-header { padding: 0 clamp(24px, 5vw, 80px); margin-bottom: 40px; position: relative; z-index: 10; }
  .roster-eyebrow {
    font-size: 11px; text-transform: uppercase; letter-spacing: 0.22em; color: var(--gold); font-weight: 700;
    margin-bottom: 16px; display: flex; align-items: center; gap: 12px;
  }
  .roster-eyebrow::before { content: ''; display: block; width: 40px; height: 1px; background: var(--gold); }
  .roster-header h2 { font-family: 'Bebas Neue', sans-serif; font-size: clamp(40px, 8vw, 90px); color: var(--ink); letter-spacing: 0.02em; line-height: 0.9; text-shadow: 0 10px 30px rgba(0,0,0,0.8); }
  .roster-header p { color: var(--ink-dim); font-size: 16px; line-height: 1.6; margin-top: 16px; max-width: 500px; text-shadow: 0 4px 10px rgba(0,0,0,0.8); }
  
  /* The Cinematic Mural Strip */
  .roster-strip {
    display: flex; gap: 0; padding: 0; overflow-x: auto; scroll-snap-type: x mandatory; -webkit-overflow-scrolling: touch; scrollbar-width: none;
    -webkit-mask-image: linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%);
    mask-image: linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%);
    margin-bottom: -40px; /* pull stats up over the fade */
  }
  .roster-strip::-webkit-scrollbar { display: none; }
  
  .player-card {
    flex: 0 0 clamp(280px, 80vw, 360px); scroll-snap-align: center;
    position: relative; overflow: hidden; background: transparent;
    border-right: 1px solid rgba(255,255,255,0.05);
    transform: scale(0.95); opacity: 0.6; filter: saturate(0.5);
    transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .player-card.is-lit, .player-card:hover {
    transform: scale(1); opacity: 1; filter: saturate(1.1); z-index: 5;
    border-color: transparent;
  }
  
  .player-img { aspect-ratio: 4 / 5; position: relative; overflow: hidden; }
  .player-img img {
    width: 100%; height: 100%; object-fit: cover; object-position: center; display: block;
    transition: transform 1.2s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .player-card.is-lit .player-img img, .player-card:hover .player-img img { transform: scale(1.04); }
  
  .player-img::after {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(to top, rgba(7,8,10,1) 0%, rgba(7,8,10,0.7) 25%, transparent 60%); pointer-events: none;
  }
  
  .player-info { position: absolute; bottom: 0; left: 0; right: 0; padding: 40px 30px; z-index: 2; transform: translateY(20px); transition: transform 0.6s ease; }
  .player-card.is-lit .player-info, .player-card:hover .player-info { transform: translateY(0); }
  
  .player-name { font-family: 'Bebas Neue', sans-serif; font-size: 38px; color: var(--ink); letter-spacing: 0.04em; line-height: 1; margin-bottom: 8px; text-shadow: 0 4px 20px rgba(226,56,10,0.4); }
  .player-cred { font-size: 11px; text-transform: uppercase; letter-spacing: 0.2em; color: var(--gold); font-weight: 700; }
  
  /* Elite Stats Section */
  .roster-stat {
    position: relative; z-index: 20;
    padding: 80px clamp(24px, 5vw, 80px);
    background: linear-gradient(to bottom, transparent, var(--void) 20%);
  }
  
  .elite-stats-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 40px; max-width: 1200px; margin: 0 auto;
  }
  
  .elite-stat-box {
    position: relative; padding: 40px 0; border-top: 1px solid rgba(201,161,90,0.2);
    display: flex; flex-direction: column; align-items: flex-start;
  }
  .elite-stat-box::before {
    content: ''; position: absolute; top: -1px; left: 0; width: 0; height: 1px;
    background: var(--gold); transition: width 1s ease;
  }
  .roster-stat.is-visible .elite-stat-box::before { width: 100px; }
  
  .stat-num {
    font-family: 'Bebas Neue', sans-serif; font-size: clamp(60px, 8vw, 90px); line-height: 1;
    color: var(--ink); margin-bottom: 16px;
    background: linear-gradient(180deg, #fff 0%, var(--gold) 100%);
    -webkit-background-clip: text; color: transparent;
  }
  .glow-num { text-shadow: 0 0 40px rgba(201,161,90,0.3); }
  
  .stat-label { font-size: 14px; text-transform: uppercase; letter-spacing: 0.15em; color: var(--ink-dim); font-weight: 600; line-height: 1.4; }'''
    
    content = content.replace(css_match.group(0), new_css)
else:
    print("Warning: CSS match failed")

# 3. Replace the Roster Stat HTML
old_stat_html = r'<div class="roster-stat">\s*<h3>5 National Representatives &amp; Counting</h3>\s*</div>'
new_stat_html = '''<div class="roster-stat js-stats">
      <div class="elite-stats-grid">
        <div class="elite-stat-box">
          <div class="stat-num glow-num">20+</div>
          <div class="stat-label">National<br>Representatives</div>
        </div>
        <div class="elite-stat-box">
          <div class="stat-num">12+</div>
          <div class="stat-label">Years of Elite<br>Coaching</div>
        </div>
        <div class="elite-stat-box">
          <div class="stat-num glow-num">500+</div>
          <div class="stat-label">Professional<br>Cricketers Trained</div>
        </div>
      </div>
    </div>'''
content = re.sub(old_stat_html, new_stat_html, content)

# 4. Add the js-stats observer logic so the gold lines animate
observer_js_add = '''
    // Animate stats lines
    const statObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if(entry.isIntersecting) entry.target.classList.add('is-visible');
      });
    }, { threshold: 0.3 });
    document.querySelectorAll('.js-stats').forEach(el => statObserver.observe(el));
'''
content = content.replace("document.querySelectorAll('.js-player').forEach(card => playerObserver.observe(card));", "document.querySelectorAll('.js-player').forEach(card => playerObserver.observe(card));\n" + observer_js_add)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("index.html updated")
