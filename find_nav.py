with open(r'e:\VortexPanel-main\VortexPanel-main\web\static\js\app.js', 'r', encoding='utf-8') as f:
    text = f.read().split('\n')

with open(r'e:\VortexPanel-main\VortexPanel-main\nav_output.txt', 'w', encoding='utf-8') as out:
    for i, line in enumerate(text):
        if "id:'dashboard'" in line.replace(" ", "") or "id:\"dashboard\"" in line.replace(" ", "") or "id:`dashboard`" in line.replace(" ", ""):
            out.write(f"Found dashboard at line {i+1}: {line.strip()}\n")
            for j in range(max(0, i-5), min(len(text), i+50)):
                out.write(f"{j+1}: {text[j]}\n")
            break
