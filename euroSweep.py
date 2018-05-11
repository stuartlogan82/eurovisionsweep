import requests, bs4, json
from pprint import pprint


res = requests.get("https://eurovision.tv/story/exclusive-running-order-eurovision-2018-grand-final")

res.raise_for_status()

euroSoup = bs4.BeautifulSoup(res.text, "html.parser")
elems = euroSoup.select("span['data-text']")
countries = []
for e in elems:
    pprint(e.getText())
    raw_country = e.getText()
    print(raw_country[0].isdigit())
    if raw_country[0].isdigit():
        country_name = raw_country[4:].lower()
        wiki_name = ""
        euro_name = ""
        if country_name.startswith('the'):
            euro_name = country_name[4:]
            wiki_name = country_name[4:]
        elif " " in country_name:
            country_split = country_name.split()
            euro_name = "-".join(country_split)
            wiki_name = "_".join(country_split)
        else:
            euro_name = country_name
            wiki_name = country_name
        country = {
            "country": country_name,
            "wiki": "https://en.wikipedia.org/wiki/{}".format(wiki_name),
            "euro_world": "https://eurovisionworld.com/eurovision/{}".format(euro_name)
        }
        countries.append(country)

pprint(countries)
print(len(countries))

with open('euroSweep.json', 'w') as es:
    json.dump(countries, es)

