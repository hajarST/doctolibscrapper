from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random

BASE_URL = "https://www.doctolib.fr/medecin-generaliste/?page="
START_PAGE = 1
END_PAGE = 1  # Vous pouvez mettre autant de pages que vous voulez

def safe_random_choice(items):
    """Choix aléatoire sécurisé qui gère les listes vides"""
    if not items:
        return None
    return random.choice(items)

def safe_random_sample(items, k):
    """Version sécurisée de random.sample qui évite l'erreur 'Sample larger than population'"""
    if not items or k <= 0:
        return []
    k = min(k, len(items))
    return random.sample(items, k)

def safe_random_int(min_val, max_val):
    """Génère un entier aléatoire sécurisé"""
    if min_val > max_val:
        min_val, max_val = max_val, min_val
    return random.randint(min_val, max_val)

def automatic_captcha_bypass(page):
    """Contournement automatique des CAPTCHAs sans intervention manuelle"""
    print("🔄 Tentative de contournement automatique du CAPTCHA...")
    
    try:
        # Stratégie 1: Rechargement avec paramètres aléatoires
        print("🎯 Stratégie 1: Rechargement avec paramètres aléatoires...")
        page.reload(wait_until='networkidle')
        time.sleep(5)
        
        # Stratégie 2: Nettoyer les cookies et storage
        print("🎯 Stratégie 2: Nettoyage des cookies...")
        page.evaluate("""
            try {
                localStorage.clear();
                sessionStorage.clear();
                document.cookie.split(";").forEach(function(c) { 
                    document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
                });
            } catch(e) {}
        """)
        
        # Stratégie 3: Changer l'user-agent dynamiquement
        print("🎯 Stratégie 3: Rotation de l'user-agent...")
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
        new_ua = safe_random_choice(user_agents)
        if new_ua:
            page.set_extra_http_headers({'User-Agent': new_ua})
        
        # Stratégie 4: Naviguer vers une URL différente puis revenir
        print("🎯 Stratégie 4: Navigation alternative...")
        try:
            page.goto("https://www.doctolib.fr", wait_until='networkidle', timeout=30000)
            time.sleep(3)
            page.go_back(wait_until='networkidle')
            time.sleep(5)
        except:
            print("⚠️ Navigation alternative échouée")
        
        # Stratégie 5: Simulation d'activité humaine intensive
        print("🎯 Stratégie 5: Simulation d'activité humaine...")
        simulate_intensive_human_behavior(page)
        
        # Stratégie 6: Attente stratégique
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
    
    try:
        # Mouvements de souris très réalistes
        viewport = page.viewport_size
        if viewport:
            moves = safe_random_int(5, 10)  # Nombre réduit mais suffisant
            for _ in range(moves):
                x = safe_random_int(50, viewport['width'] - 50)
                y = safe_random_int(50, viewport['height'] - 50)
                
                # Mouvement fluide avec plusieurs points intermédiaires
                steps = safe_random_int(2, 4)
                for step in range(steps):
                    intermediate_x = x + safe_random_int(-20, 20)
                    intermediate_y = y + safe_random_int(-20, 20)
                    page.mouse.move(intermediate_x, intermediate_y)
                    time.sleep(random.uniform(0.1, 0.3))
                
                time.sleep(random.uniform(0.3, 1.0))
    except Exception as e:
        print(f"⚠️ Erreur lors des mouvements de souris: {e}")
    
    # Clics réalistes sur différents éléments - CORRIGÉ ICI
    clickable_selectors = [
        "a", "button", "div[role='button']", "input[type='submit']",
        "span", "li", ".card", ".item"
    ]
    
    # Filtrer les sélecteurs disponibles
    available_selectors = []
    for selector in clickable_selectors:
        try:
            if page.locator(selector).count() > 0:
                available_selectors.append(selector)
        except:
            continue
    
    if available_selectors:
        # Utiliser safe_random_sample au lieu de random.sample
        num_clicks = safe_random_int(1, min(3, len(available_selectors)))
        selected_selectors = safe_random_sample(available_selectors, num_clicks)
        
        for selector in selected_selectors:
            try:
                elements = page.locator(selector)
                if elements.count() > 0:
                    # Prendre un élément aléatoire sécurisé
                    max_index = min(2, elements.count() - 1)
                    element_index = safe_random_int(0, max_index)
                    element = elements.nth(element_index)
                    if element.is_visible():
                        element.scroll_into_view_if_needed()
                        time.sleep(1)
                        element.click(force=True)
                        time.sleep(random.uniform(1, 3))
                        print(f"🖱️ Clic sur élément: {selector}")
                        break
            except Exception as e:
                print(f"⚠️ Erreur lors du clic sur {selector}: {e}")
                continue
    
    # Scroll très réaliste avec variations de vitesse
    scroll_patterns = [
        (300, 0.5),   # Petit scroll rapide
        (800, 1.5),   # Moyen scroll moyen
        (1500, 2.5),  # Grand scroll lent
        (500, 0.8),   # Retour rapide
    ]
    
    try:
        num_scrolls = safe_random_int(3, 5)
        selected_patterns = safe_random_sample(scroll_patterns, num_scrolls)
        for scroll_amount, scroll_time in selected_patterns:
            page.mouse.wheel(0, scroll_amount)
            time.sleep(scroll_time + random.uniform(0.3, 0.8))
    except Exception as e:
        print(f"⚠️ Erreur lors du scroll: {e}")
    
    # Frappe au clavier simulée dans les champs de recherche
    try:
        search_input = page.locator("input[type='search'], input[name='search'], [role='searchbox']")
        if search_input.count() > 0:
            search_input.first.click()
            time.sleep(1)
            search_input.first.fill("")
            for char in "medecin":
                search_input.first.type(char, delay=random.randint(50, 150))
                time.sleep(random.uniform(0.1, 0.2))
            time.sleep(1)
    except:
        pass

def rotate_browser_context(browser):
    """Crée un nouveau contexte avec une empreinte différente"""
    print("🔄 Rotation du contexte navigateur...")
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    ]
    
    viewports = [
        {'width': 1920, 'height': 1080},
        {'width': 1366, 'height': 768},
        {'width': 1536, 'height': 864},
    ]
    
    new_context = browser.new_context(
        viewport=safe_random_choice(viewports),
        user_agent=safe_random_choice(user_agents),
        extra_http_headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
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
    """)
    
    return new_context

def extract_profile_links_safe(page):
    """Extrait les liens des profils de manière sécurisée"""
    links = []
    
    # Essayer plusieurs sélecteurs
    selectors_to_try = [
        "div.flex.justify-between > a[href*='/medecin-generaliste/']",
        "a[href*='/medecin-generaliste/']",
        ".dl-search-result a",
        "[data-testid*='search-result'] a",
    ]
    
    for selector in selectors_to_try:
        try:
            page.wait_for_selector(selector, timeout=10000)
            found_links = page.eval_on_selector_all(
                selector,
                "elements => elements.map(el => el.href)"
            )
            if found_links:
                links.extend(found_links)
                print(f"✅ Trouvé {len(found_links)} liens avec {selector}")
                break
        except:
            continue
    
    # Si aucun lien trouvé, méthode de secours
    if not links:
        try:
            all_links = page.eval_on_selector_all(
                "a[href]",
                "elements => elements.map(el => el.href)"
            )
            links = [link for link in all_links if '/medecin-generaliste/' in link]
            if links:
                print(f"✅ Trouvé {len(links)} liens par méthode alternative")
        except Exception as e:
            print(f"⚠️ Erreur méthode alternative: {e}")
    
    return list(set(links))

def scrape_doctolib():
    data = []
    failed_pages = 0
    max_failed_pages = 3

    with sync_playwright() as p:
        # Configuration avancée pour éviter la détection
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-first-run',
                '--disable-default-apps',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-translate',
            ]
        )
        
        # Contexte initial
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        )

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
                # Navigation avec timeout
                page.goto(url, timeout=90000, wait_until='domcontentloaded')
                time.sleep(2)
                
                # Vérifier les blocages
                if page.locator("text=/retry later|blocked|access denied/i").count() > 0:
                    print("🚫 Message 'Retry later' détecté - Attente de 10 minutes")
                    failed_pages += 1
                    page.close()
                    time.sleep(600)  # Attente de 10 minutes
                    continue
                
                # Vérifier CAPTCHA
                captcha_detected = False
                captcha_selectors = [
                    "text=/captcha/i",
                    "text=/robot/i", 
                    "iframe[src*='recaptcha']",
                    "img[src*='captcha']",
                ]
                
                for selector in captcha_selectors:
                    if page.locator(selector).count() > 0:
                        captcha_detected = True
                        print(f"🛑 CAPTCHA détecté: {selector}")
                        break
                
                if captcha_detected:
                    print("🔄 Tentative de contournement CAPTCHA...")
                    if automatic_captcha_bypass(page):
                        print("✅ CAPTCHA contourné avec succès!")
                    else:
                        print("❌ Échec du contournement, rotation du contexte...")
                        page.close()
                        context.close()
                        context = rotate_browser_context(browser)
                        failed_pages += 1
                        continue
                else:
                    # Simulation comportement humain seulement si pas de CAPTCHA
                    simulate_intensive_human_behavior(page)
                
                # Scroll réaliste pour charger tous les résultats
                for i in range(4):
                    page.mouse.wheel(0, 1200)
                    time.sleep(2)
                
                # Attendre que les résultats se chargent
                time.sleep(3)

                # Récupérer TOUS les liens de profils
                links = extract_profile_links_safe(page)
                
                if not links:
                    print("❌ Aucun lien trouvé sur cette page")
                    page.close()
                    failed_pages += 1
                    continue

                print(f"🔗 {len(links)} profils trouvés sur la page {page_number}.")
                
                # Réinitialiser le compteur d'échecs en cas de succès
                failed_pages = 0

                # 🚨 SCRAPER TOUS LES PROFILS SANS LIMITATION 🚨
                for idx, link in enumerate(links):
                    try:
                        print(f"📖 Traitement du profil {idx+1}/{len(links)}")
                        
                        # Pause aléatoire entre les profils
                        time.sleep(random.uniform(3, 7))
                        
                        profile_page = context.new_page()
                        
                        # Comportement humain avant d'aller sur le profil
                        human_like_behavior(profile_page)
                        
                        profile_page.goto(link, timeout=60000, wait_until='domcontentloaded')
                        time.sleep(2)
                        
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
                        
                        # Extraction des données COMPLÈTES
                        name = "Nom non trouvé"
                        fonction = "Fonction non trouvée"
                        phone = "Téléphone non trouvé"
                        experience = "Expérience non précisée"
                        diplomes = "Non précisés"
                        address = "Adresse non trouvée"
                        horaires = "Horaires non trouvés"
                        rpps = "Non trouvé"
                        siren = "Non trouvé"

                        # Nom
                        try:
                            profile_page.wait_for_selector("h1#profile-name-with-title span[itemprop='name']", timeout=5000)
                            name = profile_page.locator("h1#profile-name-with-title span[itemprop='name']").inner_text().strip()
                        except:
                            try:
                                name = profile_page.locator("h1").first.inner_text().strip()
                            except:
                                pass

                        # Fonction
                        try:
                            fonction = profile_page.locator("div.dl-profile-header-speciality span").inner_text().strip()
                        except:
                            pass

                        # Téléphone
                        try:
                            phone = profile_page.locator("div.dl-profile-box:has(h3:has-text('Coordonnées')) div.flex").inner_text().strip()
                        except:
                            pass

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
                            pass

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
                            pass

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
                            pass

                        # Numéro RPPS
                        try:
                            rpps = profile_page.locator("p:has-text('Numéro RPPS') + p").inner_text().strip()
                        except:
                            pass

                        # SIREN
                        try:
                            siren = profile_page.locator("p:has-text('SIREN') + p").inner_text().strip()
                        except:
                            pass

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
                    pause_time = random.randint(20, 40)
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
        filename = f"doctolib_doctors_COMPLET_{START_PAGE}_to_{END_PAGE}.xlsx"
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"\n📁 Données enregistrées dans {filename} (Total : {len(data)} profils) ✅")
    else:
        print("❌ Aucune donnée collectée")

def human_like_behavior(page):
    """Simule un comportement humain réaliste"""
    try:
        # Mouvements de souris aléatoires
        for _ in range(safe_random_int(1, 3)):
            x = safe_random_int(100, page.viewport_size['width'] - 100)
            y = safe_random_int(100, page.viewport_size['height'] - 100)
            page.mouse.move(x, y)
            time.sleep(random.uniform(0.5, 1.5))
        
        # Clics aléatoires occasionnels
        if random.random() > 0.8:
            page.mouse.click(x, y)
            time.sleep(1)
    except Exception as e:
        pass

if __name__ == "__main__":
    print("🚀 Démarrage du scraping Doctolib avec contournement automatique des CAPTCHAs...")
    print("🎯 Stratégie: Rotation d'empreinte navigateur + Comportement humain intensif")
    print("⚡ AUCUNE LIMITATION - TOUS LES PROFILS SERONT SCRAPÉS")
    scrape_doctolib()