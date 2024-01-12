import psycopg2
from psycopg2 import Error
import json

try:
    # Подключение к существующей базе данных
    connection = psycopg2.connect(user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="12345",
                                  host="185.246.64.66",
                                  port="37428",
                                  database="postgres")

    # Создайте курсор для выполнения операций с базой данных
    cursor = connection.cursor()

    def examination(telegram_id):
        cursor.execute("SELECT balance from users where telegram_id = " + str(telegram_id))
        balance = cursor.fetchone()
        connection.commit()
        try:
            return balance[0]
        except:
            return balance
    def new_user(telegram_id):
        cursor.execute(" INSERT INTO users (TELEGRAM_ID, BALANCE, SKINS) VALUES (" + str(telegram_id) + ", 0, ARRAY[]::integer[]) ")
        connection.commit()
    def paiding(summ, telegram_id):
        cursor.execute("Update users set balance = " + str(summ) + " where telegram_id =" + str(telegram_id))
        connection.commit()
    def skin(name, url, rare):
        insert_query = " INSERT INTO skins (SKIN, URL, RARE) VALUES ('" + name + "','" + url + "','" + str(rare) +"')"
        print(insert_query)
        cursor.execute(insert_query)
        connection.commit()
    def id_to_url(idk):
        cursor.execute("SELECT url from skins where id = " + str(idk))
        return cursor.fetchone()
    def set_price(price, idk):
        cursor.execute("Update skins set price = " + str(price) + " where id =" + str(idk))
        connection.commit()
    def id_to_price(idk):
        cursor.execute("SELECT price from skins where id = " + str(idk))
        return cursor.fetchone()[0]
    def id_to_name(idk):
        cursor.execute("SELECT skin from skins where id = " + str(idk))
        return cursor.fetchone()[0]
    def new_skin(telegram_id, skin_id):
        cursor.execute("UPDATE users SET skins = array_append(skins, " + str(skin_id) + ") where telegram_id =" + str(telegram_id))
        #UPDATE my_table SET skins = array_remove(skins, 3); удаление значения из массива
        connection.commit()
    def inventory_case(telegram_id):
        cursor.execute("SELECT skins from users where telegram_id =" + str(telegram_id))
        balance = cursor.fetchone()
        connection.commit()
        return balance[0]
    

    def return_about_case(case_id):#возвращает массив с информацией о кейсе
        cursor.execute("SELECT * from cases where id =" + str(case_id))
        case = cursor.fetchone()
        connection.commit()
        url = case[0]
        name = case[1]
        description = case[2]
        price = case[3]
        id = case[5]
        return {"id": id, "title": name, "body": description, "imageURL": url, "price": price}

    def count_rows_in_column():
        cursor.execute("SELECT COUNT(*) FROM cases WHERE id IS NOT NULL")
        result = cursor.fetchone()[0]
        connection.commit()
        return int(result)
    
    def all_cases():
        spisoc = []
        for case_id in range(count_rows_in_column()):
            case = return_about_case(case_id+1)
            spisoc.append(case)
        return spisoc
    
except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)



