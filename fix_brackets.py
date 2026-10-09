import os
import glob
import re

TEMPLATE_DIR = r"c:\Users\Asus\Desktop\campus_connect_project - Copy\templates"

def fix_double_brackets():
    for filepath in glob.glob(os.path.join(TEMPLATE_DIR, "*.html")):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        if '>><i class="fa-solid fa-trash"' in content:
            content = content.replace('>><i class="fa-solid fa-trash"', '><i class="fa-solid fa-trash"')
            changed = True
            
        if '>><i class="fa-solid fa-pen-to-square"' in content:
            content = content.replace('>><i class="fa-solid fa-pen-to-square"', '><i class="fa-solid fa-pen-to-square"')
            changed = True

        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed double brackets in {os.path.basename(filepath)}")

if __name__ == '__main__':
    fix_double_brackets()
