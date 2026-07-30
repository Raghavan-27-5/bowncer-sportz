import re

with open('about.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove HTML block
hof_html_pattern = r'<!-- USA HALL OF FAME -->\s*<section class="hof-section">[\s\S]*?</section>'
content = re.sub(hof_html_pattern, '', content)

# Remove CSS block
hof_css_pattern = r'\s*\.hof-section\s*\{[\s\S]*?@media \(max-width: 900px\) \{[\s\S]*?\}\s*\}'
content = re.sub(hof_css_pattern, '', content)

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed HOF section.")
