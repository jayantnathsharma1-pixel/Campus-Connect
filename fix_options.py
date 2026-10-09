import os
import glob
import re

TEMPLATE_DIR = r"c:\Users\Asus\Desktop\campus_connect_project - Copy\templates"

def fix_options():
    for filepath in glob.glob(os.path.join(TEMPLATE_DIR, "*.html")):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        def remove_i_from_option(match):
            # match.group(0) is the full <option>...</option>
            option_open = match.group(1)
            inner = match.group(2)
            option_close = match.group(3)
            
            # Remove <i ...></i> from inner
            clean_inner = re.sub(r'<i[^>]*>.*?</i>\s*', '', inner)
            
            return f"{option_open}{clean_inner}{option_close}"

        pattern = r'(<option[^>]*>)(.*?)(</option>)'
        new_content = re.sub(pattern, remove_i_from_option, content, flags=re.DOTALL | re.IGNORECASE)

        if new_content != content:
            content = new_content
            changed = True
            
        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed options in {os.path.basename(filepath)}")

if __name__ == '__main__':
    fix_options()
