import os

file_path = r'e:\VortexPanel-main\VortexPanel-main\web\templates\admin.html'

with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the App Store table
html = html.replace('<table class="data-table" style="table-layout:fixed">', '<table class="data-table" style="table-layout:fixed;min-width:700px">')

# Fix flex rows that don't wrap
html = html.replace('display:flex;align-items:center;justify-content:space-between', 'display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML modified successfully.")
