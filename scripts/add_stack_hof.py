import re

with open('about.html', 'r', encoding='utf-8') as f:
    content = f.read()

stack_css = '''
  .hof-stack-section {
    padding: 120px 5%;
    background: var(--void);
    position: relative;
    border-top: 1px solid rgba(255,255,255,0.05);
  }
  .hof-stack-header {
    text-align: center;
    max-width: 800px;
    margin: 0 auto 80px auto;
  }
  .hof-stack-eyebrow {
    font-family: monospace; font-size: 14px; color: var(--gold);
    letter-spacing: 0.2em; text-transform: uppercase;
    display: flex; align-items: center; justify-content: center; gap: 12px; margin-bottom: 24px;
  }
  .hof-stack-eyebrow::before, .hof-stack-eyebrow::after {
    content: ''; width: 40px; height: 1px; background: var(--gold);
  }
  .hof-stack-title {
    font-family: 'Bebas Neue', sans-serif; font-size: clamp(48px, 8vw, 80px);
    line-height: 1; margin-bottom: 24px; color: #fff;
  }
  .hof-stack-desc {
    font-size: 18px; color: var(--ink); line-height: 1.6;
  }
  
  .hof-stack-container {
    display: flex;
    flex-direction: column;
    gap: 100px;
    max-width: 1000px;
    margin: 0 auto;
    position: relative;
    padding-bottom: 100px;
  }
  
  .hof-card {
    position: sticky;
    height: 75vh;
    min-height: 500px;
    max-height: 800px;
    border-radius: 16px;
    overflow: hidden;
    background: #000;
    box-shadow: 0 -20px 50px rgba(0,0,0,0.8);
    border: 1px solid rgba(201,161,90,0.15);
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  }
  
  /* Staggered sticky tops to create the cascading stack effect */
  .hof-card:nth-child(1) { top: 80px; z-index: 1; }
  .hof-card:nth-child(2) { top: 120px; z-index: 2; }
  .hof-card:nth-child(3) { top: 160px; z-index: 3; }
  
  .hof-card-inner {
    width: 100%; height: 100%;
    position: relative;
  }
  
  .hof-card-inner img {
    width: 100%; height: 100%;
    object-fit: cover;
    object-position: center;
    filter: grayscale(80%) sepia(10%) contrast(1.1);
    transition: filter 0.8s ease, transform 0.8s ease;
  }
  
  /* Adjusting the middle image so it doesn't crop the trophy */
  .hof-card:nth-child(2) .hof-card-inner img {
    object-fit: contain;
    background: radial-gradient(circle at center, #111 0%, #000 100%);
    padding: 20px;
  }
  
  .hof-card:hover .hof-card-inner img {
    filter: grayscale(0%) sepia(0%) contrast(1.1);
    transform: scale(1.03);
  }
  
  @media (max-width: 768px) {
    .hof-card { height: 60vh; min-height: 400px; }
    .hof-card:nth-child(1) { top: 100px; }
    .hof-card:nth-child(2) { top: 120px; }
    .hof-card:nth-child(3) { top: 140px; }
  }
'''

stack_html = '''
  <!-- THE DETROIT RECOGNITION (STACK) -->
  <section class="hof-stack-section">
    <div class="hof-stack-header">
      <div class="hof-stack-eyebrow">USA Hall of Fame Award // Michigan</div>
      <h2 class="hof-stack-title">The Detroit Recognition</h2>
      <p class="hof-stack-desc">
        An honor reserved for the game's finest architects. Recognized on a global stage, S. Thiyagarajan was officially inducted into the USA Hall of Fame in Detroit—cementing a legacy forged by uncompromising standards and an elite coaching pedigree that transcends borders.
      </p>
    </div>
    
    <div class="hof-stack-container">
      <div class="hof-card">
        <div class="hof-card-inner">
          <img src="assets/detroit_award_v2_1.webp" alt="USA Hall of Fame Award Ceremony" loading="lazy">
        </div>
      </div>
      <div class="hof-card">
        <div class="hof-card-inner">
          <img src="assets/detroit_award_v2_2.webp" alt="USA Hall of Fame Award Presentation" loading="lazy">
        </div>
      </div>
      <div class="hof-card">
        <div class="hof-card-inner">
          <img src="assets/detroit_award_v2_3.webp" alt="S. Thiyagarajan with USA Hall of Fame Award" loading="lazy">
        </div>
      </div>
    </div>
  </section>
'''

if '</style>' in content:
    content = content.replace('</style>', stack_css + '\n</style>')

foundation_pattern = r'(<!-- FOUNDATION / TRUST MARKERS -->\s*<section class="foundation-section">[\s\S]*?</section>)'
foundation_match = re.search(foundation_pattern, content)

if foundation_match:
    foundation_block = foundation_match.group(1)
    new_foundation_block = foundation_block + '\n\n' + stack_html
    content = content.replace(foundation_block, new_foundation_block)
else:
    print("Failed to find foundation block.")

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Inserted cinematic stack layout after foundation block.")
