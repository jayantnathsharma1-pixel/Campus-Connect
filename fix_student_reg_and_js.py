import os

def fix_login_and_js():
    # 1. Remove Student Registration link from login.html
    login_path = r"c:\Users\Asus\Desktop\campus_connect_project - Copy\templates\login.html"
    with open(login_path, 'r', encoding='utf-8') as f:
        login_content = f.read()

    student_reg_block = """                <div>
                    New student? 
                    <a href="{{ url_for('register') }}" style="color: #2563eb; font-weight: bold;">
                        <i class="fa-solid fa-user-plus"></i> Register Student Account
                    </a>
                </div>"""
                
    # Also check if it looks slightly different
    if student_reg_block in login_content:
        login_content = login_content.replace(student_reg_block, "")
        with open(login_path, 'w', encoding='utf-8') as f:
            f.write(login_content)
        print("Removed student registration link from login.html")
    else:
        print("Could not find the exact student registration block in login.html")

    # 2. Fix innerText emojis in script.js
    js_path = r"c:\Users\Asus\Desktop\campus_connect_project - Copy\static\js\script.js"
    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()

    replacements = {
        'btn.innerText = `👁️ View More (Show All ${rows.length} Students)`;': 'btn.innerHTML = `<i class="fa-solid fa-eye"></i> View More (Show All ${rows.length} Students)`;',
        'btn.innerText = `👁️ View More (Show All ${rows.length} Staff Members)`;': 'btn.innerHTML = `<i class="fa-solid fa-eye"></i> View More (Show All ${rows.length} Staff Members)`;',
        'btn.innerText = `👁️ View More (Show All ${rows.length})`;': 'btn.innerHTML = `<i class="fa-solid fa-eye"></i> View More (Show All ${rows.length})`;',
        'btn.innerText = "🔼 Show Less";': 'btn.innerHTML = \'<i class="fa-solid fa-chevron-up"></i> Show Less\';',
    }

    js_changed = False
    for old, new in replacements.items():
        if old in js_content:
            js_content = js_content.replace(old, new)
            js_changed = True

    # Also replace any other innerText that sets emojis, e.g. for sending OTPs
    if 'btn.innerText = "<i class="fa-solid fa-hourglass-half"></i> Sending...";' in js_content:
        js_content = js_content.replace('btn.innerText = "<i class="fa-solid fa-hourglass-half"></i> Sending...";', 'btn.innerHTML = \'<i class="fa-solid fa-hourglass-half"></i> Sending...\';')
        js_changed = True

    if js_changed:
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print("Fixed emojis in script.js (replaced innerText with innerHTML)")
    else:
        print("No innerText replacements made in script.js")

if __name__ == '__main__':
    fix_login_and_js()
