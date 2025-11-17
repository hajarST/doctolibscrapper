import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.doctolib.fr/medecin-generaliste/?page="
START_PAGE = 1
END_PAGE = 2

def scrape_doctolib():
    data = []

    # ⚙️ Configuration de Chrome avec Selenium Stealth
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--lang=fr-FR")
    # chrome_options.add_argument("--headless")  # 👉 à activer si tu veux sans interface

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    stealth(driver,
            languages=["fr-FR", "fr"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
    )

    for page_number in range(START_PAGE, END_PAGE + 1):
        url = BASE_URL + str(page_number)
        print(f"\n🔍 Chargement de la page {page_number} : {url}")
        driver.get(url)
        time.sleep(4)

        # Scroll pour charger plus de résultats
        for _ in range(4):
            driver.execute_script("window.scrollBy(0, 3000);")
            time.sleep(2)

        # Extraire les liens des profils
        links = []
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, "div.flex.justify-between > a[href*='/medecin-generaliste/']")
            links = list(set([el.get_attribute("href") for el in elements if el.get_attribute("href")]))
            print(f"🔗 {len(links)} profils trouvés sur la page {page_number}.")
        except:
            print("❌ Aucune donnée trouvée sur cette page.")
            continue

        for link in links:
            try:
                driver.execute_script("window.open(arguments[0]);", link)
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(3)

                # Nom
                try:
                    name = driver.find_element(By.CSS_SELECTOR, "h1#profile-name-with-title span[itemprop='name']").text.strip()
                except:
                    name = "Nom non trouvé"

                # Fonction
                try:
                    fonction = driver.find_element(By.CSS_SELECTOR, "div.dl-profile-header-speciality span").text.strip()
                except:
                    fonction = "Fonction non trouvée"

                # Téléphone
                try:
                    phone = driver.find_element(By.XPATH, "//h3[contains(., 'Coordonnées')]/following::div[contains(@class, 'flex')]").text.strip()
                except:
                    phone = "Téléphone non trouvé"

                # Expérience
                try:
                    exp_entries = driver.find_elements(By.CSS_SELECTOR, "h3.dl-profile-card-title:has-text('Expérience') ~ div.dl-profile-text.dl-profile-entry")
                    experience = "\n".join([e.text.strip() for e in exp_entries if e.text.strip()])
                    if not experience:
                        experience = "Expérience non précisée"
                except:
                    experience = "Expérience non précisée"

                # Diplômes
                try:
                    dipl_entries = driver.find_elements(By.XPATH, "//h3[contains(., 'Diplômes')]/following::div[contains(@class,'dl-profile-text')]")
                    diplomes = "\n".join([d.text.strip() for d in dipl_entries if d.text.strip()])
                    if not diplomes:
                        diplomes = "Non précisés"
                except:
                    diplomes = "Non précisés"

                # Adresse
                try:
                    cabinet_name = driver.find_element(By.CSS_SELECTOR, ".dl-profile-practice-name").text.strip()
                except:
                    cabinet_name = ""
                try:
                    address_text = driver.find_element(By.CSS_SELECTOR, "div[id^='practice-address-']").text.strip()
                except:
                    address_text = ""
                address = f"{cabinet_name} - {address_text}".strip(" -") if (cabinet_name or address_text) else "Adresse non trouvée"

                # Horaires
                try:
                    horaires_elements = driver.find_elements(By.CSS_SELECTOR, "div.js-opening-hours ul li div[itemprop='openingHours']")
                    horaires = "\n".join([h.text.strip() for h in horaires_elements])
                    if not horaires:
                        horaires = "Horaires non trouvés"
                except:
                    horaires = "Horaires non trouvés"

                # Numéro RPPS
                try:
                    rpps = driver.find_element(By.XPATH, "//p[contains(text(), 'Numéro RPPS')]/following-sibling::p").text.strip()
                except:
                    rpps = "Non trouvé"

                # SIREN
                try:
                    siren = driver.find_element(By.XPATH, "//p[contains(text(), 'SIREN')]/following-sibling::p").text.strip()
                except:
                    siren = "Non trouvé"

                # Sauvegarde
                data.append({
                    "Nom": name,
                    "Fonction": fonction,
                    "Téléphone": phone,
                    "Expérience": experience,
                    "Diplômes": diplomes,
                    "Adresse": address,
                    "Horaires": horaires,
                    "Numéro RPPS": rpps,
                    "SIREN": siren,
                    "Lien": link
                })

                print(f"✅ Profil {len(data)} extrait : {name} | 🔗 {link}")

                # Fermer l’onglet et revenir à la page liste
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)

            except Exception as e:
                print(f"⚠️ Erreur sur {link} : {e}")
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue

    driver.quit()

    # ✅ Sauvegarde Excel
    df = pd.DataFrame(data)
    df.to_excel(f"doctolib_selenium_page_{START_PAGE}_to_{END_PAGE}.xlsx", index=False)
    print(f"\n📁 Données enregistrées dans doctolib_selenium_page_{START_PAGE}_to_{END_PAGE}.xlsx (Total : {len(data)} profils) ✅")

if __name__ == "__main__":
    scrape_doctolib()
