import time
from pprint import pprint

from get_photo import get_photo
from partner import find_partner, partner_group_check
from get_user_info import access_token, User
from db_class import ad_to_db, persons
# Собрать информацию о пользователе
# прочитать ее с помощью регулярных выражений
# разложить основные категории информации и придать каждой категории инфрмации вес
# с полученой информацией начинаем искать пользователей
# предварительно отсортировав по полу возрасту городу
# получаем результат берем 10 первых пользователей делаем файл с ссылкой на их аккаунт
# и по 3 фотографии
# записываем результат из файла одновременно в БД
# делаем программу сверки поиска людей с информацией из БД
# делаем тесты и производим декомпозицию
if __name__ == '__main__':
    user = User(access_token, '456951815')
    user_info = user.get_info()
    user_list = find_partner(user_info, access_token)
    list_user = partner_group_check(user, user_list, user_info)
    total = get_photo(list_user, user)
    pprint(total)
    result = ad_to_db(total, persons)
    pprint(result.inserted_ids)


