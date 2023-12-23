# api_gateway.py
from flask import Flask, jsonify, request, redirect
import jwt
import requests

app = Flask(__name__)

SERVICES = {
    'authentication': 'http://authentication_service:5002/login',
    'authorization': 'http://authorization_service:5005/authorize',
    'readfile': 'http://readfile_service:5003/readfile',
    'managefile': 'http://managefile_service:5004/managefile',
}


@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the API Gateway!'})


@app.route('/login', methods=['GET', 'POST'])
def gateway_login():
    if request.method == 'GET':
        return jsonify({'message': 'Login endpoint (GET)'})
    elif request.method == 'POST':
        # Gọi dịch vụ Authentication để xác thực người dùng và chuyển hướng đến Authorization
        auth_response = requests.post(
            SERVICES['authentication'], json=request.get_json())
        if auth_response.status_code == 200:
            # Xác thực thành công, nhận token từ callback endpoint của Authentication Service
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
        # Logic đăng ký người dùng có thể được thêm vào đây
        return jsonify({'message': 'User registration endpoint'})


@app.route('/readfile', methods=['GET', 'POST'])
def gateway_readfile():
    if request.method == 'GET':
        return jsonify({'message': 'Readfile endpoint (GET)'})
    elif request.method == 'POST':
        # Gọi dịch vụ Authentication để xác thực người dùng và chuyển hướng đến Authorization
        auth_response = requests.post(
            SERVICES['authentication'], json=request.get_json())
        if auth_response.status_code == 200:
            # Xác thực thành công, nhận token từ callback endpoint của Authentication Service
            token_response = auth_response.json()
            token = token_response.get('token')

            # Kiểm tra vai trò từ token
            roles = decode_token(token).get('role', '')

            if roles == 'admin' or roles == 'user':
                # Gọi dịch vụ ReadFile với token
                readfile_response = requests.post(
                    SERVICES['readfile'], json={'token': token}).text
                return jsonify({'readfile_response': readfile_response})
            else:
                return jsonify({'error': 'Unauthorized'}), 403
        else:
            return jsonify({'error': 'Authentication failed'}), 401


@app.route('/manage', methods=['GET', 'POST'])
def gateway_managefile():
    if request.method == 'GET':
        return jsonify({'message': 'Managefile endpoint (GET)'})
    elif request.method == 'POST':
        # Gọi dịch vụ Authentication để xác thực người dùng và chuyển hướng đến Authorization
        auth_response = requests.post(
            SERVICES['authentication'], json=request.get_json())
        if auth_response.status_code == 200:
            # Xác thực thành công, nhận token từ callback endpoint của Authentication Service
            token_response = auth_response.json()
            token = token_response.get('token')

            # Kiểm tra vai trò từ token
            roles = decode_token(token).get('role', '')

            if roles == 'admin':
                # Gọi dịch vụ ManageFile với token
                managefile_response = requests.post(
                    SERVICES['managefile'], json={'token': token}).text
                return jsonify({'managefile_response': managefile_response})
            elif roles == 'user':
                # Nếu là người dùng, từ chối truy cập và chuyển hướng về trang chủ
                return redirect('/')
            else:
                return jsonify({'error': 'Unauthorized'}), 403
        else:
            return jsonify({'error': 'Authentication failed'}), 401


def decode_token(token):
    # Giải mã token và trả về nội dung
    return jwt.decode(token, verify=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
