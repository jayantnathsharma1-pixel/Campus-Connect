import os
import glob
import re

TEMPLATE_DIR = r"c:\Users\Asus\Desktop\campus_connect_project - Copy\templates"

EMOJI_REPLACEMENTS = {
    '✏️': '<i class="fa-solid fa-pen-to-square"></i>',
    '🗑️': '<i class="fa-solid fa-trash"></i>',
    '🗑': '<i class="fa-solid fa-trash"></i>',
    '👁️': '<i class="fa-solid fa-eye"></i>',
    '🎓': '<i class="fa-solid fa-user-graduate"></i>',
    '👔': '<i class="fa-solid fa-user-tie"></i>',
    '✉️': '<i class="fa-solid fa-envelope"></i>',
    '✉': '<i class="fa-solid fa-envelope"></i>',
    '🔍': '<i class="fa-solid fa-magnifying-glass"></i>',
    '🔄': '<i class="fa-solid fa-rotate-right"></i>',
    '➕': '<i class="fa-solid fa-plus"></i>',
    '⭐': '<i class="fa-solid fa-star"></i>',
    '💾': '<i class="fa-solid fa-floppy-disk"></i>',
    '📤': '<i class="fa-solid fa-arrow-up-from-bracket"></i>',
    '📖': '<i class="fa-solid fa-book-open"></i>',
    '📋': '<i class="fa-solid fa-clipboard"></i>',
    '🍱': '<i class="fa-solid fa-box-open"></i>',
    '✅': '<i class="fa-solid fa-check"></i>',
    '❌': '<i class="fa-solid fa-xmark"></i>',
    '⚠️': '<i class="fa-solid fa-triangle-exclamation"></i>',
    '👨‍🎓': '<i class="fa-solid fa-user-graduate"></i>',
    '👤': '<i class="fa-solid fa-user"></i>',
    '👑': '<i class="fa-solid fa-crown"></i>',
    '🎖️': '<i class="fa-solid fa-medal"></i>',
    '🛠️': '<i class="fa-solid fa-wrench"></i>',
    '🧹': '<i class="fa-solid fa-broom"></i>',
    '🔒': '<i class="fa-solid fa-lock"></i>',
    '🔑': '<i class="fa-solid fa-key"></i>',
    '🎉': '<i class="fa-solid fa-party-horn"></i>',
    '✕': '<i class="fa-solid fa-xmark"></i>',
    '⏳': '<i class="fa-solid fa-hourglass-half"></i>',
    '🛡️': '<i class="fa-solid fa-shield"></i>',
    '✅': '<i class="fa-solid fa-circle-check"></i>',
    '❌': '<i class="fa-solid fa-circle-xmark"></i>',
    '☀️': '<i class="fa-solid fa-sun"></i>',
    '🌙': '<i class="fa-solid fa-moon"></i>',
    '📌': '<i class="fa-solid fa-thumbtack"></i>',
    '📞': '<i class="fa-solid fa-phone"></i>',
    '🆔': '<i class="fa-solid fa-id-card"></i>',
    '🔹': '<i class="fa-solid fa-circle-dot"></i>',
    '🍳': '<i class="fa-solid fa-egg"></i>',
    '🍛': '<i class="fa-solid fa-bowl-rice"></i>',
    '☕': '<i class="fa-solid fa-mug-hot"></i>',
    '🍲': '<i class="fa-solid fa-bowl-food"></i>',
    '📅': '<i class="fa-solid fa-calendar-days"></i>',
    '🏛️': '<i class="fa-solid fa-building-columns"></i>',
    '📜': '<i class="fa-solid fa-file-contract"></i>',
    '🍽️': '<i class="fa-solid fa-utensils"></i>',
    '📢': '<i class="fa-solid fa-bullhorn"></i>',
    '💳': '<i class="fa-solid fa-money-check-dollar"></i>',
    '📊': '<i class="fa-solid fa-chart-column"></i>',
    '📚': '<i class="fa-solid fa-book"></i>',
    '📬': '<i class="fa-solid fa-envelope-open-text"></i>',
    '📝': '<i class="fa-solid fa-pen-to-square"></i>',
    '⚡': '<i class="fa-solid fa-bolt"></i>',
    '🏢': '<i class="fa-solid fa-building"></i>',
    '🧾': '<i class="fa-solid fa-file-invoice-dollar"></i>',
    '🔐': '<i class="fa-solid fa-shield-halved"></i>',
}

def fix_all_emojis():
    # Fix HTML files
    for filepath in glob.glob(os.path.join(TEMPLATE_DIR, "*.html")):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False
        
        # Sort by length descending to replace longer emojis (like variations) first
        for emoji in sorted(EMOJI_REPLACEMENTS.keys(), key=len, reverse=True):
            if emoji in content:
                content = content.replace(emoji, EMOJI_REPLACEMENTS[emoji])
                changed = True
                
        # Fix multiple icons in a row if any were introduced by previous scripts (e.g. nested icons)
        content = re.sub(r'<i class="[^"]+"></i>\s*<i class="[^"]+"></i>', lambda m: m.group(0).split('>')[0] + '></i>', content)
        
        # We also need to fix nested <i class="..."><i class="..."></i></i> if they exist by mistake
        
        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated HTML: {os.path.basename(filepath)}")

    # Fix JS file
    js_path = r"c:\Users\Asus\Desktop\campus_connect_project - Copy\static\js\script.js"
    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()
    js_changed = False
    
    # We want to remove the emoji matching regex since we use FA icons everywhere now
    # Or just replace the fallback '🔹 ' with '<i class="fa-solid fa-circle-dot"></i> '
    if "'🔹 '" in js_content:
        js_content = js_content.replace("'🔹 '", "'<i class=\"fa-solid fa-circle-dot\"></i> '")
        js_changed = True
        
    if "themeIcon.textContent = \"☀️\"" in js_content:
        js_content = js_content.replace("themeIcon.textContent = \"☀️\"", "themeIcon.innerHTML = '<i class=\"fa-solid fa-sun\"></i>'")
        js_changed = True
        
    if "themeIcon.textContent = \"🌙\"" in js_content:
        js_content = js_content.replace("themeIcon.textContent = \"🌙\"", "themeIcon.innerHTML = '<i class=\"fa-solid fa-moon\"></i>'")
        js_changed = True

    if js_changed:
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print("Updated JS: script.js")

if __name__ == '__main__':
    fix_all_emojis()
