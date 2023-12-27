from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(100),nullable = False)
    role = db.Column(db.String(20),default="user",nullable = False)
    def __init__(self, userid, password,username,role):
        self.password = password
        self.username = username