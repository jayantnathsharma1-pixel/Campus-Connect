import os
import glob
import re

TEMPLATE_DIR = r"c:\Users\Asus\Desktop\campus_connect_project - Copy\templates"
JS_FILE = r"c:\Users\Asus\Desktop\campus_connect_project - Copy\static\js\script.js"

def fix_placeholders():
    for filepath in glob.glob(os.path.join(TEMPLATE_DIR, "*.html")):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        # Find all placeholder="..."
        def replacer(match):
            placeholder_content = match.group(1)
            # Remove <i class="..."></i> and any extra spaces
            cleaned = re.sub(r'<i class="[^"]+"></i>\s*', '', placeholder_content)
            return f'placeholder="{cleaned}"'

        new_content = re.sub(r'placeholder="([^"]*<i class="[^"]+"></i>[^"]*)"', replacer, content)
        if new_content != content:
            content = new_content
            changed = True

        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed placeholders in {os.path.basename(filepath)}")

def fix_js():
    with open(JS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False

    # Replace the JS toggle logic
    old_logic = 'rows[i].style.display = isExpanded ? "none" : "";'
    new_logic = '''if (isExpanded) {
            rows[i].classList.add("hidden-row");
            rows[i].style.display = "none";
        } else {
            rows[i].classList.remove("hidden-row");
            rows[i].style.display = "table-row";
        }'''

    if old_logic in content:
        content = content.replace(old_logic, new_logic)
        changed = True

    if changed:
        with open(JS_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Fixed JS logic in script.js")

if __name__ == '__main__':
    fix_placeholders()
    fix_js()
