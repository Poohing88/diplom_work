import re
import requests


def get_photo(list_user, user):
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
    return total
