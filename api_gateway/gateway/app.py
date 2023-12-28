# api_gateway.py
from flask import Flask, jsonify, request, redirect, render_template, make_response
import jwt
import requests
from dotenv import load_dotenv
import os
from callAPI import manage_operation
from service import SERVICES

load_dotenv()

app = Flask(__name__)

SECRET_KEY = os.getenv("SECRET_KEY")


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def gateway_login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        authen_response = requests.post(
            f"http://localhost:5002/api/login", json={'username': username, 'password': password}
        )
# khi nao co author thi send data qua thang author
        if authen_response.status_code == 200:
            data = authen_response.json()
            print(data)
            userid = data['userid']
            role = data['role']
            print(userid)
            print(role)
            author_response = requests.post(
                f"http://localhost:5005/auth", json={'userid': userid, 'role': role}
            )
            if author_response.status_code == 200:
                token = author_response.json()
                access_token = token['access_token']
                response = make_response(redirect('/allFile'))
                response.set_cookie('access_token', access_token)
                return response
            else:
                return jsonify({'error': 'Authorization failed'}), 401
        else:
            return jsonify({'error': 'Authentication failed'}), 401


@app.route('/logout', methods=['GET'])
def logout():
    response.delete_cookie('cookie_name', domain="cookie_domain")
    return response


@app.route('/register', methods=['GET', 'POST'])
def gateway_register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        auth_response = requests.post(
            f"http://localhost:5002/api/register", json={'username': username, 'password': password}
        )

        if auth_response.status_code == 200:
            return jsonify({'message': 'User registration successful'})
        else:
            return jsonify({'error': 'User registration failed'}), 500

# region file


@app.route('/read/<file_id>', methods=['GET'])
def gateway_management_read(file_id):
    response = requests.get(f'http://localhost:5003/api/read_file/{file_id}')
    file_data = response.json()
    print(file_data)
    return render_template('readfile.html', file_data=file_data)


@app.route('/delete/<file_id>', methods=['POST'])
def gateway_management_delete(file_id):
    token = request.cookies.get('access_token')
    check, payload = decode_token(token)
    if (check):
        scope = payload.get("scope")
        if scope == "admin_scope":
            if request.method == 'POST':
                data_to_send = {"id": file_id}
            response = requests.post(
                'http://localhost:5003/api/delete_file', json=[data_to_send])
            status = response.json()

            for item in status:
                if item['status_code'] == "200":
                    return redirect('/allFile')
    return jsonify({'message': 'Delete failed!'})


@app.route('/insert', methods=['POST'])
def gateway_management_insert():
    if request.method == 'POST':
        file_id = request.form['id']
        file_title = request.form['title']
        file_content = request.form['content']

    data_to_send = {
        "id": file_id,
        "title": file_title,
        "content": file_content
    }

    response = requests.post(
        'http://localhost:5003/api/insert_file', json=[data_to_send])
    status = response.json()

    for item in status:
        if item['status_code'] == "200":
            return redirect('/allFile')
    return jsonify({'message': 'Insert failed!'})


@app.route('/allFile', methods=['GET'])
def gateway_management_all_file():
    token = request.cookies.get('access_token')
    check, payload = decode_token(token)
    if (check):
        response = requests.get('http://localhost:5003/api/allFile')
        files_data = response.json()
        print(files_data)
        return render_template('allfile.html', files_data=files_data)
    else:
        return redirect('/login')
# endregion

# region feedback


@app.route('/feedback', methods=['GET'])
def gateway_management_feedback():
    token = request.cookies.get('access_token')
    check, payload = decode_token(token)
    if (check):
        scope = payload.get("scope")
        if scope == "admin_scope":
            response = requests.get('http://localhost:5001/api/allfeedback')
            feedbacks_data = response.json()
            print(feedbacks_data)
            return render_template('allfeedback.html', feedbacks_data=feedbacks_data)
        else:
            return render_template('insertfeedback.html')
    else:
        return redirect('/login')


@app.route('/insert_feedback', methods=['POST'])
def gateway_management_insert_feedback():
    if request.method == 'POST':
        feedback_name = request.form['name']
        feedback_content = request.form['content']

    data_to_send = {
        "name": feedback_name,
        "content": feedback_content
    }

    response = requests.post(
        'http://localhost:5001/api/insert_feedback', json=[data_to_send])
    status = response.json()

    for item in status:
        if item['status_code'] == "200":
            return redirect('/feedback')
    return jsonify({'message': 'Insert failed!'})
# endregion


def decode_token(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True, decoded_token
    except jwt.InvalidTokenError:
        return False, "Invalid token"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
