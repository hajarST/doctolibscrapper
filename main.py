from playwright.sync_api import sync_playwright
import pandas as pd
import time

BASE_URL = "https://www.doctolib.fr/medecin-generaliste/?page="
START_PAGE = 1   # 🔁 Page de départ
END_PAGE = 2     # 🔁 Dernière page à scraper (change ici pour 50, 100, etc.)

def scrape_doctolib():
    data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=120)
        context = browser.new_context()

        for page_number in range(START_PAGE, END_PAGE + 1):
            url = BASE_URL + str(page_number)
            print(f"\n🔍 Chargement de la page {page_number} : {url}")
            page = context.new_page()
            page.goto(url, timeout=120000)
            page.wait_for_timeout(3000)

            # Scroll pour charger les résultats dynamiques
            for _ in range(4):
                page.mouse.wheel(0, 3000)
                time.sleep(2)

            # ✅ Sélecteur corrigé pour les vrais profils
            try:
                page.wait_for_selector("div.flex.justify-between > a[href*='/medecin-generaliste/']", timeout=15000)
                links = page.eval_on_selector_all(
                    "div.flex.justify-between > a[href*='/medecin-generaliste/']",
                    "elements => elements.map(el => el.href)"
                )
                links = list(set(links))
                print(f"🔗 {len(links)} profils trouvés sur la page {page_number}.")
            except:
                print("❌ Aucune donnée trouvée sur cette page.")
                links = []

            # Boucle sur chaque profil
            for idx, link in enumerate(links):
                try:
                    profile_page = context.new_page()
                    profile_page.goto(link, timeout=60000)
                    profile_page.wait_for_timeout(2000)

                    # Nom
                    try:
                        profile_page.wait_for_selector("h1#profile-name-with-title span[itemprop='name']", timeout=5000)
                        name = profile_page.locator("h1#profile-name-with-title span[itemprop='name']").inner_text().strip()
                    except:
                        name = "Nom non trouvé"

                    # Fonction
                    try:
                        fonction = profile_page.locator("div.dl-profile-header-speciality span").inner_text().strip()
                    except:
                        fonction = "Fonction non trouvée"

                    # Téléphone
                    try:
                        phone = profile_page.locator("div.dl-profile-box:has(h3:has-text('Coordonnées')) div.flex").inner_text().strip()
                    except:
                        phone = "Téléphone non trouvé"

                    # Expérience
                    experience_list = []
                    try:
                        exp_container = profile_page.locator("h3.dl-profile-card-title:has-text('Expérience')").locator("..")
                        entries = exp_container.locator("div.dl-profile-text.dl-profile-entry")
                        for i in range(entries.count()):
                            time_text = entries.nth(i).locator("div.dl-profile-entry-time").inner_text().strip()
                            label_text = entries.nth(i).locator("p.dl-profile-entry-label").inner_text().strip()
                            if time_text:
                                experience_list.append(f"{label_text} ({time_text})")
                            else:
                                experience_list.append(label_text)
                        experience = "\n".join(experience_list)
                    except:
                        experience = "Expérience non précisée"

                    # Diplômes
                    diplômes_list = []
                    try:
                        dipl_container = profile_page.locator("h3.dl-profile-card-title:has-text('Diplômes nationaux et universitaires')").locator("..")
                        dipl_entries = dipl_container.locator("div.dl-profile-text.dl-profile-entry")
                        for i in range(dipl_entries.count()):
                            year = dipl_entries.nth(i).locator("div.dl-profile-entry-time").inner_text().strip()
                            label = dipl_entries.nth(i).locator("p.dl-profile-entry-label").inner_text().strip()
                            diplômes_list.append(f"{label} ({year})")
                        diplomes = "\n".join(diplômes_list)
                    except:
                        diplomes = "Non précisés"

                    # Adresse
                    try:
                        cabinet_name = profile_page.locator("div.dl-profile-text div .dl-profile-practice-name").inner_text().strip()
                    except:
                        cabinet_name = ""

                    try:
                        address_element = profile_page.locator("div.dl-profile-text div div[id^='practice-address-']")
                        address_text = address_element.inner_text().strip()
                    except:
                        address_text = ""

                    if cabinet_name or address_text:
                        address = f"{cabinet_name} - {address_text}".strip(" -")
                    else:
                        address = "Adresse non trouvée"

                    # Horaires
                    try:
                        horaires_list = []
                        horaires_elements = profile_page.locator("div.js-opening-hours ul li div[itemprop='openingHours']")
                        for i in range(horaires_elements.count()):
                            horaires_list.append(horaires_elements.nth(i).inner_text().strip())
                        horaires = "\n".join(horaires_list)
                    except:
                        horaires = "Horaires non trouvés"

                    # Numéro RPPS
                    try:
                        rpps = profile_page.locator("p:has-text('Numéro RPPS') + p").inner_text().strip()
                    except:
                        rpps = "Non trouvé"

                    # SIREN
                    try:
                        siren = profile_page.locator("p:has-text('SIREN') + p").inner_text().strip()
                    except:
                        siren = "Non trouvé"

                    # Ajouter au tableau
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
                    profile_page.close()

                except Exception as e:
                    print(f"⚠️ Erreur lors de l'extraction : {e}")
                    continue

            page.close()

        browser.close()

    # Sauvegarde Excel
    df = pd.DataFrame(data)
    df.to_excel(f"doctolib_doctors_page_{START_PAGE}_to_{END_PAGE}.xlsx", index=False, engine='openpyxl')
    print(f"\n📁 Données enregistrées dans doctolib_doctors_page_{START_PAGE}_to_{END_PAGE}.xlsx (Total : {len(data)} profils) ✅")

if __name__ == "__main__":
    scrape_doctolib()
