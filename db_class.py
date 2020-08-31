from pymongo import MongoClient
from pprint import pprint
client = MongoClient()
love_db = client['love_db']
persons = love_db['persons']


def ad_to_db(total, db):
    result = db.insert_many(total)
    # for person in total:
    #     db.insert_one(person).inserted_id
    return result


def check_person(db, list):
    viev = db.find()
    id_have = []
    for i in viev:
        id_have.append(i['id'])
    counter = 0
    for person in list:
        if person['id'] in id_have:
            list.pop(counter)
    return list

