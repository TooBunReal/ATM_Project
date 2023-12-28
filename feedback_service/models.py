from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class feedbacks(db.Model):
    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
