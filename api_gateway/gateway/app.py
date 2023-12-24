# api_gateway.py
from flask import Flask, jsonify, request, redirect
import jwt
import requests
from callAPI import manage_operation
from service import SERVICES

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the API Gateway!'})


@app.route('/login', methods=['GET', 'POST'])
def gateway_login():
    if request.method == 'GET':
        return jsonify({'message': 'Login endpoint (GET)'})
    elif request.method == 'POST':
        auth_response = requests.post(
            SERVICES['authentication'], json=request.get_json())
        if auth_response.status_code == 200:
            token_response = auth_response.json()
            token = token_response.get('token')
            return jsonify({'token': token})
        else:
            return jsonify({'error': 'Authentication failed'}), 401


@app.route('/register', methods=['GET', 'POST'])
def gateway_register():
    if request.method == 'GET':
        return jsonify({'message': 'Register endpoint (GET)'})
    elif request.method == 'POST':
        return jsonify({'message': 'User registration endpoint'})


@app.route('/read', methods=['GET', 'POST'])
def gateway_management_read():
    return manage_operation('read', 'read_file')


@app.route('/update', methods=['GET', 'POST'])
def gateway_management_update():
    return manage_operation('update', 'update_file')


@app.route('/delete', methods=['GET', 'POST'])
def gateway_management_delete():
    return manage_operation('delete', 'delete_file')


@app.route('/insert', methods=['POST'])
def gateway_management_insert():
    return manage_operation('insert', 'insert_file')


@app.route('/allFile', methods=['GET'])
def gateway_management_all_file():
    return manage_operation('allFile', 'allFile')


def decode_token(token):
    return jwt.decode(token, verify=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
