from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://messaggio.com/messaging/canada/")

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

tables = driver.find_elements(By.TAG_NAME, "table")

def find_nearest_heading(table_element):
    # Try to find a caption first
    try:
        caption = table_element.find_element(By.TAG_NAME, "caption")
        if caption.text.strip():
            return caption.text.strip()
    except:
        pass

    # If no caption, look for closest previous heading in DOM (h1 to h4)
    script = """
    let elem = arguments[0];
    while(elem.previousElementSibling){
        elem = elem.previousElementSibling;
        if(elem.tagName.match(/^H[1-4]$/)){
            return elem.innerText.trim();
        }
    }
    return null;
    """
    heading = driver.execute_script(script, table_element)
    if heading:
        return heading
    return None

print(f"Found {len(tables)} table(s) on the page.\n")

for idx, table in enumerate(tables, start=1):
    title = find_nearest_heading(table) or f"Table {idx}"
    print(f"=== {title} ===")
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "th") + row.find_elements(By.TAG_NAME, "td")
        row_text = [cell.text.strip() for cell in cells]
        print("\t".join(row_text))
    print("\n" + "-"*40 + "\n")

driver.quit()
