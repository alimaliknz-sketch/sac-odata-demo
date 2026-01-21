from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth
import os

app = Flask(__name__)
auth = HTTPBasicAuth()

# Read credentials from environment variables
SAC_USER = os.environ.get("SAC_USER", "sac_user")
SAC_PASSWORD = os.environ.get("SAC_PASSWORD", "password123")

USERS = {
    SAC_USER: SAC_PASSWORD
}

@auth.verify_password
def verify(user, pwd):
    return USERS.get(user) == pwd

@app.route("/odata/Products")
@auth.login_required
def products():
    return jsonify({
        "value": [
            {"ID": 1, "Name": "Asset A", "Amount": 1000},
            {"ID": 2, "Name": "Asset B", "Amount": 2000}
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
