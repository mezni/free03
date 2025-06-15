import requests
from bs4 import BeautifulSoup

url = "https://messaggio.com/messaging/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

countries = []

# Find all list items with class 'pb-3' (each country entry)
for li in soup.select('li.pb-3'):
    a_tag = li.find('a')
    img_tag = li.find('img')
    span_tag = li.find('span')

    if a_tag and img_tag and span_tag:
        country = {
            "name": span_tag.get_text(strip=True),
            "url": a_tag['href'],
            "flag": img_tag['src']
        }
        countries.append(country)
i=0
# Display results
for c in countries:
    i=i+1
    print(c)
print (i)