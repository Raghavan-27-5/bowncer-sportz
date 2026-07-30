import re

with open('about.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_css = '''  .architect-image {
    position: relative;
    border-radius: 12px;
    background: linear-gradient(180deg, var(--void-2) 0%, #1a1510 100%);
    border: 1px solid rgba(201,161,90, 0.1);
    overflow: hidden;
    height: 700px;
  }
  .architect-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: top center;
    filter: grayscale(20%) contrast(1.1);
    transition: transform 0.6s ease;
  }
  .architect-image:hover img {
    transform: scale(1.05);
  }
  .architect-image::after {
    content:''; position:absolute; inset:0;
    background: linear-gradient(0deg, var(--void) 0%, transparent 40%);
  }'''

new_css = '''  .architect-image {
    position: relative;
    height: 700px;
    display: flex;
    align-items: flex-end;
    justify-content: center;
  }
  .architect-image picture, .architect-image img {
    width: 100%;
    height: 115%; /* Enlarged */
    object-fit: contain;
    object-position: bottom center;
    filter: drop-shadow(0 30px 40px rgba(0,0,0,0.8));
    transition: transform 0.6s ease;
  }
  .architect-image:hover picture, .architect-image:hover img {
    transform: scale(1.05) translateY(-10px);
  }
  .architect-image::after {
    content:''; position:absolute; bottom:0; left:0; right:0; height: 150px;
    background: linear-gradient(0deg, var(--void) 0%, transparent 100%);
    pointer-events: none;
  }'''

content = content.replace(old_css, new_css)

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated about.html css")
