import requests
from bs4 import BeautifulSoup

url = "https://messaggio.com/messaging/france/"  # Replace with desired country page
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

country_info = {}

# Loop over all cards
cards = soup.find_all("div", class_="card")
for card in cards:
    header = card.find("div", class_="card-header")
    if header and "Country info" in header.get_text(strip=True):
        # Get the first <table> inside the card
        table = card.find("table")
        if table:
            for row in table.find_all("tr"):
                th = row.find("th").get_text(strip=True)
                td = row.find("td").get_text(strip=True)
                country_info[th] = td
    if header and "Country info" in header.get_text(strip=True):
        # Get the second <table> inside the card
        table = card.find("table")
        if table:
            for row in table.find_all("tr"):
                th = row.find("th").get_text(strip=True)
                td = row.find("td").get_text(strip=True)
                country_info[th] = td

print(country_info)
