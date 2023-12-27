from flask import Flask, request
import json
import os
import time
import jwt
#import ssl
from dotenv import load_dotenv

ISSUER = 'sample-auth-server'
LIFE_SPAN = 1800

os.getenv("POSTGRESSQL_URI")
SECRET_KEY = os.getenv("SECRET_KEY")
app = Flask(__name__)

def generate_access_token():
  payload = {
    "iss": ISSUER,
    "exp": time.time() + LIFE_SPAN,
  }
  access_token = jwt.encode(payload, secret_key, algorithm = 'HS256')

  return access_token

@app.route('/auth', methods = ['POST'])
def auth():
  authorization_header = request.headers.get('Authorization')
  if authorization_header and authorization_header.startswith('Bearer '):
        authorization_token = authorization_header.split('Bearer ')[1]

        try:
            decoded_token = jwt.decode(authorization_token, SECRET_KEY, algorithms=['HS256'])
            role = decoded_token.get('role')
            id = decoded_token.get('userid')
            if role == 'admin':
                scope = 'admin_scope'
            else:
                scope = 'default_scope'
            payload = {
                "iss": ISSUER,
                "exp": time.time() + LIFE_SPAN,
                "userid": id,
                "scope": scope
            }
            access_token = jwt.encode(payload, SECRET_KEY, algorithm = 'HS256')
            return json.dumps({ 
              "access_token": access_token,
              "token_type": "JWT",
              "expires_in": LIFE_SPAN
            }),200
        except jwt.ExpiredSignatureError:
            return json.dumps({
                "error": "token_expired"
            }),401
        except jwt.InvalidTokenError:
            return json.dumps({
                "error": "invalid_token"
            }),401
  else:
      return json.dumps({
          "error": "missing_token"
      }), 400

  


if __name__ == '__main__':
  #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  #context.load_cert_chain('domain.crt', 'domain.key')
  #app.run(port = 5000, debug = True, ssl_context = context)
  app.run(port = 5001, debug = True)