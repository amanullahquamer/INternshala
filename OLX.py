import requests
from bs4 import BeautifulSoup
import csv

def fetch_olx_car_covers():
    url = "https://www.olx.in/items/q-car-cover"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch page:", response.status_code)
        return

    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.find_all("li", class_="EIR5N")  # OLX listing container class

    with open("car_covers_olx.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Location", "Price", "Link"])

        for item in items:
            title = item.find("span", class_="_2tW1I").text if item.find("span", class_="_2tW1I") else "N/A"
            price = item.find("span", class_="_89yzn").text if item.find("span", class_="_89yzn") else "N/A"
            location = item.find("span", class_="_2FRXm").text if item.find("span", class_="_2FRXm") else "N/A"
            link_tag = item.find("a", href=True)
            link = f"https://www.olx.in{link_tag['href']}" if link_tag else "N/A"
            writer.writerow([title, location, price, link])

    print("Results saved to car_covers_olx.csv")

if __name__ == "__main__":
    fetch_olx_car_covers()
