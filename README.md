Voici un **README.md professionnel, clair et prêt pour GitHub**, adapté exactement à ton script Playwright + Python.

---

# 🩺 Doctolib Scraper – Python & Playwright

Scraper avancé avec **contournement automatique des CAPTCHAs**, rotation d’empreinte navigateur, simulation de comportement humain, extraction complète des profils médecins, et export vers Excel.

---

## 🚀 Fonctionnalités principales

✔️ Extraction **complète** des profils Doctolib :

* Nom
* Fonction
* Téléphone
* Adresse
* Expérience
* Diplômes
* Horaires
* Numéro RPPS
* SIREN
* Lien du profil

✔️ Contournement automatique des CAPTCHA (multi-stratégies)
✔️ Rotation du contexte navigateur (user-agent, viewport, headers)
✔️ Simulation avancée de comportement humain (mouvements souris, scroll, saisie, clics aléatoires)
✔️ Gestion intelligente des erreurs
✔️ Sauvegarde dans un fichier **Excel (.xlsx)**
✔️ Fonctionne même sur de nombreuses pages (scraping massif)

---

## 🛠️ Technologies utilisées

* **Python 3.8+**
* **Playwright** (version sync)
* **Pandas**
* **Openpyxl**
* **Random / Time**

---

## 📦 Installation

### 1️⃣ Installer les dépendances Python

```bash
pip install playwright pandas openpyxl
```

### 2️⃣ Installer les navigateurs Playwright

```bash
playwright install
```

---

## 🧩 Structure du projet

```
📁 doctolib-scraper
│── scraper.py          # Script principal
│── README.md           # Documentation
└── doctolib_doctors_...xlsx   # Fichier généré automatiquement
```

---

## ⚙️ Utilisation

Modifiez les variables suivantes en haut du script :

```python
BASE_URL = "https://www.doctolib.fr/medecin-generaliste/?page="
START_PAGE = 1
END_PAGE = 50   # nombre de pages à scraper
```

Puis lancez :

```bash
python scraper.py
```

---

## 🔎 Fonctionnement du script

### 🧠 1. Détection et contournement des CAPTCHAs

Le script utilise plusieurs stratégies :

* Reload intelligent
* Nettoyage cookies + localStorage
* Rotation User-Agent
* Navigation alternative
* Simulations de mouvements souris / clavier
* Scroll humain
* Attente stratégique
* Rotation du contexte Playwright en cas d’échec

### 🕹️ 2. Simulation de comportement humain

Le script simule :

* Mouvements de souris fluides
* Scrolls réalistes
* Clics aléatoires
* Saisie clavier dans les champs de recherche
* Navigation non-linéaire

Cela réduit fortement la détection anti-bot.

---

## 📤 Export des données

Le script génère automatiquement un fichier Excel :

```
doctolib_doctors_COMPLET_1_to_50.xlsx
```

---

## 🛡️ Avertissement important

Ce projet est fourni à titre éducatif uniquement.
Le scraping de sites comme Doctolib peut être **contraire à leurs conditions d’utilisation**.

**L’auteur n’est pas responsable de l’usage que vous en faites.**

---

## 🤝 Contribuer

Les contributions sont les bienvenues :

* Optimisations Playwright
* Ajout de nouveaux extracteurs
* Amélioration de la rotation d'empreinte
* Ajout d’un mode headless safe

Ouvrez une issue ou un pull request !

to run project activate venv 
```
venv\Scripts\activate
```
python scrapper.py
