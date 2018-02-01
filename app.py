from flask import Flask, request, Response, \
    jsonify, abort
from flask_cors import CORS, cross_origin
from lib.user import User, check_pw
from lib.db import DataBase
import json

with open('config.json') as json_data_file:
    config = json.load(json_data_file)

base_url = '/api/v' + config['version']
basic_data_fields = config['variables']['basic_data_fields']
raw_data_fields = config['variables']['raw_data_fields']

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/', methods=['GET'])
def verify():
    return "hello world", 200


@app.route(base_url + '/verifyUser/', methods=['POST'])
@cross_origin(supports_credentials=True)
def verify_user():
    """
    Verify user credentials
    ______________________________________________________
    You can test this method using curl:
    curl -H "Content-Type: application/json" -X POST -d
                '{"username":"charles","password":"xyz"}'
                http://localhost:5000/api/v1.0/verifyUser/
    ______________________________________________________

    :return:
        JSON response
    """

    request_body = request.get_json()
    username = request_body['username']
    password = request_body['password']
    if username is None or password is None:
        abort(400)
    success = User().verify_password(password, username)
    return jsonify({'success': success})


@app.route(base_url + '/newUser/', methods=['POST'])
@cross_origin(supports_credentials=True)
def new_user():
    """
    Create a new user

    :return:
        JSON response
    """
    request_body = request.get_json()
    username = request_body['username']
    password = request_body['password']

    if username is None or password is None:
        abort(400)

    # Do the necessary checks on the password
    # and username here ...
    if check_pw(password):
        success = User().store_password(password, username)
        # TODO: We might want to return the username here
    else:
        success = False

    return jsonify({'success': success})


@app.route(base_url + '/updateBasicData/', methods=['POST'])
@cross_origin(supports_credentials=True)
def update_basic_data():
    """
    Update the database
    ___________________________________________________
    POST request example:
    curl -H "Content-Type: application/json" -X POST -d
    '{"username": "test", "password": "test", "fields":
    ["middle_name"], "values":["J."]}'
    http://localhost:5000/api/v1.0/updateBasicData/
    ___________________________________________________

    :POST body:
        {
            'username': 'user',
            'password': 'pw',
            'fields': [
                    'field 1',
                        ...,
                    'field n'
                ],
            'values': [
                    'value 1',
                        ...,
                    'value n'
                ]
        }

    :return:
        JSON response
    """
    request_body = request.get_json()
    username = request_body['username']
    password = request_body['password']
    fields = request_body['fields']
    values = request_body['values']

    # Check if the fields are accessible
    if not all([field in basic_data_fields for field in fields]):
        # bad request
        abort(400)

    if not (isinstance(fields, list)
            and isinstance(values, list)):
        # Bad request: fields and values
        # needs to be lists
        abort(400)

    authentication = User().verify_password(password, username)

    if authentication:
        success = DataBase().update_db('users',
                                       key={'username': username},
                                       field=fields,
                                       value=values)
        return jsonify({'success': success})
    else:
        # Unauthorized user
        abort(401)


@app.route(base_url + '/getBasicData/', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_basic_data():
    """
    Fetch data from the database

    :GET body:
        {
            'username': 'user',
            'password': 'pw',
            'fields': [
                    'field 1',
                        ...,
                    'field n'
                ]
        }

    :return:
        JSON response
        {
            'success': Boolean,
            'data': [
                'field 1': 'value 1',
                        ...,
                'field n': 'value n'
            ]
        }
    """

    request_body = request.get_json()
    username = request_body['username']
    password = request_body['password']
    fields = request_body['fields']

    # Check if the fields are accessible
    if not all([field in basic_data_fields for field in fields]):
        # bad request
        abort(400)

    authentication = User().verify_password(password, username)

    if authentication:
        fetched_data = DataBase().find('users',
                                       key={'username': username})
        if fetched_data is not None:
            data = {fields[i]: fetched_data[fields[i]]
                    for i in range(len(fields))}
            return jsonify({'success': True,
                            'data': data})
        else:
            return jsonify({'success': False})
    else:
        # Unauthorized user
        abort(401)


@app.route(base_url + '/updateRawData/', methods=['POST'])
@cross_origin(supports_credentials=True)
def update_raw_data():
    """
    Update raw data

    :POST body:
        {
            'username': 'user',
            'password': 'pw',
            'fields': [
                    'field 1',
                        ...,
                    'field n'
                ],
            'values: [
                    'value 1',
                        ...,
                    'value n'
                ]
        }

    :return:
        JSON response
        {
            'success': Boolean,
        }
    """
    request_body = request.get_json()
    username = request_body['username']
    password = request_body['password']
    fields = request_body['fields']
    values = request_body['values']

    # Check if the fields are accessible
    if not all([field in raw_data_fields for field in fields]):
        # bad request
        abort(400)

    authentication = User().verify_password(password, username)

    if authentication:
        success = DataBase().update_db('raw_data',
                                       key={'username': username},
                                       field=fields,
                                       value=values)
        return jsonify({'success': success})

    else:
        # Unauthorized user
        abort(401)


if __name__ == '__main__':
    app.run(debug=True, port=5000)