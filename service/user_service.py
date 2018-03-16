from mongodb import client


collection = client.infosys.user


def check_password(username, password):
    user = collection.find_one({'username': username})
    if(user['password'] == password):
        return True
    else:
        return False


def add_user(username, realname, password):
    collection.insert({'username': username, 'password': password, 'realname': realname})


def find_one_user_by_name(username):
    return collection.find_one({'username': username})


def find_one_user_by_id(realname):
    return collection.find_one({'realname': realname})


def find_one_and_update(op1, op2):
    collection.find_one_and_update(op1, op2)