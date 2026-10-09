import os
import glob

directory = r'c:\Users\Asus\Desktop\campus_connect_project - Copy\templates'
files = glob.glob(os.path.join(directory, '*.html'))

font_awesome_link = '    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">\n'

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'font-awesome' not in content.lower():
        content = content.replace('</head>', font_awesome_link + '</head>')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            print(f"Fixed {filepath}")
