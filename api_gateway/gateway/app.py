# api_gateway.py
from flask import Flask, jsonify, request, redirect
import jwt
import requests

app = Flask(__name__)

SERVICES = {
    'authentication': 'http://authentication_service:5002/login',
    'authorization': 'http://authorization_service:5005/authorize',
    'admin_service': 'http://admin_service:5003/admin',
    'management_service': 'http://management_service:5004/management',
}


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


@app.route('/management/read', methods=['GET', 'POST'])
def gateway_management_read():
    return manage_operation('read')


@app.route('/management/update', methods=['GET', 'POST'])
def gateway_management_update():
    return manage_operation('update')


@app.route('/management/delete', methods=['GET', 'POST'])
def gateway_management_delete():
    return manage_operation('delete')


@app.route('/admin', methods=['GET'])
def gateway_admin():
    auth_response = requests.post(
        SERVICES['authentication'], json=request.get_json())
    if auth_response.status_code == 200:
        token_response = auth_response.json()
        token = token_response.get('token')

        roles = decode_token(token).get('role', '')

        if roles == 'admin':
            # Gọi dịch vụ Admin để xem thông tin database
            admin_response = requests.get(
                SERVICES['admin_service'], headers={'Authorization': f'Bearer {token}'}).text
            return jsonify({'admin_response': admin_response})
        else:
            return jsonify({'error': 'Unauthorized'}), 403
    else:
        return jsonify({'error': 'Authentication failed'}), 401


def manage_operation(operation):
    if request.method == 'GET':
        return jsonify({'message': f'Management {operation} endpoint (GET)'})
    elif request.method == 'POST':
        auth_response = requests.post(
            SERVICES['authentication'], json=request.get_json())
        if auth_response.status_code == 200:
            token_response = auth_response.json()
            token = token_response.get('token')

            roles = decode_token(token).get('role', '')

            if roles == 'admin' or (roles == 'user' and operation == 'read'):
                # Gọi dịch vụ Management với token và thực hiện operation
                management_response = requests.post(
                    SERVICES['management_service'],
                    json={'token': token, 'operation': operation}).text
                return jsonify({f'management_{operation}_response': management_response})
            else:
                return jsonify({'error': 'Unauthorized'}), 403
        else:
            return jsonify({'error': 'Authentication failed'}), 401


def decode_token(token):
    return jwt.decode(token, verify=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
