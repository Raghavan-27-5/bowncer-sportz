import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# --- 1. Update the CSS for the marquee and gold effects ---
old_css_start = r'/\* The Cinematic Mural Strip \*/'
old_css_end = r'\.player-cred \{ font-size: 11px; text-transform: uppercase; letter-spacing: 0\.2em; color: var\(--gold\); font-weight: 700; \}'

css_match = re.search(old_css_start + r'[\s\S]*?' + old_css_end, content)
if css_match:
    new_css = '''/* The Cinematic Mural Strip & Gold Marquee */
  .roster-strip {
    display: flex; gap: 0; padding: 0; overflow: hidden; position: relative;
    -webkit-mask-image: linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%);
    mask-image: linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%);
    margin-bottom: -40px; /* pull stats up over the fade */
  }
  
  .roster-track {
    display: flex; gap: 0; width: max-content;
    animation: rosterScroll 25s linear infinite;
  }
  
  .roster-strip:hover .roster-track {
    animation-play-state: paused;
  }
  
  @keyframes rosterScroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
  }
  
  .player-card {
    flex: 0 0 clamp(280px, 80vw, 360px); 
    position: relative; overflow: hidden; background: transparent;
    border-right: 1px solid rgba(201,161,90,0.1);
    border-bottom: 2px solid transparent;
    transform: scale(0.95); opacity: 0.6; filter: sepia(0.3) saturate(0.5);
    transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  }
  
  .player-card::before {
    content: ''; position: absolute; inset: 0; border: 2px solid transparent; z-index: 10;
    transition: all 0.6s ease; pointer-events: none;
  }

  .player-card:hover {
    transform: scale(1); opacity: 1; filter: sepia(0) saturate(1.1); z-index: 5;
    box-shadow: 0 20px 50px rgba(201,161,90, 0.2);
    border-bottom-color: var(--gold);
  }
  
  .player-card:hover::before {
    border-color: rgba(201,161,90, 0.5);
    box-shadow: inset 0 0 40px rgba(201,161,90, 0.3);
  }
  
  .player-img { aspect-ratio: 4 / 5; position: relative; overflow: hidden; }
  .player-img img {
    width: 100%; height: 100%; object-fit: cover; object-position: center; display: block;
    transition: transform 1.2s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .player-card:hover .player-img img { transform: scale(1.04); }
  
  .player-img::after {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(to top, rgba(7,8,10,1) 0%, rgba(7,8,10,0.7) 25%, transparent 60%); pointer-events: none;
  }
  
  .player-info { position: absolute; bottom: 0; left: 0; right: 0; padding: 40px 30px; z-index: 2; transform: translateY(20px); transition: transform 0.6s ease; }
  .player-card:hover .player-info { transform: translateY(0); }
  
  .player-name { font-family: 'Bebas Neue', sans-serif; font-size: 38px; color: var(--ink); letter-spacing: 0.04em; line-height: 1; margin-bottom: 8px; text-shadow: 0 4px 20px rgba(201,161,90,0.4); }
  .player-cred { font-size: 11px; text-transform: uppercase; letter-spacing: 0.2em; color: var(--gold); font-weight: 700; text-shadow: 0 0 10px rgba(0,0,0,0.8); }'''
    
    content = content.replace(css_match.group(0), new_css)
else:
    print("Warning: CSS match failed")

# --- 2. Update the HTML to add .roster-track and duplicate the cards ---
html_start = r'<div class="roster-strip" id="rosterStrip">'
html_end = r'</div>\s*<div class="roster-stat js-stats">'

html_match = re.search(html_start + r'(.*?)' + r'(</div>\s*<div class="roster-stat js-stats">)', content, flags=re.DOTALL)
if html_match:
    cards_html = html_match.group(1)
    
    # We remove the old .js-player observer class because we don't need it for intersection observing anymore
    cards_html = cards_html.replace(' js-player', '')
    
    # Wrap in .roster-track and duplicate
    new_html = f'<div class="roster-strip" id="rosterStrip">\n      <div class="roster-track">{cards_html}{cards_html}</div>\n    </div>\n    <div class="roster-stat js-stats">'
    
    content = content.replace(html_match.group(0), new_html)
else:
    print("Warning: HTML match failed")

# Remove the old intersection observer for the player cards if it exists
obs_pattern = r"// Observer for scroll-snap revealing.*?\n.*?document\.querySelectorAll\('\.js-player'\)\.forEach\(card => playerObserver\.observe\(card\)\);"
content = re.sub(obs_pattern, '', content, flags=re.DOTALL | re.IGNORECASE)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("index.html updated")
