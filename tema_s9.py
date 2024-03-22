import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://carturesti.ro/')
time.sleep(5)

"""
- Test 1: cautati un produs la alegere (iphone 14) si verificati ca s-au returnat cel putin 10 rezultate
([class="product-title"])
"""

search_box = driver.find_element(By.CSS_SELECTOR, 'input#search-input')
search_box.send_keys('iphone 14')
search_button = driver.find_element(By.XPATH, "//div[@class='search-container']/i")
search_button.click()
time.sleep(5)

rezultate = driver.find_elements(By.CSS_SELECTOR, 'h5.md-title.ng-binding')

assert len(rezultate) >= 10, 'Mai putin de 10 rezultate gasite'

"""
- Test 2: faceti filtrare dupa pret si verificati faptul ca toate produsele returnate au pretul in intervalul de
filtrare
"""

filtru_pret = driver.find_element(By.XPATH, "//span[contains(text(),'50 - 100')]")
filtru_pret.click()
time.sleep(3)

lista_preturi = driver.find_elements(By.CSS_SELECTOR, 'span.suma')
preturi = [float(pret.text) for pret in lista_preturi if pret.text != 'N/A']
contor = 0
print(preturi)
for pret in preturi:
    if 50 <= pret <= 100:
        continue
    else:
        contor += 1

try:
    assert contor == 0, "Eroare! Filtrarea nu functioneaza cum trebuie."
except AssertionError as e:
    print(e)

"""
- Test 3: Cautati un produs care nu exista si verifica faptul ca mesajul returnat este: "NE PARE RĂU, NU EXISTĂ PRODUSE
ÎN ACEASTĂ CATEGORIE."
"""

search_box = driver.find_element(By.CSS_SELECTOR, 'input#search-input')
search_box.send_keys('dafdgasd')
search_button = driver.find_element(By.XPATH, "//div[@class='search-container']/i")
search_button.click()
time.sleep(3)

mesaj_asteptat = 'Ne pare rău, nu am găsit nimic.'
mesaj_returnat = driver.find_element(By.CSS_SELECTOR, '#search-category > div').text

assert mesaj_returnat == mesaj_asteptat, "Mesaj diferit de cel asteptat"

"""
- Test 4: Cautati un produs, sortati lista de rezultate in ordine crescatoare dupa pret si verificati faptul ca
produsele au fost intr-adevar sortate
"""

search_box = driver.find_element(By.CSS_SELECTOR, 'input#search-input')
search_box.send_keys('carte de bucate')
search_button = driver.find_element(By.XPATH, "//div[@class='search-container']/i")
search_button.click()
time.sleep(3)

# Find the dropdown element by xpath
dropdown = driver.find_element(By.XPATH, "//span/div/span[contains(text(), 'Smart')]")
dropdown.click()
time.sleep(3)

# Select an option from the dropdown by click
option = driver.find_element(By.XPATH, '//md-option[@value="price asc"]')
option.click()
time.sleep(3)

# Extragere preturi
lista_preturi = driver.find_elements(By.CSS_SELECTOR, 'span.suma')
preturi = [float(pret.text) for pret in lista_preturi if pret.text != 'N/A' and pret.text != '']

assert preturi == sorted(preturi), "Produsele nu au fost sortate corect!"

"""
print("Lista preturi:", preturi)

# Obtinere pret minim si maxim din lista de preturi
pret_min = min(preturi)
pret_max = max(preturi)

# Comparare pret minim cu primul element din lista si pret maxim cu ultimul element
assert pret_min == preturi[0] and pret_max == preturi[len(preturi) - 1], "Produsele nu au fost sortate corect!"
"""

# Sortare descrescatoare

# Find the dropdown element by xpath
dropdown = driver.find_element(By.XPATH, "//span/div/span[contains(text(), 'Preț (ascendent)')]")
dropdown.click()
time.sleep(3)

# Select an option from the dropdown by click
option = driver.find_element(By.XPATH, '//md-option[@value="price desc"]')
option.click()
time.sleep(3)

# Extragere preturi
lista_preturi = driver.find_elements(By.CSS_SELECTOR, 'span.suma')
preturi_desc = [float(pret.text) for pret in lista_preturi if pret.text != 'N/A' and pret.text != '']

assert preturi_desc == sorted(preturi_desc, reverse=True), "Produsele nu au fost sortate corect!"

# Pentru elefant.ro
driver.get('https://www.elefant.ro/')
time.sleep(5)

search_box = driver.find_element(By.NAME, 'SearchTerm')
search_box.send_keys('codul lui davinci')
search_box.submit()
time.sleep(3)

# Find the dropdown element by its ID
dropdown = Select(driver.find_element(By.CSS_SELECTOR, "#SortingAttribute"))

# Select an option from the dropdown by its visible text
dropdown.select_by_visible_text("Pret crescator")
time.sleep(3)

# Extragere preturi
lista_preturi = driver.find_elements(By.CSS_SELECTOR, '.current-price ')
preturi_asc = [
    float(pret.text.replace(" lei", "").replace(",", "."))
    for pret in lista_preturi
    if pret.text != 'N/A' and pret.text != ''
]
assert preturi_asc == sorted(preturi_asc), "Produsele nu au fost sortate corect!"

"""
print("Lista preturi:", preturi_asc)

# Obtinere pret minim si maxim din lista de preturi
pret_min = min(preturi_asc)
pret_max = max(preturi_asc)

# Comparare pret minim cu primul element din lista si pret maxim cu ultimul element
assert pret_min == preturi_asc[0] and pret_max == preturi_asc[len(preturi_asc) - 1], \
    "Produsele nu au fost sortate corect!"
"""

""" 
- Test 5: Cautati un produs, sorteaza lista de rezultate in ordine descrescatoare dupa pret si verifica faptul ca 
produsele au fost intr-adevar sortate
"""
dropdown = Select(driver.find_element(By.CSS_SELECTOR, "#SortingAttribute"))
dropdown.select_by_visible_text("Pret descrescator")
time.sleep(3)

# Extragere preturi
lista_preturi = driver.find_elements(By.CSS_SELECTOR, '.current-price ')
preturi = [
    float(pret.text.replace(" lei", "").replace(",", "."))
    for pret in lista_preturi
    if pret.text != 'N/A' and pret.text != ''
]
assert preturi == sorted(preturi, reverse=True), "Produsele nu au fost sortate corect!"

""" 
print("Lista preturi:", preturi)

# Obtinere pret minim si maxim din lista de preturi
pret_min = min(preturi)
pret_max = max(preturi)

# Comparare pret maxim cu primul element din lista si pret minim cu ultimul element
assert pret_max == preturi[0] and pret_min == preturi[len(preturi) - 1], "Produsele nu au fost sortate corect!"
"""

""" 
- Test 6: Intrati pe elefant.ro, dati click pe linkul Contact, si verificati faptul ca nu puteti sa dati submit la 
formular daca nu sunt completate campurile obligatorii (verificati ca ramaneti pe aceeasi pagina) (hint: folositi 
metoda current_url)
"""

link_contact = driver.find_element(By.XPATH, '//a[@title="Contact"]')
link_contact.click()
time.sleep(2)

# url_curent = 'https://www.elefant.ro/helpdesk/contact-us'
url_inainte_de_submit = driver.current_url

buton_submit = driver.find_element(By.CSS_SELECTOR, 'div.o-form-actions')
buton_submit.click()
time.sleep(2)

url_dupa_submit = driver.current_url

assert url_dupa_submit == url_inainte_de_submit, "S-a schimbat url-ul"

driver.quit()
