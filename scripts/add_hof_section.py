import re

with open('about.html', 'r', encoding='utf-8') as f:
    content = f.read()

hof_css = '''
  .hof-section {
    padding: 120px 5%;
    background: var(--void);
    border-top: 1px solid rgba(255,255,255,0.05);
    position: relative;
    overflow: hidden;
  }
  .hof-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 80px;
    position: relative;
    z-index: 2;
  }
  .hof-header {
    text-align: center;
    max-width: 800px;
    margin: 0 auto;
  }
  .hof-eyebrow {
    font-family: monospace; font-size: 14px; color: var(--gold);
    letter-spacing: 0.2em; text-transform: uppercase;
    display: flex; align-items: center; justify-content: center; gap: 12px; margin-bottom: 24px;
  }
  .hof-eyebrow::before, .hof-eyebrow::after {
    content: ''; width: 40px; height: 1px; background: var(--gold);
  }
  .hof-title {
    font-family: 'Bebas Neue', sans-serif; font-size: clamp(48px, 6vw, 80px);
    line-height: 1; margin-bottom: 24px; color: #fff;
  }
  .hof-desc {
    font-size: 18px; color: var(--ink); line-height: 1.6;
  }
  
  .hof-grid {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 24px;
    align-items: center;
  }
  .hof-img {
    position: relative;
    border-radius: 8px; overflow: hidden;
    border: 1px solid rgba(201,161,90,0.1);
    transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.6s ease;
    background: #000;
  }
  .hof-img img {
    width: 100%; height: 100%; object-fit: cover; object-position: center;
    filter: grayscale(40%) sepia(30%) contrast(1.1);
    transition: filter 0.6s ease, transform 1s ease;
    display: block;
  }
  
  .hof-img:nth-child(1) { grid-column: 1 / 5; aspect-ratio: 4/5; }
  .hof-img:nth-child(2) { 
    grid-column: 5 / 9; 
    aspect-ratio: 3/4; 
    transform: scale(1.1); 
    z-index: 5; 
    box-shadow: 0 20px 50px rgba(0,0,0,0.8);
    border-color: rgba(201,161,90,0.3);
  }
  .hof-img:nth-child(3) { grid-column: 9 / 13; aspect-ratio: 4/5; }
  
  .hof-img:hover {
    z-index: 10;
    box-shadow: 0 20px 50px rgba(201,161,90, 0.2);
    border-color: var(--gold);
  }
  .hof-img:nth-child(2):hover {
    transform: scale(1.15) translateY(-5px);
  }
  .hof-img:nth-child(1):hover, .hof-img:nth-child(3):hover {
    transform: scale(1.05) translateY(-5px);
  }
  .hof-img:hover img {
    filter: grayscale(0%) sepia(0%) contrast(1.0);
    transform: scale(1.05);
  }
  
  @media (max-width: 900px) {
    .hof-grid { display: flex; flex-direction: column; gap: 40px; }
    .hof-img:nth-child(n) { transform: none; aspect-ratio: auto; }
    .hof-img:nth-child(2) { transform: none; }
    .hof-img:nth-child(2):hover { transform: translateY(-5px); }
  }
'''

hof_html = '''
  <!-- USA HALL OF FAME -->
  <section class="hof-section">
    <div class="hof-container">
      <div class="hof-header">
        <div class="hof-eyebrow">USA Hall of Fame Award</div>
        <h2 class="hof-title">Michigan (Detroit)<br>United States of America</h2>
        <p class="hof-desc">
          Recognized on a global stage for unparalleled contributions to cricket development. S. Thiyagarajan was awarded the prestigious USA Hall of Fame Award in Detroit, cementing his legacy not just as an elite player, but as a visionary architect of the game.
        </p>
      </div>
      <div class="hof-grid">
        <div class="hof-img">
          <img src="assets/detroit_award_1.webp" alt="USA Hall of Fame Award Ceremony" loading="lazy">
        </div>
        <div class="hof-img">
          <img src="assets/detroit_award_2.webp" alt="USA Hall of Fame Award Presentation" loading="lazy">
        </div>
        <div class="hof-img">
          <img src="assets/detroit_award_3.webp" alt="S. Thiyagarajan with USA Hall of Fame Award" loading="lazy">
        </div>
      </div>
    </div>
  </section>
'''

# Insert CSS before </style>
if '</style>' in content:
    content = content.replace('</style>', hof_css + '\n</style>')
else:
    # If there is no </style> tag in about.html (maybe they are inline or linked), let's check. 
    # Actually about.html has a huge <style> block at the top. Let's find </style>.
    pass

# Check if we actually replaced CSS
if hof_css not in content:
    # If the first replace didn't work because </style> isn't there, let's inject before </head>
    content = content.replace('</head>', '<style>' + hof_css + '</style>\n</head>')

# Insert HTML before <!-- FOUNDATION / TRUST MARKERS -->
content = content.replace('<!-- FOUNDATION / TRUST MARKERS -->', hof_html + '\n  <!-- FOUNDATION / TRUST MARKERS -->')

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Inserted Hall of Fame section into about.html")
