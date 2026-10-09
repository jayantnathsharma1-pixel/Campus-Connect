import os
import re

template_dir = r"c:\Users\Asus\Desktop\campus_connect_project - Copy\templates"
svg_logo = '''<span class="logo-icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle;">
                    <!-- Connection Lines -->
                    <path d="M4 16L12 21L20 16" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M12 21V11" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="4" cy="16" r="1.5" fill="#3b82f6"/>
                    <circle cx="20" cy="16" r="1.5" fill="#3b82f6"/>
                    <circle cx="12" cy="21" r="1.5" fill="#3b82f6"/>
                    <!-- Graduation Cap -->
                    <path d="M12 3L2 8.5L12 14L22 8.5L12 3Z" fill="#3b82f6" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M22 8.5V14" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="22" cy="15" r="1.5" fill="#3b82f6"/>
                </svg>
            </span>'''

for filename in os.listdir(template_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(template_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace <span class="logo-icon"><i class="..."></i></span>
        # We handle multiline or single line spans.
        pattern = re.compile(r'<span class="logo-icon">\s*<i class="[^"]+"></i>\s*</span>', re.DOTALL)
        
        if pattern.search(content):
            new_content = pattern.sub(svg_logo, content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}")
