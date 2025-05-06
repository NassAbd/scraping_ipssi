from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
import time
import datetime

def scrape_doctolib(params):
    print("Début du script")
    options = Options()
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    options.add_argument("--headless") 

    service = Service(executable_path=r"C:\Users\abdal\Downloads\geckodriver-v0.36.0-win32\geckodriver.exe")
    driver = webdriver.Firefox(service=service, options=options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://www.doctolib.fr/")

        query_input = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.searchbar-input.searchbar-query-input")))
        query_input.clear()
        query_input.send_keys(params.query)

        place_input = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input.searchbar-input.searchbar-place-input")))
        place_input.clear()
        place_input.send_keys(params.location)

        search_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.searchbar-submit-button")))
        search_button.click()

        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(text(), 'résultat')]")))

        profiles = driver.find_elements(By.CSS_SELECTOR, "article[id^='search-result-']")
        profiles = profiles[:params.max_results]

        results = []

        for i in range(len(profiles)):

            profiles = driver.find_elements(By.CSS_SELECTOR, "article[id^='search-result-']")  # Re-sélectionner les éléments à chaque itération
            profile = profiles[i]

            # Nom
            try:
                name = profile.find_element(By.CSS_SELECTOR, "h2").text.strip()
            except:
                name = ""

            # Créneau
            first_slot = "Non disponible"
            try:
                availability_days = WebDriverWait(profile, 10).until(
                    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.availabilities-day"))
                )
                for day in availability_days:
                    try:
                        day_name = day.find_element(By.CSS_SELECTOR, "div.availabilities-day-name").text.strip()
                        day_date = day.find_element(By.CSS_SELECTOR, "div.availabilities-day-date").text.strip()
                    except:
                        continue
                    slots = day.find_elements(By.CSS_SELECTOR, "div[data-test='available-slot']")
                    if slots:
                        first_slot_time = slots[0].text.strip()
                        first_slot = f"{day_name} {day_date} {first_slot_time}"
                        break
            except:
                first_slot = "Non disponible"

            # Adresse
            try:
                address_lines = profile.find_elements(By.CSS_SELECTOR, "p.dl-text.dl-text-body.dl-text-regular.dl-text-s.dl-text-neutral-130")
                rue = address_lines[0].text.strip() if len(address_lines) > 0 else ""
                cp_ville = address_lines[1].text.strip() if len(address_lines) > 1 else ""
                cp, ville = cp_ville.split(" ", 1) if " " in cp_ville else ("", "")
            except:
                rue, cp, ville = "", "", ""

            assurance = "Non spécifié"
            # Visite page médecin
            try:
                button = profile.find_element(By.CSS_SELECTOR, "a.dl-p-doctor-result-link")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                time.sleep(0.5)

                WebDriverWait(driver, 10).until(EC.visibility_of(button))
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.dl-p-doctor-result-link")))

                # Clic JS en fallback si click() échoue
                try:
                    button.click()
                except:
                    driver.execute_script("arguments[0].click();", button)

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//span[@class='dl-button-label' and contains(text(), 'Prendre rendez-vous')]")
                    )
                )

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.dl-profile-text p")))

                sector_div = driver.find_element(By.CSS_SELECTOR, "div.dl-profile-text p")
                sector_text = sector_div.text.strip()
                if "Conventionné secteur" in sector_text:
                    assurance = sector_text.strip()

            except Exception as e:
                print("Erreur pendant la visite du profil:", e)

            driver.back()

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article[id^='search-result-']"))
            )


            results.append({
                "nom": name,
                "disponibilite": first_slot,
                "secteur": assurance,
                "rue": rue,
                "cp": cp,
                "ville": ville
            })

        return results
        time.sleep(10)

    finally:
        driver.quit()
