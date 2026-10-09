import os
import re
import glob

TEMPLATE_DIR = r"c:\Users\Asus\Desktop\campus_connect_project - Copy\templates"

FA_CDN = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">\n    <link rel="stylesheet"'

EMOJI_MAP = {
    '🏛️': '<i class="fa-solid fa-building-columns"></i>',
    '📅': '<i class="fa-solid fa-calendar-days"></i>',
    '📜': '<i class="fa-solid fa-file-contract"></i>',
    '🍽️': '<i class="fa-solid fa-utensils"></i>',
    '🎓': '<i class="fa-solid fa-user-graduate"></i>',
    '👔': '<i class="fa-solid fa-chalkboard-user"></i>',
    '📢': '<i class="fa-solid fa-bullhorn"></i>',
    '💳': '<i class="fa-solid fa-money-check-dollar"></i>',
    '📊': '<i class="fa-solid fa-chart-column"></i>',
    '📚': '<i class="fa-solid fa-book"></i>',
    '📬': '<i class="fa-solid fa-envelope-open-text"></i>',
    '📝': '<i class="fa-solid fa-pen-to-square"></i>',
    '📖': '<i class="fa-solid fa-book-open"></i>',
    '⚡': '<i class="fa-solid fa-bolt"></i>',
    '🏢': '<i class="fa-solid fa-building"></i>',
    '🧾': '<i class="fa-solid fa-file-invoice-dollar"></i>',
    '🔐': '<i class="fa-solid fa-shield-halved"></i>',
}

TEXT_MAP = {
    r'Sent Notices &amp; Direct Messages': r'<i class="fa-solid fa-paper-plane"></i> Sent Notices &amp; Direct Messages',
    r'Direct Communications &amp; Campus Notices': r'<i class="fa-solid fa-paper-plane"></i> Direct Communications &amp; Campus Notices',
    r'My Leave & Gate Pass Requests': r'<i class="fa-solid fa-door-open"></i> My Leave & Gate Pass Requests',
    r'My Document & Certificate Requests': r'<i class="fa-solid fa-file-invoice"></i> My Document & Certificate Requests',
    r'My Filed Electrical & Repair Complaints': r'<i class="fa-solid fa-screwdriver-wrench"></i> My Filed Electrical & Repair Complaints',
    r'My Mess Ratings & Reviews': r'<i class="fa-solid fa-star"></i> My Mess Ratings & Reviews',
    r'^Campus Services$': r'<i class="fa-solid fa-concierge-bell"></i> Campus Services',
    r'^Leave Request$': r'<i class="fa-solid fa-person-walking-arrow-right"></i> Leave Request',
    r'^Gate Pass$': r'<i class="fa-solid fa-id-card-clip"></i> Gate Pass',
    r'^Certificates$': r'<i class="fa-solid fa-certificate"></i> Certificates',
    r'^Mess Feedback$': r'<i class="fa-solid fa-comment-dots"></i> Mess Feedback',
    r'^Dashboard$': r'<i class="fa-solid fa-chart-pie"></i> Dashboard',
}

def update_templates():
    for filepath in glob.glob(os.path.join(TEMPLATE_DIR, "*.html")):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        # 1. Add FA CDN
        if 'font-awesome' not in content:
            new_content = content.replace('<link rel="stylesheet"', FA_CDN, 1)
            if new_content != content:
                content = new_content
                changed = True

        # 2. Replace emojis in h2 tags (and only h2 tags to be safe, or just globally since we map specific emojis)
        # It's better to replace globally in dashboard text, but emojis inside span/button are fine. We can replace globally for the known emojis.
        # Wait, the user said "for options like Dashboard, Attendance, Students, Teachers, Fees, Notices, and Logout".
        # It's better to specifically target <h2> contents and the logout button.
        
        # Let's replace the Logout button
        new_content = re.sub(
            r'<a([^>]*class="[^"]*logout-btn[^"]*"[^>]*)>Logout</a>',
            r'<a\1><i class="fa-solid fa-right-from-bracket"></i> Logout</a>',
            content
        )
        if new_content != content:
            content = new_content
            changed = True

        # Replace emojis in h2 tags
        def h2_repl(match):
            inner = match.group(2)
            for emoji, icon in EMOJI_MAP.items():
                inner = inner.replace(emoji + ' ', icon + ' ')
                inner = inner.replace(emoji, icon + ' ')
            
            for text, replacement in TEXT_MAP.items():
                inner = re.sub(text, replacement, inner)
            return f'<h2{match.group(1)}>{inner}</h2>'

        new_content = re.sub(r'<h2(.*?)>(.*?)</h2>', h2_repl, content, flags=re.DOTALL)
        if new_content != content:
            content = new_content
            changed = True
        
        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {os.path.basename(filepath)}")

if __name__ == '__main__':
    update_templates()
