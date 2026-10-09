import os
import glob
import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

profile_route = """
@app.context_processor
def inject_user():
    if 'user_id' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = %s', (session['user_id'],))
        user = cursor.fetchone()
        cursor.close()
        return dict(current_user=user)
    return dict(current_user=None)

@app.route('/update-profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    old_password = request.form.get('old_password', '')
    new_password = request.form.get('new_password', '')
    confirm_new_password = request.form.get('confirm_new_password', '')
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = %s', (session['user_id'],))
    user = cursor.fetchone()
    
    if not user:
        cursor.close()
        flash('User not found!', 'error')
        return redirect(request.referrer or url_for('login'))
        
    if user['password'] != old_password:
        cursor.close()
        flash('❌ Incorrect Current Password. Changes not saved.', 'error')
        return redirect(request.referrer)
        
    update_pwd = user['password']
    if new_password:
        if new_password != confirm_new_password:
            cursor.close()
            flash('❌ New Passwords do not match!', 'error')
            return redirect(request.referrer)
        update_pwd = new_password
        
    cursor.execute('UPDATE users SET name = %s, email = %s, phone = %s, password = %s WHERE user_id = %s', (name, email, phone, update_pwd, session['user_id']))
    
    mysql.connection.commit()
    cursor.close()
    
    session['name'] = name
    flash('✅ Profile & Settings updated successfully!', 'success')
    return redirect(request.referrer)
"""

if 'def update_profile():' not in content:
    content = content.replace("@app.route('/logout')", profile_route + "\n@app.route('/logout')")
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Added profile route and context processor to app.py')
else:
    print('Already added to app.py')

templates_dir = "templates"
dashboards = glob.glob(os.path.join(templates_dir, "*dashboard.html"))

modal_html = """
    <!-- MODAL: EDIT PROFILE & PASSWORD -->
    <div id="editProfileModal" class="modal">
        <div class="modal-content" style="max-width: 500px;">
            <h3><i class="fa-solid fa-user-pen"></i> Edit Profile & Change Password</h3>
            <p class="modal-subtext">Update your personal details or securely change your password.</p>
            
            <form action="{{ url_for('update_profile') }}" method="POST">
                <h4 style="margin-bottom: 10px; border-bottom: 1px solid var(--border-color); padding-bottom: 5px;">Basic Details</h4>
                <label>Full Name <span style="color:red">*</span></label>
                <input type="text" name="name" class="search-input" value="{{ current_user.name if current_user else name }}" required>
                
                <label style="margin-top: 15px; display: block;">Email Address <span style="color:red">*</span></label>
                <input type="email" name="email" class="search-input" value="{{ current_user.email if current_user else '' }}" required>
                
                <label style="margin-top: 15px; display: block;">Contact Number</label>
                <input type="text" name="phone" class="search-input" value="{{ current_user.phone if current_user and current_user.phone else '' }}" placeholder="Enter 10-digit number">
                
                <h4 style="margin-top: 25px; margin-bottom: 10px; border-bottom: 1px solid var(--border-color); padding-bottom: 5px;">Change Password <small style="font-weight: normal; color: var(--text-secondary);">(Leave blank if not changing)</small></h4>
                
                <label>Current Password <span style="color:red">*</span></label>
                <input type="password" name="old_password" class="search-input" placeholder="Required to save ANY changes" required>
                
                <label style="margin-top: 15px; display: block;">New Password</label>
                <input type="password" name="new_password" class="search-input" placeholder="Enter new password">
                
                <label style="margin-top: 15px; display: block;">Confirm New Password</label>
                <input type="password" name="confirm_new_password" class="search-input" placeholder="Confirm new password">
                
                <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 25px;">
                    <button type="button" class="btn-close" onclick="closeModal('editProfileModal')">Cancel</button>
                    <button type="submit" class="btn-submit" style="background: #0284c7;">Save Changes</button>
                </div>
            </form>
        </div>
    </div>
"""

btn_html = """
            <button class="btn-submit" style="background: #3b82f6; border-radius: 20px; padding: 6px 15px; font-size: 13px;" onclick="openModal('editProfileModal')">
                <i class="fa-solid fa-user-pen"></i> Edit Profile
            </button>
"""

for d in dashboards:
    with open(d, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'id="editProfileModal"' not in content:
        # Inject modal before </body>
        if '</body>' in content:
            content = content.replace('</body>', modal_html + '\n</body>')
        else:
            content += modal_html
        
        # Inject button before Logout button
        # Usually looks like: <a href="{{ url_for('logout') }}" class="logout-btn">Logout</a>
        logout_regex = r'(<a\s+href="\{\{\s*url_for\(\'logout\'\)\s*\}\}"[^>]*>Logout</a>)'
        content = re.sub(logout_regex, btn_html + r'\1', content)
        
        with open(d, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {d}")
    else:
        print(f"Already updated {d}")
