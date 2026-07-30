import re

with open('about.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the old HOF HTML block
old_hof_html_pattern = r'<!-- USA HALL OF FAME -->\s*<section class="hof-section">[\s\S]*?</section>'
content = re.sub(old_hof_html_pattern, '', content)

# Remove the old HOF CSS block
old_hof_css_pattern = r'\s*\.hof-section\s*\{[\s\S]*?@media \(max-width: 900px\) \{[\s\S]*?\}\s*\}'
content = re.sub(old_hof_css_pattern, '', content)

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed old HOF section.")
