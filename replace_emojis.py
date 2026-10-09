import os

template_dir = r"c:\Users\Asus\Desktop\campus_connect_project - Copy\templates"

replacements = {
    '📩 Send OTP': '<i class="fa-solid fa-envelope"></i> Send OTP',
    '📩 Resend OTP': '<i class="fa-solid fa-rotate-right"></i> Resend OTP',
    '🖨️ Print Slip': '<i class="fa-solid fa-print"></i> Print Slip',
    '🖨️ Print Pass': '<i class="fa-solid fa-print"></i> Print Pass',
    '🚨 {{ urgent_alert.category }}': '<i class="fa-solid fa-triangle-exclamation"></i> {{ urgent_alert.category }}',
    '⚠ Partial Due': '<i class="fa-solid fa-circle-exclamation"></i> Partial Due',
    '🚨 Payment Pending': '<i class="fa-solid fa-triangle-exclamation"></i> Payment Pending',
    '🚨 Overdue Warning': '<i class="fa-solid fa-triangle-exclamation"></i> Overdue Warning',
    '🚨 Library Overdue': '<i class="fa-solid fa-triangle-exclamation"></i> Library Overdue',
    '👨‍🏫 ': '',
    '👨‍‍🏫 ': '',
    '🚪 Allocate Hostel Room to Student': '<i class="fa-solid fa-door-open"></i> Allocate Hostel Room to Student',
    '<h3>🚪 Allocate Hostel Room & Accommodation</h3>': '<h3><i class="fa-solid fa-building-user"></i> Allocate Hostel Room & Accommodation</h3>',
    '📥 Student Leave Requests Assigned to You': '<i class="fa-solid fa-inbox"></i> Student Leave Requests Assigned to You',
    '🚀 Publish All Subjects Marksheet & Notify Student': '<i class="fa-solid fa-paper-plane"></i> Publish All Subjects Marksheet & Notify Student'
}

for filename in os.listdir(template_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(template_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = False
        for old_str, new_str in replacements.items():
            if old_str in content:
                content = content.replace(old_str, new_str)
                modified = True
                
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {filename}")
