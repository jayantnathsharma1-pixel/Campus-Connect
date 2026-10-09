import os
import re
import glob

TEMPLATE_DIR = r"c:\Users\Asus\Desktop\campus_connect_project - Copy\templates"
JS_FILE = r"c:\Users\Asus\Desktop\campus_connect_project - Copy\static\js\script.js"

BUTTON_MAP = {
    r'✏️ Edit': r'<i class="fa-solid fa-pen-to-square"></i> Edit',
    r'🗑️ Delete': r'<i class="fa-solid fa-trash"></i> Delete',
    r'🗑️️ Delete': r'<i class="fa-solid fa-trash"></i> Delete',
    r'🗑️ Clear': r'<i class="fa-solid fa-eraser"></i> Clear',
    r'👁️ View More': r'<i class="fa-solid fa-eye"></i> View More',
    r'👁️': r'<i class="fa-solid fa-eye"></i>',  # password toggle maybe?
    r'🎓 Direct Admit': r'<i class="fa-solid fa-user-plus"></i> Direct Admit',
    r'👔 Onboard': r'<i class="fa-solid fa-chalkboard-user"></i> Onboard',
    r'✉️ Send Message': r'<i class="fa-solid fa-paper-plane"></i> Send Message',
    r'✉️ Dispatch Message': r'<i class="fa-solid fa-paper-plane"></i> Dispatch Message',
    r'✉️ Message': r'<i class="fa-solid fa-envelope"></i> Message',
    r'🔍 Filter': r'<i class="fa-solid fa-filter"></i> Filter',
    r'🔍 Quick': r'<i class="fa-solid fa-magnifying-glass"></i> Quick',
    r'🔍 Search': r'<i class="fa-solid fa-magnifying-glass"></i> Search',
    r'🔄 Handover': r'<i class="fa-solid fa-rotate-right"></i> Handover',
    r'➕ Add': r'<i class="fa-solid fa-plus"></i> Add',
    r'🎓 Register': r'<i class="fa-solid fa-user-plus"></i> Register',
    r'🎓 Student': r'<i class="fa-solid fa-user-graduate"></i> Student',
    r'🎓 Bonafide': r'<i class="fa-solid fa-file-signature"></i> Bonafide',
    r'🎓 {{': r'<i class="fa-solid fa-user-graduate"></i> {{',
    r'👔 Faculty': r'<i class="fa-solid fa-user-tie"></i> Faculty',
}

def update_templates():
    for filepath in glob.glob(os.path.join(TEMPLATE_DIR, "*.html")):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changed = False
        
        # Replace button texts globally
        for old, new in BUTTON_MAP.items():
            if old in content:
                content = content.replace(old, new)
                changed = True
                
        # Theme Toggle Button Update
        # from: <span id="themeIcon">🌙</span> <span id="themeText">Dark</span>
        # to: <span id="themeIcon"><i class="fa-solid fa-moon"></i></span> <span id="themeText">Dark</span>
        old_theme_btn = '<span id="themeIcon">🌙</span>'
        new_theme_btn = '<span id="themeIcon"><i class="fa-solid fa-moon"></i></span>'
        if old_theme_btn in content:
            content = content.replace(old_theme_btn, new_theme_btn)
            changed = True
            
        old_theme_btn2 = '<span id="themeIcon">☀️</span>'
        new_theme_btn2 = '<span id="themeIcon"><i class="fa-solid fa-sun"></i></span>'
        if old_theme_btn2 in content:
            content = content.replace(old_theme_btn2, new_theme_btn2)
            changed = True

        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated HTML: {os.path.basename(filepath)}")

def update_js():
    with open(JS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False
    
    # Update script.js theme icons
    old_sun = 'themeIcon.textContent = "☀️"'
    new_sun = 'themeIcon.innerHTML = \'<i class="fa-solid fa-sun"></i>\''
    if old_sun in content:
        content = content.replace(old_sun, new_sun)
        changed = True
        
    old_moon = 'themeIcon.textContent = "🌙"'
    new_moon = 'themeIcon.innerHTML = \'<i class="fa-solid fa-moon"></i>\''
    if old_moon in content:
        content = content.replace(old_moon, new_moon)
        changed = True
        
    if changed:
        with open(JS_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated JS: script.js")

if __name__ == '__main__':
    update_templates()
    update_js()
