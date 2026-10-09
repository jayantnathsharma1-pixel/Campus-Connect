import os
import glob
import re

TEMPLATE_DIR = r"c:\Users\Asus\Desktop\campus_connect_project - Copy\templates"
CSS_FILE = r"c:\Users\Asus\Desktop\campus_connect_project - Copy\static\css\style.css"

def fix_action_buttons():
    for filepath in glob.glob(os.path.join(TEMPLATE_DIR, "*.html")):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        # 1. Standardize Delete buttons
        # Pattern looks for <button ...> ... fa-trash ... </button>
        # or <a ...> ... fa-trash ... </a>
        def replace_delete(match):
            tag_open = match.group(1) # e.g. <button type="button" class="foo" onclick="...">
            inner = match.group(2)
            tag_close = match.group(3)
            
            # Remove existing class and style
            tag_open_clean = re.sub(r'\s*class="[^"]*"', '', tag_open)
            tag_open_clean = re.sub(r'\s*style="[^"]*"', '', tag_open_clean)
            
            # Add new class
            tag_open_clean = tag_open_clean.replace('<button', '<button class="btn-action btn-delete"')
            tag_open_clean = tag_open_clean.replace('<a', '<a class="btn-action btn-delete"')
            
            # Replace inner text with standard if it contains Delete
            if 'Delete' in inner:
                inner = '<i class="fa-solid fa-trash"></i> Delete'
                
            return f"{tag_open_clean}>{inner}{tag_close}"

        # Regex for button or anchor containing fa-trash
        pattern_delete = r'(<(?:button|a)[^>]*>)\s*(.*?<i class="fa-solid fa-trash"></i>.*?)\s*(</(?:button|a)>)'
        new_content = re.sub(pattern_delete, replace_delete, content, flags=re.DOTALL)
        
        if new_content != content:
            content = new_content
            changed = True

        # 2. Standardize Edit buttons
        def replace_edit(match):
            tag_open = match.group(1)
            inner = match.group(2)
            tag_close = match.group(3)
            
            tag_open_clean = re.sub(r'\s*class="[^"]*"', '', tag_open)
            tag_open_clean = re.sub(r'\s*style="[^"]*"', '', tag_open_clean)
            tag_open_clean = tag_open_clean.replace('<button', '<button class="btn-action btn-edit"')
            tag_open_clean = tag_open_clean.replace('<a', '<a class="btn-action btn-edit"')
            
            if 'Edit' in inner:
                inner = '<i class="fa-solid fa-pen-to-square"></i> Edit'
                
            return f"{tag_open_clean}>{inner}{tag_close}"

        pattern_edit = r'(<(?:button|a)[^>]*>)\s*(.*?<i class="fa-solid fa-pen-to-square"></i>.*?)\s*(</(?:button|a)>)'
        new_content = re.sub(pattern_edit, replace_edit, content, flags=re.DOTALL)

        if new_content != content:
            content = new_content
            changed = True
            
        # 3. Fix back to top button emoji
        if '⬆️' in content:
            content = content.replace('⬆️', '<i class="fa-solid fa-arrow-up"></i>')
            changed = True
            
        # Clean up any button tag that might be badly formed
        # Replace instances of class="btn-action btn-delete" class="something else"
        
        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed action buttons in {os.path.basename(filepath)}")

def fix_css():
    with open(CSS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    changed = False
    
    css_to_add = """
/* ================= ACTION BUTTONS (EDIT/DELETE) ================= */
.btn-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 6px 12px;
    font-size: 13px;
    font-weight: 600;
    border-radius: 6px;
    cursor: pointer;
    text-decoration: none;
    border: none;
    transition: all 0.2s ease;
}
.btn-action i {
    font-size: 14px;
}
.btn-edit {
    background-color: #e0e7ff;
    color: #4338ca;
}
.btn-edit:hover {
    background-color: #c7d2fe;
    color: #3730a3;
}
.btn-delete {
    background-color: #fee2e2;
    color: #dc2626;
}
.btn-delete:hover {
    background-color: #fecaca;
    color: #b91c1c;
}
body.dark-theme .btn-edit {
    background-color: rgba(67, 56, 202, 0.2);
    color: #818cf8;
}
body.dark-theme .btn-edit:hover {
    background-color: rgba(67, 56, 202, 0.4);
}
body.dark-theme .btn-delete {
    background-color: rgba(220, 38, 38, 0.2);
    color: #f87171;
}
body.dark-theme .btn-delete:hover {
    background-color: rgba(220, 38, 38, 0.4);
}

/* ================= ENHANCED BACK TO TOP ================= */
.back-to-top-btn {
    display: none;
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 45px;
    height: 45px;
    border: none;
    border-radius: 50%;
    background-color: #4f46e5;
    color: white;
    font-size: 18px;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
    z-index: 1000;
    transition: all 0.3s ease;
    align-items: center;
    justify-content: center;
}
.back-to-top-btn:hover {
    background-color: #4338ca;
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.6);
}
.back-to-top-btn.show {
    display: flex;
}
body.dark-theme .back-to-top-btn {
    background-color: #6366f1;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}
"""
    if "/* ================= ACTION BUTTONS (EDIT/DELETE) ================= */" not in content:
        # We will append the new CSS and optionally remove old back-to-top-btn CSS
        # Let's remove old back-to-top-btn rules
        content = re.sub(r'\.back-to-top-btn\s*\{[^}]*\}', '', content, flags=re.DOTALL)
        content = re.sub(r'\.back-to-top-btn\.show\s*\{[^}]*\}', '', content, flags=re.DOTALL)
        content = re.sub(r'body\.dark-theme \.back-to-top-btn\s*\{[^}]*\}', '', content, flags=re.DOTALL)
        
        content += css_to_add
        changed = True
        
    if changed:
        with open(CSS_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated style.css with sleek Action Buttons and Back to Top floating widget!")

if __name__ == '__main__':
    fix_action_buttons()
    fix_css()
