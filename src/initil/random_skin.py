import random
from postsql import id_to_price, id_to_name
weigt = []
price = []
all_prices = 0
skins_id = list(range(1, 23))
for i in range(22):
    weigt.append(1/id_to_price(i+1))
def random_skin_one():
    skin_id = random.choices(skins_id, weights=weigt)[0]
    return skin_id

    return str(id_to_name(skin_id)) + ' ' + str(id_to_price(skin_id))






