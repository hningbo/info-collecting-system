from mongodb import client
from bson.objectid import ObjectId
import time

collection = client.infosys.information


def find_one_and_update(op1, op2):
    collection.find_one_and_update(op1, op2)


def add_information(infoname, subscriber, end_time, number, content):
    collection.insert({'infoname': infoname, 'subscriber': subscriber, 'start_time': time.strftime("%Y-%m-%d %H:%M", time.localtime()), 'end_time': end_time, 'number': number, 'content': content})


def find_all_information():
    return collection.find()


def find_one_by_id(id):
    return collection.find_one({'_id': ObjectId(id)})


def add_one_to_collection(coll, info):
    client.infosys[coll].insert(info)


def update_one_to_collection(coll, op1, op2):
    client.infosys[coll].update(op1, op2)


def find_by_collection(id):
    return client.infosys[id].find()


def delete_one_by_realname(id, realname):
    client.infosys[id].delete_one({'姓名': realname})


def delete_one_by_id(id):
    print(collection.delete_one({'_id': ObjectId(id)}))
    print(client.infosys[id].drop())



