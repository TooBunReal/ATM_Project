from flask import Flask, request, render_template, redirect, abort, url_for, send_from_directory, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from models import *
import os
import json
import re
import jwt
from conf import settings

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("POSTGRESSQL_URI")
db.init_app(app)
SECRET_KEY = os.getenv("SECRET_KEY")
#ALGORITHM = os.getenv("ALGORITHM")


@app.route('/api/signup', methods=['POST'])
def signup():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if not (username and password ):
        return json.dumps({"status":"You have to specify username *and* password"})

    if not re.match("^[a-zA-Z0-9_]{1,200}$", username):
        return json.dumps({"status":"The username should match this regular expression '^[a-zA-Z0-9_]{1,200}$'","status_code":500})
    user = User.query.filter_by(username=username).first()
    try:
        user = User(username, generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        return json.dumps({"status":"Username already taken"})
    return json.dumps({"status":"User sign up sucessfully, please return to login"})

@app.route('/api/signin', methods=['POST'])
def signin():
    username = request.form.get('username', '')
    if not re.match("^[a-zA-Z0-9_]{1,200}$", username):
        return json.dumps({"status":"The username should match this regular expression '^[a-zA-Z0-9_]{1,200}$'","status_code":500})
    user = User.query.filter_by(username=username).first()
    if not user:
        return json.dumps({"status":"Invalid username", "status_code":404})
    if not check_password_hash(user.password, request.form.get('password', '')):
        return json.dumps({"status":"Invalid password", "status_code":403})
    ret = {"userid":user.userid, "role":user.role}
    return json.dumps(ret)
