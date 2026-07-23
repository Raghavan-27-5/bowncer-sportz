#!/usr/bin/env python3
import re
from pathlib import Path

index_text = Path("/home/raghavan/projects/bowncer_sportz/index.html").read_text(encoding="utf-8")

# Extract head (styles, fonts)
head_match = re.search(r'<head>(.*?)</head>', index_text, re.DOTALL)
head_content = head_match.group(1) if head_match else ""

# Extract media showcase section HTML
showcase_match = re.search(r'(<!-- ═+ SECTION 3.5.*?<!-- SECTION 4)', index_text, re.DOTALL)
showcase_html = showcase_match.group(1) if showcase_match else ""

# Extract media showcase script
script_match = re.search(r'(// YouTube Media Showcase Facade.*?</script>)', index_text, re.DOTALL)
script_content = script_match.group(1) if script_match else ""

standalone_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
{head_content}
<style>
  body {{ background: var(--void); margin: 0; padding: 0; }}
  .showcase-reveal {{ opacity: 1 !important; transform: none !important; }}
</style>
</head>
<body>
{showcase_html}
<script>
{script_content}
</body>
</html>
"""

# Adjust relative paths for assets
standalone_doc = standalone_doc.replace('src="assets/', 'src="../../assets/')
standalone_doc = standalone_doc.replace("url('assets/", "url('../../assets/")
standalone_doc = standalone_doc.replace('data-poster="assets/', 'data-poster="../../assets/')

out_path = Path("/home/raghavan/projects/bowncer_sportz/.agents/teamwork_preview_worker_m2_1/standalone_showcase.html")
out_path.write_text(standalone_doc, encoding="utf-8")
print(f"Created {out_path}")
