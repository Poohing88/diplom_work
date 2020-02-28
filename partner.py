import re
import requests


def find_partner(user_info, access_token):
    if user_info['sex'] == 2:
        sex = 1
    elif user_info['sex'] == 1:
        sex = 2
    else:
        sex = 0
    params = {
        'user_ids': '456951815',
        'access_token': access_token,
        'v': 5.89,
        'age_from': user_info['age'] - 5,
        'age_to': user_info['age'] + 5,
        'sex': sex,
        'city': user_info['city']['id'],
        'is_closed': False,
        'count': 1000,
        'fields': 'about,books,interests,movies,music,personal,status,relation,common_count'
    }
    response = requests.get(
        'https://api.vk.com/method/users.search',
        params=params
    )
    find_word = '[А-Яа-я]+'
    user_search = response.json()['response']['items']
    list_user = []
    for i in user_search:
        if not i['is_closed']:
            try:
                if i['relation'] in [1, 6, 0]:
                    list_user.append(i)
                else:
                    pass
            except KeyError:
                list_user.append(i)
    music_user = re.findall(find_word, user_info['music'], re.IGNORECASE)
    books_user = re.findall(find_word, user_info['books'], re.IGNORECASE)
    interest_user = re.findall(find_word, user_info['interests'], re.IGNORECASE)
    movies_user = re.findall(find_word, user_info['movies'], re.IGNORECASE)
    user_list = []
    for person in list_user:
        coefficient = 0.0
        if person['common_count']:
            coefficient += 0.5
        our_friends = person['common_count'] * 0.1
        coefficient += our_friends
        for music in music_user:
            try:
                person_music = re.findall(find_word, person['music'], re.IGNORECASE)
                if len(music) > 4:
                    music = music[0: -2]
                    for mus in person_music:
                        mus = mus[0: -2]
                        if music == mus:
                            coefficient += 0.4
                else:
                    if music in person_music:
                        coefficient += 0.4
            except KeyError:
                pass
        for book in books_user:
            try:
                person_books = re.findall(find_word, person['books'], re.IGNORECASE)
                if book in person_books:
                    coefficient += 0.3
            except KeyError:
                pass
        for interest in interest_user:
            try:
                person_interest = re.findall(find_word, person['interests'], re.IGNORECASE)
                for per_int in person_interest:
                    if len(interest) > 4 and len(per_int) > 4:
                        interest = interest[0: -2]
                        per_int = per_int[0: -2]
                        if interest == per_int:
                            coefficient += 0.5
                    else:
                        if interest == per_int:
                            coefficient += 0.5
            except KeyError:
                pass
        for movie in movies_user:
            try:
                person_movies = re.findall(find_word, person['movies'], re.IGNORECASE)
                if movie in person_movies:
                    coefficient += 0.5
            except KeyError:
                pass
        try:
            if user_info['personal']['alcohol'] == person['personal']['alcohol']:
                coefficient += 0.3
            if user_info['personal']['life_main'] == person['personal']['life_main']:
                coefficient += 0.5
            if user_info['personal']['people_main'] == person['personal']['people_main']:
                coefficient += 0.5
            if user_info['personal']['political'] == person['personal']['political']:
                coefficient += 0.1
            if user_info['personal']['religion'] == person['personal']['religion']:
                coefficient += 0.4
            if user_info['personal']['smoking'] == person['personal']['smoking']:
                coefficient += 0.3
        except KeyError:
            pass
        person['coefficient'] = coefficient
        user_list.append(person)
    user_list = sorted(user_list, key=lambda user_list: user_list['coefficient'])
    user_list = user_list[-101: -1]
    return user_list

