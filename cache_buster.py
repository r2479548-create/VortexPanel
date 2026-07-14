import time
v = int(time.time())

with open(r'e:\VortexPanel-main\VortexPanel-main\web\templates\admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('src="/static/js/app.js"', f'src="/static/js/app.js?v={v}"')
text = text.replace('href="/static/css/theme.css"', f'href="/static/css/theme.css?v={v}"')

with open(r'e:\VortexPanel-main\VortexPanel-main\web\templates\admin.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Done")
