from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# change these later if you want
USERS = {"sac_user": "password123"}

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
    app.run(h
