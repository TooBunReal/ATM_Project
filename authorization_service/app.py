from flask import Flask, request
from flask_oauthlib.provider import OAuth2Provider

app = Flask(__name__)
app.config['OAUTH2_PROVIDER_TOKEN_EXPIRES_IN'] = 3600 

oauth = OAuth2Provider(app)

CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
USERNAME = 'user'
PASSWORD = 'password'

users = {'user': {'password': 'password'}}
clients = {'your_client_id': {'secret': 'your_client_secret', 'redirect_uris': []}}


@oauth.clientgetter
def load_client(client_id):
    return clients.get(client_id)


@oauth.usergetter
def get_user(username, password, *args, **kwargs):
    if username == USERNAME and password == PASSWORD:
        return {'id': 'user'}
    return None


@app.route('/token', methods=['POST'])
@oauth.token_handler
def access_token():
    return None


if __name__ == '__main__':
    app.run(debug=True)
