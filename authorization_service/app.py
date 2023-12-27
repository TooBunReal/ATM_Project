import json
import os
import time

import jwt

# import ssl
from dotenv import load_dotenv
from flask import Flask, request
load_dotenv()

ISSUER = "sample-auth-server"
LIFE_SPAN = 1800

os.getenv("POSTGRESSQL_URI")
SECRET_KEY = os.getenv("SECRET_KEY")
app = Flask(__name__)


@app.route("/auth", methods=["POST"])
def auth():
    try:
        data = request.get_json()
        userid = data.get("userid")
        role = data.get("role")
        if role == "admin":
            scope = "admin_scope"
        else:
            scope = "default_scope"

        payload = {
            "iss": ISSUER,
            "exp": time.time() + LIFE_SPAN,
            "userid": userid,
            "scope": scope,
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return (
            json.dumps(
                {
                    "access_token": access_token,
                    "token_type": "JWT",
                    "expires_in": LIFE_SPAN,
                }
            ),
            200,
        )
    except Exception as e:
        return json.dumps({"error": "internal_server_error"}), 500


if __name__ == "__main__":
    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # context.load_cert_chain('domain.crt', 'domain.key')
    # app.run(port = 5000, debug = True, ssl_context = context)
    app.run(host='0.0.0.0', port=5005)
