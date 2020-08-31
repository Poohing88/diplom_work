import re
import requests
import datetime


access_token = 'ba2c08d6b90a81f253ff667a5c8e894704984d183a19266f63d170f307890f68312bf935ecab000f6c383'


class User:
    def __init__(self, access_token, user_id):
        self.access_token = access_token
        self.user_id = user_id
        self.url = f'https://vk.com/id{self.user_id}'

    def get_params(self):
        return {
            'user_id': self.user_id,
            'access_token': self.access_token,
            'v': 5.89
        }

    def get_friends(self):
        params = self.get_params()
        response = requests.get(
            'https://api.vk.com/method/friends.get',
            params=params
        )
        return response.json()

    def get_groups(self, user_id):
        params = {
            'user_id': user_id,
            'access_token': self.access_token,
            'extended': 0,
            'v': 5.89
        }
        response = requests.get(
            'https://api.vk.com/method/groups.get',
            params=params
        )
        return response.json()

    def get_info(self):
        params = {
            'user_ids': self.user_id,
            'access_token': self.access_token,
            # 'fields': 'bdate,city,interests,personal,relation,sex,tv',
            'fields': 'bdate,about,activities,books,city,games,interests,movies,music,personal,relation,sex,tv',

            'v': 5.89
        }
        response = requests.get(
            'https://api.vk.com/method/users.get',
            params=params
        )
        now = datetime.date.today()
        find_year = '\d{4}'
        answer = response.json()
        year_birth = re.findall(find_year, answer['response'][0]['bdate'])
        year_birth = int(year_birth[0])
        age = now.year - year_birth
        group = self.get_groups(self.user_id)
        user_info = {
            'id': answer['response'][0]['id'],
            'sex': answer['response'][0]['sex'],
            'city': answer['response'][0]['city'],
            'group_user': group['response']['items'],
            'age': age,
            'interests': answer['response'][0]['interests'],
            'music': answer['response'][0]['music'],
            'books': answer['response'][0]['books'],
            'movies': answer['response'][0]['movies'],
            'personal': answer['response'][0]['personal']
        }
        return user_info

    def get_photo(self, user_id):
        params = {
            'user_ids': self.user_id,
            'owner_id': user_id,
            'album_id': 'profile',
            'access_token': self.access_token,
            'extended': 1,
            'photo_sizes': 1,
            'v': 5.89
        }
        response = requests.get(
            'https://api.vk.com/method/photos.get',
            params=params
        )
        return response.json()



