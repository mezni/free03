from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ⚙️ Setup headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://messaggio.com/messaging")

wait = WebDriverWait(driver, 10)

try:
    # Wait for any hint of the countries container to appear
    countries_container = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//section[contains(., 'The catalog presents the countries') or contains(@class,'countries')]")
        )
    )

    # Try different approaches to grab country names
    countries = set()
    for xpath in [
        ".//li",                         # list items
        ".//a",                          # link items
        ".//p[contains(@class,'country')]" # paragraphs with 'country' class
    ]:
        elems = countries_container.find_elements(By.XPATH, xpath)
        for el in elems:
            text = el.text.strip()
            if text:
                countries.add(text)

    if countries:
        print("Countries found:")
        for country in sorted(countries):
            print("-", country)
    else:
        print("⚠️ No countries found – check the container or try different selectors.")

except Exception as e:
    print("❌ Error extracting countries:", e)

driver.quit()
