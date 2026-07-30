import glob
import re

html_files = glob.glob('*.html')

for file in html_files:
    if file == 'temp.html':
        continue
    
    print(f"Processing {file}...")
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Replace html{}
    content = re.sub(r'html\s*\{\s*scroll-behavior:\s*smooth;\s*\}', 'html{scroll-behavior:smooth; overflow-x:hidden; width:100%;}', content)
    
    # Replace body{}
    content = re.sub(r'overflow-x:\s*hidden;', 'overflow-x:hidden;\n    width: 100%;\n    position: relative;', content)
    # Fix double applications if any
    content = content.replace('width: 100%;\n    position: relative;\n    width: 100%;\n    position: relative;', 'width: 100%;\n    position: relative;')
    
    # Replace nav-links right: -100%
    content = content.replace('right: -100%;', 'right: 0;\n      transform: translateX(100%);')
    
    # Replace nav-links active
    content = content.replace('transition: right 0.4s ease;', 'transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);')
    content = content.replace('transition: right 0.4s;', 'transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);')
    content = content.replace('.nav-links.active {\n      right: 0;\n    }', '.nav-links.active {\n      transform: translateX(0);\n    }')
    content = content.replace('.nav-links.active {\n  right: 0;\n}', '.nav-links.active {\n  transform: translateX(0);\n}')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done updating CSS across HTML files.")
