import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

products = soup.find_all("div", class_="thumbnail")

data = []

for p in products:
    name = p.find("a", class_="title").text.strip()
    price = p.find("h4", class_="price").text.replace("$", "")
    desc = p.find("p", class_="description").text.strip()
    img = "https://webscraper.io" + p.find("img")["src"]

    data.append({
        "Model": name,
        "Price": price,
        "Description": desc,
        "Image": img
    })

df = pd.DataFrame(data)
df.to_csv("scraped_laptops.csv", index=False)

print("✅ Laptop data scraped successfully")
