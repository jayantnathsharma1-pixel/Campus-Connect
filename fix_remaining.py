import os
import glob
import re

def fix_all():
    # 1. Fix "Yes, Delete" button to have FontAwesome icon
    TEMPLATE_DIR = r"c:\Users\Asus\Desktop\campus_connect_project - Copy\templates"
    for filepath in glob.glob(os.path.join(TEMPLATE_DIR, "*.html")):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False
        if '>Yes, Delete<' in content:
            content = content.replace('>Yes, Delete<', '><i class="fa-solid fa-trash"></i> Yes, Delete<')
            changed = True
            
        if 'btn.innerText = "<i class="fa-solid fa-hourglass-half"></i> Sending...";' in content:
            content = content.replace('btn.innerText = "<i class="fa-solid fa-hourglass-half"></i> Sending...";', 'btn.innerHTML = \'<i class="fa-solid fa-hourglass-half"></i> Sending...\';')
            changed = True

        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed {os.path.basename(filepath)}")

    # 2. Fix app.py to auto-login the new student after OTP verification
    app_py_path = r"c:\Users\Asus\Desktop\campus_connect_project - Copy\app.py"
    with open(app_py_path, 'r', encoding='utf-8') as f:
        app_content = f.read()

    # We want to replace the part in verify_otp()
    # Find:
    #         session.pop('reg_data', None)
    #         flash('🎉 Registration successful! You can now log in to the student portal.', 'success')
    #         return redirect(url_for('login'))
    
    old_code = """        session.pop('reg_data', None)
        flash('🎉 Registration successful! You can now log in to the student portal.', 'success')
        return redirect(url_for('login'))"""

    new_code = """        # Auto-login the new student directly
        session['user_id'] = reg_data['user_id']
        session['name'] = reg_data['name']
        session['role'] = 'student'
        session['college_id'] = 'kmbb1234'
        session['college_name'] = 'KMBB College of Engineering and Technology'
        session['branch'] = reg_data['branch']
        session['year'] = reg_data['year']
        session['designation'] = ''

        session.pop('reg_data', None)
        flash('🎉 Registration successful! Welcome to the student portal.', 'success')
        return redirect(url_for('student_dashboard'))"""

    if old_code in app_content:
        app_content = app_content.replace(old_code, new_code)
        with open(app_py_path, 'w', encoding='utf-8') as f:
            f.write(app_content)
        print("Fixed app.py auto-login for new students!")
    else:
        print("Could not find the exact code block in app.py to replace.")

if __name__ == '__main__':
    fix_all()
