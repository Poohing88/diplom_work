import time
from pprint import pprint
from partner import find_partner
from get_user_info import access_token, User

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

user = User(access_token, '456951815')
user_info = user.get_info()
user_list = find_partner(user_info, access_token)
list_user = []
counter = 0
for partner in user_list:
    group_partner = user.get_groups(partner['id'])
    try:
        group_partner = group_partner['response']['items']
    except KeyError:
        time.sleep(0.3)
    counter += 1
    print(counter)
    for group in user_info['group_user']:
        if group in group_partner:
            partner['coefficient'] += 0.1
    list_user.append(partner)
list_user = sorted(list_user, key=lambda list_user: list_user['coefficient'])
list_user = list_user[-6: -1]

total = []
for i in list_user:
    partner_user_photo = user.get_photo(i['id'])
    try:
        partner_user_photo = partner_user_photo['response']['items']
    except KeyError:
        photo = 'Не удалось получить фотографии'
        continue
    photo = None
    list_photo = []
    print('\n\n\n')
    for work_photo in partner_user_photo:
        for size in work_photo['sizes']:
            if size['type'] == 'y':
                photo = {'url': size['url'], 'likes': work_photo['likes']['count']}
            elif size['type'] == 'z':
                photo = {'url': size['url'], 'likes': work_photo['likes']['count']}
            elif size['type'] == 'w':
                photo = {'url': size['url'], 'likes': work_photo['likes']['count']}
            else:
                photo = None
        list_photo.append(photo)
    list_photo = sorted(list_photo, key=lambda list_photo: photo['likes'])
    if len(list_photo) > 3:
        list_photo = list_photo[-3: -1]
    result_love = {
        'foto': list_photo,
        'id': i['id'],
        'name': f'{i["first_name"]} {i["last_name"]}',
        'page': f'https://vk.com/id{i["id"]}'
    }
    total.append(result_love)

pprint(total)

