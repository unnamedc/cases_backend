import requests
from bs4 import BeautifulSoup
from postsql import id_to_url, set_price

k = 1

while True:
    request = requests.get(pricess(k)[0])
    soup = BeautifulSoup(request.text, 'html.parser')
    price_span = soup.find('span', class_='styles_price__1m7op MinimumPriceBlock_price_view__1EWY5')
    price = price_span.text.strip()
    set_price(price.replace('₽', '').replace(' ', ''), k)
    print(price.replace('₽', '').replace(' ', ''))
    k += 1
