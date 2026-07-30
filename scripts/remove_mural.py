import re

with open('about.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove HTML block
mural_html_pattern = r'<!-- THE DETROIT RECOGNITION \(HOF\) -->\s*<section class="hof-mural-section">[\s\S]*?</section>'
content = re.sub(mural_html_pattern, '', content)

# Remove CSS block
mural_css_pattern = r'\s*\.hof-mural-section\s*\{[\s\S]*?@media \(max-width: 600px\) \{[\s\S]*?\}\s*\}'
content = re.sub(mural_css_pattern, '', content)

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed HOF mural section.")
