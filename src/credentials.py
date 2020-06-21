import json
import os

def guard(request):
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        return False

    if not verify_credentials(username, password):
        return False

    return True

def verify_credentials(username, password):
    with open(os.path.dirname(os.path.realpath(__file__)) + '/private/credentials.json') as json_credentials:
        users = json.load(json_credentials)

        for user in users:
            if user['username'] == username and user['password'] == password:
                return True

    return False
