import json
import os
import re

from dotenv import load_dotenv
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from models import *
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRESSQL_URI")
db.init_app(app)
SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM")
ISSUER = "authen-server"
LIFE_SPAN = 1800


@app.route("/api/signup", methods=["POST"])
def signup():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if not (username and password):
        return json.dumps({"status": "You have to specify username *and* password"})

    if not re.match("^[a-zA-Z0-9_]{1,200}$", username):
        return json.dumps(
            {
                "status": "The username should match this regular expression '^[a-zA-Z0-9_]{1,200}$'",
                "status_code": 500,
            }
        )
    user = users.query.filter_by(username=username).first()
    try:
        user = users(username, generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        return json.dumps({"status": "Username already taken"})
    return json.dumps({"status": "User sign up sucessfully, please return to login"})


@app.route("/api/signin", methods=["POST"])
def signin():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if not re.match("^[a-zA-Z0-9_]{1,200}$", username):
        return json.dumps(
            {
                "status": "The username should match this regular expression '^[a-zA-Z0-9_]{1,200}$'",
                "status_code": 500,
            }
        )
    user = users.query.filter_by(username=username).first()
    if not user:
        return json.dumps({"status": "Invalid username", "status_code": 404})
    if not check_password_hash(user.password, password):
        return json.dumps({"status": "Invalid password", "status_code": 403})
    return json.dumps({"userid": user.userid, "role": user.role})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
