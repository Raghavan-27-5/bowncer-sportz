#!/usr/bin/env python3
from pathlib import Path

index_content = Path("/home/raghavan/projects/bowncer_sportz/index.html").read_text(encoding="utf-8")

# Adjust relative paths for assets so they point to ../../assets/
modified_content = index_content.replace('src="assets/', 'src="../../assets/')
modified_content = modified_content.replace("url('assets/", "url('../../assets/")
modified_content = modified_content.replace('data-poster="assets/', 'data-poster="../../assets/')

# Auto-hide intro cinematic and show reveal elements immediately
modified_content = modified_content.replace(
    '</head>',
    '<style>#intro-cinematic { display: none !important; } .showcase-reveal { opacity: 1 !important; transform: none !important; }</style></head>'
)

output_path = Path("/home/raghavan/projects/bowncer_sportz/.agents/teamwork_preview_worker_m2_1/preview_showcase.html")
output_path.write_text(modified_content, encoding="utf-8")
print(f"Created {output_path}")
