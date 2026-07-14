with open(r'e:\VortexPanel-main\VortexPanel-main\web\templates\admin.html', 'r', encoding='utf-8') as f:
    text = f.read()
    print('Users Page: ', 'x-data="usersPage()"' in text)
    print('Plans Page: ', 'x-data="plansPage()"' in text)
    print('Orders Page: ', 'x-data="ordersPage()"' in text)
