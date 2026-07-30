import re

with open('about.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the hof-section block
hof_pattern = r'(<!-- USA HALL OF FAME -->\s*<section class="hof-section">[\s\S]*?</section>)'
hof_match = re.search(hof_pattern, content)

if hof_match:
    hof_block = hof_match.group(1)
    
    # Remove it from its current position
    content = content.replace(hof_block, '')
    
    # Find the foundation-section end and insert it there
    foundation_pattern = r'(<!-- FOUNDATION / TRUST MARKERS -->\s*<section class="foundation-section">[\s\S]*?</section>)'
    foundation_match = re.search(foundation_pattern, content)
    
    if foundation_match:
        foundation_block = foundation_match.group(1)
        # Insert HOF block after foundation block
        new_foundation_block = foundation_block + '\n\n  ' + hof_block
        content = content.replace(foundation_block, new_foundation_block)
        
        with open('about.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Successfully moved USA Hall of Fame section.")
    else:
        print("Could not find foundation section.")
else:
    print("Could not find HOF section.")
