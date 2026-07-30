import re

with open('about.html', 'r', encoding='utf-8') as f:
    content = f.read()

mural_css = '''
  .hof-mural-section {
    padding: 140px 5%;
    background: var(--void);
    position: relative;
    overflow: hidden;
  }
  .hof-mural-container {
    max-width: 1400px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 1.3fr;
    gap: 80px;
    align-items: center;
  }
  .hof-mural-text {
    position: relative;
    z-index: 20;
  }
  .hof-mural-eyebrow {
    font-family: monospace; font-size: 14px; color: var(--gold);
    letter-spacing: 0.2em; text-transform: uppercase;
    display: flex; align-items: center; gap: 12px; margin-bottom: 24px;
  }
  .hof-mural-eyebrow::before {
    content: ''; width: 40px; height: 1px; background: var(--gold);
  }
  .hof-mural-title {
    font-family: 'Bebas Neue', sans-serif; font-size: clamp(60px, 8vw, 100px);
    line-height: 0.9; margin-bottom: 32px; color: #fff;
  }
  .hof-mural-desc {
    font-size: 18px; color: var(--ink); line-height: 1.6; max-width: 480px;
  }
  
  .hof-mural-images {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    grid-template-rows: repeat(12, 1fr);
    height: 750px;
    position: relative;
  }
  
  .hof-mural-img {
    position: relative;
    overflow: hidden;
    background: #000;
    transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .hof-mural-img img {
    width: 100%; height: 100%; object-fit: cover; object-position: center;
    filter: grayscale(100%) contrast(1.3) brightness(0.7);
    transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    display: block;
  }
  
  .hof-mural-img-1 { 
    grid-column: 1 / 7; grid-row: 3 / 10; 
    z-index: 1; 
    box-shadow: -20px 20px 40px rgba(0,0,0,0.8);
  }
  .hof-mural-img-2 { 
    grid-column: 5 / 10; grid-row: 1 / 13; 
    z-index: 2; 
    box-shadow: 0 30px 60px rgba(0,0,0,0.9);
    border: 1px solid rgba(201,161,90,0.2);
  }
  .hof-mural-img-3 { 
    grid-column: 9 / 13; grid-row: 4 / 11; 
    z-index: 3; 
    box-shadow: 20px 20px 40px rgba(0,0,0,0.8);
  }
  
  .hof-mural-img:hover {
    transform: scale(1.05);
    z-index: 10;
    box-shadow: 0 40px 80px rgba(201,161,90, 0.15);
    border: 1px solid var(--gold);
  }
  .hof-mural-img:hover img {
    filter: grayscale(0%) contrast(1.1) brightness(1.1);
    transform: scale(1.02);
  }

  @media (max-width: 1100px) {
    .hof-mural-container { grid-template-columns: 1fr; gap: 60px; }
    .hof-mural-text { text-align: center; display: flex; flex-direction: column; align-items: center; }
    .hof-mural-eyebrow::after { content: ''; width: 40px; height: 1px; background: var(--gold); }
    .hof-mural-images { height: 600px; width: 100%; max-width: 800px; margin: 0 auto; }
  }
  @media (max-width: 600px) {
    .hof-mural-images { display: flex; flex-direction: column; height: auto; gap: 24px; }
    .hof-mural-img { grid-column: auto; grid-row: auto; aspect-ratio: 4/5; }
    .hof-mural-img-2 { border: none; }
  }
'''

mural_html = '''
  <!-- THE DETROIT RECOGNITION (HOF) -->
  <section class="hof-mural-section">
    <div class="hof-mural-container">
      <div class="hof-mural-text">
        <div class="hof-mural-eyebrow">USA Hall of Fame Award // Michigan</div>
        <h2 class="hof-mural-title">The Detroit<br>Recognition</h2>
        <p class="hof-mural-desc">
          An honor reserved for the game's finest architects. Recognized on a global stage, S. Thiyagarajan was officially inducted into the USA Hall of Fame in Detroit—cementing a legacy forged by uncompromising standards and an elite coaching pedigree that transcends borders.
        </p>
      </div>
      <div class="hof-mural-images">
        <div class="hof-mural-img hof-mural-img-1">
          <img src="assets/detroit_award_v2_1.webp" alt="Award 1" loading="lazy">
        </div>
        <div class="hof-mural-img hof-mural-img-2">
          <img src="assets/detroit_award_v2_2.webp" alt="Award 2" loading="lazy">
        </div>
        <div class="hof-mural-img hof-mural-img-3">
          <img src="assets/detroit_award_v2_3.webp" alt="Award 3" loading="lazy">
        </div>
      </div>
    </div>
  </section>
'''

if '</style>' in content:
    content = content.replace('</style>', mural_css + '\n</style>')

# Insert after Foundation Section
foundation_pattern = r'(<!-- FOUNDATION / TRUST MARKERS -->\s*<section class="foundation-section">[\s\S]*?</section>)'
foundation_match = re.search(foundation_pattern, content)

if foundation_match:
    foundation_block = foundation_match.group(1)
    new_foundation_block = foundation_block + '\n\n' + mural_html
    content = content.replace(foundation_block, new_foundation_block)
else:
    print("Failed to find foundation block.")

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Inserted cinematic mural layout after foundation block.")
