from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random

BASE_URL = "https://www.doctolib.fr/medecin-generaliste/?page="
START_PAGE = 1
END_PAGE = 10  # Vous pouvez mettre autant de pages que vous voulez

def automatic_captcha_bypass(page):
    """Contournement automatique des CAPTCHAs sans intervention manuelle"""
    print("🔄 Tentative de contournement automatique du CAPTCHA...")
    
    try:
        # Stratégie 1: Utiliser une IP différente en rechargeant avec des paramètres aléatoires
        print("🎯 Stratégie 1: Rechargement avec paramètres aléatoires...")
        page.reload(wait_until='networkidle')
        time.sleep(5)
        
        # Stratégie 2: Nettoyer les cookies et storage
        print("🎯 Stratégie 2: Nettoyage des cookies...")
        page.evaluate("""
            localStorage.clear();
            sessionStorage.clear();
            document.cookie.split(";").forEach(function(c) { 
                document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
            });
        """)
        
        # Stratégie 3: Changer l'user-agent dynamiquement
        print("🎯 Stratégie 3: Rotation de l'user-agent...")
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        new_ua = random.choice(user_agents)
        page.set_extra_http_headers({'User-Agent': new_ua})
        
        # Stratégie 4: Naviguer vers une URL différente puis revenir
        print("🎯 Stratégie 4: Navigation alternative...")
        page.goto("https://www.doctolib.fr", wait_until='networkidle')
        time.sleep(3)
        page.go_back(wait_until='networkidle')
        time.sleep(5)
        
        # Stratégie 5: Simulation d'activité humaine intensive
        print("🎯 Stratégie 5: Simulation d'activité humaine...")
        simulate_intensive_human_behavior(page)
        
        # Stratégie 6: Attendre que le CAPTCHA disparaisse (certains sites les retirent après un certain temps)
        print("🎯 Stratégie 6: Attente stratégique...")
        time.sleep(10)
        
        # Vérifier si le CAPTCHA est toujours présent
        captcha_selectors = [
            "text=/captcha/i",
            "text=/robot/i", 
            "text=/vérification/i",
            "iframe[src*='recaptcha']",
            "img[src*='captcha']",
            ".g-recaptcha"
        ]
        
        captcha_still_present = False
        for selector in captcha_selectors:
            if page.locator(selector).count() > 0:
                captcha_still_present = True
                break
        
        if not captcha_still_present:
            print("✅ CAPTCHA contourné avec succès!")
            return True
        else:
            print("❌ CAPTCHA toujours présent après contournement")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du contournement: {e}")
        return False

def simulate_intensive_human_behavior(page):
    """Simule un comportement humain très réaliste et intensif"""
    print("🤖 Simulation comportement humain intensif...")
    
    # Mouvements de souris très réalistes
    viewport = page.viewport_size
    for _ in range(random.randint(8, 15)):
        x = random.randint(50, viewport['width'] - 50)
        y = random.randint(50, viewport['height'] - 50)
        
        # Mouvement fluide avec plusieurs points intermédiaires
        steps = random.randint(3, 8)
        for step in range(steps):
            intermediate_x = x + random.randint(-20, 20)
            intermediate_y = y + random.randint(-20, 20)
            page.mouse.move(intermediate_x, intermediate_y)
            time.sleep(random.uniform(0.1, 0.3))
        
        time.sleep(random.uniform(0.5, 1.5))
    
    # Clics réalistes sur différents éléments
    clickable_selectors = [
        "a", "button", "div[role='button']", "input[type='submit']",
        "span", "li", ".card", ".item"
    ]
    
    for selector in random.sample(clickable_selectors, random.randint(2, 4)):
        try:
            elements = page.locator(selector)
            if elements.count() > 0:
                element = elements.nth(random.randint(0, min(3, elements.count() - 1)))
                if element.is_visible():
                    element.scroll_into_view_if_needed()
                    time.sleep(1)
                    element.click(force=True)
                    time.sleep(random.uniform(2, 4))
                    print(f"🖱️ Clic sur élément: {selector}")
                    break
        except:
            continue
    
    # Scroll très réaliste avec variations de vitesse
    scroll_patterns = [
        (300, 0.5),   # Petit scroll rapide
        (800, 1.5),   # Moyen scroll moyen
        (1500, 2.5),  # Grand scroll lent
        (500, 0.8),   # Retour rapide
    ]
    
    for scroll_amount, scroll_time in random.sample(scroll_patterns, random.randint(3, 6)):
        page.mouse.wheel(0, scroll_amount)
        time.sleep(scroll_time + random.uniform(0.5, 1.0))
    
    # Frappe au clavier simulée dans les champs de recherche
    try:
        search_input = page.locator("input[type='search'], input[name='search'], [role='searchbox']")
        if search_input.count() > 0:
            search_input.first.click()
            time.sleep(1)
            search_input.first.fill("")
            for char in "medecin generaliste":
                search_input.first.type(char, delay=random.randint(50, 200))
                time.sleep(random.uniform(0.1, 0.3))
            time.sleep(2)
    except:
        pass

def rotate_browser_context(context):
    """Crée un nouveau contexte avec une empreinte différente"""
    print("🔄 Rotation du contexte navigateur...")
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0'
    ]
    
    viewports = [
        {'width': 1920, 'height': 1080},
        {'width': 1366, 'height': 768},
        {'width': 1536, 'height': 864},
        {'width': 1440, 'height': 900}
    ]
    
    new_context = context.browser.new_context(
        viewport=random.choice(viewports),
        user_agent=random.choice(user_agents),
        extra_http_headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
        }
    )
    
    # Nouveau script d'init pour masquer l'automation
    new_context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        
        Object.defineProperty(navigator, 'languages', {
            get: () => ['fr-FR', 'fr', 'en-US', 'en'],
        });
        
        // Masquer d'autres indicateurs d'automation
        window.chrome = { runtime: {} };
    """)
    
    return new_context

def scrape_doctolib():
    data = []
    failed_pages = 0
    max_failed_pages = 3  # Maximum de pages échouées avant arrêt

    with sync_playwright() as p:
        # Configuration avancée pour éviter la détection
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-features=VizDisplayCompositor',
                '--no-first-run',
                '--disable-default-apps',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-translate',
                '--disable-dev-shm-usage',
                '--no-sandbox',
            ]
        )
        
        # Contexte initial
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        )

        # Script pour masquer l'automation
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)

        for page_number in range(START_PAGE, END_PAGE + 1):
            if failed_pages >= max_failed_pages:
                print(f"🚨 Trop de pages échouées ({failed_pages}). Arrêt du scraping.")
                break
                
            url = BASE_URL + str(page_number)
            print(f"\n🔍 Chargement de la page {page_number} : {url}")
            
            page = context.new_page()
            
            try:
                # Navigation avec timeout long
                page.goto(url, timeout=120000, wait_until='networkidle')
                
                # Simulation comportement humain avant vérification
                simulate_intensive_human_behavior(page)
                
                # Vérifier si un CAPTCHA est présent
                captcha_selectors = [
                    "text=/captcha/i",
                    "text=/robot/i", 
                    "text=/vérification/i",
                    "iframe[src*='recaptcha']",
                    "img[src*='captcha']",
                    ".g-recaptcha"
                ]
                
                captcha_detected = False
                for selector in captcha_selectors:
                    if page.locator(selector).count() > 0:
                        captcha_detected = True
                        print(f"🛑 CAPTCHA détecté avec le sélecteur: {selector}")
                        break
                
                if captcha_detected:
                    print("🔄 Tentative de contournement automatique du CAPTCHA...")
                    if automatic_captcha_bypass(page):
                        print("✅ CAPTCHA contourné avec succès!")
                        # Continuer le scraping normalement
                    else:
                        print("❌ Échec du contournement, rotation du contexte...")
                        page.close()
                        
                        # Rotation du contexte navigateur
                        context.close()
                        context = rotate_browser_context(context)
                        failed_pages += 1
                        continue
                
                # Scroll réaliste pour charger tous les résultats
                scroll_steps = random.randint(5, 8)
                for i in range(scroll_steps):
                    scroll_amount = random.randint(800, 1500)
                    page.mouse.wheel(0, scroll_amount)
                    time.sleep(random.uniform(2, 4))
                    human_like_behavior(page)
                
                # Attendre que les résultats se chargent
                page.wait_for_timeout(5000)

                # Récupérer TOUS les liens de profils
                try:
                    page.wait_for_selector("div.flex.justify-between > a[href*='/medecin-generaliste/']", timeout=15000)
                    links = page.eval_on_selector_all(
                        "div.flex.justify-between > a[href*='/medecin-generaliste/']",
                        "elements => elements.map(el => el.href)"
                    )
                    links = list(set(links))
                    print(f"🔗 {len(links)} profils trouvés sur la page {page_number}.")
                except Exception as e:
                    print(f"❌ Aucune donnée trouvée sur cette page: {e}")
                    page.close()
                    failed_pages += 1
                    continue

                # Réinitialiser le compteur d'échecs en cas de succès
                failed_pages = 0

                # Scraper TOUS les profils sans limitation
                for idx, link in enumerate(links):
                    try:
                        print(f"📖 Traitement du profil {idx+1}/{len(links)}")
                        
                        # Pause aléatoire entre les profils
                        time.sleep(random.uniform(3, 7))
                        
                        profile_page = context.new_page()
                        
                        # Comportement humain avant d'aller sur le profil
                        human_like_behavior(profile_page)
                        
                        profile_page.goto(link, timeout=60000, wait_until='domcontentloaded')
                        
                        # Vérifier CAPTCHA sur la page de profil
                        captcha_detected_profile = False
                        for selector in captcha_selectors:
                            if profile_page.locator(selector).count() > 0:
                                captcha_detected_profile = True
                                break
                        
                        if captcha_detected_profile:
                            print("🛑 CAPTCHA détecté sur le profil, tentative de contournement...")
                            if automatic_captcha_bypass(profile_page):
                                print("✅ CAPTCHA contourné sur le profil!")
                            else:
                                print("❌ Échec du contournement sur le profil, passage au suivant...")
                                profile_page.close()
                                continue
                        
                        profile_page.wait_for_timeout(3000)

                        # Extraction des données
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

                        print(f"✅ Profil {len(data)} extrait : {name}")
                        profile_page.close()

                    except Exception as e:
                        print(f"⚠️ Erreur lors de l'extraction du profil {link}: {e}")
                        try:
                            profile_page.close()
                        except:
                            pass
                        continue

                page.close()
                
                # Pause stratégique entre les pages
                if page_number < END_PAGE:
                    pause_time = random.randint(15, 30)
                    print(f"⏳ Pause de {pause_time} secondes avant la page suivante...")
                    time.sleep(pause_time)

            except Exception as e:
                print(f"❌ Erreur sur la page {page_number}: {e}")
                try:
                    page.close()
                except:
                    pass
                failed_pages += 1
                continue

        browser.close()

    # Sauvegarde Excel
    if data:
        df = pd.DataFrame(data)
        filename = f"doctolib_doctors_auto_captcha_{START_PAGE}_to_{END_PAGE}.xlsx"
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"\n📁 Données enregistrées dans {filename} (Total : {len(data)} profils) ✅")
    else:
        print("❌ Aucune donnée collectée")

def human_like_behavior(page):
    """Simule un comportement humain réaliste"""
    # Mouvements de souris aléatoires
    for _ in range(random.randint(2, 4)):
        x = random.randint(100, page.viewport_size['width'] - 100)
        y = random.randint(100, page.viewport_size['height'] - 100)
        page.mouse.move(x, y)
        time.sleep(random.uniform(0.5, 1.5))
    
    # Clics aléatoires occasionnels
    if random.random() > 0.8:
        page.mouse.click(x, y)
        time.sleep(1)

if __name__ == "__main__":
    print("🚀 Démarrage du scraping Doctolib avec contournement automatique des CAPTCHAs...")
    print("🎯 Stratégie: Rotation d'empreinte navigateur + Comportement humain intensif")
    print("⚡ Aucune limitation - Tous les profils seront scrapés")
    scrape_doctolib()