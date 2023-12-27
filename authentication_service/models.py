from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class users(db.Model):
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100),nullable = False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20),default="user",nullable = False)
    def __init__(self, username, password):
        self.username = username
        self.password = password