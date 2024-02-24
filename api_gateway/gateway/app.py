# api_gateway.py
from flask import Flask, jsonify, request, redirect, render_template, make_response
import jwt
import requests
from dotenv import load_dotenv
import os
from service import SERVICES
from datetime import datetime, timezone

load_dotenv()

app = Flask(__name__)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHMS = os.getenv("ALGORITHMS")


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    token = request.cookies.get('access_token')
    check, payload = decode_token(token)
    if (check):
        return render_template('dashboard.html')
    else:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def gateway_login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        url = f"http://{os.getenv('AUTHENTICATION_SERVICE_URL')}/api/login"
        authen_response = requests.post(
            url, json={'username': username, 'password': password}
        )
        if authen_response.status_code == 200:
            data = authen_response.json()
            print(data)
            userid = data['userid']
            role = data['role']
            print(userid)
            print(role)
            author_response = requests.post(
                f"http://{os.getenv('AUTHORIZATION_SERVICE_URL')}/auth", json={'userid': userid, 'role': role}
            )
            if author_response.status_code == 200:
                token = author_response.json()
                access_token = token['access_token']
                response = make_response(redirect('/dashboard'))
                response.set_cookie('access_token', access_token)
                return response
            else:
                print('error: Authorization failed')
                return redirect('/login')
        else:
            print('error : Authentication failed')
            return redirect('/login')


@app.route('/logout', methods=['GET'])
def logout():
    response = make_response(redirect('/login'))
    response.delete_cookie('access_token')
    return response


@app.route('/register', methods=['GET', 'POST'])
def gateway_register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        url = f"http://{os.getenv('AUTHENTICATION_SERVICE_URL')}/api/register"
        auth_response = requests.post(
            url, json={'username': username, 'password': password}
        )

        if auth_response.status_code == 200:
            return redirect('/login')
        else:
            print('error : User registration failed')
            return redirect('/register')

# region file

#region file
@app.route('/read/<file_id>', methods=['GET'])
def gateway_management_read(file_id):
    token = request.cookies.get('access_token')
    check, payload = decode_token(token)
    if (check):
        url = f"http://{os.getenv('FILE_SERVICE_URL')}/api/read_file/{file_id}"
        response = requests.get(url)
        file_data = response.json()
        print(file_data)
        return render_template('readfile.html', file_data=file_data)
    else:
        return redirect('/login')

<<<<<<< HEAD
=======

>>>>>>> origin/fix-docker
@app.route('/delete/<file_id>', methods=['POST'])
def gateway_management_delete(file_id):
    token = request.cookies.get('access_token')
    check, payload = decode_token(token)
    if (check):
        scope = payload.get("scope")
        if scope == "admin_scope":
            if request.method == 'POST':
                data_to_send = {"id": file_id}
<<<<<<< HEAD
            response = requests.post('http://localhost:5003/api/delete_file', json=[data_to_send])
            status = response.json()
            
=======
            url = f"http://{os.getenv('FILE_SERVICE_URL')}/api/delete_file"
            response = requests.post(url, json=[data_to_send])
            status = response.json()

>>>>>>> origin/fix-docker
            for item in status:
                if item['status_code'] == "200":
                    return redirect('/allFile')
    return jsonify({'message': 'Delete failed!'})
<<<<<<< HEAD
=======

>>>>>>> origin/fix-docker

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
<<<<<<< HEAD

    response = requests.post('http://localhost:5003/api/insert_file', json=[data_to_send])
    status = response.json()
    
    for item in status:
            if item['status_code'] == "200":
                return redirect('/allFile')
=======
    url = f"http://{os.getenv('FILE_SERVICE_URL')}/api/insert_file"
    response = requests.post(url, json=[data_to_send])
    status = response.json()

    for item in status:
        if item['status_code'] == "200":
            return redirect('/allFile')
>>>>>>> origin/fix-docker
    return jsonify({'message': 'Insert failed!'})


@app.route('/allFile', methods=['GET'])
def gateway_management_all_file():
    token = request.cookies.get('access_token')
    check, payload = decode_token(token)
    if (check):
        url = f"http://{os.getenv('FILE_SERVICE_URL')}/api/allFile"
        response = requests.get(url)
        files_data = response.json()
        print(files_data)
        return render_template('allfile.html', files_data=files_data)
    else:
        return redirect('/login')
<<<<<<< HEAD
#endregion
=======
# endregion

# region feedback


@app.route('/feedback', methods=['GET'])
def gateway_management_feedback():
    token = request.cookies.get('access_token')
    check, payload = decode_token(token)
    if (check):
        scope = payload.get("scope")
        if scope == "admin_scope":
            url = f"http://{os.getenv('FEEDBACK_SERVICE_URL')}/api/allfeedback"
            response = requests.get(url)
            feedbacks_data = response.json()
            print(feedbacks_data)
            return render_template('allfeedback.html', feedbacks_data=feedbacks_data)
        else:
            return render_template('insert_feedback.html')
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
    url = f"http://{os.getenv('FEEDBACK_SERVICE_URL')}/api/insert_feedback"
    response = requests.post(url, json=[data_to_send])
    status = response.json()

    for item in status:
        if item['status_code'] == "200":
            return redirect('/feedback')
    return jsonify({'message': 'Insert failed!'})
# endregion
>>>>>>> origin/fix-docker

#region feedback
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

    response = requests.post('http://localhost:5001/api/insert_feedback', json=[data_to_send])
    status = response.json()
    
    for item in status:
            if item['status_code'] == "200":
                return redirect('/feedback')
    return jsonify({'message': 'Insert failed!'})
#endregion

def decode_token(token):
    try:
        decoded_token = jwt.decode(
            token, SECRET_KEY, algorithms=ALGORITHMS)
        return True, decoded_token
    except jwt.ExpiredSignatureError:
        return False, "Token has expired"
    except jwt.InvalidTokenError:
        return False, "Invalid token"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
