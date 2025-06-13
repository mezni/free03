from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome options
options = Options()
options.add_argument("--headless")  # Remove this if you want to see the browser
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Start driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://messaggio.com/messaging")

# Wait until at least one country span is visible
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.pb-3 span.ms-2")))

# Extract all countries
country_elements = driver.find_elements(By.CSS_SELECTOR, "li.pb-3 span.ms-2")
countries = [el.text.strip() for el in country_elements if el.text.strip()]

# Print results
print("🌍 Countries found:", len(countries))
for country in countries:
    print("-", country)

driver.quit()
