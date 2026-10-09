import os

css_classes = """
/* Utility classes replacing inline styles */
.no-underline { text-decoration: none !important; }
.ml-2 { margin-left: 8px !important; }
.mr-1 { margin-right: 4px !important; }
.mr-2 { margin-right: 6px !important; }
.mt-10 { margin-top: 10px !important; }
.mt-40 { margin-top: 40px !important; }
.mt-45 { margin-top: 45px !important; }
.mb-12 { margin-bottom: 12px !important; }
.mb-25 { margin-bottom: 25px !important; }
.m-0 { margin: 0 !important; }
.text-sm { font-size: 13px !important; }
.text-xs { font-size: 12px !important; }
.text-md { font-size: 15px !important; }
.font-bold { font-weight: bold !important; }
.text-success { color: #16a34a !important; }
.text-danger { color: #dc2626 !important; }
.text-secondary { color: var(--text-secondary) !important; }
.text-center { text-align: center !important; }
.btn-sm { padding: 4px 8px !important; font-size: 11px !important; }
.btn-red { background: #dc2626 !important; }
.btn-yellow { background: #f59e0b !important; }
.btn-delete { background: none; border: none; color: #ef4444; font-weight: bold; cursor: pointer; }
.flex-between { display: flex; justify-content: space-between; align-items: center; }
.flex-center { display: flex; justify-content: center; }
.flex-wrap { flex-wrap: wrap; }
.gap-12 { gap: 12px !important; }
.gap-15 { gap: 15px !important; }
.relative { position: relative; }
.min-w-280 { min-width: 280px; }
.mw-550 { max-width: 550px !important; }
.search-input { width: 100%; padding: 8px 14px; border: 1.5px solid #16a34a; border-radius: 25px; font-size: 13.5px; outline: none; background: var(--input-bg); color: var(--input-text); }
.hidden-row { display: none !important; }
.rounded-full { border-radius: 20px !important; }
.px-5 { padding: 8px 22px !important; }
"""

html_replacements = [
    ('class="logo" style="text-decoration: none;"', 'class="logo no-underline"'),
    ('class="badge" style="background: #dcfce7; color: #15803d; font-size: 13px; margin-left: 8px;"', 'class="badge approved text-sm ml-2"'),
    ('<strong style="color: #16a34a; font-size: 15px;">', '<strong class="text-success text-md">'),
    ('class="badge" style="background: #e0f2fe; color: #0284c7;"', 'class="badge in_progress"'),
    ('<small style="color: var(--text-secondary);">', '<small class="text-secondary">'),
    ('class="badge" style="background: #fef3c7; color: #b45309; font-weight: bold;"', 'class="badge pending font-bold"'),
    ('class="badge" style="background: #dcfce7; color: #15803d; font-weight: bold;"', 'class="badge approved font-bold"'),
    ('class="badge" style="background: #fee2e2; color: #b91c1c; font-weight: bold;"', 'class="badge rejected font-bold"'),
    ('class="btn-submit"\\n                                style="padding: 4px 8px; font-size: 11px; background: #16a34a; text-decoration: none; margin-right: 4px;"', 'class="btn-submit btn-sm btn-green no-underline mr-1"'),
    ('class="btn-submit"\\n                                style="padding: 4px 8px; font-size: 11px; background: #dc2626; text-decoration: none; margin-right: 4px;"', 'class="btn-submit btn-sm btn-red no-underline mr-1"'),
    ('<small style="color: var(--text-secondary); margin-right: 6px;">', '<small class="text-secondary mr-2">'),
    ('style="background: none; border: none; color: #ef4444; font-weight: bold; cursor: pointer;"', 'class="btn-delete"'),
    ('colspan="8" style="text-align: center; color: var(--text-secondary);"', 'colspan="8" class="text-center text-secondary"'),
    ('style="display: flex; justify-content: space-between; align-items: center; margin-top: 45px; margin-bottom: 12px; flex-wrap: wrap; gap: 15px;"', 'class="flex-between mt-45 mb-12 flex-wrap gap-15"'),
    ('style="margin: 0;"', 'class="m-0"'),
    ('style="position: relative; min-width: 280px;"', 'class="relative min-w-280"'),
    ('style="width: 100%; padding: 8px 14px; border: 1.5px solid #16a34a; border-radius: 25px; font-size: 13.5px; outline: none; background: var(--input-bg); color: var(--input-text);"', 'class="search-input"'),
    ('class="fee-row" style="{% if loop.index > 4 %}display: none;{% endif %}"', 'class="fee-row {% if loop.index > 4 %}hidden-row{% endif %}"'),
    ('<strong style="color: #16a34a;">', '<strong class="text-success">'),
    ('<strong style="color: #dc2626;">', '<strong class="text-danger">'),
    ('class="btn-submit"\\n                                style="padding: 4px 8px; font-size: 11px; background: #f59e0b; text-decoration: none; margin-right: 4px;"', 'class="btn-submit btn-sm btn-yellow no-underline mr-1"'),
    ('style="color: #16a34a; font-weight: bold; font-size: 12px; margin-right: 4px;"', 'class="text-success font-bold text-xs mr-1"'),
    ('colspan="8" style="text-align: center; color: var(--text-secondary);"', 'colspan="8" class="text-center text-secondary"'),
    ('style="text-align: center; margin-top: 10px; margin-bottom: 25px;"', 'class="text-center mt-10 mb-25"'),
    ('class="btn-submit"\\n                style="background: #16a34a; font-size: 13px; padding: 8px 22px; border-radius: 20px;"', 'class="btn-submit btn-green text-sm px-5 rounded-full"'),
    ('style="margin-top: 40px;"', 'class="mt-40"'),
    ('colspan="5" style="text-align: center; color: var(--text-secondary);"', 'colspan="5" class="text-center text-secondary"'),
    ('class="badge" style="background: #fef08a; color: #854d0e;"', 'class="badge private-memo-badge"'),
    ('class="modal-content" style="max-width: 550px;"', 'class="modal-content mw-550"'),
    ('class="btn-submit" style="background: #16a34a;"', 'class="btn-submit btn-green"'),
    ('style="display: flex; justify-content: center; gap: 12px;"', 'class="flex-center gap-12"'),
]

css_file = "c:/Users/Asus/Desktop/campus_connect_project - Copy/static/css/style.css"
html_file = "c:/Users/Asus/Desktop/campus_connect_project - Copy/templates/accountant-dashboard.html"

# Append CSS
with open(css_file, "a", encoding="utf-8") as f:
    f.write(css_classes)

# Replace HTML
with open(html_file, "r", encoding="utf-8") as f:
    html_content = f.read()

for old, new in html_replacements:
    html_content = html_content.replace(old.replace("\\n", "\n"), new)

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print("Styles fixed successfully.")
