from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///authen.db'
app.config['JWT_SECRET_KEY'] = 'secret-key'

db = SQLAlchemy(app)
jwt = JWTManager(app)

class UserModel(db.Model):
    id = db.Column (db.Integer, primary_key=True)
    username = db.Column (db.String(70), unique=True, nullable=False)
    password = db.Column (db.String(70), nullable=False)

    def __repr__(self):
        return f"User(username={username}, password={password})"
    
with app.app_context():
    db.create_all()

class UserRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        data = parser.parse_args()

        if UserModel.query.filter_by(username=data['username']).first():
            return {'message': 'User already exists'}, 400
        hashed_password = generate_password_hash(data['password'])
        new_user = UserModel(username=data['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 201

class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        data = parser.parse_args()

        user = UserModel.query.filter_by(username=data['username']).first()

        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=data['username'])
            return {'access_token': access_token}, 200

        return {'message': 'Invalid credentials'}, 401

class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {'message': 'You are accessing a protected resource', 'user': current_user}
    
@app.route('/wipe_database', methods=['POST'])
def wipe_database():
    try:
        db.session.query(UserModel).delete()
        db.session.commit()
        return jsonify({'message': 'Database wiped successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(ProtectedResource, '/protected')

if __name__ == '__main__':
    app.run(debug=True)
