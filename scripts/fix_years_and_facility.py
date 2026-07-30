import re

# 1. Update programs.html
with open('programs.html', 'r', encoding='utf-8') as f:
    prog = f.read()

prog = prog.replace('<option value="poonamallee">Poonamallee (Flagship Facility)</option>\n', '')
with open('programs.html', 'w', encoding='utf-8') as f:
    f.write(prog)
print('programs.html updated')

# 2. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

idx = idx.replace('<div class="val">8+ Years</div>', '<div class="val">12+ Years</div>')
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)
print('index.html updated')

# 3. Update about.html
with open('about.html', 'r', encoding='utf-8') as f:
    abt = f.read()

script_pattern = r'<script>\s*const founded = new Date\(\'2017-10-30\'\);\s*const now = new Date\(\);\s*let years = now\.getFullYear\(\) - founded\.getFullYear\(\);\s*if\(now\.getMonth\(\) < founded\.getMonth\(\) \|\| \(now\.getMonth\(\) === founded\.getMonth\(\) && now\.getDate\(\) < founded\.getDate\(\)\)\) \{\s*years--;\s*\}\s*document\.write\(`<div class="f-num">\$\{years\}\+</div>`\);\s*</script>'
if re.search(script_pattern, abt):
    abt = re.sub(script_pattern, '<div class="f-num">12+</div>', abt)
else:
    print('Failed to find script in about.html')

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(abt)
print('about.html updated')
