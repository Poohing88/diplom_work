import re
import json
from pprint import pprint

import requests

from get_user_info import User
import datetime


def get_user_info(access_token, id_user):
    user = User(access_token, id_user)
    now = datetime.date.today()
    find_year = '\d{4}'
    answer = user.get_info()
    year_birth = re.findall(find_year, answer['response'][0]['bdate'])
    year_birth = int(year_birth[0])
    age = now.year - year_birth
    group = user.get_groups(id_user)
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


