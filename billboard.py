# import cloudscraper
import requests
import datetime
import csv
import time

from bs4 import BeautifulSoup

with open('next_date', 'r') as f:
    date = f.read()

# scraper = cloudscraper.create_scraper()
base_url = "https://www.billboard.com/charts/hot-100/"
start_date = datetime.date.fromisoformat(date)
sat = start_date + datetime.timedelta( (5-start_date.weekday()) % 7 )
# final_date = datetime.date.today()
final_date = datetime.date.fromisoformat("1994-01-30")
header = ["song", "artist", "weeks_on_chart"]

while sat < final_date:
    url = base_url + sat.strftime("%Y-%m-%d")
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    list = soup.find_all("div", class_="o-chart-results-list-row-container")

    if len(list) < 99:
        with open('next_date', 'w') as f:
            f.write(sat.strftime("%Y-%m-%d"))
        print(sat)
        # break
        print(len(list))
        print("waiting...")
        time.sleep(30)
        continue

    with open('billboard100/daily-charts/' + sat.strftime("%Y-%m-%d"), 'w') as f:
        print("writing to " + f.name + "...")
        writer = csv.writer(f)
        writer.writerow(header)

        for element in list:
            song = element.find(id="title-of-a-story").text.strip()
            artist = element.find(id="title-of-a-story").findNext("span").text.strip()
            weeks_on_chart = element.ul.find_all("li")[-1].span.text.strip()

            row = [song, artist, weeks_on_chart]
            writer.writerow(row)

    sat = sat + datetime.timedelta(7)