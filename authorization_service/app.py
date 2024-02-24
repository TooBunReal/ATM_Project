import json
import os
import time
import jwt
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

os.getenv("POSTGRESSQL_URI")
SECRET_KEY = os.getenv("SECRET_KEY")
LIFE_SPAN = int(os.getenv("LIFE_SPAN"))
ISSUER = os.getenv("ISSUER")
ALGORITHMS = os.getenv("ALGORITHMS")

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

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHMS)
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
    app.run(host='0.0.0.0', port=5005)
