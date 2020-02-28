from urllib.parse import urlencode


OUTH_URL = 'https://oauth.vk.com/authorize'
params = {
    'client_id': 7227407,
    'display': 'page',
    'scope': [
        'friends',
        'groups',
        'photos',
    ],
    'response_type': "token",
    'v': 5.89
}

print('?'.join((OUTH_URL, urlencode(params))))