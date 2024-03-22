# Intrati pe site-ul https://www.elefant.ro/ si efectuati urmatoarele teste:

import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.maximize_window()

driver.get('https://www.elefant.ro/')
time.sleep(2)

# Test 1: Identificati butonul "accept cookies" si dati click pe el

accept_button = driver.find_element(By.CSS_SELECTOR, 'button#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
accept_button.click()
time.sleep(3)

"""
Test 2: cautati un produs la alegere (iphone 14) si verificati ca s-au returnat cel putin 10 rezultate
([class="product-title"])
"""

search_box = driver.find_element(By.NAME, 'SearchTerm')
search_box.send_keys('iphone 14')
search_box.submit()

time.sleep(3)

rezultate = driver.find_elements(By.CSS_SELECTOR, '.product-title')

assert len(rezultate) >= 10, 'Mai putin de 10 rezultate gasite'

# Test 3: Extrageti din lista produsul cu pretul cel mai mic [class="current-price "] -> //img[@class="product-image"]

# Liste de elemente cu nume produse si preturi
lista_elemente_nume = driver.find_elements(By.CSS_SELECTOR, '.product-title')
lista_elemente_pret = driver.find_elements(By.CLASS_NAME, 'current-price ')

# Lista tupluri (nume, pret)
lista_nume_pret = [
    (nume.text, float(pret.text.replace(' lei', '').replace(',', '.')))
    for nume, pret in zip(lista_elemente_nume, lista_elemente_pret)
    if pret.text != 'N/A'
]

# Sortare lista dupa elementul cu indexul 1 (pret)
lista_nume_pret.sort(key=lambda x: x[1])
print(lista_nume_pret)

# Extragere pret minim si nume produs cu pretul cel mai mic si afisare rezultate
pret_minim = lista_nume_pret[0][1]
nume_produs_pret_minim = lista_nume_pret[0][0]
print("Pretul cel mai mic este:", pret_minim)
print("Numele produsului cu pretul cel mai mic este:", nume_produs_pret_minim)

# Test 4: Extrageti titlul paginii si verificati ca este corect

page_title = driver.title

assert 'elefant' in page_title.lower()

"""
Test 5: Intrati pe site, accesati butonul cont si click pe conectare. Identificati elementele de tip user si parola si
inserati valori incorecte (valori incorecte inseamna oricare valori care nu sunt recunoscute drept cont valid)
"""

buton_cont = driver.find_element(By.XPATH, "//a[@data-toggle='collapse']//i[contains(text(), 'face')]")
buton_cont.click()
time.sleep(2)

link_conectare = driver.find_element(By.XPATH, "//a[@class='my-account-login btn btn-primary btn-block']")
link_conectare.click()
time.sleep(3)

email = driver.find_element(By.ID, 'ShopLoginForm_Login')
email.send_keys('gresit@test.com')

parola = driver.find_element(By.ID, 'ShopLoginForm_Password')
parola.send_keys('gresita')

"""
Test 6: Dati click pe butonul "conectare" si verificati urmatoarele:
           1. Faptul ca nu s-a facut logarea in cont
           2. Faptul ca se returneaza eroarea corecta
"""

login_button = driver.find_element(By.NAME, 'login')
login_button.click()
time.sleep(5)

login_button = driver.find_element(By.NAME, 'login')
assert login_button.is_displayed() is True

eroare_asteptata = 'Adresa dumneavoastră de email / Parola este incorectă. Vă rugăm să încercați din nou.'
eroare_primita = driver.find_element(By.XPATH, "//div[@role='alert']").text
assert eroare_primita == eroare_asteptata, "Mesaj eroare diferit de cel asteptat"

"""
Test 7: Stergeti valoarea de pe campul email si introduceti o valoare invalida (adica fara caracterul "@"), fara sa 
introduceti si parola si verificati faptul ca butonul de login este dezactivat
"""

email = driver.find_element(By.ID, 'ShopLoginForm_Login')
email.clear()
email.send_keys('invalid')
time.sleep(3)
login_button = driver.find_element(By.NAME, 'login')

assert login_button.is_enabled() is False

driver.quit()
