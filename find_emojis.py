import os
import re

template_dir = r"c:\Users\Asus\Desktop\campus_connect_project - Copy\templates"
# Regex for matching emojis
emoji_pattern = re.compile(r'[\U00010000-\U0010ffff\u2600-\u27ff]')

with open("emojis_found.txt", "w", encoding="utf-8") as out_f:
    for filename in os.listdir(template_dir):
        if filename.endswith(".html"):
            filepath = os.path.join(template_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines):
                emojis = emoji_pattern.findall(line)
                if emojis:
                    out_f.write(f"{filename}:{i+1} : {''.join(set(emojis))} : {line.strip()}\n")
