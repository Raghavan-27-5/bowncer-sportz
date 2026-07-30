import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace roster-strip
pattern1 = r'\.roster-strip\s*\{[\s\S]*?\}'
replacement1 = '''  .roster-strip {
    display: flex; gap: 0; padding: 0; position: relative;
    overflow-x: auto;
    overflow-y: hidden;
    scroll-behavior: auto;
    scrollbar-width: none;
    -ms-overflow-style: none;
    -webkit-mask-image: linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%);
    mask-image: linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%);
    margin-bottom: -40px;
    cursor: grab;
  }
  .roster-strip::-webkit-scrollbar { display: none; }
  .roster-strip:active { cursor: grabbing; }'''
content = re.sub(pattern1, replacement1, content)

# Replace roster-track
pattern2 = r'\.roster-track\s*\{[\s\S]*?\}'
replacement2 = '''  .roster-track {
    display: flex; gap: 0; width: max-content;
  }'''
content = re.sub(pattern2, replacement2, content)

# Remove hover pause and keyframes
pattern3 = r'\.roster-strip:hover \.roster-track\s*\{[\s\S]*?\}\s*@keyframes rosterScroll\s*\{[\s\S]*?\}'
content = re.sub(pattern3, '', content)

# Add JS script
js_script = '''
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const rosterStrip = document.querySelector('.roster-strip');
      if (!rosterStrip) return;
      const rosterTrack = document.querySelector('.roster-track');
      
      let isScrolling = true;
      let scrollSpeed = 1.5;
      
      rosterStrip.addEventListener('mouseenter', () => isScrolling = false);
      rosterStrip.addEventListener('mouseleave', () => isScrolling = true);
      rosterStrip.addEventListener('touchstart', () => isScrolling = false);
      rosterStrip.addEventListener('touchend', () => isScrolling = true);
      
      rosterStrip.addEventListener('wheel', () => {
        isScrolling = false;
        clearTimeout(rosterStrip.resumeTimeout);
        rosterStrip.resumeTimeout = setTimeout(() => isScrolling = true, 500);
      }, {passive: true});

      function autoScroll() {
        if (isScrolling) {
          rosterStrip.scrollLeft += scrollSpeed;
          // Duplicate track detection for infinite scroll
          if (rosterStrip.scrollLeft >= rosterTrack.scrollWidth / 2) {
            rosterStrip.scrollLeft = 0;
          }
        }
        requestAnimationFrame(autoScroll);
      }
      requestAnimationFrame(autoScroll);
    });
  </script>
'''

if "const rosterStrip = document.querySelector('.roster-strip');" not in content:
    content = content.replace('</body>', js_script + '\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated roster scroll behavior.")
