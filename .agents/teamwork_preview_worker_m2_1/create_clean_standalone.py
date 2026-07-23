#!/usr/bin/env python3
import re
from pathlib import Path

index_text = Path("/home/raghavan/projects/bowncer_sportz/index.html").read_text(encoding="utf-8")

# Extract style content from index.html
style_match = re.search(r'<style>(.*?)</style>', index_text, re.DOTALL)
style_css = style_match.group(1) if style_match else ""

# Extract section #media-showcase HTML
start_idx = index_text.find('<section class="media-showcase-section" id="media-showcase">')
end_idx = index_text.find('</section>', start_idx) + len('</section>')
showcase_html = index_text[start_idx:end_idx]

# Extract script for media showcase
script_start = index_text.find('// YouTube Media Showcase Facade')
script_end = index_text.find('</script>', script_start)
script_js = index_text[script_start:script_end]

standalone = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Media Showcase Preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Archivo:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
<style>
{style_css}
  body {{ background: var(--void); margin: 0; padding: 0; }}
  .showcase-reveal {{ opacity: 1 !important; transform: none !important; }}
</style>
</head>
<body>

{showcase_html}

<script>
{script_js}
</script>
</body>
</html>
"""

# Adjust relative paths for assets to point to assets/ in repo root
standalone = standalone.replace('src="assets/', 'src="../../assets/')
standalone = standalone.replace("url('assets/", "url('../../assets/")
standalone = standalone.replace('data-poster="assets/', 'data-poster="../../assets/')

out_path = Path("/home/raghavan/projects/bowncer_sportz/.agents/teamwork_preview_worker_m2_1/standalone_showcase.html")
out_path.write_text(standalone, encoding="utf-8")
print(f"Successfully generated standalone HTML ({len(standalone)} bytes)")
