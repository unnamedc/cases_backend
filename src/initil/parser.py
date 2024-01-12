import requests
from bs4 import BeautifulSoup
from postsql import skin

k = 0

while True:
    url = ('https://cs.money/csgo/ak-47-nightwish-battle-scarred', 'https://cs.money/csgo/hydra-gloves-rattler-field-tested')
    request = requests.get(url[k])
    soup = BeautifulSoup(request.text, 'html.parser')
    name_span = soup.find('h1', class_="Text-module_normalize__w1P0l Text-module_headline-22__Uzl4r")
    name = name_span.text.strip()
    skin(name, url[k], 'Restricted')
    k = k + 1
