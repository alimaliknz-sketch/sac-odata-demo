from flask import Flask, Response, request, jsonify
from flask_httpauth import HTTPBasicAuth
import os

app = Flask(__name__)
auth = HTTPBasicAuth()

SAC_USER = os.environ.get("SAC_USER", "sac_user")
SAC_PASSWORD = os.environ.get("SAC_PASSWORD", "password123")
USERS = {SAC_USER: SAC_PASSWORD}

@auth.verify_password
def verify(user, pwd):
    return USERS.get(user) == pwd


# ---- Minimal OData V2 metadata (EDMX) ----
EDMX = """<?xml version="1.0" encoding="utf-8"?>
<edmx:Edmx Version="1.0"
  xmlns:edmx="http://schemas.microsoft.com/ado/2007/06/edmx">
  <edmx:DataServices m:DataServiceVersion="2.0"
    xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata">
    <Schema Namespace="Demo"
      xmlns="http://schemas.microsoft.com/ado/2008/09/edm">
      <EntityType Name="Product">
        <Key>
          <PropertyRef Name="ID" />
        </Key>
        <Property Name="ID" Type="Edm.Int32" Nullable="false" />
        <Property Name="Name" Type="Edm.String" Nullable="true" />
       <Property Name="Amount" Type="Edm.Int32" Nullable="true" />
      </EntityType>
      <EntityContainer Name="Container" m:IsDefaultEntityContainer="true">
        <EntitySet Name="Products" EntityType="Demo.Product" />
      </EntityContainer>
    </Schema>
  </edmx:DataServices>
</edmx:Edmx>
"""

DATA = [
    {"ID": 1, "Name": "Asset A", "Amount": 1000},
    {"ID": 2, "Name": "Asset B", "Amount": 2000},
]

# Service root (important): /odata or /odata/
@app.route("/odata", strict_slashes=False)
@auth.login_required
def odata_root():
    # Minimal service document for OData V2
    payload = {
        "d": {
            "EntitySets": ["Products"]
        }
    }
    return jsonify(payload)

# Metadata endpoint SAC will test: /odata/$metadata
@app.route("/odata/$metadata", strict_slashes=False)
@auth.login_required
def odata_metadata():
    return Response(EDMX, mimetype="application/xml")

# Entity set: /odata/Products
@app.route("/odata/Products", strict_slashes=False)
@auth.login_required
def odata_products():
    # Basic support for $top and $skip
    top = request.args.get("$top", type=int)
    skip = request.args.get("$skip", type=int, default=0)

    rows = DATA[skip:]
    if top is not None:
        rows = rows[:top]

    # OData V2 JSON shape
    return jsonify({"d": {"results": rows}})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
