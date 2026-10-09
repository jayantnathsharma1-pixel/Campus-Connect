import os
import glob

TEMPLATE_DIR = r"c:\Users\Asus\Desktop\campus_connect_project - Copy\templates"

def polish_buttons():
    for filepath in glob.glob(os.path.join(TEMPLATE_DIR, "*.html")):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        changed = False

        replacements = {
            '>Submit Payment': '><i class="fa-solid fa-paper-plane"></i> Submit Payment',
            '>Submit to Teacher': '><i class="fa-solid fa-paper-plane"></i> Submit to Teacher',
            '>Submit Review': '><i class="fa-solid fa-paper-plane"></i> Submit Review',
            '>Submit Complaint': '><i class="fa-solid fa-paper-plane"></i> Submit Complaint',
            '>Add Book': '><i class="fa-solid fa-plus"></i> Add Book',
            '>Issue Book': '><i class="fa-solid fa-share-from-square"></i> Issue Book',
            '>Apply Leave': '><i class="fa-solid fa-person-walking-arrow-right"></i> Apply Leave',
            '>Request Pass': '><i class="fa-solid fa-id-card-clip"></i> Request Pass',
            '>Apply Certificate': '><i class="fa-solid fa-file-contract"></i> Apply Certificate',
            '>Search & Borrow': '><i class="fa-solid fa-magnifying-glass"></i> Search & Borrow'
        }

        for old, new in replacements.items():
            if old in content:
                content = content.replace(old, new)
                changed = True

        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Polished {os.path.basename(filepath)}")

if __name__ == '__main__':
    polish_buttons()
