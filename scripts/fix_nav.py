import os
import glob
import re

nav_links_html = """  <div class="nav-links">
    <a href="index.html">Home</a>
    <a href="founder.html">The Founder</a>
    <a href="programs.html">Programs</a>
    <a href="media.html">Media</a>
    <a href="locations.html">Locations</a>
  </div>"""

def update_nav(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find the <div class="nav-links">...</div> block
    # Note: re.DOTALL allows . to match newlines
    pattern = r'<div class="nav-links">.*?</div>'
    
    if re.search(pattern, content, re.DOTALL):
        # We need to preserve the "active" class on the correct link for each page
        filename = os.path.basename(filepath)
        
        # Determine which link should be active
        active_href = filename
        if filename == "about.html": # Just in case it's still being used
            active_href = "founder.html"
            
        custom_nav = nav_links_html.replace(f'href="{active_href}"', f'href="{active_href}" class="active"')
        
        # Edge case: If no link matches (e.g. some other page), just use default without active class.
        
        new_content = re.sub(pattern, custom_nav, content, flags=re.DOTALL)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated nav in {filepath}")
    else:
        print(f"Nav links not found in {filepath}")

for html_file in glob.glob("*.html"):
    update_nav(html_file)
