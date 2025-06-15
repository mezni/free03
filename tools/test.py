import requests
from bs4 import BeautifulSoup

url = "https://messaggio.com/messaging/france/"  # Replace with any country page
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

tables = soup.find_all("table")

print(f"Found {len(tables)} tables:\n")

for i, table in enumerate(tables, start=1):
    print(f"Table {i} preview:")
    
    # Try to show up to 3 rows (key-value or header cells)
    rows = table.find_all("tr")
    for row in rows[:3]:
        cols = row.find_all(["th", "td"])
        values = [col.get_text(strip=True) for col in cols]
        print("  ", values)
    
    print("-" * 40)
