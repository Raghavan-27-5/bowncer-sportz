import re
import sys

files = ['index.html', 'programs.html', 'locations.html']

hamburger_html = """
  <button class="hamburger" aria-label="Toggle menu">
    <span class="bar"></span>
    <span class="bar"></span>
    <span class="bar"></span>
  </button>
"""

hamburger_css = """
  .hamburger {
    display: none;
    flex-direction: column;
    justify-content: space-between;
    width: 30px;
    height: 20px;
    background: transparent;
    border: none;
    cursor: pointer;
    z-index: 1001;
  }
  .hamburger .bar {
    width: 100%;
    height: 2px;
    background-color: var(--gold);
    transition: all 0.3s ease;
  }
  
  @media (max-width: 768px) {
    .hamburger {
      display: flex;
    }
    .nav-links {
      position: fixed;
      top: 0;
      right: -100%;
      width: 100vw;
      height: 100vh;
      background: rgba(10, 8, 6, 0.98);
      backdrop-filter: blur(10px);
      flex-direction: column;
      justify-content: center;
      align-items: center;
      transition: right 0.4s ease;
      z-index: 1000;
    }
    .nav-links.active {
      right: 0;
    }
    .nav-links a {
      font-size: 24px;
      margin: 16px 0;
    }
    .hamburger.active .bar:nth-child(1) {
      transform: translateY(9px) rotate(45deg);
    }
    .hamburger.active .bar:nth-child(2) {
      opacity: 0;
    }
    .hamburger.active .bar:nth-child(3) {
      transform: translateY(-9px) rotate(-45deg);
    }
  }
"""

hamburger_js = """
<script>
  document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    if (hamburger && navLinks) {
      hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navLinks.classList.toggle('active');
        document.body.style.overflow = navLinks.classList.contains('active') ? 'hidden' : 'auto';
      });
    }
    
    // Close menu when a link is clicked
    document.querySelectorAll('.nav-links a').forEach(link => {
      link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navLinks.classList.remove('active');
        document.body.style.overflow = 'auto';
      });
    });
  });
</script>
"""

for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    # 1. Add hamburger HTML to nav if not already there
    if 'class="hamburger"' not in content:
        content = re.sub(r'(<div class="nav-links">)', r'\n  <button class="hamburger" aria-label="Toggle menu">\n    <span class="bar"></span>\n    <span class="bar"></span>\n    <span class="bar"></span>\n  </button>\n  \1', content)
        
    # 2. Add hamburger CSS
    if '.hamburger {' not in content:
        content = content.replace('</style>', hamburger_css + '\n</style>')
        
    # 3. Add hamburger JS
    if 'const hamburger =' not in content:
        content = content.replace('</body>', hamburger_js + '\n</body>')
        
    # Programs specific fixes
    if file == 'programs.html':
        content = content.replace('.apply-section {\n    padding: 120px 40px;', '.apply-section {\n    padding: 120px 40px;\n  }\n  @media (max-width: 768px) {\n    .apply-section { padding: 60px 16px; }\n  }\n  .apply-section-base {')

    with open(file, 'w') as f:
        f.write(content)

print("Done updating mobile fixes!")
